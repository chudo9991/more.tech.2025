"""
VacancyQuestion model for linking vacancies and questions
"""
from sqlalchemy import Column, String, Integer, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class VacancyQuestion(Base):
    __tablename__ = "vacancy_questions"

    vacancy_id = Column(String(50), ForeignKey("vacancies.id"), primary_key=True)
    question_id = Column(String(50), ForeignKey("questions.id"), primary_key=True)
    step_no = Column(Integer, nullable=False)
    question_weight = Column(Numeric(3, 2), default=1.0)
    must_have = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    vacancy = relationship("Vacancy", back_populates="vacancy_questions")
    question = relationship("Question", back_populates="vacancy_questions")
