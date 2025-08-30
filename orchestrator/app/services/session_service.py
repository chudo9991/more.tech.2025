"""
Session management service
"""
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import and_, func

from app.models import Session as SessionModel, QA, QAScore, Media, Question, Criteria, VacancyQuestion, QuestionCriterion
from app.schemas.session import SessionCreate, SessionResponse, SessionNextResponse
from app.core.config import settings
import httpx


class SessionService:
    def __init__(self, db: DBSession):
        self.db = db

    def create_session(self, session_data: SessionCreate) -> SessionResponse:
        """Create a new interview session"""
        try:
            # Get vacancy info to set vacancy_code
            vacancy_code = None
            if session_data.vacancy_id:
                from app.models import Vacancy
                vacancy = self.db.query(Vacancy).filter(Vacancy.id == session_data.vacancy_id).first()
                if vacancy:
                    vacancy_code = vacancy.vacancy_code
            
            session = SessionModel(
                id=str(uuid.uuid4()),
                vacancy_id=session_data.vacancy_id,
                vacancy_code=vacancy_code,
                phone=session_data.phone,
                email=session_data.email,
                status="created",
                current_step=0,
                total_steps=8  # Default number of questions
            )
            
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)
            
            return SessionResponse.from_orm(session)
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to create session: {str(e)}")

    def get_next_question(self, session_id: str) -> SessionNextResponse:
        """Get the next question for the session with vacancy context"""
        try:
            session = self.db.query(SessionModel).filter(
                SessionModel.id == session_id
            ).first()
            
            if not session:
                raise Exception("Session not found")
            
            if session.status == "completed":
                raise Exception("Session already completed")
            
            # Get vacancy information for context
            vacancy_info = None
            if session.vacancy_id:
                from app.models import Vacancy
                vacancy = self.db.query(Vacancy).filter(Vacancy.id == session.vacancy_id).first()
                if vacancy:
                    vacancy_info = {
                        "id": vacancy.id,
                        "title": vacancy.title,
                        "vacancy_code": vacancy.vacancy_code,
                        "requirements": vacancy.requirements,
                        "responsibilities": vacancy.responsibilities,
                        "experience_required": vacancy.experience_required,
                        "education_level": vacancy.education_level
                    }
            
            # Get questions for this vacancy with proper ordering
            vacancy_questions = self.db.query(VacancyQuestion).filter(
                VacancyQuestion.vacancy_id == session.vacancy_id
            ).order_by(VacancyQuestion.step_no).all()
            
            if session.current_step >= len(vacancy_questions):
                # Session completed
                session.status = "completed"
                session.finished_at = datetime.utcnow()
                self.db.commit()
                raise Exception("No more questions available")
            
            current_vacancy_question = vacancy_questions[session.current_step]
            current_question = current_vacancy_question.question
            
            # Get criteria for this question with weights
            criteria_data = self.db.query(Criteria, QuestionCriterion).join(
                QuestionCriterion, Criteria.id == QuestionCriterion.criterion_id
            ).filter(
                QuestionCriterion.question_id == current_question.id
            ).all()
            
            # Enhance question text with vacancy context if needed
            question_text = current_question.text
            if vacancy_info and current_question.is_vacancy_specific:
                # Add vacancy context to question
                context_parts = []
                if vacancy_info.get("requirements"):
                    context_parts.append(f"Требования к позиции: {vacancy_info['requirements']}")
                if vacancy_info.get("responsibilities"):
                    context_parts.append(f"Обязанности: {vacancy_info['responsibilities']}")
                
                if context_parts:
                    question_text = f"{question_text}\n\nКонтекст вакансии:\n" + "\n".join(context_parts)
            
            return SessionNextResponse(
                session_id=session_id,
                question_id=current_question.id,
                question_text=question_text,
                question_type=current_question.type,
                vacancy_context=vacancy_info,
                criteria=[{
                    "id": c.id,
                    "name": c.name,
                    "weight": float(qc.weight),
                    "must_have": qc.must_have,
                    "min_score": float(qc.min_score)
                } for c, qc in criteria_data],
                current_step=session.current_step + 1,
                total_steps=len(vacancy_questions),
                question_weight=float(current_vacancy_question.question_weight),
                must_have=current_vacancy_question.must_have
            )
        except Exception as e:
            raise Exception(f"Failed to get next question: {str(e)}")

    async def submit_answer(
        self, 
        session_id: str, 
        question_id: str, 
        audio_url: str
    ) -> Dict[str, Any]:
        """Submit an answer and process it through the pipeline"""
        try:
            session = self.db.query(SessionModel).filter(
                SessionModel.id == session_id
            ).first()
            
            if not session:
                raise Exception("Session not found")
            
            # 1. Transcribe audio using STT service
            transcription = await self._transcribe_audio(audio_url)
            
            # 2. Get question and criteria
            question = self.db.query(Question).filter(
                Question.id == question_id
            ).first()
            
            criteria_data = self.db.query(Criteria, QuestionCriterion).join(
                QuestionCriterion, Criteria.id == QuestionCriterion.criterion_id
            ).filter(
                QuestionCriterion.question_id == question_id
            ).all()
            
            # 3. Score answer using LLM service
            scoring_result = await self._score_answer(
                question.text,
                transcription["text"],
                criteria_data
            )
            
            # 4. Save QA record
            qa_record = QA(
                id=str(uuid.uuid4()),
                session_id=session_id,
                question_id=question_id,
                answer_text=transcription["text"],
                audio_url=audio_url,
                transcription_confidence=transcription["confidence"],
                pre_answer_pause_s=transcription["pre_answer_pause_s"],
                speech_rate_wpm=transcription["speech_rate_wpm"],
                created_at=datetime.utcnow()
            )
            self.db.add(qa_record)
            self.db.flush()  # Get the ID
            
            # 5. Save scores
            for criterion_score in scoring_result["per_criterion"]:
                qa_score = QAScore(
                    id=str(uuid.uuid4()),
                    qa_id=qa_record.id,
                    criterion_id=criterion_score["id"],
                    score=criterion_score["score"],
                    evidence=criterion_score.get("evidence", ""),
                    created_at=datetime.utcnow()
                )
                self.db.add(qa_score)
            
            # 6. Save media record
            media_record = Media(
                id=str(uuid.uuid4()),
                session_id=session_id,
                qa_id=qa_record.id,
                file_url=audio_url,
                file_type="audio",
                file_size_bytes=0,  # Will be updated by webhook
                duration_ms=0,  # Will be updated by webhook
                created_at=datetime.utcnow()
            )
            self.db.add(media_record)
            
            # 7. Update session progress
            session.current_step += 1
            
            # Get total steps from vacancy questions
            total_steps = self.db.query(VacancyQuestion).filter(
                VacancyQuestion.vacancy_id == session.vacancy_id
            ).count()
            
            if session.current_step >= total_steps:
                session.status = "completed"
                session.finished_at = datetime.utcnow()
            
            self.db.commit()
            
            return {
                "status": "success",
                "qa_id": qa_record.id,
                "transcription": transcription,
                "scoring": scoring_result,
                "session_progress": {
                    "current_step": session.current_step,
                    "total_steps": session.total_steps,
                    "status": session.status
                }
            }
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to submit answer: {str(e)}")

    def get_session(self, session_id: str) -> SessionResponse:
        """Get session details with aggregated results"""
        try:
            session = self.db.query(SessionModel).filter(
                SessionModel.id == session_id
            ).first()
            
            if not session:
                raise Exception("Session not found")
            
            # Get aggregated results
            qa_records = self.db.query(QA).filter(
                QA.session_id == session_id
            ).all()
            
            total_score = 0
            total_criteria = 0
            passed_criteria = 0
            
            for qa in qa_records:
                scores = self.db.query(QAScore).filter(
                    QAScore.qa_id == qa.id
                ).all()
                
                for score in scores:
                    total_criteria += 1
                    total_score += score.score
                    if score.score >= 0.7:  # Threshold for passing
                        passed_criteria += 1
            
            avg_score = total_score / total_criteria if total_criteria > 0 else 0
            pass_rate = passed_criteria / total_criteria if total_criteria > 0 else 0
            
            # Update session with aggregated data
            session.total_score = avg_score
            session.pass_rate = pass_rate
            session.qa_count = len(qa_records)
            
            self.db.commit()
            
            return SessionResponse.from_orm(session)
            
        except Exception as e:
            raise Exception(f"Failed to get session: {str(e)}")

    def update_session(self, session_id: str, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update session details"""
        try:
            session = self.db.query(SessionModel).filter(
                SessionModel.id == session_id
            ).first()
            
            if not session:
                raise Exception("Session not found")
            
            # Update fields
            if 'status' in session_data:
                session.status = session_data['status']
            if 'finished_at' in session_data:
                session.finished_at = datetime.fromisoformat(session_data['finished_at'].replace('Z', '+00:00'))
            if 'total_score' in session_data:
                session.total_score = session_data['total_score']
            
            self.db.commit()
            self.db.refresh(session)
            
            return {"status": "success", "session_id": session_id}
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to update session: {str(e)}")

    def delete_session(self, session_id: str) -> Dict[str, Any]:
        """Delete a session and all related data"""
        try:
            session = self.db.query(SessionModel).filter(
                SessionModel.id == session_id
            ).first()
            
            if not session:
                raise Exception("Session not found")
            
            # Delete related records (cascade will handle most)
            # Delete messages
            from app.models import Message
            self.db.query(Message).filter(Message.session_id == session_id).delete()
            
            # Delete QA records (cascade will delete QA scores)
            self.db.query(QA).filter(QA.session_id == session_id).delete()
            
            # Delete media records
            self.db.query(Media).filter(Media.session_id == session_id).delete()
            
            # Delete the session itself
            self.db.delete(session)
            self.db.commit()
            
            return {"status": "success", "message": f"Session {session_id} deleted successfully"}
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to delete session: {str(e)}")

    def get_audio_file(self, session_id: str, filename: str) -> bytes:
        """Get audio file from MinIO"""
        try:
            from minio import Minio
            
            print(f"Getting audio file: session_id={session_id}, filename={filename}")
            
            # Initialize MinIO client
            minio_client = Minio(
                'minio:9000',
                access_key='minioadmin',
                secret_key='minioadmin123',
                secure=False
            )
            
            # Get file from MinIO
            bucket_name = 'audio-files'
            object_key = f"{session_id}_{filename}"
            
            print(f"Looking for object: {bucket_name}/{object_key}")
            
            # List objects in bucket to debug
            try:
                objects = list(minio_client.list_objects(bucket_name, prefix=session_id))
                print(f"Found {len(objects)} objects with prefix {session_id}:")
                for obj in objects:
                    print(f"  - {obj.object_name} ({obj.size} bytes)")
            except Exception as list_error:
                print(f"Error listing objects: {list_error}")
            
            # Get object data
            response = minio_client.get_object(bucket_name, object_key)
            data = response.read()
            print(f"Successfully read {len(data)} bytes from {object_key}")
            return data
            
        except Exception as e:
            print(f"Exception getting audio file: {e}")
            raise Exception(f"Failed to get audio file: {str(e)}")

    def get_messages(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all messages for a session"""
        try:
            from app.models import Message
            messages = self.db.query(Message).filter(
                Message.session_id == session_id
            ).order_by(Message.timestamp.asc()).all()
            
            return [
                {
                    "id": msg.id,
                    "session_id": msg.session_id,
                    "text": msg.text,
                    "message_type": msg.message_type,
                    "audio_url": msg.audio_url,
                    "transcription_confidence": msg.transcription_confidence,
                    "tone_analysis": msg.tone_analysis,
                    "timestamp": msg.timestamp.isoformat() if msg.timestamp else None,
                    "created_at": msg.created_at.isoformat() if msg.created_at else None
                }
                for msg in messages
            ]
        except Exception as e:
            raise Exception(f"Failed to get messages: {str(e)}")

    async def _transcribe_audio(self, audio_url: str) -> Dict[str, Any]:
        """Transcribe audio using STT service"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.STT_SERVICE_URL}/api/v1/transcribe",
                    json={
                        "audio_url": audio_url,
                        "language": "ru",
                        "vad_enabled": True
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise Exception(f"STT transcription failed: {str(e)}")

    async def _score_answer(
        self, 
        question: str, 
        answer_text: str, 
        criteria_data: List[tuple]
    ) -> Dict[str, Any]:
        """Score answer using LLM service"""
        try:
            criteria_data = [{
                "id": c.id,
                "weight": float(qc.weight),
                "must_have": qc.must_have,
                "min_score": float(qc.min_score)
            } for c, qc in criteria_data]
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.LLM_SERVICE_URL}/api/v1/llm/score",
                    json={
                        "question": question,
                        "answer_text": answer_text,
                        "criteria": criteria_data,
                        "rubric_version": "v1"
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise Exception(f"LLM scoring failed: {str(e)}")

    def save_message(self, session_id: str, message_id: str, text: str, message_type: str, timestamp: str, audio_url: str = None, transcription_confidence: int = None, tone_analysis: str = None) -> Dict[str, Any]:
        """Save a chat message to database"""
        try:
            from app.models import Message
            
            # Create a new message record
            message = Message(
                id=message_id,
                session_id=session_id,
                text=text,
                message_type=message_type,
                audio_url=audio_url,
                transcription_confidence=transcription_confidence,
                tone_analysis=tone_analysis,
                timestamp=datetime.fromisoformat(timestamp.replace('Z', '+00:00')) if timestamp else datetime.utcnow()
            )
            
            self.db.add(message)
            self.db.commit()
            self.db.refresh(message)
            
            print(f"Message saved to database: {message_id}")
            
            return {"status": "success", "message_id": message_id}
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to save message: {str(e)}")

    def aggregate_session_results(self, session_id: str) -> Dict[str, Any]:
        """Aggregate all results for a session"""
        try:
            session = self.db.query(SessionModel).filter(
                SessionModel.id == session_id
            ).first()
            
            if not session:
                raise Exception("Session not found")
            
            # Get all QA records with scores
            qa_records = self.db.query(QA).filter(
                QA.session_id == session_id
            ).all()
            
            results = {
                "session_id": session_id,
                "status": session.status,
                "total_questions": session.total_steps,
                "answered_questions": len(qa_records),
                "completion_rate": len(qa_records) / session.total_steps if session.total_steps > 0 else 0,
                "total_score": session.total_score or 0,
                "pass_rate": session.pass_rate or 0,
                "started_at": session.created_at.isoformat() if session.created_at else None,
                "completed_at": session.completed_at.isoformat() if session.completed_at else None,
                "questions": []
            }
            
            for qa in qa_records:
                question = self.db.query(Question).filter(
                    Question.id == qa.question_id
                ).first()
                
                scores = self.db.query(QAScore).filter(
                    QAScore.qa_id == qa.id
                ).all()
                
                question_result = {
                    "question_id": qa.question_id,
                    "question_text": question.text if question else "",
                    "answer_text": qa.answer_text,
                    "audio_url": qa.audio_url,
                    "transcription_confidence": qa.transcription_confidence,
                    "pre_answer_pause_s": qa.pre_answer_pause_s,
                    "speech_rate_wpm": qa.speech_rate_wpm,
                    "scores": [{
                        "criterion_id": score.criterion_id,
                        "score": score.score,
                        "evidence": score.evidence
                    } for score in scores],
                    "avg_score": sum(s.score for s in scores) / len(scores) if scores else 0
                }
                
                results["questions"].append(question_result)
            
            return results
            
        except Exception as e:
            raise Exception(f"Failed to aggregate results: {str(e)}")
