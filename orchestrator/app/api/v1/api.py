"""
Main API router for orchestrator service
"""
from fastapi import APIRouter

from app.api.v1.endpoints import sessions, webhooks, hr, monitoring, vacancies, smart_scenario, llm_interview

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
api_router.include_router(hr.router, prefix="/hr", tags=["hr"])
api_router.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])
api_router.include_router(vacancies.router, prefix="/vacancies", tags=["vacancies"])
api_router.include_router(smart_scenario.router, prefix="/smart-scenario", tags=["smart-scenario"])
api_router.include_router(llm_interview.router, prefix="/llm-interview", tags=["llm-interview"])
