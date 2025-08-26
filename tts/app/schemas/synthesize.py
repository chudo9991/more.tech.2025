"""
Speech synthesis schemas for TTS service
"""
from typing import Dict, Any
from pydantic import BaseModel


class SynthesizeRequest(BaseModel):
    """Request schema for speech synthesis"""
    text: str
    voice: str = "default"
    speaker: str = "default"
    language: str = "ru"


class SynthesizeResponse(BaseModel):
    """Response schema for speech synthesis"""
    audio_url: str
    duration_ms: int
    text_length: int

    class Config:
        from_attributes = True
