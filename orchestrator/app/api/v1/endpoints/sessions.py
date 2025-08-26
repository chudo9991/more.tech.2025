"""
Session management endpoints
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Body
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
        session = await session_service.create_session(session_data)
        return session
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
        next_question = await session_service.get_next_question(session_id)
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


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get session details and progress"""
    try:
        session_service = SessionService(db)
        session = await session_service.get_session(session_id)
        return session
    except Exception as e:
        raise HTTPException(status_code=404, detail="Session not found")


@router.get("/{session_id}/results", response_model=SessionAggregatedResponse)
async def get_session_results(
    session_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get aggregated session results"""
    try:
        session_service = SessionService(db)
        results = await session_service.aggregate_session_results(session_id)
        return results
    except Exception as e:
        raise HTTPException(status_code=404, detail="Session not found")
