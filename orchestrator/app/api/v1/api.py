"""
Main API router for orchestrator service
"""
from fastapi import APIRouter

from app.api.v1.endpoints import sessions, webhooks, hr, monitoring

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
api_router.include_router(hr.router, prefix="/hr", tags=["hr"])
api_router.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])
