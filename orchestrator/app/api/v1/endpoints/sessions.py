"""
Session management endpoints
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Body, Query, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.session import SessionCreate, SessionResponse, SessionNextResponse, SessionAggregatedResponse
from app.services.session_service import SessionService

router = APIRouter()


@router.post("/", response_model=SessionResponse)
async def create_session(
    session_data: SessionCreate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Create a new interview session"""
    try:
        session_service = SessionService(db)
        session = session_service.create_session(session_data)
        return session
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/messages")
async def save_message(
    message_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Save a chat message to database"""
    try:
        session_id = message_data.get("session_id")
        message_id = message_data.get("message_id")
        text = message_data.get("text")
        message_type = message_data.get("message_type")
        timestamp = message_data.get("timestamp")
        audio_url = message_data.get("audio_url")
        transcription_confidence = message_data.get("transcription_confidence")
        tone_analysis = message_data.get("tone_analysis")
        
        if not all([session_id, message_id, text, message_type]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        session_service = SessionService(db)
        result = session_service.save_message(
            session_id, message_id, text, message_type, timestamp, 
            audio_url, transcription_confidence, tone_analysis
        )
        return {"status": "success", "message_id": message_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/messages")
async def get_messages(
    session_id: str = Query(..., description="Session ID"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get all messages for a session"""
    try:
        session_service = SessionService(db)
        messages = session_service.get_messages(session_id)
        return {"status": "success", "messages": messages}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/audio/{session_id}/{filename}")
async def get_audio_file(
    session_id: str,
    filename: str,
    db: Session = Depends(get_db)
):
    """Get audio file from MinIO"""
    try:
        session_service = SessionService(db)
        audio_data = session_service.get_audio_file(session_id, filename)
        return Response(
            content=audio_data,
            media_type="audio/webm",
            headers={"Content-Disposition": f"inline; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="Audio file not found")


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get session details and progress"""
    try:
        session_service = SessionService(db)
        session = session_service.get_session(session_id)
        return session
    except Exception as e:
        raise HTTPException(status_code=404, detail="Session not found")


@router.patch("/{session_id}")
async def update_session(
    session_id: str,
    session_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Update session details"""
    try:
        session_service = SessionService(db)
        result = session_service.update_session(session_id, session_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{session_id}")
async def delete_session(
    session_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Delete a session and all related data"""
    try:
        session_service = SessionService(db)
        result = session_service.delete_session(session_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{session_id}/next", response_model=SessionNextResponse)
async def get_next_question(
    session_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get the next question for the session"""
    try:
        session_service = SessionService(db)
        next_question = session_service.get_next_question(session_id)
        return next_question
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{session_id}/answer")
async def submit_answer(
    session_id: str,
    answer_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Submit an answer for a question"""
    try:
        question_id = answer_data.get("question_id")
        audio_url = answer_data.get("audio_url")
        
        if not question_id or not audio_url:
            raise HTTPException(status_code=400, detail="question_id and audio_url are required")
        
        session_service = SessionService(db)
        result = await session_service.submit_answer(session_id, question_id, audio_url)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{session_id}/results", response_model=SessionAggregatedResponse)
async def get_session_results(
    session_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get aggregated session results"""
    try:
        session_service = SessionService(db)
        results = session_service.aggregate_session_results(session_id)
        return results
    except Exception as e:
        raise HTTPException(status_code=404, detail="Session not found")
