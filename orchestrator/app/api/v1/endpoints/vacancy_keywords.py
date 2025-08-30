from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import SectionType
from app.schemas.vacancy_keywords import (
    SectionKeywordsRequest,
    SectionKeywordsResponse,
    AllSectionKeywordsResponse,
    VacancySectionKeywordsResponse,
    VacancySectionKeywordsUpdate,
    KeywordsExtractionStats
)
from app.services.keywords_extractor import KeywordsExtractor

router = APIRouter()


@router.post("/vacancies/{vacancy_id}/keywords/extract/{section_type}", response_model=SectionKeywordsResponse)
async def extract_section_keywords(
    vacancy_id: str,
    section_type: SectionType,
    request: SectionKeywordsRequest,
    db: Session = Depends(get_db)
) -> SectionKeywordsResponse:
    """
    Extract keywords from a specific section of a vacancy
    
    Args:
        vacancy_id: ID of the vacancy
        section_type: Type of section to extract keywords from
        request: Request with options (force_reload)
        db: Database session
        
    Returns:
        Extracted keywords with confidence score
    """
    try:
        keywords_extractor = KeywordsExtractor(db)
        
        result = await keywords_extractor.extract_keywords_from_section(
            vacancy_id=vacancy_id,
            section_type=section_type,
            force_reload=request.force_reload
        )
        
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.error
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract keywords: {str(e)}"
        )


@router.post("/vacancies/{vacancy_id}/keywords/extract-all", response_model=AllSectionKeywordsResponse)
async def extract_all_keywords(
    vacancy_id: str,
    request: SectionKeywordsRequest,
    db: Session = Depends(get_db)
) -> AllSectionKeywordsResponse:
    """
    Extract keywords from all sections of a vacancy
    
    Args:
        vacancy_id: ID of the vacancy
        request: Request with options (force_reload)
        db: Database session
        
    Returns:
        Extracted keywords for all sections
    """
    try:
        keywords_extractor = KeywordsExtractor(db)
        
        result = await keywords_extractor.extract_all_keywords(
            vacancy_id=vacancy_id,
            force_reload=request.force_reload
        )
        
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.error
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract all keywords: {str(e)}"
        )


@router.get("/vacancies/{vacancy_id}/keywords", response_model=List[VacancySectionKeywordsResponse])
async def get_all_keywords(
    vacancy_id: str,
    db: Session = Depends(get_db)
) -> List[VacancySectionKeywordsResponse]:
    """
    Get all keywords for a vacancy
    
    Args:
        vacancy_id: ID of the vacancy
        db: Database session
        
    Returns:
        List of all keywords for the vacancy
    """
    try:
        keywords_extractor = KeywordsExtractor(db)
        keywords_records = keywords_extractor.get_all_keywords(vacancy_id)
        
        return [
            VacancySectionKeywordsResponse(
                id=record.id,
                vacancy_id=record.vacancy_id,
                section_type=record.section_type,
                keywords=record.keywords,
                confidence_score=record.confidence_score,
                extraction_date=record.extraction_date,
                created_at=record.created_at,
                updated_at=record.updated_at
            )
            for record in keywords_records
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get keywords: {str(e)}"
        )


@router.get("/vacancies/{vacancy_id}/keywords/{section_type}", response_model=VacancySectionKeywordsResponse)
async def get_section_keywords(
    vacancy_id: str,
    section_type: SectionType,
    db: Session = Depends(get_db)
) -> VacancySectionKeywordsResponse:
    """
    Get keywords for a specific section of a vacancy
    
    Args:
        vacancy_id: ID of the vacancy
        section_type: Type of section
        db: Database session
        
    Returns:
        Keywords for the specific section
    """
    try:
        keywords_extractor = KeywordsExtractor(db)
        record = keywords_extractor.get_keywords(vacancy_id, section_type)
        
        if not record:
            # Return empty keywords instead of 404
            return VacancySectionKeywordsResponse(
                id=None,
                vacancy_id=vacancy_id,
                section_type=section_type,
                keywords=[],
                confidence_score=0.0,
                extraction_date=None,
                created_at=None,
                updated_at=None
            )
        
        return VacancySectionKeywordsResponse(
            id=record.id,
            vacancy_id=record.vacancy_id,
            section_type=record.section_type,
            keywords=record.keywords,
            confidence_score=record.confidence_score,
            extraction_date=record.extraction_date,
            created_at=record.created_at,
            updated_at=record.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get section keywords: {str(e)}"
        )


