"""
LLM Interview API endpoints
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.llm_question_generator import LLMQuestionGenerator
from app.schemas.smart_scenario import SmartScenarioNavigationRequest, SmartScenarioNavigationResponse

router = APIRouter()


@router.post("/generate-question")
async def generate_next_question(
    request: dict,
    db: Session = Depends(get_db)
):
    """
    Генерация следующего вопроса с помощью LLM
    """
    try:
        session_id = request.get("session_id", "")
        vacancy_id = request.get("vacancy_id", "")
        previous_answers = request.get("previous_answers", [])
        
        if not session_id or not vacancy_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="session_id и vacancy_id обязательны"
            )
        
        generator = LLMQuestionGenerator(db)
        question_data = await generator.generate_next_question(
            session_id, vacancy_id, previous_answers
        )
        
        return {
            "session_id": session_id,
            "question_data": question_data,
            "generated_at": "2025-08-30T18:00:00Z"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка генерации вопроса: {str(e)}"
        )


@router.post("/analyze-answer")
async def analyze_answer_with_llm(
    request: dict,
    db: Session = Depends(get_db)
):
    """
    Анализ ответа с помощью LLM
    """
    try:
        question_text = request.get("question_text", "")
        answer_text = request.get("answer_text", "")
        vacancy_requirements = request.get("vacancy_requirements", "")
        
        if not question_text or not answer_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="question_text и answer_text обязательны"
            )
        
        generator = LLMQuestionGenerator(db)
        analysis = await generator.analyze_answer_context(
            question_text, answer_text, vacancy_requirements
        )
        
        return {
            "analysis": analysis,
            "analyzed_at": "2025-08-30T18:00:00Z"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка анализа ответа: {str(e)}"
        )


@router.post("/smart-navigate")
async def smart_navigation_with_llm(
    request: dict,
    db: Session = Depends(get_db)
):
    """
    Умная навигация с генерацией вопросов через LLM
    """
    try:
        session_id = request.get("session_id", "")
        vacancy_id = request.get("vacancy_id", "")
        current_answer = request.get("current_answer", "")
        question_text = request.get("question_text", "")
        vacancy_requirements = request.get("vacancy_requirements", "")
        
        if not session_id or not vacancy_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="session_id и vacancy_id обязательны"
            )
        
        generator = LLMQuestionGenerator(db)
        
        # Если есть ответ, анализируем его
        if current_answer and question_text:
            analysis = await generator.analyze_answer_context(
                question_text, current_answer, vacancy_requirements
            )
            
            # Проверяем, нужно ли завершить интервью
            from app.models import SessionContext
            session_context = db.query(SessionContext).filter(
                SessionContext.session_id == session_id
            ).first()
            
            if session_context:
                termination_check = await generator.should_terminate_interview(
                    session_context, vacancy_requirements
                )
                
                if termination_check.get("should_terminate", False):
                    return {
                        "should_terminate": True,
                        "reason": termination_check.get("reason", "Условия завершения выполнены"),
                        "analysis": analysis
                    }
        
        # Генерируем следующий вопрос
        previous_answers = request.get("previous_answers", [])
        question_data = await generator.generate_next_question(
            session_id, vacancy_id, previous_answers
        )
        
        return {
            "session_id": session_id,
            "next_question": question_data,
            "should_terminate": question_data.get("should_terminate", False),
            "reasoning": question_data.get("reasoning", "Вопрос сгенерирован")
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка умной навигации: {str(e)}"
        )


@router.post("/check-termination")
async def check_interview_termination(
    request: dict,
    db: Session = Depends(get_db)
):
    """
    Проверка необходимости завершения интервью
    """
    try:
        session_id = request.get("session_id", "")
        vacancy_requirements = request.get("vacancy_requirements", "")
        
        if not session_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="session_id обязателен"
            )
        
        from app.models import SessionContext
        session_context = db.query(SessionContext).filter(
            SessionContext.session_id == session_id
        ).first()
        
        if not session_context:
            return {
                "should_terminate": False,
                "reason": "Контекст сессии не найден"
            }
        
        generator = LLMQuestionGenerator(db)
        termination_check = await generator.should_terminate_interview(
            session_context, vacancy_requirements
        )
        
        return termination_check
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка проверки завершения: {str(e)}"
        )
