"""
Avatar service endpoints
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends

from app.schemas.avatar import (
    AvatarGenerateRequest, 
    AvatarResponse
)
from app.services.avatar_service import AvatarService

router = APIRouter()


@router.post("/generate", response_model=AvatarResponse)
async def generate_avatar(
    request: AvatarGenerateRequest
) -> Dict[str, Any]:
    """Generate avatar for interview session"""
    try:
        avatar_service = AvatarService()
        result = await avatar_service.generate_avatar(
            session_id=request.session_id,
            style=request.style,
            gender=request.gender,
            age_range=request.age_range,
            profession=request.profession,
            custom_prompt=request.custom_prompt
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))





@router.get("/{session_id}")
async def get_avatar(session_id: str) -> Dict[str, Any]:
    """Get avatar for session"""
    try:
        avatar_service = AvatarService()
        avatar_url = await avatar_service.get_avatar_url(session_id)
        
        if avatar_url:
            return {
                "avatar_url": avatar_url,
                "session_id": session_id
            }
        else:
            raise HTTPException(status_code=404, detail="Avatar not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/healthz")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "avatar",
        "version": "1.0.0"
    }
