"""
Monitoring and logging endpoints
"""
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.monitoring_service import MonitoringService

router = APIRouter()


@router.get("/health")
async def get_system_health(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get overall system health"""
    try:
        monitoring_service = MonitoringService(db)
        return await monitoring_service.get_system_health()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/sessions")
async def get_session_metrics(
    time_range: str = Query("24h", regex="^(1h|24h|7d|30d)$"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get session-related metrics"""
    try:
        monitoring_service = MonitoringService(db)
        return await monitoring_service.get_session_metrics(time_range)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/logs/errors")
async def get_error_logs(
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Get recent error logs"""
    try:
        monitoring_service = MonitoringService(db)
        return await monitoring_service.get_error_logs(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts")
async def get_performance_alerts(
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Get performance alerts"""
    try:
        monitoring_service = MonitoringService(db)
        return await monitoring_service.get_performance_alerts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/logs/event")
async def log_event(
    event_type: str,
    event_data: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Log an event"""
    try:
        monitoring_service = MonitoringService(db)
        await monitoring_service.log_event(event_type, event_data)
        return {"status": "success", "message": "Event logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export")
async def export_monitoring_report(
    format: str = Query("json", regex="^(json)$"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Export monitoring report"""
    try:
        monitoring_service = MonitoringService(db)
        return await monitoring_service.export_monitoring_report(format)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
