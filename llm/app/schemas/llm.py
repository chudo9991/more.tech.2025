"""
LLM service schemas
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ScoringRequest(BaseModel):
    """Request for answer scoring"""
    vacancy_id: str
    question_id: str
    question: str
    answer_text: str
    criteria: List[Dict[str, Any]]
    rubric_version: str = "v1"


class CriterionScore(BaseModel):
    """Individual criterion score"""
    id: str
    score: float = Field(ge=0.0, le=1.0)
    evidence: Optional[str] = None
    red_flag: bool = False


class ScoringResponse(BaseModel):
    """Response for answer scoring"""
    overall_score: float = Field(ge=0.0, le=1.0)
    passed: bool
    per_criterion: List[CriterionScore]
    red_flags: List[str] = []
    explanations: List[str] = []
    version: str = "v1"


class ChatRequest(BaseModel):
    """Request for chat with avatar"""
    session_id: str
    message: str
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """Response for chat with avatar"""
    response: str
    avatar_emotion: str = "neutral"
    confidence: float = Field(ge=0.0, le=1.0)
    session_id: str


class ToneAnalysisRequest(BaseModel):
    """Request for tone analysis"""
    text: str
    session_id: str


class ToneAnalysisResponse(BaseModel):
    """Response for tone analysis"""
    emotion: str
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str
