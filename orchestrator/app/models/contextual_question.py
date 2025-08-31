"""
ContextualQuestion model for storing individual interview questions
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ContextualQuestion(Base):
    __tablename__ = "contextual_questions"

    id = Column(String(50), primary_key=True, index=True)
    session_id = Column(String(50), ForeignKey("sessions.id"), nullable=False)
    scenario_node_id = Column(String(50), ForeignKey("scenario_nodes.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50))  # 'experience', 'project', 'technical'
    context_source = Column(JSON)  # источник контекста (резюме, ответы)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    is_used = Column(Boolean, default=False)
    used_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    session = relationship("Session", back_populates="contextual_questions")
    scenario_node = relationship("ScenarioNode", back_populates="contextual_questions")
