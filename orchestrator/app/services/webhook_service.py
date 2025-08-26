"""
Webhook service for handling SIP provider events
"""
import uuid
from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session as DBSession

from app.models import Session as SessionModel


class WebhookService:
    def __init__(self, db: DBSession):
        self.db = db

    async def handle_call_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle call events from SIP provider"""
        event_type = event_data.get("event")
        
        if event_type == "call_start":
            return await self._handle_call_start(event_data)
        elif event_type == "call_answer":
            return await self._handle_call_answer(event_data)
        elif event_type == "call_end":
            return await self._handle_call_end(event_data)
        else:
            raise ValueError(f"Unknown event type: {event_type}")

    async def handle_record_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle recording events from SIP provider"""
        record_url = event_data.get("record_url")
        session_id = event_data.get("session_id")
        
        if not record_url or not session_id:
            raise ValueError("Missing required fields: record_url or session_id")
        
        # Store recording URL in media table
        # This would be implemented with Media model
        
        return {
            "status": "success",
            "record_url": record_url,
            "session_id": session_id
        }

    async def _handle_call_start(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle call start event"""
        call_id = event_data.get("call_id")
        phone = event_data.get("phone")
        
        # Create or find session based on call_id
        session = self.db.query(SessionModel).filter(
            SessionModel.id == call_id
        ).first()
        
        if not session:
            # Create new session
            session = SessionModel(
                id=call_id,
                status="created"
            )
            self.db.add(session)
            self.db.commit()
        
        return {
            "status": "success",
            "call_id": call_id,
            "session_id": session.id
        }

    async def _handle_call_answer(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle call answer event"""
        call_id = event_data.get("call_id")
        
        session = self.db.query(SessionModel).filter(
            SessionModel.id == call_id
        ).first()
        
        if session:
            session.status = "in_progress"
            self.db.commit()
        
        return {
            "status": "success",
            "call_id": call_id
        }

    async def _handle_call_end(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle call end event"""
        call_id = event_data.get("call_id")
        
        session = self.db.query(SessionModel).filter(
            SessionModel.id == call_id
        ).first()
        
        if session:
            session.status = "completed"
            self.db.commit()
        
        return {
            "status": "success",
            "call_id": call_id
        }
