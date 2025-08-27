"""
Avatar service API router
"""
from fastapi import APIRouter

from app.api.v1.endpoints import avatar

api_router = APIRouter()

api_router.include_router(avatar.router, prefix="/avatar", tags=["avatar"])
