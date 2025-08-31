"""
Session model
"""
from sqlalchemy import Column, String, Integer, DateTime, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String(50), primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=True)
    vacancy_id = Column(String(50), ForeignKey("vacancies.id"), nullable=True)
    vacancy_code = Column(String(50), nullable=True, index=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    status = Column(String(50), default="created")
    started_at = Column(DateTime(timezone=True))
    finished_at = Column(DateTime(timezone=True))
    total_score = Column(Numeric(3, 2))
    pass_rate = Column(Numeric(3, 2))
    current_step = Column(Integer, default=0)
    total_steps = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    candidate = relationship("Candidate", back_populates="sessions")
    vacancy = relationship("Vacancy", back_populates="sessions")
    qa_records = relationship("QA", back_populates="session", cascade="all, delete-orphan")
    media_files = relationship("Media", back_populates="session", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    session_context = relationship("SessionContext", back_populates="session", uselist=False, cascade="all, delete-orphan")
    contextual_questions = relationship("ContextualQuestion", back_populates="session", cascade="all, delete-orphan")
