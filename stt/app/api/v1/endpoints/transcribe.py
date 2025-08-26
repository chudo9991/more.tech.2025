"""
Transcription endpoints for STT service
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException

from app.schemas.transcribe import TranscribeRequest, TranscribeResponse
from app.services.transcribe_service import TranscribeService

router = APIRouter()


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(
    request: TranscribeRequest
) -> Dict[str, Any]:
    """Transcribe audio file to text"""
    try:
        transcribe_service = TranscribeService()
        result = await transcribe_service.transcribe(
            audio_url=request.audio_url,
            language=request.language,
            vad_enabled=request.vad_enabled
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
