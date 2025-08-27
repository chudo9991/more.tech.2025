"""
HR service for managing interview data and reports
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import and_
from datetime import datetime

from app.models import Session as SessionModel, QA, QAScore, Criteria, Vacancy, Candidate
from app.schemas.hr import SessionListResponse, SessionDetailResponse, QAResponse, QAScoreResponse, VacancyResponse


class HRService:
    def __init__(self, db: DBSession):
        self.db = db

    async def get_vacancies(self) -> List[VacancyResponse]:
        """Get list of all vacancies"""
        vacancies = self.db.query(Vacancy).all()
        return [VacancyResponse.from_orm(vacancy) for vacancy in vacancies]

    async def get_sessions(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        status: Optional[str] = None,
        vacancy_id: Optional[str] = None
    ) -> List[SessionListResponse]:
        """Get list of interview sessions with filters"""
        query = self.db.query(SessionModel)
        
        if status:
            query = query.filter(SessionModel.status == status)
        
        if vacancy_id:
            query = query.filter(SessionModel.vacancy_id == vacancy_id)
        
        sessions = query.offset(skip).limit(limit).all()
        
        # Get vacancy titles and candidate phones
        vacancy_ids = list(set([s.vacancy_id for s in sessions if s.vacancy_id]))
        candidate_ids = list(set([s.candidate_id for s in sessions if s.candidate_id]))
        
        vacancies = {}
        if vacancy_ids:
            from app.models import Vacancy
            vacancy_models = self.db.query(Vacancy).filter(Vacancy.id.in_(vacancy_ids)).all()
            vacancies = {v.id: v.title for v in vacancy_models}
        
        candidates = {}
        if candidate_ids:
            from app.models import Candidate
            candidate_models = self.db.query(Candidate).filter(Candidate.id.in_(candidate_ids)).all()
            candidates = {c.id: c.phone for c in candidate_models}
        
        # Count total steps for each session
        session_steps = {}
        for session in sessions:
            qa_count = self.db.query(QA).filter(QA.session_id == session.id).count()
            session_steps[session.id] = qa_count
        
        result = []
        for session in sessions:
            session_data = SessionListResponse.from_orm(session)
            session_data.vacancy_title = vacancies.get(session.vacancy_id)
            session_data.phone = candidates.get(session.candidate_id)
            session_data.total_steps = session_steps.get(session.id, 0)
            result.append(session_data)
        
        return result

    async def get_session_detail(self, session_id: str) -> SessionDetailResponse:
        """Get detailed session information with Q&A records"""
        session = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not session:
            raise ValueError("Session not found")

        # Get Q&A records with scores
        qa_records = self.db.query(QA).filter(QA.session_id == session_id).all()
        
        qa_responses = []
        for qa_record in qa_records:
            # Get scores for this Q&A
            scores = self.db.query(QAScore, Criteria).join(
                Criteria, QAScore.criterion_id == Criteria.id
            ).filter(QAScore.qa_id == qa_record.id).all()
            
            score_responses = []
            for score, criterion in scores:
                score_responses.append(QAScoreResponse(
                    criterion_id=criterion.id,
                    criterion_name=criterion.name,
                    score=float(score.score),
                    evidence=score.evidence,
                    red_flag=score.red_flag
                ))
            
            qa_responses.append(QAResponse(
                id=qa_record.id,
                step_no=qa_record.step_no,
                question_text=qa_record.question_text,
                answer_text=qa_record.answer_text,
                audio_url=qa_record.audio_url,
                tone=qa_record.tone,
                passed=qa_record.passed,
                scores=score_responses,
                created_at=qa_record.created_at
            ))

        return SessionDetailResponse(
            id=session.id,
            candidate_id=session.candidate_id,
            vacancy_id=session.vacancy_id,
            status=session.status,
            started_at=session.started_at,
            finished_at=session.finished_at,
            total_score=float(session.total_score) if session.total_score else None,
            current_step=session.current_step,
            qa_records=qa_responses,
            created_at=session.created_at,
            updated_at=session.updated_at
        )

    async def get_session_results(self, session_id: str) -> Dict[str, Any]:
        """Get session results with Q&A details"""
        session = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not session:
            raise ValueError("Session not found")

        # Get Q&A records with scores
        qa_records = self.db.query(QA).filter(QA.session_id == session_id).all()
        
        qa_responses = []
        for qa_record in qa_records:
            # Get scores for this Q&A
            scores = self.db.query(QAScore, Criteria).join(
                Criteria, QAScore.criterion_id == Criteria.id
            ).filter(QAScore.qa_id == qa_record.id).all()
            
            score_responses = []
            for score, criterion in scores:
                score_responses.append({
                    "criterion_id": criterion.id,
                    "criterion_name": criterion.name,
                    "score": float(score.score),
                    "evidence": score.evidence,
                    "red_flag": score.red_flag
                })
            
            qa_responses.append({
                "id": qa_record.id,
                "step_no": qa_record.step_no,
                "question_text": qa_record.question_text,
                "answer_text": qa_record.answer_text,
                "audio_url": qa_record.audio_url,
                "tone": qa_record.tone,
                "passed": qa_record.passed,
                "scores": score_responses,
                "created_at": qa_record.created_at.isoformat() if qa_record.created_at else None
            })

        return {
            "session_id": session.id,
            "candidate_id": session.candidate_id,
            "vacancy_id": session.vacancy_id,
            "status": session.status,
            "started_at": session.started_at.isoformat() if session.started_at else None,
            "finished_at": session.finished_at.isoformat() if session.finished_at else None,
            "total_score": float(session.total_score) if session.total_score else None,
            "current_step": session.current_step,
            "qa_records": qa_responses,
            "created_at": session.created_at.isoformat() if session.created_at else None,
            "updated_at": session.updated_at.isoformat() if session.updated_at else None
        }

    async def review_answer(self, qa_id: str, review_data: Dict[str, Any]) -> Dict[str, Any]:
        """Manually review and override answer scores"""
        qa = self.db.query(QA).filter(QA.id == qa_id).first()
        if not qa:
            raise ValueError("Q&A record not found")

        # Update scores based on review data
        per_criterion_override = review_data.get("per_criterion_override", [])
        
        for override in per_criterion_override:
            criterion_id = override.get("criterion_id")
            new_score = override.get("score")
            new_evidence = override.get("evidence")
            
            if criterion_id and new_score is not None:
                score = self.db.query(QAScore).filter(
                    and_(
                        QAScore.qa_id == qa_id,
                        QAScore.criterion_id == criterion_id
                    )
                ).first()
                
                if score:
                    score.score = new_score
                    if new_evidence:
                        score.evidence = new_evidence
                    score.updated_at = datetime.utcnow()

        self.db.commit()
        
        return {
            "status": "success",
            "qa_id": qa_id,
            "message": "Scores updated successfully"
        }

    async def export_session_report(self, session_id: str, format: str = "pdf") -> Dict[str, Any]:
        """Export session report in specified format"""
        session_detail = await self.get_session_detail(session_id)
        
        if format == "pdf":
            # This would generate PDF report
            return {
                "status": "success",
                "format": "pdf",
                "download_url": f"/reports/{session_id}.pdf",
                "session": session_detail
            }
        elif format == "csv":
            # This would generate CSV report
            return {
                "status": "success",
                "format": "csv",
                "download_url": f"/reports/{session_id}.csv",
                "session": session_detail
            }
        else:
            raise ValueError(f"Unsupported format: {format}")
