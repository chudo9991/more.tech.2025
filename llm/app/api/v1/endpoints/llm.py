"""
LLM service endpoints
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends

from app.schemas.llm import ScoringRequest, ScoringResponse, ChatRequest, ChatResponse, ToneAnalysisRequest, ToneAnalysisResponse
from app.services.llm_service import LLMService

router = APIRouter()


@router.post("/score", response_model=ScoringResponse)
async def score_answer(
    request: ScoringRequest
) -> Dict[str, Any]:
    """Score an answer based on criteria"""
    try:
        llm_service = LLMService()
        result = await llm_service.score_answer(
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


@router.post("/chat", response_model=ChatResponse)
async def chat_with_avatar(
    request: ChatRequest
) -> Dict[str, Any]:
    """Chat with avatar"""
    try:
        llm_service = LLMService()
        result = await llm_service.chat_with_avatar(
            session_id=request.session_id,
            message=request.message,
            context=request.context
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/analyze-tone", response_model=ToneAnalysisResponse)
async def analyze_tone(
    request: ToneAnalysisRequest
) -> Dict[str, Any]:
    """Analyze tone of voice from text"""
    try:
        llm_service = LLMService()
        result = await llm_service.analyze_tone(
            text=request.text,
            session_id=request.session_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/generate")
async def generate_text(
    request: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate text using LLM"""
    try:
        llm_service = LLMService()
        result = await llm_service.generate(
            prompt=request.get("prompt", ""),
            max_tokens=request.get("max_tokens", 2000),
            temperature=request.get("temperature", 0.7),
            system_message=request.get("system_message")
        )
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/healthz")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "llm",
        "version": "1.0.0"
    }
