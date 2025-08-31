"""
API endpoints for contextual questions
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.contextual_question_generator import ContextualQuestionGenerator
from app.services.llm_question_generator import LLMQuestionGenerator
from app.schemas.contextual_question import (
    ContextualQuestionGenerationRequest,
    ContextualQuestionGenerationResponse,
    ContextualQuestionResponse,
    ContextualQuestionListResponse,
    ContextualQuestionUsageRequest,
    ContextualQuestionUsageResponse
)

router = APIRouter()


@router.post("/sessions/{session_id}/contextual-questions", response_model=ContextualQuestionGenerationResponse)
async def generate_contextual_questions(
    session_id: str,
    request: ContextualQuestionGenerationRequest,
    db: Session = Depends(get_db)
):
    """
    Генерирует контекстные вопросы для ноды
    
    Args:
        session_id: ID сессии интервью
        request: Запрос с параметрами генерации
        db: Сессия базы данных
        
    Returns:
        Сгенерированные контекстные вопросы
    """
    try:
        generator = ContextualQuestionGenerator(db)
        
        contextual_questions = await generator.generate_contextual_questions(
            session_id=session_id,
            scenario_node_id=request.scenario_node_id,
            max_questions=request.max_questions
        )
        
        return ContextualQuestionGenerationResponse(
            success=True,
            questions=contextual_questions,
            message=f"Сгенерировано {len(contextual_questions)} контекстных вопросов"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка генерации контекстных вопросов: {str(e)}"
        )


@router.get("/sessions/{session_id}/contextual-questions/{node_id}", response_model=ContextualQuestionListResponse)
async def get_contextual_questions(
    session_id: str,
    node_id: str,
    db: Session = Depends(get_db)
):
    """
    Получает контекстные вопросы для ноды
    
    Args:
        session_id: ID сессии интервью
        node_id: ID ноды сценария
        db: Сессия базы данных
        
    Returns:
        Список контекстных вопросов
    """
    try:
        generator = ContextualQuestionGenerator(db)
        
        contextual_questions = generator.get_contextual_questions_for_node(
            session_id=session_id,
            scenario_node_id=node_id
        )
        
        return ContextualQuestionListResponse(
            questions=contextual_questions,
            total=len(contextual_questions)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения контекстных вопросов: {str(e)}"
        )


@router.get("/sessions/{session_id}/contextual-questions/{node_id}/next", response_model=ContextualQuestionResponse)
async def get_next_contextual_question(
    session_id: str,
    node_id: str,
    db: Session = Depends(get_db)
):
    """
    Получает следующий неиспользованный контекстный вопрос
    
    Args:
        session_id: ID сессии интервью
        node_id: ID ноды сценария
        db: Сессия базы данных
        
    Returns:
        Следующий контекстный вопрос
    """
    try:
        generator = ContextualQuestionGenerator(db)
        
        contextual_question = generator.get_next_contextual_question(
            session_id=session_id,
            scenario_node_id=node_id
        )
        
        if not contextual_question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Нет доступных контекстных вопросов"
            )
        
        return contextual_question
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения следующего вопроса: {str(e)}"
        )


@router.post("/sessions/{session_id}/contextual-questions/{question_id}/use", response_model=ContextualQuestionUsageResponse)
async def mark_question_as_used(
    session_id: str,
    question_id: str,
    request: ContextualQuestionUsageRequest,
    db: Session = Depends(get_db)
):
    """
    Отмечает контекстный вопрос как использованный
    
    Args:
        session_id: ID сессии интервью
        question_id: ID контекстного вопроса
        request: Запрос с данными использования
        db: Сессия базы данных
        
    Returns:
        Результат операции
    """
    try:
        generator = ContextualQuestionGenerator(db)
        
        success = generator.mark_question_as_used(question_id=question_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Контекстный вопрос не найден"
            )
        
        from datetime import datetime
        
        return ContextualQuestionUsageResponse(
            success=True,
            question_id=question_id,
            used_at=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка отметки вопроса: {str(e)}"
        )


@router.get("/sessions/{session_id}/contextual-questions/{node_id}/status")
async def get_contextual_questions_status(
    session_id: str,
    node_id: str,
    db: Session = Depends(get_db)
):
    """
    Получает статус контекстных вопросов для ноды
    
    Args:
        session_id: ID сессии интервью
        node_id: ID ноды сценария
        db: Сессия базы данных
        
    Returns:
        Статус контекстных вопросов
    """
    try:
        generator = ContextualQuestionGenerator(db)
        
        status_data = generator.get_contextual_questions_status(
            session_id=session_id,
            scenario_node_id=node_id
        )
        
        return status_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения статуса: {str(e)}"
        )


@router.post("/sessions/{session_id}/contextual-questions/current/generate")
async def generate_contextual_questions_for_current_node(
    session_id: str,
    max_questions: int = 3,
    db: Session = Depends(get_db)
):
    """
    Генерирует контекстные вопросы для текущего узла
    
    Args:
        session_id: ID сессии интервью
        max_questions: Максимальное количество вопросов
        db: Сессия базы данных
        
    Returns:
        Сгенерированные контекстные вопросы
    """
    try:
        from app.services.scenario_navigation_service import ScenarioNavigationService
        
        navigation_service = ScenarioNavigationService(db)
        
        contextual_questions = await navigation_service.generate_contextual_questions_for_current_node(
            session_id=session_id,
            max_questions=max_questions
        )
        
        return {
            "success": True,
            "questions": contextual_questions,
            "message": f"Сгенерировано {len(contextual_questions)} контекстных вопросов для текущего узла"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка генерации контекстных вопросов: {str(e)}"
        )


@router.get("/sessions/{session_id}/contextual-questions/current/status")
async def get_current_contextual_questions_status(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Получает статус контекстных вопросов для текущего узла
    
    Args:
        session_id: ID сессии интервью
        db: Сессия базы данных
        
    Returns:
        Статус контекстных вопросов
    """
    try:
        from app.services.scenario_navigation_service import ScenarioNavigationService
        
        navigation_service = ScenarioNavigationService(db)
        
        status_data = navigation_service.get_contextual_questions_status(session_id=session_id, node_id=None)
        
        return status_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения статуса: {str(e)}"
        )
