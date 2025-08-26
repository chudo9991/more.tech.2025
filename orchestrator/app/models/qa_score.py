"""
QA Score model for answer evaluations
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class QAScore(Base):
    __tablename__ = "qa_scores"

    id = Column(Integer, primary_key=True, index=True)
    qa_id = Column(Integer, ForeignKey("qa.id"), nullable=False)
    criterion_id = Column(String(50), ForeignKey("criteria.id"), nullable=True)
    score = Column(Numeric(3, 2), nullable=False)
    evidence = Column(Text)
    red_flag = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    qa = relationship("QA", back_populates="scores")
    criterion = relationship("Criteria")
