"""
Main API router for STT service
"""
from fastapi import APIRouter

from app.api.v1.endpoints import transcribe

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(transcribe.router, prefix="/stt", tags=["stt"])
