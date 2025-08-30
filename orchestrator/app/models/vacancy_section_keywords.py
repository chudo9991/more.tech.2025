from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class SectionType(enum.Enum):
    """Enum for vacancy section types"""
    RESPONSIBILITIES = "responsibilities"
    REQUIREMENTS = "requirements"
    PROGRAMS = "programs"
    SKILLS = "skills"
    LANGUAGES = "languages"
    DESCRIPTION = "description"
    ADDITIONAL = "additional"


class VacancySectionKeywords(Base):
    """Model for storing keywords extracted from vacancy sections"""
    __tablename__ = "vacancy_section_keywords"

    id = Column(String(50), primary_key=True, index=True)
    vacancy_id = Column(String(50), ForeignKey("vacancies.id"), nullable=False, index=True)
    section_type = Column(Enum(SectionType), nullable=False, index=True)
    keywords = Column(JSON, nullable=False, default=list)
    confidence_score = Column(Float, nullable=False, default=0.0)
    extraction_date = Column(DateTime(timezone=True), nullable=False, default=func.now())
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())

    # Relationship
    vacancy = relationship("Vacancy", back_populates="section_keywords")

    def __repr__(self):
        return f"<VacancySectionKeywords(id={self.id}, vacancy_id={self.vacancy_id}, section_type={self.section_type})>"
