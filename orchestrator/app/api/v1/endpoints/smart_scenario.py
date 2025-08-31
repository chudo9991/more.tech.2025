"""
Smart scenario API endpoints
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.scenario_navigation_service import ScenarioNavigationService
from app.services.negative_response_analyzer import NegativeResponseAnalyzer
from app.schemas.smart_scenario import (
    SmartScenarioNavigationRequest,
    SmartScenarioNavigationResponse,
    SessionContextResponse
)

router = APIRouter()


@router.post("/navigate", response_model=SmartScenarioNavigationResponse)
async def navigate_scenario(
    request: SmartScenarioNavigationRequest,
    db: Session = Depends(get_db)
):
    """
    Умная навигация по сценарию интервью
    """
    try:
        navigation_service = ScenarioNavigationService(db)
        
        # Если есть ответ, обновляем контекст
        if request.current_answer:
            # Получаем оценку ответа (в реальной системе это будет из LLM)
            answer_score = request.answer_score or 0.5
            
            # Обновляем контекст
            context_update = navigation_service.update_context_after_answer(
                request.session_id,
                "current_question_id",  # В реальной системе это будет из сессии
                request.current_answer,
                answer_score
            )
        
        # Получаем следующий вопрос
        next_question = navigation_service.get_next_question(request.session_id)
        
        if not next_question:
            return SmartScenarioNavigationResponse(
                should_terminate=True,
                transition_reason="Нет доступных вопросов"
            )
        
        # Проверяем, нужно ли завершить интервью
        if navigation_service.should_terminate_interview(request.session_id):
            return SmartScenarioNavigationResponse(
                should_terminate=True,
                transition_reason="Условия завершения интервью выполнены"
            )
        
        # Получаем доступные переходы
        available_transitions = navigation_service.get_available_transitions(request.session_id)
        
        return SmartScenarioNavigationResponse(
            next_node_id=next_question.get('node_id'),
            next_question_id=next_question.get('question_id'),
            question_text=next_question.get('question_text'),
            transition_reason="Успешная навигация",
            should_terminate=next_question.get('should_terminate', False),
            available_transitions=available_transitions,
            has_contextual_questions=next_question.get('has_contextual_questions', False),
            contextual_questions_count=next_question.get('contextual_questions_count', 0)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка навигации: {str(e)}"
        )


@router.get("/context/{session_id}", response_model=SessionContextResponse)
async def get_session_context(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Получение контекста сессии
    """
    try:
        navigation_service = ScenarioNavigationService(db)
        session_context = navigation_service.get_session_context(session_id)
        
        if not session_context:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Контекст сессии не найден"
            )
        
        return SessionContextResponse(
            id=session_context.id,
            session_id=session_context.session_id,
            skill_assessments=session_context.skill_assessments,
            negative_responses=session_context.negative_responses,
            current_path=session_context.current_path,
            context_data=session_context.context_data,
            current_node_id=session_context.current_node_id,
            scenario_id=session_context.scenario_id,
            created_at=session_context.created_at,
            updated_at=session_context.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения контекста: {str(e)}"
        )


@router.post("/analyze-negative")
async def analyze_negative_response(
    request: dict,
    db: Session = Depends(get_db)
):
    """
    Анализ негативного ответа
    """
    try:
        text = request.get("text", "")
        analyzer = NegativeResponseAnalyzer(db)
        analysis = analyzer.analyze_negative_patterns(text)
        
        return {
            "analysis": analysis,
            "is_negative": analysis['is_negative'],
            "confidence_level": analysis['confidence_level'],
            "patterns_found": analysis['negative_patterns_found']
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка анализа: {str(e)}"
        )


@router.post("/transitions")
async def get_available_transitions(
    request: dict,
    db: Session = Depends(get_db)
):
    """
    Получение доступных переходов для сессии
    """
    try:
        session_id = request.get("session_id", "")
        navigation_service = ScenarioNavigationService(db)
        transitions = navigation_service.get_available_transitions(session_id)
        
        return {
            "session_id": session_id,
            "available_transitions": transitions
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения переходов: {str(e)}"
        )


@router.post("/update-context")
async def update_session_context(
    request: dict,
    db: Session = Depends(get_db)
):
    """
    Обновление контекста сессии после ответа
    """
    try:
        session_id = request.get("session_id", "")
        question_id = request.get("question_id", "")
        answer_text = request.get("answer_text", "")
        answer_score = request.get("answer_score", 0.0)
        
        navigation_service = ScenarioNavigationService(db)
        context_update = navigation_service.update_context_after_answer(
            session_id, question_id, answer_text, answer_score
        )
        
        return {
            "session_id": session_id,
            "context_updated": True,
            "skill_assessments": context_update['skill_assessments'],
            "negative_responses": context_update['negative_responses'],
            "analysis": context_update['analysis']
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка обновления контекста: {str(e)}"
        )
