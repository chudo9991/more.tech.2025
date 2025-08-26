"""
QA model for questions and answers
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class QA(Base):
    __tablename__ = "qa"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(50), ForeignKey("sessions.id"), nullable=False)
    step_no = Column(Integer, nullable=False)
    question_id = Column(String(50), ForeignKey("questions.id"), nullable=True)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text)
    audio_url = Column(String(500))
    tone = Column(String(50))
    passed = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    session = relationship("Session", back_populates="qa_records")
    question = relationship("Question")
    scores = relationship("QAScore", back_populates="qa", cascade="all, delete-orphan")
