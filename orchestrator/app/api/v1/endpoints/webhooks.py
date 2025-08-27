"""
Webhook endpoints for SIP provider integration
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Request, Header, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.webhook_service import WebhookService

router = APIRouter()


@router.post("/call")
async def handle_call_webhook(
    request: Request,
    x_request_id: str = Header(None),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Handle call events from SIP provider"""
    try:
        webhook_service = WebhookService(db)
        event_data = await request.json()
        
        # Add request ID for tracing
        if x_request_id:
            event_data["request_id"] = x_request_id
        
        result = await webhook_service.handle_call_event(event_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/record")
async def handle_record_webhook(
    request: Request,
    x_request_id: str = Header(None),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Handle recording events from SIP provider"""
    try:
        webhook_service = WebhookService(db)
        event_data = await request.json()
        
        # Add request ID for tracing
        if x_request_id:
            event_data["request_id"] = x_request_id
        
        result = await webhook_service.handle_record_event(event_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
