# Pydantic schemas for API
from .vacancy import VacancyCreate, VacancyUpdate, VacancyResponse, VacancyListResponse
from .resume import (
    ResumeCreate, ResumeUpdate, ResumeResponse, ResumeListResponse,
    ResumeBlockCreate, ResumeBlockResponse,
    ResumeSkillCreate, ResumeSkillResponse,
    ResumeUploadRequest, ResumeAnalysisResponse, ResumeStatisticsResponse
)
