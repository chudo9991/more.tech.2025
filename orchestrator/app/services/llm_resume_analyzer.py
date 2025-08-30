"""
LLM-based resume analysis service
"""
import json
import asyncio
from typing import Dict, List, Any, Optional
import httpx
from app.core.config import settings
from app.schemas.vacancy_skills import VacancySkill, SkillMatch, ResumeSkillsAnalysisResponse


class LLMResumeAnalyzer:
    """Service for LLM-based resume analysis"""
    
    def __init__(self):
        self.llm_service_url = settings.LLM_SERVICE_URL
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def analyze_resume(self, resume_text: str, vacancy_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze resume using LLM
        
        Args:
            resume_text: Raw resume text
            vacancy_requirements: Vacancy requirements and criteria
            
        Returns:
            Dict with structured analysis results
        """
        try:
            # Create analysis prompt
            prompt = self._create_analysis_prompt(resume_text, vacancy_requirements)
            
            # Send request to LLM service
            response = await self._call_llm_service(prompt)
            
            # Parse and validate response
            analysis_result = self._parse_llm_response(response)
            
            return {
                "success": True,
                "analysis": analysis_result,
                "raw_response": response
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis": {},
                "raw_response": None
            }
    
    def _create_analysis_prompt(self, resume_text: str, vacancy_requirements: Dict[str, Any]) -> str:
        """Create prompt for LLM analysis"""
        
        # Extract key requirements
        required_skills = vacancy_requirements.get("required_skills", [])
        experience_years = vacancy_requirements.get("experience_years", 0)
        education_level = vacancy_requirements.get("education_level", "")
        job_title = vacancy_requirements.get("title", "Unknown Position")
        
        prompt = f"""
Ты - эксперт по анализу резюме и оценке соответствия кандидатов вакансиям. 

АНАЛИЗИРУЙ РЕЗЮМЕ:
{resume_text}

ТРЕБОВАНИЯ ВАКАНСИИ:
Должность: {job_title}
Требуемый опыт: {experience_years} лет
Образование: {education_level}
Требуемые навыки: {', '.join(required_skills)}

ИНСТРУКЦИИ:
1. Проанализируй резюме и извлеки структурированную информацию
2. Оцени соответствие требованиям вакансии
3. Верни результат в формате JSON

ТРЕБУЕМЫЙ ФОРМАТ ОТВЕТА:
{{
    "personal_info": {{
        "name": "имя кандидата",
        "email": "email",
        "phone": "телефон",
        "location": "местоположение"
    }},
    "experience_analysis": {{
        "total_years": "общий стаж в годах",
        "relevant_years": "релевантный опыт в годах",
        "positions": [
            {{
                "title": "должность",
                "company": "компания",
                "duration": "период работы",
                "relevance_score": "оценка релевантности 0-100"
            }}
        ]
    }},
    "skills_analysis": {{
        "matched_skills": ["найденные требуемые навыки"],
        "missing_skills": ["отсутствующие требуемые навыки"],
        "additional_skills": ["дополнительные навыки"],
        "skill_levels": {{
            "skill_name": "уровень владения (beginner/intermediate/expert)"
        }}
    }},
    "education_analysis": {{
        "level": "уровень образования",
        "relevance": "релевантность образованию 0-100",
        "institution": "учебное заведение"
    }},
    "overall_assessment": {{
        "total_score": "общая оценка 0-100",
        "strengths": ["сильные стороны"],
        "weaknesses": ["слабые стороны"],
        "recommendation": "рекомендация (hire/consider/reject)",
        "confidence": "уверенность в оценке 0-100"
    }}
}}

ВАЖНО: Отвечай ТОЛЬКО в формате JSON, без дополнительного текста.
"""
        
        return prompt
    
    async def _call_llm_service(self, prompt: str) -> str:
        """Call LLM service for analysis"""
        try:
            payload = {
                "prompt": prompt,
                "max_tokens": 2000,
                "temperature": 0.3,
                "system_message": "Ты - эксперт по анализу резюме. Отвечай только в формате JSON."
            }
            
            response = await self.client.post(
                f"{self.llm_service_url}/api/v1/llm/generate",
                json=payload
            )
            
            if response.status_code != 200:
                raise Exception(f"LLM service error: {response.status_code}")
            
            result = response.json()
            return result.get("response", "")
            
        except Exception as e:
            raise Exception(f"Failed to call LLM service: {str(e)}")
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate LLM response"""
        try:
            # Try to extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[json_start:json_end]
            parsed = json.loads(json_str)
            
            # Validate required fields
            required_fields = ["personal_info", "experience_analysis", "skills_analysis", "overall_assessment"]
            for field in required_fields:
                if field not in parsed:
                    parsed[field] = {}
            
            return parsed
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to parse response: {str(e)}")
    
    async def analyze_skills_match(self, resume_skills: List[str], required_skills: List[str]) -> Dict[str, Any]:
        """
        Analyze skills matching using LLM
        
        Args:
            resume_skills: Skills from resume
            required_skills: Required skills for vacancy
            
        Returns:
            Skills matching analysis
        """
        try:
            prompt = f"""
Проанализируй соответствие навыков кандидата требованиям вакансии.

НАВЫКИ КАНДИДАТА:
{', '.join(resume_skills)}

ТРЕБУЕМЫЕ НАВЫКИ:
{', '.join(required_skills)}

Оцени соответствие и верни результат в формате JSON:
{{
    "matched_skills": ["найденные требуемые навыки"],
    "missing_skills": ["отсутствующие требуемые навыки"],
    "skill_similarities": {{
        "resume_skill": "похожий требуемый навык"
    }},
    "match_percentage": "процент соответствия 0-100",
    "critical_missing": ["критически важные отсутствующие навыки"]
}}
"""
            
            response = await self._call_llm_service(prompt)
            result = self._parse_llm_response(response)
            
            return {
                "success": True,
                "skills_analysis": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "skills_analysis": {}
            }
    
    async def analyze_experience_relevance(self, experience_text: str, job_requirements: str) -> Dict[str, Any]:
        """
        Analyze experience relevance using LLM
        
        Args:
            experience_text: Experience section from resume
            job_requirements: Job requirements
            
        Returns:
            Experience relevance analysis
        """
        try:
            prompt = f"""
Проанализируй релевантность опыта работы требованиям вакансии.

ОПЫТ РАБОТЫ:
{experience_text}

ТРЕБОВАНИЯ ВАКАНСИИ:
{job_requirements}

Оцени релевантность и верни результат в формате JSON:
{{
    "relevant_years": "релевантный опыт в годах",
    "relevance_score": "оценка релевантности 0-100",
    "key_achievements": ["ключевые достижения"],
    "relevant_projects": ["релевантные проекты"],
    "gaps": ["пробелы в опыте"],
    "recommendations": ["рекомендации"]
}}
"""
            
            response = await self._call_llm_service(prompt)
            result = self._parse_llm_response(response)
            
            return {
                "success": True,
                "experience_analysis": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "experience_analysis": {}
            }
    
    async def generate_interview_questions(self, resume_analysis: Dict[str, Any], vacancy_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate interview questions based on resume analysis
        
        Args:
            resume_analysis: Analysis results
            vacancy_requirements: Vacancy requirements
            
        Returns:
            Generated interview questions
        """
        try:
            prompt = f"""
Сгенерируй вопросы для интервью на основе анализа резюме.

АНАЛИЗ РЕЗЮМЕ:
{json.dumps(resume_analysis, ensure_ascii=False, indent=2)}

ТРЕБОВАНИЯ ВАКАНСИИ:
{json.dumps(vacancy_requirements, ensure_ascii=False, indent=2)}

Сгенерируй вопросы в формате JSON:
{{
    "technical_questions": [
        {{
            "question": "технический вопрос",
            "category": "категория навыка",
            "difficulty": "сложность (easy/medium/hard)",
            "purpose": "цель вопроса"
        }}
    ],
    "experience_questions": [
        {{
            "question": "вопрос об опыте",
            "focus": "фокус вопроса",
            "expected_answer": "ожидаемый ответ"
        }}
    ],
    "behavioral_questions": [
        {{
            "question": "поведенческий вопрос",
            "competency": "оцениваемая компетенция"
        }}
    ],
    "follow_up_questions": [
        {{
            "question": "уточняющий вопрос",
            "trigger": "когда задавать"
        }}
    ]
}}
"""
            
            response = await self._call_llm_service(prompt)
            result = self._parse_llm_response(response)
            
            return {
                "success": True,
                "questions": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "questions": {}
            }
    
    async def analyze_resume_with_dynamic_skills(
        self, 
        resume_text: str, 
        vacancy_skills: List[VacancySkill],
        vacancy_id: str
    ) -> ResumeSkillsAnalysisResponse:
        """
        Analyze resume using dynamic skills from VacancySkillsExtractor
        
        Args:
            resume_text: Raw resume text
            vacancy_skills: List of skills extracted from vacancy
            vacancy_id: ID of the vacancy
            
        Returns:
            ResumeSkillsAnalysisResponse with detailed skill matching
        """
        try:
            # Create analysis prompt with dynamic skills
            prompt = self._create_dynamic_skills_prompt(resume_text, vacancy_skills)
            
            # Send request to LLM service
            response = await self._call_llm_service(prompt)
            
            # Parse and validate response
            skill_matches = self._parse_skills_analysis_response(response, vacancy_skills)
            
            # Calculate overall metrics
            overall_score = self._calculate_overall_score(skill_matches)
            mandatory_skills_covered = self._count_mandatory_skills_covered(skill_matches)
            total_mandatory_skills = self._count_total_mandatory_skills(vacancy_skills)
            
            return ResumeSkillsAnalysisResponse(
                success=True,
                resume_id="",  # Will be set by caller
                vacancy_id=vacancy_id,
                skill_matches=skill_matches,
                overall_score=overall_score,
                mandatory_skills_covered=mandatory_skills_covered,
                total_mandatory_skills=total_mandatory_skills
            )
            
        except Exception as e:
            return ResumeSkillsAnalysisResponse(
                success=False,
                resume_id="",
                vacancy_id=vacancy_id,
                skill_matches=[],
                overall_score=0.0,
                mandatory_skills_covered=0,
                total_mandatory_skills=0,
                analysis_time=0.0,
                strengths=[],
                weaknesses=[],
                recommendations=[],
                error="Analysis failed"
            )
    
    def _create_dynamic_skills_prompt(self, resume_text: str, vacancy_skills: List[VacancySkill]) -> str:
        """Create prompt for dynamic skills analysis"""
        
        # Format skills for prompt
        skills_info = []
        for skill in vacancy_skills:
            alternatives_text = f" (альтернативы: {', '.join(skill.alternatives)})" if skill.alternatives else ""
            mandatory_text = " [ОБЯЗАТЕЛЬНЫЙ]" if skill.is_mandatory else ""
            skills_info.append(
                f"- {skill.skill_name}{alternatives_text}{mandatory_text}\n"
                f"  Категория: {skill.category}\n"
                f"  Важность: {skill.importance}\n"
                f"  Требуемый уровень: {skill.required_level}\n"
                f"  Описание: {skill.description or 'Не указано'}"
            )
        
        skills_text = "\n".join(skills_info)
        
        prompt = f"""
Ты - эксперт по анализу резюме и оценке соответствия навыков кандидата требованиям вакансии.

АНАЛИЗИРУЙ РЕЗЮМЕ:
{resume_text}

ТРЕБУЕМЫЕ НАВЫКИ ДЛЯ ВАКАНСИИ:
{skills_text}

ИНСТРУКЦИИ:
1. Проанализируй резюме и найди упоминания каждого требуемого навыка
2. Оцени уровень владения каждым навыком (beginner/intermediate/expert)
3. Рассчитай оценку соответствия (0.0-1.0) на основе:
   - Наличия навыка в резюме
   - Уровня владения
   - Соответствия требуемому уровню
   - Важности навыка
4. Предоставь доказательства из резюме
5. Учти альтернативные названия навыков

ВЕРНИ РЕЗУЛЬТАТ В ФОРМАТЕ JSON:
{{
    "skill_matches": [
        {{
            "skill_name": "название навыка",
            "category": "категория",
            "required_level": "требуемый уровень",
            "candidate_level": "уровень кандидата (beginner/intermediate/expert)",
            "match_score": 0.85,
            "confidence": 0.9,
            "evidence": ["доказательства из резюме"],
            "is_mandatory": true/false,
            "importance": 0.8
        }}
    ]
}}

ВАЖНО: 
- Отвечай ТОЛЬКО в формате JSON
- Не добавляй дополнительный текст
- Оценивай объективно на основе содержимого резюме
- Если навык не найден, установи match_score = 0.0
- Учитывай альтернативные названия навыков
"""
        
        return prompt
    
    def _parse_skills_analysis_response(self, response: str, vacancy_skills: List[VacancySkill]) -> List[SkillMatch]:
        """Parse LLM response for skills analysis"""
        try:
            # Try to extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[json_start:json_end]
            parsed = json.loads(json_str)
            
            skill_matches = []
            llm_matches = parsed.get("skill_matches", [])
            
            # Create SkillMatch objects
            for llm_match in llm_matches:
                # Find corresponding vacancy skill
                vacancy_skill = next(
                    (s for s in vacancy_skills if s.skill_name.lower() == llm_match.get("skill_name", "").lower()),
                    None
                )
                
                if vacancy_skill:
                    skill_match = SkillMatch(
                        skill_name=llm_match.get("skill_name", vacancy_skill.skill_name),
                        category=llm_match.get("category", vacancy_skill.category),
                        required_level=llm_match.get("required_level", vacancy_skill.required_level),
                        candidate_level=llm_match.get("candidate_level"),
                        match_score=llm_match.get("match_score", 0.0),
                        confidence=llm_match.get("confidence", 0.5),
                        evidence=llm_match.get("evidence", []),
                        is_mandatory=llm_match.get("is_mandatory", vacancy_skill.is_mandatory),
                        importance=llm_match.get("importance", vacancy_skill.importance)
                    )
                    skill_matches.append(skill_match)
            
            return skill_matches
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to parse response: {str(e)}")
    
    def _calculate_overall_score(self, skill_matches: List[SkillMatch]) -> float:
        """Calculate overall match score"""
        if not skill_matches:
            return 0.0
        
        total_weighted_score = 0.0
        total_weight = 0.0
        
        for match in skill_matches:
            weight = match.importance
            total_weighted_score += match.match_score * weight
            total_weight += weight
        
        return total_weighted_score / total_weight if total_weight > 0 else 0.0
    
    def _count_mandatory_skills_covered(self, skill_matches: List[SkillMatch]) -> int:
        """Count mandatory skills that are covered"""
        return sum(1 for match in skill_matches if match.is_mandatory and match.match_score >= 0.5)
    
    def _count_total_mandatory_skills(self, vacancy_skills: List[VacancySkill]) -> int:
        """Count total mandatory skills"""
        return sum(1 for skill in vacancy_skills if skill.is_mandatory)
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Global instance
llm_analyzer = LLMResumeAnalyzer()
