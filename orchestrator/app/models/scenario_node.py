"""
ScenarioNode model for storing nodes in interview scenarios
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ScenarioNode(Base):
    __tablename__ = "scenario_nodes"

    id = Column(String(50), primary_key=True, index=True)
    scenario_id = Column(String(50), ForeignKey("interview_scenarios.id"), nullable=False)
    question_id = Column(String(50), ForeignKey("questions.id"), nullable=True)
    node_type = Column(String(50), nullable=False)  # 'start', 'question', 'condition', 'end', 'skip'
    position_x = Column(Integer, default=0)
    position_y = Column(Integer, default=0)
    node_config = Column(JSON)  # Дополнительная конфигурация узла
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    scenario = relationship("InterviewScenario", back_populates="scenario_nodes")
    outgoing_transitions = relationship("ScenarioTransition", foreign_keys="ScenarioTransition.from_node_id", back_populates="from_node")
    incoming_transitions = relationship("ScenarioTransition", foreign_keys="ScenarioTransition.to_node_id", back_populates="to_node")
    contextual_questions = relationship("ContextualQuestion", back_populates="scenario_node", cascade="all, delete-orphan")
