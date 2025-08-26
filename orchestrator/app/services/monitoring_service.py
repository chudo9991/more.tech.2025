"""
Monitoring and logging service
"""
import time
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import func, and_
import structlog

from app.models import Session as SessionModel, QA, QAScore
from app.core.config import settings


class MonitoringService:
    def __init__(self, db: DBSession):
        self.db = db
        self.logger = structlog.get_logger()

    async def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health metrics"""
        try:
            # Database health
            db_health = await self._check_database_health()
            
            # Service metrics
            service_metrics = await self._get_service_metrics()
            
            # Performance metrics
            performance_metrics = await self._get_performance_metrics()
            
            return {
                "status": "healthy" if db_health["status"] == "healthy" else "degraded",
                "timestamp": datetime.utcnow().isoformat(),
                "database": db_health,
                "services": service_metrics,
                "performance": performance_metrics
            }
        except Exception as e:
            self.logger.error("Failed to get system health", error=str(e))
            return {
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e)
            }

    async def get_session_metrics(self, time_range: str = "24h") -> Dict[str, Any]:
        """Get session-related metrics"""
        try:
            end_time = datetime.utcnow()
            
            if time_range == "1h":
                start_time = end_time - timedelta(hours=1)
            elif time_range == "24h":
                start_time = end_time - timedelta(days=1)
            elif time_range == "7d":
                start_time = end_time - timedelta(days=7)
            elif time_range == "30d":
                start_time = end_time - timedelta(days=30)
            else:
                start_time = end_time - timedelta(days=1)

            # Total sessions
            total_sessions = self.db.query(SessionModel).filter(
                and_(
                    SessionModel.created_at >= start_time,
                    SessionModel.created_at <= end_time
                )
            ).count()

            # Completed sessions
            completed_sessions = self.db.query(SessionModel).filter(
                and_(
                    SessionModel.created_at >= start_time,
                    SessionModel.created_at <= end_time,
                    SessionModel.status == "completed"
                )
            ).count()

            # Failed sessions
            failed_sessions = self.db.query(SessionModel).filter(
                and_(
                    SessionModel.created_at >= start_time,
                    SessionModel.created_at <= end_time,
                    SessionModel.status == "failed"
                )
            ).count()

            # Average completion time
            completion_times = self.db.query(
                func.extract('epoch', SessionModel.completed_at - SessionModel.created_at)
            ).filter(
                and_(
                    SessionModel.created_at >= start_time,
                    SessionModel.created_at <= end_time,
                    SessionModel.status == "completed",
                    SessionModel.completed_at.isnot(None)
                )
            ).all()

            avg_completion_time = sum(t[0] for t in completion_times) / len(completion_times) if completion_times else 0

            # Average scores
            avg_scores = self.db.query(func.avg(SessionModel.total_score)).filter(
                and_(
                    SessionModel.created_at >= start_time,
                    SessionModel.created_at <= end_time,
                    SessionModel.status == "completed",
                    SessionModel.total_score.isnot(None)
                )
            ).scalar()

            return {
                "time_range": time_range,
                "total_sessions": total_sessions,
                "completed_sessions": completed_sessions,
                "failed_sessions": failed_sessions,
                "completion_rate": completed_sessions / total_sessions if total_sessions > 0 else 0,
                "avg_completion_time_minutes": avg_completion_time / 60 if avg_completion_time > 0 else 0,
                "avg_score": float(avg_scores) if avg_scores else 0,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat()
            }
        except Exception as e:
            self.logger.error("Failed to get session metrics", error=str(e))
            raise Exception(f"Failed to get session metrics: {str(e)}")

    async def get_error_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent error logs"""
        try:
            # In a real implementation, this would query a logging database
            # For now, return mock data
            return [
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "level": "ERROR",
                    "service": "orchestrator",
                    "message": "Failed to process webhook",
                    "details": "Connection timeout to STT service"
                },
                {
                    "timestamp": (datetime.utcnow() - timedelta(minutes=5)).isoformat(),
                    "level": "WARNING",
                    "service": "scoring",
                    "message": "LLM response validation failed",
                    "details": "Invalid JSON format in response"
                }
            ]
        except Exception as e:
            self.logger.error("Failed to get error logs", error=str(e))
            return []

    async def log_event(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Log an event"""
        try:
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "event_type": event_type,
                "event_data": event_data,
                "service": "orchestrator"
            }
            
            self.logger.info("Event logged", **log_entry)
            
            # In a real implementation, this would be stored in a logging database
            # For now, just log to structured logger
            
        except Exception as e:
            self.logger.error("Failed to log event", error=str(e))

    async def get_performance_alerts(self) -> List[Dict[str, Any]]:
        """Get performance alerts"""
        try:
            alerts = []
            
            # Check for high error rates
            recent_errors = await self.get_error_logs(limit=50)
            if len(recent_errors) > 10:
                alerts.append({
                    "type": "high_error_rate",
                    "severity": "warning",
                    "message": f"High error rate detected: {len(recent_errors)} errors in recent logs",
                    "timestamp": datetime.utcnow().isoformat()
                })

            # Check for slow response times
            session_metrics = await self.get_session_metrics("1h")
            if session_metrics["avg_completion_time_minutes"] > 10:
                alerts.append({
                    "type": "slow_response_time",
                    "severity": "warning",
                    "message": f"Slow response time: {session_metrics['avg_completion_time_minutes']:.1f} minutes average",
                    "timestamp": datetime.utcnow().isoformat()
                })

            # Check for low completion rates
            if session_metrics["completion_rate"] < 0.8:
                alerts.append({
                    "type": "low_completion_rate",
                    "severity": "critical",
                    "message": f"Low completion rate: {session_metrics['completion_rate']:.1%}",
                    "timestamp": datetime.utcnow().isoformat()
                })

            return alerts
        except Exception as e:
            self.logger.error("Failed to get performance alerts", error=str(e))
            return []

    async def _check_database_health(self) -> Dict[str, Any]:
        """Check database health"""
        try:
            start_time = time.time()
            
            # Simple query to check database connectivity
            result = self.db.query(func.count(SessionModel.id)).scalar()
            
            response_time = time.time() - start_time
            
            return {
                "status": "healthy",
                "response_time_ms": response_time * 1000,
                "active_connections": 1,  # Mock value
                "total_sessions": result
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "response_time_ms": 0
            }

    async def _get_service_metrics(self) -> Dict[str, Any]:
        """Get service metrics"""
        try:
            # Mock service metrics - in real implementation would query service health endpoints
            return {
                "stt_service": {
                    "status": "healthy",
                    "response_time_ms": 150,
                    "uptime_percentage": 99.9
                },
                "tts_service": {
                    "status": "healthy",
                    "response_time_ms": 200,
                    "uptime_percentage": 99.8
                },
                "scoring_service": {
                    "status": "healthy",
                    "response_time_ms": 300,
                    "uptime_percentage": 99.7
                }
            }
        except Exception as e:
            return {
                "error": str(e)
            }

    async def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        try:
            # Get recent session metrics
            session_metrics = await self.get_session_metrics("1h")
            
            return {
                "requests_per_minute": session_metrics["total_sessions"] / 60 if session_metrics["total_sessions"] > 0 else 0,
                "avg_response_time_ms": session_metrics["avg_completion_time_minutes"] * 60 * 1000,
                "error_rate": session_metrics["failed_sessions"] / session_metrics["total_sessions"] if session_metrics["total_sessions"] > 0 else 0,
                "success_rate": session_metrics["completion_rate"]
            }
        except Exception as e:
            return {
                "error": str(e)
            }

    async def export_monitoring_report(self, format: str = "json") -> Dict[str, Any]:
        """Export monitoring report"""
        try:
            # Gather all monitoring data
            system_health = await self.get_system_health()
            session_metrics = await self.get_session_metrics("24h")
            performance_alerts = await self.get_performance_alerts()
            error_logs = await self.get_error_logs(limit=50)

            report_data = {
                "report_type": "monitoring",
                "generated_at": datetime.utcnow().isoformat(),
                "system_health": system_health,
                "session_metrics": session_metrics,
                "performance_alerts": performance_alerts,
                "recent_errors": error_logs
            }

            if format.lower() == "json":
                return {
                    "format": "json",
                    "timestamp": datetime.utcnow().isoformat(),
                    "filename": f"monitoring_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json",
                    "content": json.dumps(report_data, indent=2)
                }
            else:
                raise ValueError(f"Unsupported format: {format}")

        except Exception as e:
            self.logger.error("Failed to export monitoring report", error=str(e))
            raise Exception(f"Failed to export monitoring report: {str(e)}")
