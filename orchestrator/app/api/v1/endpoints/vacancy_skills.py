"""
API endpoints for vacancy skills extraction
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Vacancy
from app.schemas.vacancy_skills import (
    VacancySkillsExtractionRequest, VacancySkillsExtractionResponse,
    SkillAnalysisRequest, ResumeSkillsAnalysisResponse,
    SemanticMatchingRequest, SemanticMatch, SemanticMatchingResponse
)
from app.services.vacancy_skills_extractor import vacancy_skills_extractor
from app.services.resume_service import ResumeService

router = APIRouter()


@router.post("/vacancies/{vacancy_id}/extract-skills", response_model=VacancySkillsExtractionResponse)
async def extract_vacancy_skills(
    vacancy_id: str,
    request: VacancySkillsExtractionRequest,
    db: Session = Depends(get_db)
) -> VacancySkillsExtractionResponse:
    """
    Extract skills from vacancy description using LLM
    
    Args:
        vacancy_id: ID of the vacancy
        request: Extraction request with options
        db: Database session
        
    Returns:
        Extracted skills with metadata
    """
    try:
        # Get vacancy from database
        vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
        if not vacancy:
            raise HTTPException(status_code=404, detail=f"Vacancy {vacancy_id} not found")
        
        # Extract skills using LLM
        result = await vacancy_skills_extractor.extract_skills_from_vacancy(
            vacancy=vacancy,
            force_reload=request.force_reload
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract skills: {str(e)}")


@router.get("/vacancies/{vacancy_id}/skills", response_model=VacancySkillsExtractionResponse)
async def get_vacancy_skills(
    vacancy_id: str,
    force_reload: bool = False,
    db: Session = Depends(get_db)
) -> VacancySkillsExtractionResponse:
    """
    Get extracted skills for vacancy (cached or fresh)
    
    Args:
        vacancy_id: ID of the vacancy
        force_reload: Force reload from LLM, bypass cache
        db: Database session
        
    Returns:
        Extracted skills with metadata
    """
    try:
        # Get vacancy from database
        vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
        if not vacancy:
            raise HTTPException(status_code=404, detail=f"Vacancy {vacancy_id} not found")
        
        # Extract skills using LLM
        result = await vacancy_skills_extractor.extract_skills_from_vacancy(
            vacancy=vacancy,
            force_reload=force_reload
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get skills: {str(e)}")


@router.post("/resumes/{resume_id}/analyze-skills", response_model=ResumeSkillsAnalysisResponse)
async def analyze_resume_skills(
    resume_id: str,
    request: SkillAnalysisRequest,
    db: Session = Depends(get_db)
) -> ResumeSkillsAnalysisResponse:
    """
    Analyze resume skills against vacancy using dynamic skills extraction
    
    Args:
        resume_id: ID of the resume to analyze
        request: Analysis request with options
        db: Database session
        
    Returns:
        Detailed skills analysis results
    """
    try:
        resume_service = ResumeService(db)
        
        # Analyze resume with dynamic skills
        result = await resume_service.analyze_resume_with_dynamic_skills(
            resume_id=resume_id,
            vacancy_id=request.vacancy_id,
            force_reload=False  # Use cached skills by default
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze resume skills: {str(e)}")


@router.delete("/vacancies/{vacancy_id}/skills/cache")
async def invalidate_vacancy_skills_cache(
    vacancy_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Invalidate cached skills for vacancy
    
    Args:
        vacancy_id: ID of the vacancy
        db: Database session
        
    Returns:
        Success status
    """
    try:
        # Invalidate cache
        vacancy_skills_extractor.invalidate_cache(vacancy_id)
        
        return {
            "success": True,
            "message": f"Cache invalidated for vacancy {vacancy_id}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to invalidate cache: {str(e)}")


@router.post("/skills/semantic-matching", response_model=SemanticMatchingResponse)
async def semantic_skills_matching(
    request: SemanticMatchingRequest,
    db: Session = Depends(get_db)
) -> SemanticMatchingResponse:
    """
    Perform semantic matching between candidate skills and vacancy requirements
    
    Args:
        request: Semantic matching request
        db: Database session
        
    Returns:
        Semantic matching results
    """
    try:
        # TODO: Implement semantic matching logic
        # This will be implemented in future stages
        
        return SemanticMatchingResponse(
            success=True,
            matches=[],
            total_matches=0,
            confidence=0.0
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to perform semantic matching: {str(e)}")
