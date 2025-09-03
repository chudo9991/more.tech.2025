"""
LLM Interview API endpoints
"""
import httpx
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.services.llm_question_generator import LLMQuestionGenerator
from app.schemas.smart_scenario import SmartScenarioNavigationRequest, SmartScenarioNavigationResponse

router = APIRouter()

class AvatarSpeakRequest(BaseModel):
    session_id: str
    text: str
    avatar_id: str = "68af59a86eeedd0042ca7e27"  # Alice (working for video)
    voice_id: str = "66d3f6a704d077b1432fb7d3"   # Anna


@router.post("/generate-question")
async def generate_next_question(
    request: dict,
    db: Session = Depends(get_db)
):
    """
    Генерация следующего вопроса (базового или контекстного) с помощью LLM
    """
    try:
        session_id = request.get("session_id", "")
        vacancy_id = request.get("vacancy_id", "")
        scenario_node_id = request.get("scenario_node_id", None)
        previous_answers = request.get("previous_answers", [])
        
        if not session_id or not vacancy_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="session_id и vacancy_id обязательны"
            )
        
        generator = LLMQuestionGenerator(db)
        
        # Используем новый метод для получения вопроса с контекстом
        question_data = await generator.get_next_question_with_context(
            session_id=session_id,
            vacancy_id=vacancy_id,
            scenario_node_id=scenario_node_id,
            previous_answers=previous_answers
        )
        
        return {
            "session_id": session_id,
            "question_data": question_data,
            "is_contextual": question_data.get("is_contextual", False),
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
        session_id = request.get("session_id", "")
        audio_url = request.get("audio_url", "")
        question_id = request.get("question_id", "")
        
        if not question_text or not answer_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="question_text и answer_text обязательны"
            )
        
        generator = LLMQuestionGenerator(db)
        analysis = await generator.analyze_answer_context(
            question_text, answer_text, vacancy_requirements
        )
        
        # Сохраняем данные в таблицу qa если есть session_id
        qa_record = None
        if session_id:
            qa_record = await save_qa_record(
                db, session_id, question_id, question_text, answer_text, 
                audio_url, analysis
            )
        
        return {
            "analysis": analysis,
            "qa_record": qa_record,
            "analyzed_at": "2025-08-30T18:00:00Z"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка анализа ответа: {str(e)}"
        )

async def save_qa_record(
    db: Session, 
    session_id: str, 
    question_id: str, 
    question_text: str, 
    answer_text: str, 
    audio_url: str, 
    analysis: Dict[str, Any]
) -> Dict[str, Any]:
    """Сохраняет запись в таблицу qa"""
    try:
        from app.models import QA, QAScore, Criteria
        from datetime import datetime
        import uuid
        
        # Получаем следующий номер шага
        existing_qa_count = db.query(QA).filter(QA.session_id == session_id).count()
        step_no = existing_qa_count + 1
        
        # Создаем запись QA (id будет автоинкремент)
        qa_record = QA(
            session_id=session_id,
            step_no=step_no,
            question_id=None,  # Не привязываем к конкретному вопросу пока
            question_text=question_text,
            answer_text=answer_text,
            audio_url=audio_url,
            tone=analysis.get("tone", "neutral"),
            passed=analysis.get("score", 0) >= 0.7,  # Проходной балл 70%
            created_at=datetime.utcnow()
        )
        
        db.add(qa_record)
        db.flush()  # Получаем ID
        
        # Сохраняем оценки по критериям
        if "per_criterion" in analysis:
            for criterion_score in analysis["per_criterion"]:
                qa_score = QAScore(
                    qa_id=qa_record.id,
                    criterion_id=criterion_score.get("id", "general"),
                    score=criterion_score.get("score", 0.0),
                    evidence=criterion_score.get("evidence", ""),
                    red_flag=criterion_score.get("red_flag", False),
                    created_at=datetime.utcnow()
                )
                db.add(qa_score)
        
        db.commit()
        
        return {
            "id": qa_record.id,
            "session_id": qa_record.session_id,
            "step_no": qa_record.step_no,
            "question_text": qa_record.question_text,
            "answer_text": qa_record.answer_text,
            "audio_url": qa_record.audio_url,
            "tone": qa_record.tone,
            "passed": qa_record.passed,
            "created_at": qa_record.created_at.isoformat() if qa_record.created_at else None
        }
        
    except Exception as e:
        db.rollback()
        raise Exception(f"Ошибка сохранения QA записи: {str(e)}")


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


