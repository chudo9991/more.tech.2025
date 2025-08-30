import asyncio
import json
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models import VacancySectionKeywords, SectionType, Vacancy
from app.schemas.vacancy_keywords import (
    VacancySectionKeywordsCreate,
    VacancySectionKeywordsUpdate,
    SectionKeywordsResponse,
    AllSectionKeywordsResponse,
    KeywordsExtractionStats
)
from app.services.cache_service import CacheService
from app.core.config import settings

logger = logging.getLogger(__name__)


class KeywordsExtractor:
    """Service for extracting keywords from vacancy sections using LLM"""
    
    def __init__(self, db: Session):
        self.db = db
        self.cache_service = CacheService()
        
    def _generate_id(self) -> str:
        """Generate unique ID for keywords record"""
        return f"KEYWORDS_{uuid.uuid4().hex[:8].upper()}"
    
    def _get_section_text(self, vacancy: Vacancy, section_type: SectionType) -> Optional[str]:
        """Get text content for specific section type"""
        section_mapping = {
            SectionType.RESPONSIBILITIES: vacancy.responsibilities,
            SectionType.REQUIREMENTS: vacancy.requirements,
            SectionType.PROGRAMS: vacancy.special_programs,
            SectionType.SKILLS: vacancy.computer_skills,
            SectionType.LANGUAGES: vacancy.foreign_languages,
            SectionType.DESCRIPTION: vacancy.description,
            SectionType.ADDITIONAL: vacancy.additional_info
        }
        return section_mapping.get(section_type)
    
    def _create_extraction_prompt(self, section_type: SectionType, text: str) -> str:
        """Create LLM prompt for keyword extraction based on section type"""
        base_prompt = f"""
        Извлеки ключевые слова из следующего текста раздела вакансии "{section_type.value}".
        
        Текст:
        {text}
        
        Инструкции по извлечению:
        """
        
        section_instructions = {
            SectionType.RESPONSIBILITIES: """
            - Извлекай действия, задачи, обязанности
            - Фокусируйся на глаголах и существительных, описывающих работу
            - Примеры: "разработка", "тестирование", "управление проектами"
            """,
            SectionType.REQUIREMENTS: """
            - Извлекай требования к навыкам, опыту, квалификации
            - Фокусируйся на технических и профессиональных компетенциях
            - Примеры: "Python", "3 года опыта", "высшее образование"
            """,
            SectionType.PROGRAMS: """
            - Извлекай названия программ, технологий, инструментов
            - Фокусируйся на конкретных технологиях и ПО
            - Примеры: "Docker", "Git", "PostgreSQL", "VS Code"
            """,
            SectionType.SKILLS: """
            - Извлекай технические навыки и компетенции
            - Фокусируйся на программировании, фреймворках, методологиях
            - Примеры: "React", "Agile", "REST API", "SQL"
            """,
            SectionType.LANGUAGES: """
            - Извлекай языки программирования и естественные языки
            - Фокусируйся на названиях языков и уровнях владения
            - Примеры: "Python", "Английский B2", "JavaScript"
            """,
            SectionType.DESCRIPTION: """
            - Извлекай общие ключевые слова из описания
            - Фокусируйся на важных концепциях и терминах
            - Примеры: "стартап", "удаленная работа", "инновации"
            """,
            SectionType.ADDITIONAL: """
            - Извлекай дополнительные ключевые слова
            - Фокусируйся на специфических требованиях и условиях
            - Примеры: "командировки", "гибкий график", "премии"
            """
        }
        
        prompt = base_prompt + section_instructions.get(section_type, "")
        prompt += """
        
        Верни результат в формате JSON:
        {
            "keywords": ["ключевое_слово_1", "ключевое_слово_2", ...],
            "confidence_score": 0.85,
            "explanation": "краткое объяснение извлечения"
        }
        
        Извлеки 5-15 наиболее важных ключевых слов. Уверенность (confidence_score) от 0.0 до 1.0.
        """
        
        return prompt
    
    async def _call_llm_service(self, prompt: str) -> Dict[str, Any]:
        """Call LLM service for keyword extraction"""
        try:
            import httpx
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.LLM_SERVICE_URL}/api/v1/llm/generate",
                    json={
                        "prompt": prompt,
                        "max_tokens": 500,
                        "temperature": 0.3
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result
                else:
                    logger.error(f"LLM service error: {response.status_code} - {response.text}")
                    return {"error": f"LLM service error: {response.status_code}"}
                    
        except Exception as e:
            logger.error(f"Error calling LLM service: {str(e)}")
            return {"error": str(e)}
    
    def _parse_llm_response(self, response: Dict[str, Any]) -> tuple[List[str], float]:
        """Parse LLM response and extract keywords and confidence"""
        try:
            logger.info(f"Parsing LLM response: {response}")
            
            if "error" in response:
                logger.error(f"LLM response contains error: {response['error']}")
                return [], 0.0
                
            content = response.get("content", "") or response.get("response", "")
            if not content:
                logger.warning("LLM response has no content or response")
                return [], 0.0
            
            # Try to extract JSON from response
            try:
                # Find JSON in the response
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                if start_idx != -1 and end_idx != 0:
                    json_str = content[start_idx:end_idx]
                    logger.info(f"Extracted JSON string: {json_str}")
                    data = json.loads(json_str)
                else:
                    # Fallback: try to parse the whole content
                    logger.info(f"Trying to parse whole content as JSON: {content}")
                    data = json.loads(content)
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON from LLM response: {content}, error: {e}")
                return [], 0.0
            
            keywords = data.get("keywords", [])
            confidence = data.get("confidence_score", 0.0)
            
            # Validate keywords
            if not isinstance(keywords, list):
                keywords = []
            if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
                confidence = 0.0
                
            return keywords, confidence
            
        except Exception as e:
            logger.error(f"Error parsing LLM response: {str(e)}")
            return [], 0.0
    
    async def extract_keywords_from_section(
        self, 
        vacancy_id: str, 
        section_type: SectionType, 
        force_reload: bool = False
    ) -> SectionKeywordsResponse:
        """Extract keywords from a specific section"""
        start_time = datetime.now()
        
        try:
            # Get vacancy
            vacancy = self.db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
            if not vacancy:
                return SectionKeywordsResponse(
                    success=False,
                    vacancy_id=vacancy_id,
                    section_type=section_type,
                    error="Vacancy not found"
                )
            
            # Check cache if not forcing reload
            cache_identifier = f"{vacancy_id}:{section_type.value}"
            if not force_reload:
                cached_result = self.cache_service.get('keywords', cache_identifier)
                if cached_result:
                    logger.info(f"Using cached keywords for {vacancy_id}:{section_type.value}")
                    return SectionKeywordsResponse(
                        success=True,
                        vacancy_id=vacancy_id,
                        section_type=section_type,
                        keywords=cached_result.get("keywords", []),
                        confidence_score=cached_result.get("confidence_score", 0.0),
                        extraction_time=0.0
                    )
            
            # Get section text
            section_text = self._get_section_text(vacancy, section_type)
            if not section_text or not section_text.strip():
                return SectionKeywordsResponse(
                    success=False,
                    vacancy_id=vacancy_id,
                    section_type=section_type,
                    error="Section text is empty"
                )
            
            # Create prompt and call LLM
            prompt = self._create_extraction_prompt(section_type, section_text)
            llm_response = await self._call_llm_service(prompt)
            
            # Parse response
            keywords, confidence = self._parse_llm_response(llm_response)
            
            if not keywords:
                return SectionKeywordsResponse(
                    success=False,
                    vacancy_id=vacancy_id,
                    section_type=section_type,
                    error="Failed to extract keywords from LLM response"
                )
            
            # Save to database
            keywords_record = self._save_keywords_to_db(
                vacancy_id=vacancy_id,
                section_type=section_type,
                keywords=keywords,
                confidence_score=confidence
            )
            
            # Cache result
            cache_data = {
                "keywords": keywords,
                "confidence_score": confidence,
                "extraction_date": datetime.now().isoformat()
            }
            self.cache_service.set('keywords', cache_identifier, cache_data, ttl=3600)  # 1 hour
            
            # Calculate extraction time
            extraction_time = (datetime.now() - start_time).total_seconds()
            
            return SectionKeywordsResponse(
                success=True,
                vacancy_id=vacancy_id,
                section_type=section_type,
                keywords=keywords,
                confidence_score=confidence,
                extraction_time=extraction_time
            )
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {str(e)}")
            return SectionKeywordsResponse(
                success=False,
                vacancy_id=vacancy_id,
                section_type=section_type,
                error=str(e)
            )
    
    def _save_keywords_to_db(
        self, 
        vacancy_id: str, 
        section_type: SectionType, 
        keywords: List[str], 
        confidence_score: float
    ) -> VacancySectionKeywords:
        """Save or update keywords in database"""
        
        # Check if record exists
        existing_record = self.db.query(VacancySectionKeywords).filter(
            and_(
                VacancySectionKeywords.vacancy_id == vacancy_id,
                VacancySectionKeywords.section_type == section_type
            )
        ).first()
        
        if existing_record:
            # Update existing record
            existing_record.keywords = keywords
            existing_record.confidence_score = confidence_score
            existing_record.extraction_date = datetime.now()
            existing_record.updated_at = datetime.now()
            self.db.commit()
            return existing_record
        else:
            # Create new record
            new_record = VacancySectionKeywords(
                id=self._generate_id(),
                vacancy_id=vacancy_id,
                section_type=section_type,
                keywords=keywords,
                confidence_score=confidence_score,
                extraction_date=datetime.now()
            )
            self.db.add(new_record)
            self.db.commit()
            self.db.refresh(new_record)
            return new_record
    
    async def extract_all_keywords(self, vacancy_id: str, force_reload: bool = False) -> AllSectionKeywordsResponse:
        """Extract keywords for all sections of a vacancy"""
        start_time = datetime.now()
        
        try:
            # Get vacancy
            vacancy = self.db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
            if not vacancy:
                return AllSectionKeywordsResponse(
                    success=False,
                    vacancy_id=vacancy_id,
                    error="Vacancy not found"
                )
            
            # Extract keywords for all sections
            section_types = list(SectionType)
            results = []
            
            for section_type in section_types:
                result = await self.extract_keywords_from_section(
                    vacancy_id=vacancy_id,
                    section_type=section_type,
                    force_reload=force_reload
                )
                results.append(result)
            
            # Calculate total time
            total_time = (datetime.now() - start_time).total_seconds()
            
            return AllSectionKeywordsResponse(
                success=True,
                vacancy_id=vacancy_id,
                sections=results,
                total_extraction_time=total_time
            )
            
        except Exception as e:
            logger.error(f"Error extracting all keywords: {str(e)}")
            return AllSectionKeywordsResponse(
                success=False,
                vacancy_id=vacancy_id,
                error=str(e)
            )
    
    def get_keywords(self, vacancy_id: str, section_type: SectionType) -> Optional[VacancySectionKeywords]:
        """Get keywords for a specific section"""
        return self.db.query(VacancySectionKeywords).filter(
            and_(
                VacancySectionKeywords.vacancy_id == vacancy_id,
                VacancySectionKeywords.section_type == section_type
            )
        ).first()
    
    def get_all_keywords(self, vacancy_id: str) -> List[VacancySectionKeywords]:
        """Get keywords for all sections of a vacancy"""
        return self.db.query(VacancySectionKeywords).filter(
            VacancySectionKeywords.vacancy_id == vacancy_id
        ).all()
    
    def update_keywords(
        self, 
        vacancy_id: str, 
        section_type: SectionType, 
        keywords: List[str], 
        confidence_score: Optional[float] = None
    ) -> Optional[VacancySectionKeywords]:
        """Update keywords for a specific section"""
        try:
            record = self.get_keywords(vacancy_id, section_type)
            
            if record:
                record.keywords = keywords
                if confidence_score is not None:
                    record.confidence_score = confidence_score
                record.updated_at = datetime.now()
                self.db.commit()
                self.db.refresh(record)
                
                # Clear cache
                cache_identifier = f"{vacancy_id}:{section_type.value}"
                self.cache_service.delete('keywords', cache_identifier)
                
                return record
            else:
                # Create new record if doesn't exist
                return self._save_keywords_to_db(
                    vacancy_id=vacancy_id,
                    section_type=section_type,
                    keywords=keywords,
                    confidence_score=confidence_score or 0.0
                )
                
        except Exception as e:
            logger.error(f"Error updating keywords: {str(e)}")
            self.db.rollback()
            return None
    
    def delete_keywords(self, vacancy_id: str, section_type: SectionType) -> bool:
        """Delete keywords for a specific section"""
        try:
            record = self.get_keywords(vacancy_id, section_type)
            if record:
                self.db.delete(record)
                self.db.commit()
                
                # Clear cache
                cache_identifier = f"{vacancy_id}:{section_type.value}"
                self.cache_service.delete('keywords', cache_identifier)
                
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error deleting keywords: {str(e)}")
            self.db.rollback()
            return False
    
    def get_extraction_stats(self, vacancy_id: str) -> KeywordsExtractionStats:
        """Get statistics for keywords extraction"""
        try:
            all_keywords = self.get_all_keywords(vacancy_id)
            
            total_sections = len(SectionType)
            extracted_sections = len(all_keywords)
            
            if extracted_sections == 0:
                return KeywordsExtractionStats(
                    total_sections=total_sections,
                    extracted_sections=0,
                    average_confidence=0.0,
                    total_keywords=0
                )
            
            total_keywords = sum(len(kw.keywords) for kw in all_keywords)
            average_confidence = sum(kw.confidence_score for kw in all_keywords) / extracted_sections
            
            return KeywordsExtractionStats(
                total_sections=total_sections,
                extracted_sections=extracted_sections,
                average_confidence=average_confidence,
                total_keywords=total_keywords
            )
            
        except Exception as e:
            logger.error(f"Error getting extraction stats: {str(e)}")
            return KeywordsExtractionStats(
                total_sections=len(SectionType),
                extracted_sections=0,
                average_confidence=0.0,
                total_keywords=0
            )
