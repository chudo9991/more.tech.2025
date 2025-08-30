"""
Vacancy model
"""
from sqlalchemy import Column, String, Text, DateTime, Boolean, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(String(50), primary_key=True, index=True)
    vacancy_code = Column(String(50), unique=True, nullable=True, index=True)
    
    # Основная информация
    title = Column(String(255), nullable=False)
    status = Column(String(50), nullable=True, default="active")
    region = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    
    # Условия труда
    employment_type = Column(String(50), nullable=True)
    contract_type = Column(String(50), nullable=True)
    work_schedule = Column(Text, nullable=True)
    business_trips = Column(Boolean, nullable=True, default=False)
    
    # Финансовые условия
    salary_min = Column(Numeric(10, 2), nullable=True)
    salary_max = Column(Numeric(10, 2), nullable=True)
    total_income = Column(Numeric(10, 2), nullable=True)
    annual_bonus_percent = Column(Numeric(5, 2), nullable=True)
    bonus_description = Column(Text, nullable=True)
    
    # Требования к кандидату
    responsibilities = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)
    education_level = Column(String(100), nullable=True)
    experience_required = Column(String(100), nullable=True)
    special_programs = Column(Text, nullable=True)
    computer_skills = Column(Text, nullable=True)
    foreign_languages = Column(Text, nullable=True)
    language_level = Column(String(50), nullable=True)
    
    # Дополнительная информация
    additional_info = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    
    # Системные поля
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    sessions = relationship("Session", back_populates="vacancy")
    vacancy_questions = relationship("VacancyQuestion", back_populates="vacancy")
    interview_scenarios = relationship("InterviewScenario", back_populates="vacancy")
    resumes = relationship("Resume", back_populates="vacancy")
