"""
Answer scoring schemas for scoring service
"""
from typing import List
from pydantic import BaseModel


class Criterion(BaseModel):
    """Scoring criterion"""
    id: str
    weight: float
    must_have: bool = False
    min_score: float = 0.0


class ScoreRequest(BaseModel):
    """Request schema for answer scoring"""
    vacancy_id: str
    question_id: str
    question: str
    answer_text: str
    criteria: List[Criterion]
    rubric_version: str = "v1"


class CriterionScore(BaseModel):
    """Individual criterion score"""
    id: str
    score: float
    evidence: str = ""


class ScoreResponse(BaseModel):
    """Response schema for answer scoring"""
    overall_score: float
    passed: bool
    per_criterion: List[CriterionScore]
    red_flags: List[str] = []
    explanations: List[str] = []
    version: str

    class Config:
        from_attributes = True
