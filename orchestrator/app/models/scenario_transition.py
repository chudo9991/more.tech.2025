"""
ScenarioTransition model for storing transitions between scenario nodes
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ScenarioTransition(Base):
    __tablename__ = "scenario_transitions"

    id = Column(String(50), primary_key=True, index=True)
    scenario_id = Column(String(50), ForeignKey("interview_scenarios.id"), nullable=False)
    from_node_id = Column(String(50), ForeignKey("scenario_nodes.id"), nullable=False)
    to_node_id = Column(String(50), ForeignKey("scenario_nodes.id"), nullable=False)
    condition_type = Column(String(50))  # 'score_threshold', 'negative_response', 'skill_missing', 'always'
    condition_value = Column(JSON)  # JSON с условиями перехода
    priority = Column(Integer, default=1)
    transition_label = Column(String(255))  # Человекочитаемая метка перехода
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    scenario = relationship("InterviewScenario", back_populates="scenario_transitions")
    from_node = relationship("ScenarioNode", foreign_keys=[from_node_id], back_populates="outgoing_transitions")
    to_node = relationship("ScenarioNode", foreign_keys=[to_node_id], back_populates="incoming_transitions")
