"""
Main API router for TTS service
"""
from fastapi import APIRouter

from app.api.v1.endpoints import synthesize

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(synthesize.router, prefix="/tts", tags=["tts"])
