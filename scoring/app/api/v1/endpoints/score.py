"""
Answer scoring endpoints for scoring service
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException

from app.schemas.score import ScoreRequest, ScoreResponse
from app.services.scoring_service import ScoringService

router = APIRouter()


@router.post("/", response_model=ScoreResponse)
async def score_answer(
    request: ScoreRequest
) -> Dict[str, Any]:
    """Score an answer based on criteria"""
    try:
        scoring_service = ScoringService()
        result = await scoring_service.score_answer(
            vacancy_id=request.vacancy_id,
            question_id=request.question_id,
            question=request.question,
            answer_text=request.answer_text,
            criteria=request.criteria,
            rubric_version=request.rubric_version
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
