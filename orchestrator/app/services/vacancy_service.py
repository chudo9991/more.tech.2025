"""
Vacancy service
"""
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.vacancy import Vacancy
from app.models.vacancy_section_keywords import VacancySectionKeywords
from app.schemas.vacancy import VacancyCreate, VacancyUpdate
from app.schemas.vacancy_keywords import VacancySectionKeywordsResponse


class VacancyService:
    def __init__(self, db: Session):
        self.db = db
    
    def generate_vacancy_code(self, title: str) -> str:
        """Генерирует уникальный код вакансии"""
        year = datetime.now().year
        
        # Создаем аббревиатуру из названия
        words = title.split()
        abbreviation = ''.join(word[0].upper() for word in words if word[0].isalpha())
        
        # Если аббревиатура пустая, используем первые буквы
        if not abbreviation:
            abbreviation = title[:3].upper()
        
        # Получаем следующий номер для этого года и аббревиатуры
        existing_codes = self.db.query(Vacancy.vacancy_code).filter(
            Vacancy.vacancy_code.like(f"{abbreviation}-{year}-%")
        ).all()
        
        if existing_codes:
            numbers = []
            for code in existing_codes:
                try:
                    number_part = code[0].split('-')[-1]
                    numbers.append(int(number_part))
                except (ValueError, IndexError):
                    continue
            
            if numbers:
                next_number = max(numbers) + 1
            else:
                next_number = 1
        else:
            next_number = 1
        
        return f"{abbreviation}-{year}-{next_number:03d}"
    
    def create_vacancy(self, vacancy_data: VacancyCreate) -> Vacancy:
        """Создает новую вакансию"""
        # Генерируем уникальный код вакансии
        vacancy_code = self.generate_vacancy_code(vacancy_data.title)
        
        # Создаем вакансию
        vacancy = Vacancy(
            id=str(uuid.uuid4()),
            vacancy_code=vacancy_code,
            **vacancy_data.dict()
        )
        
        self.db.add(vacancy)
        self.db.commit()
        self.db.refresh(vacancy)
        return vacancy
    
    def get_vacancies(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None,
        region: Optional[str] = None,
        city: Optional[str] = None,
        employment_type: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Vacancy]:
        """Получает список вакансий с фильтрацией"""
        query = self.db.query(Vacancy)
        
        # Применяем фильтры
        if status:
            query = query.filter(Vacancy.status == status)
        
        if region:
            query = query.filter(Vacancy.region.ilike(f"%{region}%"))
        
        if city:
            query = query.filter(Vacancy.city.ilike(f"%{city}%"))
        
        if employment_type:
            query = query.filter(Vacancy.employment_type == employment_type)
        
        if search:
            search_filter = or_(
                Vacancy.title.ilike(f"%{search}%"),
                Vacancy.description.ilike(f"%{search}%"),
                Vacancy.requirements.ilike(f"%{search}%"),
                Vacancy.responsibilities.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        return query.offset(skip).limit(limit).all()
    
    def get_vacancy_keywords(self, vacancy_id: str) -> List[VacancySectionKeywordsResponse]:
        """Получает ключевые слова для вакансии"""
        keywords_records = self.db.query(VacancySectionKeywords).filter(
            VacancySectionKeywords.vacancy_id == vacancy_id
        ).all()
        
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
    
    def get_vacancy(self, vacancy_id: str) -> Optional[Vacancy]:
        """Получает вакансию по ID"""
        return self.db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    
    def get_vacancy_by_code(self, vacancy_code: str) -> Optional[Vacancy]:
        """Получает вакансию по коду"""
        return self.db.query(Vacancy).filter(Vacancy.vacancy_code == vacancy_code).first()
    
    def update_vacancy(self, vacancy_id: str, vacancy_data: VacancyUpdate) -> Optional[Vacancy]:
        """Обновляет вакансию"""
        vacancy = self.get_vacancy(vacancy_id)
        if not vacancy:
            return None
        
        # Обновляем только переданные поля
        update_data = vacancy_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(vacancy, field, value)
        
        # Обновляем время изменения
        vacancy.updated_at = datetime.now()
        
        self.db.commit()
        self.db.refresh(vacancy)
        return vacancy
    
    def delete_vacancy(self, vacancy_id: str) -> bool:
        """Удаляет вакансию"""
        vacancy = self.get_vacancy(vacancy_id)
        if not vacancy:
            return False
        
        self.db.delete(vacancy)
        self.db.commit()
        return True
    
    def get_vacancy_statistics(self) -> Dict[str, Any]:
        """Получает статистику по вакансиям"""
        total_vacancies = self.db.query(Vacancy).count()
        active_vacancies = self.db.query(Vacancy).filter(Vacancy.status == "active").count()
        closed_vacancies = self.db.query(Vacancy).filter(Vacancy.status == "closed").count()
        draft_vacancies = self.db.query(Vacancy).filter(Vacancy.status == "draft").count()
        
        # Статистика по регионам
        regions = self.db.query(Vacancy.region).filter(
            Vacancy.region.isnot(None)
        ).distinct().all()
        region_count = len(regions)
        
        # Статистика по типам занятости
        employment_types = self.db.query(Vacancy.employment_type).filter(
            Vacancy.employment_type.isnot(None)
        ).distinct().all()
        employment_type_count = len(employment_types)
        
        return {
            "total": total_vacancies,
            "active": active_vacancies,
            "closed": closed_vacancies,
            "draft": draft_vacancies,
            "regions": region_count,
            "employment_types": employment_type_count
        }
    
    def search_vacancies(self, search_term: str, limit: int = 10) -> List[Vacancy]:
        """Поиск вакансий по тексту"""
        query = self.db.query(Vacancy).filter(
            or_(
                Vacancy.title.ilike(f"%{search_term}%"),
                Vacancy.description.ilike(f"%{search_term}%"),
                Vacancy.requirements.ilike(f"%{search_term}%"),
                Vacancy.responsibilities.ilike(f"%{search_term}%"),
                Vacancy.vacancy_code.ilike(f"%{search_term}%")
            )
        )
        
        return query.limit(limit).all()
