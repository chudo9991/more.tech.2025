"""
Question model
"""
from sqlalchemy import Column, String, Text, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(String(50), primary_key=True, index=True)
    text = Column(Text, nullable=False)
    type = Column(String(50), default="text")
    max_duration_s = Column(Integer, default=60)
    is_vacancy_specific = Column(Boolean, default=False)
    category = Column(String(100), nullable=True)
    difficulty_level = Column(String(50), default="medium")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    vacancy_questions = relationship("VacancyQuestion", back_populates="question")