@router.post("/contextual-questions/{question_id}/mark-used")
async def mark_contextual_question_as_used(
    question_id: str,
    request: dict,
    db: Session = Depends(get_db)
):
    """
    Отмечает контекстный вопрос как использованный
    
    Args:
        question_id: ID контекстного вопроса
        request: Запрос с дополнительными данными
        db: Сессия базы данных
        
    Returns:
        Результат операции
    """
    try:
        session_id = request.get("session_id", "")
        
        if not session_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="session_id обязателен"
            )
        
        generator = LLMQuestionGenerator(db)
        
        success = generator.mark_contextual_question_as_used(question_id=question_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Контекстный вопрос не найден"
            )
        
        from datetime import datetime
        
        return {
            "success": True,
            "question_id": question_id,
            "used_at": datetime.utcnow().isoformat(),
            "message": "Контекстный вопрос отмечен как использованный"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка отметки вопроса: {str(e)}"
        )


@router.get("/sessions/{session_id}/contextual-questions/status")
async def get_contextual_questions_status(
    session_id: str,
    node_id: str = None,
    db: Session = Depends(get_db)
):
    """
    Получает статус контекстных вопросов для сессии
    
    Args:
        session_id: ID сессии интервью
        node_id: ID ноды (опционально, если не указан - для текущего узла)
        db: Сессия базы данных
        
    Returns:
        Статус контекстных вопросов
    """
    try:
        generator = LLMQuestionGenerator(db)
        
        if node_id:
            status = generator.get_contextual_questions_status(
                session_id=session_id,
                scenario_node_id=node_id
            )
        else:
            from app.services.scenario_navigation_service import ScenarioNavigationService
            navigation_service = ScenarioNavigationService(db)
            status = navigation_service.get_contextual_questions_status(session_id=session_id, node_id=None)
        
        return status
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения статуса: {str(e)}"
        )


@router.post("/avatar-speak")
async def avatar_speak(request: AvatarSpeakRequest):
    """
    Интеграция с avatar сервисом для генерации видео с аватаром
    
    Логика:
    1. Сначала пытаемся получить streaming token
    2. Если streaming недоступен, переключаемся на fallback генерацию видео
    3. Возвращаем URL для отображения (stream или video)
    """
    try:
        print(f"=== Avatar speak endpoint called ===")
        print(f"Session ID: {request.session_id}")
        print(f"Text: {request.text[:50]}...")
        
        # Step 1: Try to get streaming token (using fixed v2 endpoint)
        # Use very short timeout to avoid hanging
        async with httpx.AsyncClient() as client:
            try:
                streaming_response = await client.post(
                    "http://avatar:8005/api/v1/avatar/streaming-v2/get-token",
                    json={
                        "avatar_id": request.avatar_id
                    },
                    timeout=5.0  # Very short timeout for streaming check
                )
            except httpx.TimeoutException:
                print("Streaming token request timeout - using fallback mode")
                # Go directly to fallback mode if streaming times out
                streaming_data = {
                    "success": False,
                    "fallback_mode": True,
                    "error": "timeout",
                    "message": "Streaming service timeout"
                }
            else:
                streaming_data = streaming_response.json()
            
            # Check streaming data (either from response or timeout fallback)
            if streaming_data.get("success") and streaming_data.get("stream_url"):
                # Streaming is available
                print("Streaming mode available")
                return {
                    "success": True,
                    "mode": "streaming",
                    "stream_url": streaming_data.get("stream_url"),
                    "session_id": request.session_id,
                    "text": request.text
                }
            elif streaming_data.get("fallback_mode"):
                # Streaming unavailable, use fallback video generation
                print("Streaming unavailable, using fallback video generation")
                
                # Step 2: Generate fallback video
                fallback_response = await client.post(
                    "http://avatar:8005/api/v1/avatar/fallback/generate-video",
                    json={
                        "text": request.text,
                        "session_id": request.session_id,
                        "voice_id": request.voice_id,
                        "avatar_id": request.avatar_id,
                        "resolution": 720  # 1:1 format (720x720)
                    },
                    timeout=300.0  # Longer timeout for video generation
                )
                
                if fallback_response.status_code == 200:
                    fallback_data = fallback_response.json()
                    
                    if fallback_data.get("success"):
                        print("Fallback video generated successfully")
                        return {
                            "success": True,
                            "mode": "fallback_video",
                            "video_url": fallback_data.get("video_url"),
                            "session_id": request.session_id,
                            "text": request.text
                        }
                    else:
                        print(f"Fallback video generation failed - response: {fallback_data}")
                        raise HTTPException(
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Fallback video generation failed"
                        )
                else:
                    print(f"Avatar service error - status: {fallback_response.status_code}, response: {fallback_response.text}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Avatar service error: {fallback_response.status_code}"
                    )
            else:
                # Other streaming error
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Streaming error: {streaming_data.get('message', 'Unknown error')}"
                )
                
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Avatar service timeout"
        )
    except Exception as e:
        print(f"Error in avatar_speak: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Avatar speak error: {str(e)}"
        )
