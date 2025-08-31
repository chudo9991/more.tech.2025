"""
Dynamic criteria schemas
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class DynamicCriteriaBase(BaseModel):
    """Base schema for dynamic criteria"""
    skill_name: str = Field(..., description="Название навыка")
    category: str = Field(..., description="Категория навыка")
    importance: float = Field(..., ge=0.0, le=1.0, description="Важность навыка (0.0-1.0)")
    required_level: str = Field(..., description="Требуемый уровень владения")
    is_mandatory: bool = Field(default=False, description="Обязательный навык")
    description: Optional[str] = Field(None, description="Описание критерия")
    alternatives: Optional[List[str]] = Field(default=[], description="Альтернативные названия")


class DynamicCriteriaCreate(DynamicCriteriaBase):
    """Schema for creating dynamic criteria"""
    vacancy_id: str = Field(..., description="ID вакансии")


class DynamicCriteriaUpdate(BaseModel):
    """Schema for updating dynamic criteria"""
    skill_name: Optional[str] = None
    category: Optional[str] = None
    importance: Optional[float] = Field(None, ge=0.0, le=1.0)
    required_level: Optional[str] = None
    is_mandatory: Optional[bool] = None
    description: Optional[str] = None
    alternatives: Optional[List[str]] = None


class DynamicCriteriaResponse(DynamicCriteriaBase):
    """Schema for dynamic criteria response"""
    id: str
    vacancy_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ScenarioCriteriaMappingBase(BaseModel):
    """Base schema for scenario criteria mapping"""
    scenario_id: str = Field(..., description="ID сценария")
    criterion_id: str = Field(..., description="ID критерия")
    weight: float = Field(..., ge=0.0, le=1.0, description="Вес критерия в сценарии")
    is_mandatory: bool = Field(default=False, description="Обязательный критерий")
    min_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Минимальный балл")


class ScenarioCriteriaMappingCreate(ScenarioCriteriaMappingBase):
    """Schema for creating scenario criteria mapping"""
    pass


class ScenarioCriteriaMappingUpdate(BaseModel):
    """Schema for updating scenario criteria mapping"""
    weight: Optional[float] = Field(None, ge=0.0, le=1.0)
    is_mandatory: Optional[bool] = None
    min_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class ScenarioCriteriaMappingResponse(ScenarioCriteriaMappingBase):
    """Schema for scenario criteria mapping response"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ScenarioGenerationRequest(BaseModel):
    """Schema for scenario generation request"""
    vacancy_id: str = Field(..., description="ID вакансии")
    scenario_name: Optional[str] = Field(None, description="Название сценария")
    description: Optional[str] = Field(None, description="Описание сценария")
    force_regenerate: bool = Field(default=False, description="Принудительная перегенерация")


class ScenarioGenerationResponse(BaseModel):
    """Schema for scenario generation response"""
    success: bool
    scenario_id: Optional[str] = None
    scenario_name: Optional[str] = None
    nodes_count: Optional[int] = None
    transitions_count: Optional[int] = None
    criteria_count: Optional[int] = None
    skills_used: Optional[List[str]] = None
    error: Optional[str] = None


class ScenarioPreviewRequest(BaseModel):
    """Schema for scenario preview request"""
    vacancy_id: str = Field(..., description="ID вакансии")
    scenario_name: Optional[str] = None
    description: Optional[str] = None


class ScenarioPreviewResponse(BaseModel):
    """Schema for scenario preview response"""
    scenario_name: str
    description: str
    nodes: List[Dict[str, Any]]
    transitions: List[Dict[str, Any]]
    criteria: List[DynamicCriteriaResponse]
    skills_used: List[str]


class DynamicCriteriaListResponse(BaseModel):
    """Schema for dynamic criteria list response"""
    criteria: List[DynamicCriteriaResponse]
    total_count: int
    vacancy_id: str


class VacancyDynamicCriteriaResponse(BaseModel):
    """Schema for vacancy dynamic criteria response"""
    vacancy_id: str
    vacancy_title: str
    criteria: List[DynamicCriteriaResponse]
    skills_count: int
    mandatory_skills_count: int
    average_importance: float
