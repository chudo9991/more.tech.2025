"""
Smart scenario schemas
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class ScenarioNodeConfig(BaseModel):
    label: Optional[str] = None
    weight: Optional[float] = 1.0
    must_have: Optional[bool] = False
    skip_reason: Optional[str] = None


class ScenarioNodeBase(BaseModel):
    id: str
    scenario_id: str
    question_id: Optional[str] = None
    node_type: str  # 'start', 'question', 'condition', 'end', 'skip'
    position_x: int = 0
    position_y: int = 0
    node_config: Optional[Dict[str, Any]] = None


class ScenarioNodeCreate(ScenarioNodeBase):
    pass


class ScenarioNodeResponse(ScenarioNodeBase):
    created_at: datetime
    updated_at: datetime


class TransitionCondition(BaseModel):
    condition_type: str  # 'score_threshold', 'negative_response', 'skill_missing', 'always'
    condition_value: Dict[str, Any]
    priority: int = 1
    transition_label: Optional[str] = None


class ScenarioTransitionBase(BaseModel):
    id: str
    scenario_id: str
    from_node_id: str
    to_node_id: str
    condition_type: Optional[str] = None
    condition_value: Optional[Dict[str, Any]] = None
    priority: int = 1
    transition_label: Optional[str] = None


class ScenarioTransitionCreate(ScenarioTransitionBase):
    pass


class ScenarioTransitionResponse(ScenarioTransitionBase):
    created_at: datetime
    updated_at: datetime


class InterviewScenarioBase(BaseModel):
    id: str
    vacancy_id: Optional[str] = None
    name: str
    description: Optional[str] = None
    is_active: bool = True
    version: str = "1.0"


class InterviewScenarioCreate(InterviewScenarioBase):
    pass


class InterviewScenarioResponse(InterviewScenarioBase):
    created_at: datetime
    updated_at: datetime
    nodes: List[ScenarioNodeResponse] = []
    transitions: List[ScenarioTransitionResponse] = []


class SessionContextBase(BaseModel):
    id: str
    session_id: str
    skill_assessments: Optional[Dict[str, Any]] = None
    negative_responses: Optional[Dict[str, Any]] = None
    current_path: Optional[Dict[str, Any]] = None
    context_data: Optional[Dict[str, Any]] = None
    current_node_id: Optional[str] = None
    scenario_id: Optional[str] = None


class SessionContextCreate(SessionContextBase):
    pass


class SessionContextResponse(SessionContextBase):
    created_at: datetime
    updated_at: datetime


class SmartScenarioNavigationRequest(BaseModel):
    session_id: str
    current_answer: Optional[str] = None
    answer_score: Optional[float] = None
    force_next: Optional[bool] = False


class SmartScenarioNavigationResponse(BaseModel):
    next_node_id: Optional[str] = None
    next_question_id: Optional[str] = None
    question_text: Optional[str] = None
    transition_reason: Optional[str] = None
    should_terminate: bool = False
    context_update: Optional[Dict[str, Any]] = None
    available_transitions: List[Dict[str, Any]] = []
    has_contextual_questions: bool = False
    contextual_questions_count: int = 0
