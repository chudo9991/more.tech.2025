"""
HR panel endpoints
"""
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.hr import SessionListResponse, SessionDetailResponse, VacancyResponse
from app.services.hr_service import HRService
from app.services.export_service import ExportService

router = APIRouter()


@router.get("/vacancies", response_model=List[VacancyResponse])
async def get_vacancies(
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Get list of vacancies"""
    try:
        hr_service = HRService(db)
        vacancies = await hr_service.get_vacancies()
        return vacancies
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sessions", response_model=List[SessionListResponse])
async def get_sessions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: str = Query(None),
    vacancy_id: str = Query(None),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Get list of interview sessions"""
    try:
        hr_service = HRService(db)
        sessions = await hr_service.get_sessions(skip, limit, status, vacancy_id)
        return sessions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sessions/{session_id}", response_model=SessionDetailResponse)
async def get_session_detail(
    session_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get detailed session information"""
    try:
        hr_service = HRService(db)
        session = await hr_service.get_session_detail(session_id)
        return session
    except Exception as e:
        raise HTTPException(status_code=404, detail="Session not found")


@router.get("/sessions/{session_id}/results")
async def get_session_results(
    session_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get session results with Q&A details"""
    try:
        hr_service = HRService(db)
        results = await hr_service.get_session_results(session_id)
        return results
    except Exception as e:
        raise HTTPException(status_code=404, detail="Session not found")


@router.post("/qa/{qa_id}/review")
async def review_answer(
    qa_id: str,
    review_data: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Manually review and override answer scores"""
    try:
        hr_service = HRService(db)
        result = await hr_service.review_answer(qa_id, review_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.get("/sessions/{session_id}/export")
async def export_session_report(
    session_id: str,
    format: str = Query("json", regex="^(json|csv|summary|pdf|html)$"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Export session report in specified format"""
    try:
        export_service = ExportService(db)
        result = await export_service.export_session_report(session_id, format)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/vacancies/{vacancy_id}/export")
async def export_vacancy_report(
    vacancy_id: str,
    format: str = Query("json", regex="^(json|csv|pdf|html)$"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Export vacancy report with all sessions"""
    try:
        export_service = ExportService(db)
        result = await export_service.export_vacancy_report(vacancy_id, format)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
