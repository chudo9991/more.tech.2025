"""
HR service for managing interview data and reports
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import and_
from datetime import datetime

from app.models import Session as SessionModel, QA, QAScore, Criteria
from app.schemas.hr import SessionListResponse, SessionDetailResponse, QAResponse, QAScoreResponse


class HRService:
    def __init__(self, db: DBSession):
        self.db = db

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
        
        return [SessionListResponse.from_orm(session) for session in sessions]

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
