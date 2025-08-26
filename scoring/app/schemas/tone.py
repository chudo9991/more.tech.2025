"""
Tone analysis schemas for scoring service
"""
from pydantic import BaseModel


class ToneRequest(BaseModel):
    """Request schema for tone analysis"""
    text: str
    language: str = "ru"


class Paralinguistic(BaseModel):
    """Paralinguistic features"""
    answer_duration_s: float
    pre_answer_pause_s: float
    avg_silence_ratio: float
    speech_rate_wpm: float


class ToneResponse(BaseModel):
    """Response schema for tone analysis"""
    tone: str  # positive, neutral, negative
    confidence: float
    paraling: Paralinguistic

    class Config:
        from_attributes = True
