"""
Pydantic schemas for vacancy skills
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class SkillCategory(str, Enum):
    """Categories of skills"""
    PROGRAMMING = "programming"
    DATABASE = "database"
    DEVOPS = "devops"
    SOFT_SKILLS = "soft_skills"
    FRAMEWORKS = "frameworks"
    TOOLS = "tools"
    LANGUAGES = "languages"
    METHODOLOGIES = "methodologies"
    CLOUD = "cloud"
    TESTING = "testing"
    ANALYTICS = "analytics"
    DESIGN = "design"
    MANAGEMENT = "management"
    OTHER = "other"


class SkillLevel(str, Enum):
    """Skill proficiency levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"


class VacancySkill(BaseModel):
    """Schema for a single skill required by a vacancy"""
    skill_name: str = Field(..., description="Name of the skill")
    category: SkillCategory = Field(..., description="Category of the skill")
    importance: float = Field(..., ge=0.0, le=1.0, description="Importance weight 0.0-1.0")
    required_level: SkillLevel = Field(..., description="Required proficiency level")
    is_mandatory: bool = Field(default=False, description="Whether this skill is mandatory")
    alternatives: List[str] = Field(default=[], description="Alternative names for this skill")
    description: Optional[str] = Field(None, description="Description of the skill requirement")
    
    class Config:
        use_enum_values = True


class VacancySkillsExtractionRequest(BaseModel):
    """Request for extracting skills from vacancy"""
    force_reload: bool = Field(default=False, description="Force reload from cache")


class VacancySkillsExtractionResponse(BaseModel):
    """Response with extracted skills from vacancy"""
    success: bool = Field(..., description="Whether extraction was successful")
    vacancy_id: str = Field(..., description="ID of the vacancy")
    skills: List[VacancySkill] = Field(default=[], description="Extracted skills")
    total_skills: int = Field(..., description="Total number of skills")
    mandatory_skills: int = Field(..., description="Number of mandatory skills")
    extraction_time: float = Field(..., description="Time taken for extraction in seconds")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in extraction")
    error: Optional[str] = Field(None, description="Error message if extraction failed")
    
    class Config:
        use_enum_values = True


class SkillAnalysisRequest(BaseModel):
    """Request for analyzing resume skills against vacancy"""
    resume_id: str = Field(..., description="ID of the resume")
    vacancy_id: str = Field(..., description="ID of the vacancy")
    include_semantic_analysis: bool = Field(default=True, description="Include semantic analysis")


class SkillMatch(BaseModel):
    """Schema for skill matching result"""
    skill_name: str = Field(..., description="Name of the skill")
    category: SkillCategory = Field(..., description="Category of the skill")
    required_level: SkillLevel = Field(..., description="Required level")
    candidate_level: Optional[SkillLevel] = Field(None, description="Candidate's level")
    match_score: float = Field(..., ge=0.0, le=1.0, description="Match score 0.0-1.0")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in assessment")
    evidence: List[str] = Field(default=[], description="Evidence from resume")
    is_mandatory: bool = Field(default=False, description="Whether skill is mandatory")
    importance: float = Field(..., ge=0.0, le=1.0, description="Skill importance")
    
    class Config:
        use_enum_values = True


class ResumeSkillsAnalysisResponse(BaseModel):
    """Response with resume skills analysis"""
    success: bool = Field(..., description="Whether analysis was successful")
    resume_id: str = Field(..., description="ID of the resume")
    vacancy_id: str = Field(..., description="ID of the vacancy")
    skill_matches: List[SkillMatch] = Field(default=[], description="Skill matching results")
    overall_score: float = Field(..., ge=0.0, le=1.0, description="Overall match score")
    mandatory_skills_covered: int = Field(..., description="Number of mandatory skills covered")
    total_mandatory_skills: int = Field(..., description="Total number of mandatory skills")
    analysis_time: float = Field(default=0.0, description="Time taken for analysis in seconds")
    strengths: List[str] = Field(default=[], description="Candidate's strengths")
    weaknesses: List[str] = Field(default=[], description="Candidate's weaknesses")
    recommendations: List[str] = Field(default=[], description="Recommendations")
    error: Optional[str] = Field(None, description="Error message if analysis failed")
    
    class Config:
        use_enum_values = True


class SemanticMatchingRequest(BaseModel):
    """Request for semantic skills matching"""
    resume_id: str = Field(..., description="ID of the resume")
    vacancy_id: str = Field(..., description="ID of the vacancy")


class SemanticMatch(BaseModel):
    """Schema for semantic skill matching"""
    resume_skill: str = Field(..., description="Skill mentioned in resume")
    vacancy_skill: str = Field(..., description="Matching skill from vacancy")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Semantic similarity score")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in matching")
    reasoning: str = Field(..., description="Reasoning for the match")
    
    class Config:
        use_enum_values = True


class SemanticMatchingResponse(BaseModel):
    """Response with semantic matching results"""
    success: bool = Field(..., description="Whether matching was successful")
    resume_id: str = Field(..., description="ID of the resume")
    vacancy_id: str = Field(..., description="ID of the vacancy")
    semantic_matches: List[SemanticMatch] = Field(default=[], description="Semantic matches")
    total_matches: int = Field(..., description="Total number of semantic matches")
    average_similarity: float = Field(..., ge=0.0, le=1.0, description="Average similarity score")
    matching_time: float = Field(..., description="Time taken for matching in seconds")
    error: Optional[str] = Field(None, description="Error message if matching failed")
    
    class Config:
        use_enum_values = True
