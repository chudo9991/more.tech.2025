"""
Transcription schemas for STT service
"""
from typing import List, Dict, Any
from pydantic import BaseModel


class TranscribeRequest(BaseModel):
    """Request schema for transcription"""
    audio_url: str
    language: str = "ru"
    vad_enabled: bool = True


class TranscribeSegment(BaseModel):
    """Individual transcription segment"""
    start: float
    end: float
    text: str
    confidence: float


class TranscribeResponse(BaseModel):
    """Response schema for transcription"""
    text: str
    segments: List[TranscribeSegment]
    pre_answer_pause_s: float
    speech_rate_wpm: float
    confidence: float

    class Config:
        from_attributes = True
