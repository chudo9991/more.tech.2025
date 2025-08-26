"""
HR panel schemas
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class SessionListResponse(BaseModel):
    id: str
    candidate_id: Optional[int]
    vacancy_id: Optional[str]
    status: str
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    total_score: Optional[float]
    current_step: int
    created_at: datetime

    class Config:
        from_attributes = True


class QAScoreResponse(BaseModel):
    criterion_id: str
    criterion_name: str
    score: float
    evidence: Optional[str]
    red_flag: bool

    class Config:
        from_attributes = True


class QAResponse(BaseModel):
    id: int
    step_no: int
    question_text: str
    answer_text: Optional[str]
    audio_url: Optional[str]
    tone: Optional[str]
    passed: Optional[bool]
    scores: List[QAScoreResponse]
    created_at: datetime

    class Config:
        from_attributes = True


class SessionDetailResponse(BaseModel):
    id: str
    candidate_id: Optional[int]
    vacancy_id: Optional[str]
    status: str
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    total_score: Optional[float]
    current_step: int
    qa_records: List[QAResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
