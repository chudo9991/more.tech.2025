"""
Tone analysis endpoints for scoring service
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException

from app.schemas.tone import ToneRequest, ToneResponse
from app.services.tone_service import ToneService

router = APIRouter()


@router.post("/analyze", response_model=ToneResponse)
async def analyze_tone(
    request: ToneRequest
) -> Dict[str, Any]:
    """Analyze tone and paralinguistic features of text"""
    try:
        tone_service = ToneService()
        result = await tone_service.analyze_tone(
            text=request.text,
            language=request.language
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
