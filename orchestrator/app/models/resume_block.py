"""
ResumeBlock model for storing resume analysis blocks
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, DECIMAL, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ResumeBlock(Base):
    __tablename__ = "resume_blocks"

    id = Column(String(50), primary_key=True, index=True)
    resume_id = Column(String(50), ForeignKey("resumes.id"), nullable=False)
    block_type = Column(String(100), nullable=False)  # experience, education, skills, projects, etc.
    block_name = Column(String(255), nullable=False)  # название блока (например, "Опыт работы")
    extracted_text = Column(Text, nullable=True)  # извлеченный текст из резюме
    relevance_score = Column(DECIMAL(5, 2), nullable=True)  # оценка релевантности (0-100)
    confidence_score = Column(DECIMAL(5, 2), nullable=True)  # уверенность в оценке
    matched_requirements = Column(ARRAY(String), nullable=True)  # какие требования вакансии покрыты
    missing_requirements = Column(ARRAY(String), nullable=True)  # какие требования не найдены
    analysis_notes = Column(Text, nullable=True)  # заметки анализа (читаемый текст)
    extracted_keywords = Column(ARRAY(String), nullable=True)  # извлеченные ключевые слова для сравнения
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    resume = relationship("Resume", back_populates="resume_blocks")
