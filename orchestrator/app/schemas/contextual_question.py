"""
Pydantic schemas for contextual questions
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class ContextualQuestionBase(BaseModel):
    question_text: str = Field(..., description="Текст вопроса")
    question_type: str = Field(..., description="Тип вопроса: experience, project, technical")
    context_source: Dict[str, Any] = Field(default={}, description="Источник контекста")


class ContextualQuestionCreate(ContextualQuestionBase):
    session_id: str = Field(..., description="ID сессии интервью")
    scenario_node_id: str = Field(..., description="ID ноды сценария")


class ContextualQuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    question_type: Optional[str] = None
    context_source: Optional[Dict[str, Any]] = None
    is_used: Optional[bool] = None
    used_at: Optional[datetime] = None


class ContextualQuestionResponse(ContextualQuestionBase):
    id: str = Field(..., description="ID контекстного вопроса")
    session_id: str = Field(..., description="ID сессии интервью")
    scenario_node_id: str = Field(..., description="ID ноды сценария")
    generated_at: datetime = Field(..., description="Время генерации")
    is_used: bool = Field(..., description="Использован ли вопрос")
    used_at: Optional[datetime] = Field(None, description="Время использования")
    created_at: datetime = Field(..., description="Время создания")
    updated_at: datetime = Field(..., description="Время обновления")

    class Config:
        from_attributes = True


class ContextualQuestionListResponse(BaseModel):
    questions: List[ContextualQuestionResponse] = Field(..., description="Список контекстных вопросов")
    total: int = Field(..., description="Общее количество вопросов")


class ContextualQuestionGenerationRequest(BaseModel):
    session_id: str = Field(..., description="ID сессии интервью")
    scenario_node_id: str = Field(..., description="ID ноды сценария")
    max_questions: int = Field(default=3, ge=1, le=5, description="Максимальное количество вопросов")


class ContextualQuestionGenerationResponse(BaseModel):
    success: bool = Field(..., description="Успешность генерации")
    questions: List[ContextualQuestionResponse] = Field(..., description="Сгенерированные вопросы")
    message: Optional[str] = Field(None, description="Сообщение о результате")


class ContextualQuestionUsageRequest(BaseModel):
    question_id: str = Field(..., description="ID вопроса для отметки как использованного")


class ContextualQuestionUsageResponse(BaseModel):
    success: bool = Field(..., description="Успешность операции")
    question_id: str = Field(..., description="ID вопроса")
    used_at: datetime = Field(..., description="Время использования")
