"""
InterviewScenario model for storing interview scenarios
"""
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class InterviewScenario(Base):
    __tablename__ = "interview_scenarios"

    id = Column(String(50), primary_key=True, index=True)
    vacancy_id = Column(String(50), ForeignKey("vacancies.id"), nullable=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    version = Column(String(20), default="1.0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    vacancy = relationship("Vacancy", back_populates="interview_scenarios")
    scenario_nodes = relationship("ScenarioNode", back_populates="scenario", cascade="all, delete-orphan")
    scenario_transitions = relationship("ScenarioTransition", back_populates="scenario", cascade="all, delete-orphan")
    criteria_mappings = relationship("ScenarioCriteriaMapping", back_populates="scenario", cascade="all, delete-orphan")
