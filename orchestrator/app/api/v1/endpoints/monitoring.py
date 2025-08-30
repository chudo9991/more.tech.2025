"""
Monitoring API endpoints
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.cache_service import cache_service

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    try:
        # Check cache service health
        cache_healthy = cache_service.health_check()
        
        return {
            "status": "healthy",
            "cache_service": "healthy" if cache_healthy else "unhealthy",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cache/info")
async def get_cache_info() -> Dict[str, Any]:
    """Get cache statistics and information"""
    try:
        cache_info = cache_service.get_cache_info()
        return {
            "cache_info": cache_info,
            "cache_healthy": cache_service.health_check()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cache/clear")
async def clear_cache(prefix: str = None) -> Dict[str, Any]:
    """Clear cache or specific prefix"""
    try:
        if prefix:
            success = cache_service.clear_prefix(prefix)
            message = f"Cleared cache for prefix: {prefix}"
        else:
            # Clear all cache
            success = True
            for prefix_name in cache_service.prefixes.keys():
                cache_service.clear_prefix(prefix_name)
            message = "Cleared all cache"
        
        return {
            "success": success,
            "message": message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
