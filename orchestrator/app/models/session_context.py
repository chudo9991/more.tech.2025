"""
SessionContext model for storing interview session context
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class SessionContext(Base):
    __tablename__ = "session_context"

    id = Column(String(50), primary_key=True, index=True)
    session_id = Column(String(50), ForeignKey("sessions.id"), nullable=False)
    skill_assessments = Column(JSON)  # Оценки навыков
    negative_responses = Column(JSON)  # Зафиксированные отрицания
    current_path = Column(JSON)  # Текущий путь в сценарии
    context_data = Column(JSON)  # Дополнительный контекст
    current_node_id = Column(String(50), nullable=True)  # Текущий узел в сценарии
    scenario_id = Column(String(50), nullable=True)  # ID используемого сценария
    contextual_questions = Column(JSON)  # Контекстные вопросы по нодам
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    session = relationship("Session", back_populates="session_context")
