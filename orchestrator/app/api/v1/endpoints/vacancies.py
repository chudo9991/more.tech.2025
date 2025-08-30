"""
Vacancy management endpoints
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.vacancy import (
    VacancyCreate, 
    VacancyUpdate, 
    VacancyResponse, 
    VacancyListResponse
)
from app.services.vacancy_service import VacancyService

router = APIRouter()


@router.post("/", response_model=VacancyResponse)
async def create_vacancy(
    vacancy_data: VacancyCreate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Создает новую вакансию"""
    try:
        vacancy_service = VacancyService(db)
        vacancy = vacancy_service.create_vacancy(vacancy_data)
        return vacancy
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[VacancyResponse])
async def get_vacancies(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей"),
    status: Optional[str] = Query(None, description="Фильтр по статусу"),
    region: Optional[str] = Query(None, description="Фильтр по региону"),
    city: Optional[str] = Query(None, description="Фильтр по городу"),
    employment_type: Optional[str] = Query(None, description="Фильтр по типу занятости"),
    search: Optional[str] = Query(None, description="Поиск по тексту"),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Получает список вакансий с фильтрацией"""
    try:
        vacancy_service = VacancyService(db)
        vacancies = vacancy_service.get_vacancies(
            skip=skip,
            limit=limit,
            status=status,
            region=region,
            city=city,
            employment_type=employment_type,
            search=search
        )
        return vacancies
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/search", response_model=List[VacancyResponse])
async def search_vacancies(
    q: str = Query(..., description="Поисковый запрос"),
    limit: int = Query(10, ge=1, le=50, description="Максимальное количество результатов"),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Поиск вакансий по тексту"""
    try:
        vacancy_service = VacancyService(db)
        vacancies = vacancy_service.search_vacancies(q, limit=limit)
        return vacancies
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/statistics")
async def get_vacancy_statistics(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Получает статистику по вакансиям"""
    try:
        vacancy_service = VacancyService(db)
        statistics = vacancy_service.get_vacancy_statistics()
        return statistics
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{vacancy_id}", response_model=VacancyResponse)
async def get_vacancy(
    vacancy_id: str = Path(..., description="ID вакансии"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Получает вакансию по ID"""
    try:
        vacancy_service = VacancyService(db)
        vacancy = vacancy_service.get_vacancy(vacancy_id)
        if not vacancy:
            raise HTTPException(status_code=404, detail="Вакансия не найдена")
        return vacancy
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/code/{vacancy_code}", response_model=VacancyResponse)
async def get_vacancy_by_code(
    vacancy_code: str = Path(..., description="Код вакансии"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Получает вакансию по коду"""
    try:
        vacancy_service = VacancyService(db)
        vacancy = vacancy_service.get_vacancy_by_code(vacancy_code)
        if not vacancy:
            raise HTTPException(status_code=404, detail="Вакансия не найдена")
        return vacancy
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{vacancy_id}", response_model=VacancyResponse)
async def update_vacancy(
    vacancy_id: str = Path(..., description="ID вакансии"),
    vacancy_data: VacancyUpdate = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Обновляет вакансию"""
    try:
        vacancy_service = VacancyService(db)
        vacancy = vacancy_service.update_vacancy(vacancy_id, vacancy_data)
        if not vacancy:
            raise HTTPException(status_code=404, detail="Вакансия не найдена")
        return vacancy
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{vacancy_id}")
async def delete_vacancy(
    vacancy_id: str = Path(..., description="ID вакансии"),
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """Удаляет вакансию"""
    try:
        vacancy_service = VacancyService(db)
        success = vacancy_service.delete_vacancy(vacancy_id)
        if not success:
            raise HTTPException(status_code=404, detail="Вакансия не найдена")
        return {"message": "Вакансия успешно удалена"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
