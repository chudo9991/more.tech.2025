# Pydantic schemas for API
from .vacancy import VacancyCreate, VacancyUpdate, VacancyResponse, VacancyListResponse
from .resume import (
    ResumeCreate, ResumeUpdate, ResumeResponse, ResumeListResponse,
    ResumeBlockCreate, ResumeBlockResponse,
    ResumeSkillCreate, ResumeSkillResponse,
    ResumeUploadRequest, ResumeAnalysisResponse, ResumeStatisticsResponse
)
from .vacancy_skills import (
    VacancySkill, SkillCategory, SkillLevel,
    VacancySkillsExtractionRequest, VacancySkillsExtractionResponse,
    SkillAnalysisRequest, SkillMatch, ResumeSkillsAnalysisResponse,
    SemanticMatchingRequest, SemanticMatch, SemanticMatchingResponse
)
