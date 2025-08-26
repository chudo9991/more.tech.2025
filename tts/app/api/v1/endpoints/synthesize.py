"""
Speech synthesis endpoints for TTS service
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException

from app.schemas.synthesize import SynthesizeRequest, SynthesizeResponse
from app.services.synthesize_service import SynthesizeService

router = APIRouter()


@router.post("/synthesize", response_model=SynthesizeResponse)
async def synthesize_speech(
    request: SynthesizeRequest
) -> Dict[str, Any]:
    """Synthesize text to speech"""
    try:
        synthesize_service = SynthesizeService()
        result = await synthesize_service.synthesize(
            text=request.text,
            voice=request.voice,
            speaker=request.speaker,
            language=request.language
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