@router.put("/vacancies/{vacancy_id}/keywords/{section_type}", response_model=VacancySectionKeywordsResponse)
async def update_section_keywords(
    vacancy_id: str,
    section_type: SectionType,
    update_data: VacancySectionKeywordsUpdate,
    db: Session = Depends(get_db)
) -> VacancySectionKeywordsResponse:
    """
    Update keywords for a specific section of a vacancy
    
    Args:
        vacancy_id: ID of the vacancy
        section_type: Type of section
        update_data: Updated keywords data
        db: Database session
        
    Returns:
        Updated keywords record
    """
    try:
        keywords_extractor = KeywordsExtractor(db)
        
        record = keywords_extractor.update_keywords(
            vacancy_id=vacancy_id,
            section_type=section_type,
            keywords=update_data.keywords,
            confidence_score=update_data.confidence_score
        )
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Failed to update keywords for vacancy {vacancy_id} and section {section_type.value}"
            )
        
        return VacancySectionKeywordsResponse(
            id=record.id,
            vacancy_id=record.vacancy_id,
            section_type=record.section_type,
            keywords=record.keywords,
            confidence_score=record.confidence_score,
            extraction_date=record.extraction_date,
            created_at=record.created_at,
            updated_at=record.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update keywords: {str(e)}"
        )


@router.delete("/vacancies/{vacancy_id}/keywords/{section_type}")
async def delete_section_keywords(
    vacancy_id: str,
    section_type: SectionType,
    db: Session = Depends(get_db)
):
    """
    Delete keywords for a specific section of a vacancy
    
    Args:
        vacancy_id: ID of the vacancy
        section_type: Type of section
        db: Database session
        
    Returns:
        Success message
    """
    try:
        keywords_extractor = KeywordsExtractor(db)
        
        success = keywords_extractor.delete_keywords(vacancy_id, section_type)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Keywords not found for vacancy {vacancy_id} and section {section_type.value}"
            )
        
        return {"message": f"Keywords deleted successfully for section {section_type.value}"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete keywords: {str(e)}"
        )


@router.get("/vacancies/{vacancy_id}/keywords-stats", response_model=KeywordsExtractionStats)
async def get_keywords_stats(
    vacancy_id: str,
    db: Session = Depends(get_db)
) -> KeywordsExtractionStats:
    """
    Get statistics for keywords extraction for a vacancy
    
    Args:
        vacancy_id: ID of the vacancy
        db: Database session
        
    Returns:
        Keywords extraction statistics
    """
    try:
        keywords_extractor = KeywordsExtractor(db)
        stats = keywords_extractor.get_extraction_stats(vacancy_id)
        
        return stats
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get keywords stats: {str(e)}"
        )


@router.delete("/vacancies/{vacancy_id}/keywords-cache")
async def clear_keywords_cache(
    vacancy_id: str,
    db: Session = Depends(get_db)
):
    """
    Clear cache for all keywords of a vacancy
    
    Args:
        vacancy_id: ID of the vacancy
        db: Database session
        
    Returns:
        Success message
    """
    try:
        keywords_extractor = KeywordsExtractor(db)
        
        # Get all section types and clear cache for each
        section_types = list(SectionType)
        cleared_count = 0
        
        for section_type in section_types:
            cache_identifier = f"{vacancy_id}:{section_type.value}"
            keywords_extractor.cache_service.delete('keywords', cache_identifier)
            cleared_count += 1
        
        return {
            "message": f"Cache cleared for {cleared_count} sections",
            "vacancy_id": vacancy_id,
            "cleared_sections": cleared_count
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear cache: {str(e)}"
        )
