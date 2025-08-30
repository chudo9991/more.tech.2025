"""
ResumeSkill model for storing skills extracted from resumes
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, DECIMAL, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ResumeSkill(Base):
    __tablename__ = "resume_skills"

    id = Column(String(50), primary_key=True, index=True)
    resume_id = Column(String(50), ForeignKey("resumes.id"), nullable=False)
    skill_name = Column(String(255), nullable=False)
    skill_category = Column(String(100), nullable=True)  # programming, soft_skills, tools, etc.
    experience_level = Column(String(50), nullable=True)  # beginner, intermediate, expert
    years_experience = Column(Integer, nullable=True)
    confidence_score = Column(DECIMAL(5, 2), nullable=True)
    extracted_from = Column(Text, nullable=True)  # из какого блока извлечен
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    resume = relationship("Resume", back_populates="resume_skills")
