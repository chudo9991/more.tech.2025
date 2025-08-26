"""
QuestionCriterion model for linking questions and criteria
"""
from sqlalchemy import Column, String, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class QuestionCriterion(Base):
    __tablename__ = "question_criteria"

    question_id = Column(String(50), ForeignKey("questions.id"), primary_key=True)
    criterion_id = Column(String(50), ForeignKey("criteria.id"), primary_key=True)
    weight = Column(Numeric(3, 2), default=1.0)
    must_have = Column(Boolean, default=False)
    min_score = Column(Numeric(3, 2), default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    question = relationship("Question")
    criterion = relationship("Criteria")
