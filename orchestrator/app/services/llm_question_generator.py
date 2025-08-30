"""
LLM Question Generator Service
"""
import httpx
import json
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from app.models import Vacancy, SessionContext
from app.core.config import settings


class LLMQuestionGenerator:
    """Сервис генерации вопросов с помощью LLM"""
    
    def __init__(self, db: Session):
        self.db = db
        self.llm_service_url = settings.LLM_SERVICE_URL

    async def generate_next_question(
        self, 
        session_id: str, 
        vacancy_id: str,
        previous_answers: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Генерация следующего вопроса на основе требований вакансии и контекста
        
        Args:
            session_id: ID сессии
            vacancy_id: ID вакансии
            previous_answers: Предыдущие ответы кандидата
            
        Returns:
            Сгенерированный вопрос
        """
        try:
            # Получаем информацию о вакансии
            vacancy = self.db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
            if not vacancy:
                raise Exception("Вакансия не найдена")
            
            # Получаем контекст сессии
            session_context = self.db.query(SessionContext).filter(
                SessionContext.session_id == session_id
            ).first()
            
            # Формируем промпт для LLM
            prompt = self._build_question_generation_prompt(
                vacancy, session_context, previous_answers
            )
            
            # Отправляем запрос к LLM
            question_data = await self._call_llm_service(prompt)
            
            return question_data
            
        except Exception as e:
            raise Exception(f"Ошибка генерации вопроса: {str(e)}")

    def _build_question_generation_prompt(
        self, 
        vacancy: Vacancy, 
        session_context: Optional[SessionContext],
        previous_answers: List[Dict[str, Any]] = None
    ) -> str:
        """
        Формирование промпта для генерации вопроса
        """
        prompt = f"""
Ты - опытный HR-специалист, проводящий техническое интервью для позиции {vacancy.title}.

ТРЕБОВАНИЯ К ВАКАНСИИ:
{vacancy.requirements}

ОБЯЗАННОСТИ:
{vacancy.responsibilities}

ОПЫТ РАБОТЫ: {vacancy.experience_required}
УРОВЕНЬ ОБРАЗОВАНИЯ: {vacancy.education_level}

КОНТЕКСТ ПРЕДЫДУЩИХ ОТВЕТОВ:
"""
        
        if previous_answers:
            for i, answer in enumerate(previous_answers, 1):
                prompt += f"""
Вопрос {i}: {answer.get('question_text', 'N/A')}
Ответ кандидата: {answer.get('answer_text', 'N/A')}
Оценка ответа: {answer.get('score', 'N/A')}
Анализ: {answer.get('analysis', 'N/A')}
"""
        
        if session_context and session_context.skill_assessments:
            prompt += f"""
ТЕКУЩИЕ ОЦЕНКИ НАВЫКОВ:
"""
            for skill, data in session_context.skill_assessments.items():
                avg_score = data.get('average_score', 0.0)
                prompt += f"- {skill}: {avg_score:.2f}\n"
        
        if session_context and session_context.negative_responses:
            prompt += f"""
ОТРИЦАТЕЛЬНЫЕ ОТВЕТЫ:
"""
            for skill, responses in session_context.negative_responses.items():
                prompt += f"- {skill}: {len(responses)} отрицательных ответов\n"
        
        prompt += f"""

ИНСТРУКЦИИ:
1. Сгенерируй следующий вопрос для интервью
2. Учитывай предыдущие ответы и оценки навыков
3. Если кандидат показал слабые знания в определенной области - задай уточняющий вопрос или перейди к другой теме
4. Если кандидат показал сильные знания - углубись в эту область
5. Избегай вопросов по темам, на которые кандидат уже дал отрицательные ответы
6. Вопрос должен быть конкретным и практическим
7. Учитывай уровень сложности на основе опыта кандидата

ФОРМАТ ОТВЕТА (JSON):
{{
    "question_text": "Текст вопроса",
    "question_type": "text|audio",
    "max_duration_s": 60,
    "category": "название категории навыков",
    "difficulty_level": "easy|medium|hard",
    "target_skills": ["список целевых навыков"],
    "reasoning": "объяснение, почему выбран этот вопрос",
    "should_terminate": false
}}

Сгенерируй следующий вопрос:
"""
        
        return prompt

    async def _call_llm_service(self, prompt: str) -> Dict[str, Any]:
        """
        Вызов LLM сервиса для генерации вопроса
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.llm_service_url}/generate-question",
                    json={
                        "prompt": prompt,
                        "max_tokens": 500,
                        "temperature": 0.7
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("question_data", {})
                else:
                    raise Exception(f"LLM сервис вернул ошибку: {response.status_code}")
                    
        except Exception as e:
            # Fallback - возвращаем базовый вопрос
            return {
                "question_text": "Расскажите о вашем опыте работы с технологиями, указанными в требованиях к вакансии.",
                "question_type": "text",
                "max_duration_s": 60,
                "category": "general",
                "difficulty_level": "medium",
                "target_skills": ["general_experience"],
                "reasoning": "Базовый вопрос при недоступности LLM",
                "should_terminate": False
            }

    async def analyze_answer_context(
        self, 
        question_text: str, 
        answer_text: str,
        vacancy_requirements: str
    ) -> Dict[str, Any]:
        """
        Анализ контекста ответа с помощью LLM
        """
        try:
            prompt = f"""
Ты - опытный HR-специалист, анализирующий ответ кандидата на техническое интервью.

ВОПРОС: {question_text}
ОТВЕТ КАНДИДАТА: {answer_text}
ТРЕБОВАНИЯ К ВАКАНСИИ: {vacancy_requirements}

ПРОАНАЛИЗИРУЙ ОТВЕТ И ВЕРНИ JSON:
{{
    "score": 0.85,
    "confidence": 0.9,
    "is_negative": false,
    "skill_assessments": {{
        "Python": 0.8,
        "FastAPI": 0.7,
        "Database": 0.6
    }},
    "missing_skills": ["Docker", "Kubernetes"],
    "positive_aspects": ["хорошее понимание основ", "практический опыт"],
    "negative_aspects": ["недостаточно глубокие знания"],
    "recommendations": ["задать уточняющий вопрос по Docker", "перейти к теме микросервисов"],
    "should_skip_related": false,
    "next_question_focus": "практический опыт с Docker"
}}
"""
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.llm_service_url}/analyze-answer",
                    json={
                        "prompt": prompt,
                        "max_tokens": 300,
                        "temperature": 0.3
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("analysis", {})
                else:
                    # Fallback анализ
                    return self._fallback_answer_analysis(answer_text)
                    
        except Exception as e:
            return self._fallback_answer_analysis(answer_text)

    def _fallback_answer_analysis(self, answer_text: str) -> Dict[str, Any]:
        """
        Fallback анализ ответа без LLM
        """
        # Простой анализ на основе ключевых слов
        text_lower = answer_text.lower()
        
        # Определяем негативные паттерны
        negative_patterns = ["не знаю", "не работал", "не знаком", "не использовал"]
        is_negative = any(pattern in text_lower for pattern in negative_patterns)
        
        # Простая оценка на основе длины и содержания
        word_count = len(answer_text.split())
        base_score = min(1.0, word_count / 50.0)  # Больше слов = лучше ответ
        
        if is_negative:
            base_score *= 0.3
        
        return {
            "score": base_score,
            "confidence": 0.5,
            "is_negative": is_negative,
            "skill_assessments": {},
            "missing_skills": [],
            "positive_aspects": ["ответ получен"],
            "negative_aspects": ["недостаточно данных для анализа"],
            "recommendations": ["задать уточняющий вопрос"],
            "should_skip_related": is_negative,
            "next_question_focus": "общие навыки"
        }

    async def should_terminate_interview(
        self, 
        session_context: SessionContext,
        vacancy_requirements: str
    ) -> Dict[str, Any]:
        """
        Определение необходимости завершения интервью
        """
        try:
            if not session_context or not session_context.skill_assessments:
                return {"should_terminate": False, "reason": "Недостаточно данных"}
            
            # Анализируем оценки навыков
            total_skills = len(session_context.skill_assessments)
            low_skills = sum(1 for data in session_context.skill_assessments.values() 
                           if data.get('average_score', 0) < 0.3)
            
            # Если больше 70% навыков имеют низкую оценку
            if total_skills > 0 and (low_skills / total_skills) > 0.7:
                return {
                    "should_terminate": True,
                    "reason": "Кандидат показал недостаточный уровень знаний по большинству требуемых навыков"
                }
            
            # Проверяем критические навыки
            critical_skills = ["Python", "Programming", "Development"]
            critical_failures = 0
            
            for skill in critical_skills:
                if skill in session_context.negative_responses:
                    critical_failures += 1
            
            if critical_failures >= 2:
                return {
                    "should_terminate": True,
                    "reason": "Кандидат отрицает знание критически важных навыков"
                }
            
            return {"should_terminate": False, "reason": "Интервью может продолжаться"}
            
        except Exception as e:
            return {"should_terminate": False, "reason": f"Ошибка анализа: {str(e)}"}
