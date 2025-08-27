"""
Session schemas
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    vacancy_id: str
    phone: Optional[str] = None
    email: Optional[str] = None


class SessionResponse(BaseModel):
    id: str
    vacancy_id: str
    phone: Optional[str]
    email: Optional[str]
    status: str
    current_step: int
    total_steps: int
    total_score: Optional[float] = None
    pass_rate: Optional[float] = None
    qa_count: Optional[int] = None
    created_at: Optional[datetime]
    finished_at: Optional[datetime]

    class Config:
        from_attributes = True


class SessionNextResponse(BaseModel):
    session_id: str
    question_id: str
    question_text: str
    question_type: str
    criteria: List[dict]
    current_step: int
    total_steps: int

    class Config:
        from_attributes = True


class SessionAggregatedResponse(BaseModel):
    """Aggregated session results"""
    session_id: str
    status: str
    total_questions: int
    answered_questions: int
    completion_rate: float
    total_score: float
    pass_rate: float
    started_at: Optional[str]
    completed_at: Optional[str]
    questions: List[dict]

    class Config:
        from_attributes = True
