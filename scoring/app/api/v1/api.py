"""
Main API router for scoring service
"""
from fastapi import APIRouter

from app.api.v1.endpoints import score, tone

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(score.router, prefix="/score", tags=["score"])
api_router.include_router(tone.router, prefix="/tone", tags=["tone"])
