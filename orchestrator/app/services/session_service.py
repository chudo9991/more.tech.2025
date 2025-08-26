"""
Session management service
"""
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import and_, func

from app.models import Session as SessionModel, QA, QAScore, Media, Question, Criteria
from app.schemas.session import SessionCreate, SessionResponse, SessionNextResponse
from app.core.config import settings
import httpx


class SessionService:
    def __init__(self, db: DBSession):
        self.db = db

    async def create_session(self, session_data: SessionCreate) -> SessionResponse:
        """Create a new interview session"""
        try:
            session = SessionModel(
                id=str(uuid.uuid4()),
                vacancy_id=session_data.vacancy_id,
                phone=session_data.phone,
                email=session_data.email,
                status="created",
                current_step=0,
                total_steps=0
            )
            
            # Get total questions for this vacancy
            total_questions = self.db.query(Question).join(
                Question.vacancy_questions
            ).filter(
                Question.vacancy_questions.any(vacancy_id=session_data.vacancy_id)
            ).count()
            
            session.total_steps = total_questions
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)
            
            return SessionResponse.from_orm(session)
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to create session: {str(e)}")

    async def get_next_question(self, session_id: str) -> SessionNextResponse:
        """Get the next question for the session"""
        try:
            session = self.db.query(SessionModel).filter(
                SessionModel.id == session_id
            ).first()
            
            if not session:
                raise Exception("Session not found")
            
            if session.status == "completed":
                raise Exception("Session already completed")
            
            # Get questions for this vacancy
            questions = self.db.query(Question).join(
                Question.vacancy_questions
            ).filter(
                Question.vacancy_questions.any(vacancy_id=session.vacancy_id)
            ).order_by(Question.order_index).all()
            
            if session.current_step >= len(questions):
                # Session completed
                session.status = "completed"
                session.completed_at = datetime.utcnow()
                self.db.commit()
                raise Exception("No more questions available")
            
            current_question = questions[session.current_step]
            
            # Get criteria for this question
            criteria = self.db.query(Criteria).join(
                Criteria.question_criteria
            ).filter(
                Criteria.question_criteria.any(question_id=current_question.id)
            ).all()
            
            return SessionNextResponse(
                session_id=session_id,
                question_id=current_question.id,
                question_text=current_question.text,
                question_type=current_question.type,
                criteria=[{
                    "id": c.id,
                    "name": c.name,
                    "weight": c.weight,
                    "must_have": c.must_have,
                    "min_score": c.min_score
                } for c in criteria],
                current_step=session.current_step + 1,
                total_steps=session.total_steps
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
            
            criteria = self.db.query(Criteria).join(
                Criteria.question_criteria
            ).filter(
                Criteria.question_criteria.any(question_id=question_id)
            ).all()
            
            # 3. Score answer using scoring service
            scoring_result = await self._score_answer(
                question.text,
                transcription["text"],
                criteria
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
            if session.current_step >= session.total_steps:
                session.status = "completed"
                session.completed_at = datetime.utcnow()
            
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

    async def get_session(self, session_id: str) -> SessionResponse:
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
        criteria: List[Criteria]
    ) -> Dict[str, Any]:
        """Score answer using scoring service"""
        try:
            criteria_data = [{
                "id": c.id,
                "weight": c.weight,
                "must_have": c.must_have,
                "min_score": c.min_score
            } for c in criteria]
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.SCORING_SERVICE_URL}/api/v1/score",
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
            raise Exception(f"Scoring failed: {str(e)}")

    async def aggregate_session_results(self, session_id: str) -> Dict[str, Any]:
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
