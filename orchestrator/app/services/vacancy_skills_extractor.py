"""
Vacancy skills extraction service using LLM
"""
import json
import time
import asyncio
from typing import Dict, List, Any, Optional
import httpx
from app.models import Vacancy
from app.schemas.vacancy_skills import (
    VacancySkill, SkillCategory, SkillLevel, VacancySkillsExtractionResponse
)
from app.core.config import settings
from app.services.cache_service import cache_service


class VacancySkillsExtractor:
    """Service for extracting skills from vacancy descriptions using LLM"""
    
    def __init__(self):
        self.llm_service_url = settings.LLM_SERVICE_URL
        self.client = httpx.AsyncClient(timeout=60.0)
        self.cache_ttl = 3600  # 1 hour cache
    
    async def extract_skills_from_vacancy(self, vacancy: Vacancy, force_reload: bool = False) -> VacancySkillsExtractionResponse:
        """
        Extract skills from vacancy description using LLM
        
        Args:
            vacancy: Vacancy object
            force_reload: Force reload from LLM, bypass cache
            
        Returns:
            VacancySkillsExtractionResponse with extracted skills
        """
        start_time = time.time()
        
        try:
            # Check cache first
            if not force_reload:
                cached_result = self._get_cached_skills(vacancy.id)
                if cached_result:
                    return cached_result
            
            # Extract skills using LLM
            skills = await self._extract_skills_with_llm(vacancy)
            
            # Calculate metrics
            extraction_time = time.time() - start_time
            total_skills = len(skills)
            mandatory_skills = len([s for s in skills if s.is_mandatory])
            
            # Create response
            response = VacancySkillsExtractionResponse(
                success=True,
                vacancy_id=vacancy.id,
                skills=skills,
                total_skills=total_skills,
                mandatory_skills=mandatory_skills,
                extraction_time=extraction_time,
                confidence=0.85  # High confidence for LLM extraction
            )
            
            # Cache the result
            self._cache_skills(vacancy.id, response)
            
            return response
            
        except Exception as e:
            extraction_time = time.time() - start_time
            return VacancySkillsExtractionResponse(
                success=False,
                vacancy_id=vacancy.id,
                skills=[],
                total_skills=0,
                mandatory_skills=0,
                extraction_time=extraction_time,
                confidence=0.0,
                error=str(e)
            )
    
    async def _extract_skills_with_llm(self, vacancy: Vacancy) -> List[VacancySkill]:
        """Extract skills from vacancy using LLM"""
        
        # Prepare vacancy text for analysis
        vacancy_text = self._prepare_vacancy_text(vacancy)
        
        # Create LLM prompt
        prompt = self._create_extraction_prompt(vacancy_text)
        
        # Call LLM service
        response = await self._call_llm_service(prompt)
        
        # Parse and validate response
        skills_data = self._parse_llm_response(response)
        
        # Convert to VacancySkill objects
        skills = []
        for skill_data in skills_data:
            try:
                skill = VacancySkill(
                    skill_name=skill_data["skill_name"],
                    category=skill_data["category"],
                    importance=float(skill_data["importance"]),
                    required_level=skill_data["required_level"],
                    is_mandatory=skill_data["is_mandatory"],
                    alternatives=skill_data.get("alternatives", []),
                    description=skill_data.get("description")
                )
                skills.append(skill)
            except Exception as e:
                # Log invalid skill data but continue
                print(f"Invalid skill data: {skill_data}, error: {e}")
                continue
        
        return skills
    
    def _prepare_vacancy_text(self, vacancy: Vacancy) -> str:
        """Prepare vacancy text for LLM analysis"""
        text_parts = []
        
        if vacancy.title:
            text_parts.append(f"Должность: {vacancy.title}")
        
        if vacancy.description:
            text_parts.append(f"Описание: {vacancy.description}")
        
        if vacancy.requirements:
            text_parts.append(f"Требования: {vacancy.requirements}")
        
        if vacancy.responsibilities:
            text_parts.append(f"Обязанности: {vacancy.responsibilities}")
        
        if vacancy.experience_required:
            text_parts.append(f"Требуемый опыт: {vacancy.experience_required}")
        
        if vacancy.education_level:
            text_parts.append(f"Образование: {vacancy.education_level}")
        
        return "\n\n".join(text_parts)
    
    def _create_extraction_prompt(self, vacancy_text: str) -> str:
        """Create LLM prompt for skills extraction"""
        
        prompt = f"""
Ты - эксперт по анализу вакансий и извлечению требуемых навыков. 

АНАЛИЗИРУЙ ВАКАНСИЮ:
{vacancy_text}

ИНСТРУКЦИИ:
1. Извлеки все требуемые навыки из описания вакансии
2. Определи категорию каждого навыка
3. Оцени важность навыка (0.0-1.0)
4. Определи требуемый уровень владения
5. Определи, является ли навык обязательным
6. Предложи альтернативные названия навыка

КАТЕГОРИИ НАВЫКОВ:
- programming: языки программирования (Python, Java, JavaScript, etc.)
- database: базы данных (PostgreSQL, MySQL, MongoDB, etc.)
- devops: DevOps инструменты (Docker, Kubernetes, CI/CD, etc.)
- frameworks: фреймворки (Django, Flask, React, etc.)
- tools: инструменты разработки (Git, IDE, etc.)
- soft_skills: мягкие навыки (коммуникация, лидерство, etc.)
- methodologies: методологии (Agile, Scrum, etc.)
- cloud: облачные платформы (AWS, Azure, GCP, etc.)
- testing: тестирование (unit testing, integration testing, etc.)
- analytics: аналитика (data analysis, BI tools, etc.)
- design: дизайн (UI/UX, graphic design, etc.)
- management: управление (project management, team lead, etc.)
- languages: иностранные языки
- other: прочие навыки

УРОВНИ ВЛАДЕНИЯ:
- beginner: начальный уровень
- intermediate: средний уровень  
- expert: экспертный уровень

ВЕРНИ РЕЗУЛЬТАТ В ФОРМАТЕ JSON:
{{
    "skills": [
        {{
            "skill_name": "название навыка",
            "category": "категория из списка выше",
            "importance": 0.8,
            "required_level": "beginner/intermediate/expert",
            "is_mandatory": true/false,
            "alternatives": ["альтернативные названия"],
            "description": "описание требования к навыку"
        }}
    ]
}}

ВАЖНО: 
- Отвечай ТОЛЬКО в формате JSON
- Не добавляй дополнительный текст
- Используй только указанные категории и уровни
- Оценивай важность объективно (0.0-1.0)
- Обязательные навыки - те, без которых невозможно выполнять работу
"""
        
        return prompt
    
    async def _call_llm_service(self, prompt: str) -> str:
        """Call LLM service for skills extraction"""
        try:
            payload = {
                "prompt": prompt,
                "max_tokens": 3000,
                "temperature": 0.2,  # Low temperature for consistent extraction
                "system_message": "Ты - эксперт по анализу вакансий. Извлекай навыки точно и структурированно."
            }
            
            print(f"Calling LLM service at: {self.llm_service_url}/api/v1/llm/generate")
            print(f"Payload: {payload}")
            
            response = await self.client.post(
                f"{self.llm_service_url}/api/v1/llm/generate",
                json=payload
            )
            
            print(f"LLM response status: {response.status_code}")
            print(f"LLM response headers: {response.headers}")
            
            if response.status_code != 200:
                error_text = await response.text()
                print(f"LLM error response: {error_text}")
                raise Exception(f"LLM service error: {response.status_code} - {error_text}")
            
            result = response.json()
            print(f"LLM response: {result}")
            return result.get("response", "")
            
        except Exception as e:
            print(f"LLM service exception: {e}")
            raise Exception(f"Failed to call LLM service: {str(e)}")
    
    def _parse_llm_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse and validate LLM response"""
        try:
            # Try to extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[json_start:json_end]
            parsed = json.loads(json_str)
            
            # Validate structure
            if "skills" not in parsed:
                raise ValueError("No 'skills' field in response")
            
            skills_data = parsed["skills"]
            if not isinstance(skills_data, list):
                raise ValueError("'skills' field is not a list")
            
            # Validate each skill
            validated_skills = []
            for skill in skills_data:
                if not isinstance(skill, dict):
                    continue
                
                # Check required fields
                required_fields = ["skill_name", "category", "importance", "required_level", "is_mandatory"]
                if all(field in skill for field in required_fields):
                    validated_skills.append(skill)
            
            return validated_skills
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to parse response: {str(e)}")
    
    def _get_cached_skills(self, vacancy_id: str) -> Optional[VacancySkillsExtractionResponse]:
        """Get cached skills for vacancy"""
        try:
            cached_data = cache_service.get_vacancy_requirements(vacancy_id)
            
            if cached_data and 'skills' in cached_data:
                return VacancySkillsExtractionResponse(**cached_data)
            
            return None
            
        except Exception as e:
            print(f"Error getting cached skills: {e}")
            return None
    
    def _cache_skills(self, vacancy_id: str, response: VacancySkillsExtractionResponse):
        """Cache skills for vacancy"""
        try:
            cache_service.set_vacancy_requirements(vacancy_id, response.dict())
        except Exception as e:
            print(f"Error caching skills: {e}")
    
    def invalidate_cache(self, vacancy_id: str):
        """Invalidate cache for vacancy"""
        try:
            cache_service.invalidate_vacancy_cache(vacancy_id)
        except Exception as e:
            print(f"Error invalidating cache: {e}")
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Global instance
vacancy_skills_extractor = VacancySkillsExtractor()
