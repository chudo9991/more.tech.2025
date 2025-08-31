"""
DynamicCriteria model for storing dynamic criteria based on vacancy skills
"""
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class DynamicCriteria(Base):
    __tablename__ = "dynamic_criteria"

    id = Column(String(50), primary_key=True, index=True)
    vacancy_id = Column(String(50), ForeignKey("vacancies.id"), nullable=False)
    
    # Навык, на основе которого создан критерий
    skill_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)  # programming, database, devops, etc.
    importance = Column(Float, nullable=False, default=0.5)  # 0.0-1.0
    required_level = Column(String(50), nullable=False)  # beginner, intermediate, expert
    is_mandatory = Column(Boolean, default=False)
    
    # Дополнительная информация
    description = Column(String(500), nullable=True)
    alternatives = Column(JSON, nullable=True)  # Альтернативные названия навыка
    
    # Системные поля
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    vacancy = relationship("Vacancy", back_populates="dynamic_criteria")
    scenario_mappings = relationship("ScenarioCriteriaMapping", back_populates="criterion", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<DynamicCriteria(id={self.id}, skill_name={self.skill_name}, category={self.category})>"


class ScenarioCriteriaMapping(Base):
    __tablename__ = "scenario_criteria_mappings"

    id = Column(String(50), primary_key=True, index=True)
    scenario_id = Column(String(50), ForeignKey("interview_scenarios.id"), nullable=False)
    criterion_id = Column(String(50), ForeignKey("dynamic_criteria.id"), nullable=False)
    
    # Веса и настройки для конкретного сценария
    weight = Column(Float, nullable=False, default=1.0)
    is_mandatory = Column(Boolean, default=False)
    min_score = Column(Float, nullable=True)  # Минимальный балл для прохождения
    
    # Системные поля
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    scenario = relationship("InterviewScenario", back_populates="criteria_mappings")
    criterion = relationship("DynamicCriteria", back_populates="scenario_mappings")

    def __repr__(self):
        return f"<ScenarioCriteriaMapping(scenario_id={self.scenario_id}, criterion_id={self.criterion_id}, weight={self.weight})>"
