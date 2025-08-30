"""
Resume model for storing resume information
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, DECIMAL, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(String(50), primary_key=True, index=True)
    vacancy_id = Column(String(50), ForeignKey("vacancies.id"), nullable=True)
    vacancy_code = Column(String(100), nullable=True)  # для быстрого поиска
    filename = Column(String(255), nullable=False)  # имя файла в MinIO
    original_filename = Column(String(255), nullable=False)  # оригинальное имя файла
    file_size = Column(Integer, nullable=False)  # размер файла в байтах
    file_type = Column(String(50), nullable=False)  # pdf, docx, rtf, txt
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default="uploaded")  # uploaded, processing, analyzed, error
    total_score = Column(DECIMAL(5, 2), nullable=True)  # общая оценка релевантности (0-100)
    confidence_score = Column(DECIMAL(5, 2), nullable=True)  # уверенность в анализе (0-100)
    processing_errors = Column(Text, nullable=True)  # ошибки обработки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    vacancy = relationship("Vacancy", back_populates="resumes")
    resume_blocks = relationship("ResumeBlock", back_populates="resume", cascade="all, delete-orphan")
    resume_skills = relationship("ResumeSkill", back_populates="resume", cascade="all, delete-orphan")
