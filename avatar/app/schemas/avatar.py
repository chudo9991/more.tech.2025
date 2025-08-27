"""
Avatar service schemas
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class AvatarGenerateRequest(BaseModel):
    """Request for avatar generation"""
    session_id: str
    style: str = "professional"
    gender: Optional[str] = None
    age_range: Optional[str] = None
    profession: Optional[str] = None
    custom_prompt: Optional[str] = None


class AvatarResponse(BaseModel):
    """Response for avatar generation"""
    avatar_url: str
    session_id: str
    style: str
    metadata: Dict[str, Any] = {}





class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str
