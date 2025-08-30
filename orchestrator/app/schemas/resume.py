"""
Resume schemas for API requests and responses
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class ResumeSkillBase(BaseModel):
    skill_name: str
    skill_category: Optional[str] = None
    experience_level: Optional[str] = None
    years_experience: Optional[int] = None
    confidence_score: Optional[float] = None
    extracted_from: Optional[str] = None


class ResumeSkillCreate(ResumeSkillBase):
    pass


class ResumeSkillResponse(ResumeSkillBase):
    id: str
    resume_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class ResumeBlockBase(BaseModel):
    block_type: str
    block_name: str
    extracted_text: Optional[str] = None
    relevance_score: Optional[float] = None
    confidence_score: Optional[float] = None
    matched_requirements: Optional[List[str]] = None
    missing_requirements: Optional[List[str]] = None
    analysis_notes: Optional[str] = None


class ResumeBlockCreate(ResumeBlockBase):
    pass


class ResumeBlockResponse(ResumeBlockBase):
    id: str
    resume_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class ResumeBase(BaseModel):
    vacancy_id: Optional[str] = None
    vacancy_code: Optional[str] = None
    filename: str
    original_filename: str
    file_size: int
    file_type: str
    status: str = "uploaded"
    total_score: Optional[float] = None
    confidence_score: Optional[float] = None
    processing_errors: Optional[str] = None


class ResumeCreate(ResumeBase):
    pass


class ResumeUpdate(BaseModel):
    status: Optional[str] = None
    total_score: Optional[float] = None
    confidence_score: Optional[float] = None
    processing_errors: Optional[str] = None


class ResumeResponse(ResumeBase):
    id: str
    upload_date: datetime
    created_at: datetime
    updated_at: datetime
    vacancy_title: Optional[str] = None
    resume_blocks: List[ResumeBlockResponse] = []
    resume_skills: List[ResumeSkillResponse] = []

    class Config:
        from_attributes = True


class ResumeListResponse(BaseModel):
    id: str
    original_filename: str
    file_type: str
    file_size: int
    status: str
    total_score: Optional[float] = None
    confidence_score: Optional[float] = None
    upload_date: datetime
    vacancy_id: Optional[str] = None
    vacancy_code: Optional[str] = None
    vacancy_title: Optional[str] = None

    class Config:
        from_attributes = True


class ResumeUploadRequest(BaseModel):
    vacancy_id: Optional[str] = None
    vacancy_code: Optional[str] = None


class ResumeAnalysisResponse(BaseModel):
    resume: ResumeResponse
    analysis_summary: Dict[str, Any]
    block_scores: Dict[str, float]
    overall_recommendation: str


class ResumeStatisticsResponse(BaseModel):
    total_resumes: int
    processed_resumes: int
    error_resumes: int
    average_score: float
    score_distribution: Dict[str, int]
    top_vacancies: List[Dict[str, Any]]


class BatchFileData(BaseModel):
    filename: str
    content: bytes
    file_type: str = "pdf"


class BatchUploadRequest(BaseModel):
    files: List[BatchFileData]
    vacancy_id: Optional[str] = None
    max_concurrent: int = 3


class BatchResult(BaseModel):
    file_index: int
    filename: str
    status: str
    resume_id: Optional[str] = None
    sections_found: Optional[int] = None
    skills_found: Optional[int] = None
    error: Optional[str] = None


class BatchUploadResponse(BaseModel):
    batch_id: str
    status: str
    total_files: int
    successful: int
    failed: int
    processing_time_seconds: float
    results: List[BatchResult]
