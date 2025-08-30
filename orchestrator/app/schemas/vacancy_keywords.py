from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class SectionType(str, Enum):
    """Enum for vacancy section types"""
    RESPONSIBILITIES = "responsibilities"
    REQUIREMENTS = "requirements"
    PROGRAMS = "programs"
    SKILLS = "skills"
    LANGUAGES = "languages"
    DESCRIPTION = "description"
    ADDITIONAL = "additional"


class VacancySectionKeywordsBase(BaseModel):
    """Base schema for vacancy section keywords"""
    section_type: SectionType = Field(..., description="Type of vacancy section")
    keywords: List[str] = Field(default=[], description="List of extracted keywords")
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence score for extraction")


class VacancySectionKeywordsCreate(VacancySectionKeywordsBase):
    """Schema for creating vacancy section keywords"""
    vacancy_id: str = Field(..., description="ID of the vacancy")


class VacancySectionKeywordsUpdate(BaseModel):
    """Schema for updating vacancy section keywords"""
    keywords: List[str] = Field(..., description="List of keywords")
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score for extraction")


class VacancySectionKeywordsResponse(VacancySectionKeywordsBase):
    """Schema for vacancy section keywords response"""
    id: Optional[str] = Field(None, description="Unique identifier")
    vacancy_id: str = Field(..., description="ID of the vacancy")
    extraction_date: Optional[datetime] = Field(None, description="Date when keywords were extracted")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        from_attributes = True


class SectionKeywordsRequest(BaseModel):
    """Request for extracting keywords from a specific section"""
    force_reload: bool = Field(default=False, description="Force reload from LLM, ignore cache")


class SectionKeywordsResponse(BaseModel):
    """Response with extracted keywords for a section"""
    success: bool = Field(..., description="Whether extraction was successful")
    vacancy_id: str = Field(..., description="ID of the vacancy")
    section_type: SectionType = Field(..., description="Type of section")
    keywords: List[str] = Field(default=[], description="Extracted keywords")
    confidence_score: float = Field(default=0.0, description="Confidence score")
    extraction_time: float = Field(default=0.0, description="Time taken for extraction in seconds")
    error: Optional[str] = Field(None, description="Error message if extraction failed")


class AllSectionKeywordsResponse(BaseModel):
    """Response with keywords for all sections of a vacancy"""
    success: bool = Field(..., description="Whether extraction was successful")
    vacancy_id: str = Field(..., description="ID of the vacancy")
    sections: List[SectionKeywordsResponse] = Field(default=[], description="Keywords for all sections")
    total_extraction_time: float = Field(default=0.0, description="Total time taken for all extractions")
    error: Optional[str] = Field(None, description="Error message if extraction failed")


class KeywordsExtractionStats(BaseModel):
    """Statistics for keywords extraction"""
    total_sections: int = Field(..., description="Total number of sections")
    extracted_sections: int = Field(..., description="Number of sections with extracted keywords")
    average_confidence: float = Field(..., description="Average confidence score")
    total_keywords: int = Field(..., description="Total number of keywords across all sections")
