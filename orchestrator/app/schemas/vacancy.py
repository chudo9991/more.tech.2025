"""
Vacancy schemas
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class VacancyBase(BaseModel):
    """Base vacancy schema"""
    title: str = Field(..., description="Название вакансии")
    status: Optional[str] = Field("active", description="Статус вакансии")
    region: Optional[str] = Field(None, description="Регион")
    city: Optional[str] = Field(None, description="Город")
    address: Optional[str] = Field(None, description="Адрес")
    
    # Условия труда
    employment_type: Optional[str] = Field(None, description="Тип занятости")
    contract_type: Optional[str] = Field(None, description="Тип трудового договора")
    work_schedule: Optional[str] = Field(None, description="График работы")
    business_trips: Optional[bool] = Field(False, description="Наличие командировок")
    
    # Финансовые условия
    salary_min: Optional[Decimal] = Field(None, description="Оклад мин. (руб/мес)")
    salary_max: Optional[Decimal] = Field(None, description="Оклад макс. (руб/мес)")
    total_income: Optional[Decimal] = Field(None, description="Доход (руб/мес)")
    annual_bonus_percent: Optional[Decimal] = Field(None, description="Годовая премия (%)")
    bonus_description: Optional[str] = Field(None, description="Описание премирования")
    
    # Требования к кандидату
    responsibilities: Optional[str] = Field(None, description="Обязанности")
    requirements: Optional[str] = Field(None, description="Требования")
    education_level: Optional[str] = Field(None, description="Уровень образования")
    experience_required: Optional[str] = Field(None, description="Требуемый опыт работы")
    special_programs: Optional[str] = Field(None, description="Знание специальных программ")
    computer_skills: Optional[str] = Field(None, description="Навыки работы на компьютере")
    foreign_languages: Optional[str] = Field(None, description="Знание иностранных языков")
    language_level: Optional[str] = Field(None, description="Уровень владения языка")
    
    # Дополнительная информация
    additional_info: Optional[str] = Field(None, description="Дополнительная информация")
    description: Optional[str] = Field(None, description="Описание вакансии")


class VacancyCreate(VacancyBase):
    """Schema for creating a vacancy"""
    pass


class VacancyUpdate(BaseModel):
    """Schema for updating a vacancy"""
    title: Optional[str] = Field(None, description="Название вакансии")
    status: Optional[str] = Field(None, description="Статус вакансии")
    region: Optional[str] = Field(None, description="Регион")
    city: Optional[str] = Field(None, description="Город")
    address: Optional[str] = Field(None, description="Адрес")
    
    # Условия труда
    employment_type: Optional[str] = Field(None, description="Тип занятости")
    contract_type: Optional[str] = Field(None, description="Тип трудового договора")
    work_schedule: Optional[str] = Field(None, description="График работы")
    business_trips: Optional[bool] = Field(None, description="Наличие командировок")
    
    # Финансовые условия
    salary_min: Optional[Decimal] = Field(None, description="Оклад мин. (руб/мес)")
    salary_max: Optional[Decimal] = Field(None, description="Оклад макс. (руб/мес)")
    total_income: Optional[Decimal] = Field(None, description="Доход (руб/мес)")
    annual_bonus_percent: Optional[Decimal] = Field(None, description="Годовая премия (%)")
    bonus_description: Optional[str] = Field(None, description="Описание премирования")
    
    # Требования к кандидату
    responsibilities: Optional[str] = Field(None, description="Обязанности")
    requirements: Optional[str] = Field(None, description="Требования")
    education_level: Optional[str] = Field(None, description="Уровень образования")
    experience_required: Optional[str] = Field(None, description="Требуемый опыт работы")
    special_programs: Optional[str] = Field(None, description="Знание специальных программ")
    computer_skills: Optional[str] = Field(None, description="Навыки работы на компьютере")
    foreign_languages: Optional[str] = Field(None, description="Знание иностранных языков")
    language_level: Optional[str] = Field(None, description="Уровень владения языка")
    
    # Дополнительная информация
    additional_info: Optional[str] = Field(None, description="Дополнительная информация")
    description: Optional[str] = Field(None, description="Описание вакансии")


class VacancyResponse(VacancyBase):
    """Schema for vacancy response"""
    id: str = Field(..., description="ID вакансии")
    vacancy_code: Optional[str] = Field(None, description="Код вакансии")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата обновления")
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v) if v else None
        }


class VacancyListResponse(BaseModel):
    """Schema for vacancy list response"""
    vacancies: list[VacancyResponse] = Field(..., description="Список вакансий")
    total: int = Field(..., description="Общее количество")
    page: int = Field(..., description="Номер страницы")
    size: int = Field(..., description="Размер страницы")
    
    class Config:
        from_attributes = True
