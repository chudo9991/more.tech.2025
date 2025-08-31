"""
Contextual Question Generator Service
"""
import json
import uuid
import httpx
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models import (
    ContextualQuestion, Session, ScenarioNode, Resume, 
    SessionContext, Vacancy, ResumeSkill
)
from app.schemas.contextual_question import (
    ContextualQuestionCreate, ContextualQuestionResponse
)
from app.services.vacancy_skills_extractor import VacancySkillsExtractor
from app.services.contextual_question_validator import ContextualQuestionValidator
from app.core.config import settings


class ContextualQuestionGenerator:
    """
    Генерирует индивидуальные вопросы на основе:
    - Базовой ноды сценария
    - Резюме кандидата
    - Предыдущих ответов
    - Навыков вакансии
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.llm_service_url = settings.LLM_SERVICE_URL
        self.vacancy_skills_extractor = VacancySkillsExtractor()
        self.validator = ContextualQuestionValidator(db)
    
    async def generate_contextual_questions(
        self,
        session_id: str,
        scenario_node_id: str,
        max_questions: int = 3
    ) -> List[ContextualQuestionResponse]:
        """
        Генерирует до 3 индивидуальных вопросов для ноды
        
        Args:
            session_id: ID сессии интервью
            scenario_node_id: ID ноды сценария
            max_questions: Максимальное количество вопросов
            
        Returns:
            Список сгенерированных контекстных вопросов
        """
        try:
            # Получаем данные сессии
            session = self.db.query(Session).filter(Session.id == session_id).first()
            if not session:
                raise Exception(f"Сессия {session_id} не найдена")
            
            # Получаем ноду сценария
            scenario_node = self.db.query(ScenarioNode).filter(
                ScenarioNode.id == scenario_node_id
            ).first()
            if not scenario_node:
                raise Exception(f"Нода сценария {scenario_node_id} не найдена")
            
            # Получаем вакансию
            vacancy = self.db.query(Vacancy).filter(Vacancy.id == session.vacancy_id).first()
            if not vacancy:
                raise Exception(f"Вакансия для сессии {session_id} не найдена")
            
            # Получаем резюме кандидата (если есть)
            resume = None
            if session.candidate_id:
                resume = self.db.query(Resume).filter(
                    Resume.candidate_id == session.candidate_id
                ).first()
            
            # Получаем контекст сессии
            session_context = self.db.query(SessionContext).filter(
                SessionContext.session_id == session_id
            ).first()
            
            # Извлекаем навыки из вакансии
            vacancy_skills = await self.vacancy_skills_extractor.extract_skills_from_vacancy(
                vacancy=vacancy,
                force_reload=False
            )
            
            # Анализируем резюме для ноды
            resume_context = self.analyze_resume_for_node(
                resume=resume,
                scenario_node=scenario_node,
                vacancy_skills=vacancy_skills.skills if vacancy_skills else []
            )
            
            # Анализируем предыдущие ответы
            answer_context = self.analyze_previous_answers(session_context)
            
            # Генерируем вопросы через LLM
            questions_data = await self._generate_questions_with_llm(
                node_name=scenario_node.node_config.get("label", "Unknown") if scenario_node.node_config else "Unknown",
                resume_context=resume_context,
                answer_context=answer_context,
                vacancy_skills=vacancy_skills.skills if vacancy_skills else [],
                max_questions=max_questions
            )
            
            # Валидируем сгенерированные вопросы
            questions_texts = [q["question"] for q in questions_data]
            valid_questions, rejection_reasons = self.validator.validate_questions(
                questions_texts, scenario_node, resume_context
            )
            
            # Если валидных вопросов недостаточно, добавляем fallback
            if len(valid_questions) < max_questions:
                fallback_questions = self._get_fallback_questions(
                    scenario_node.node_config.get("label", "Unknown") if scenario_node.node_config else "Unknown",
                    max_questions - len(valid_questions)
                )
                valid_questions.extend([q["question"] for q in fallback_questions])
            
            # Обновляем questions_data только валидными вопросами
            questions_data = [
                q for q in questions_data 
                if q["question"] in valid_questions
            ]
            
            # Создаем записи в базе данных
            contextual_questions = []
            for question_data in questions_data:
                contextual_question = ContextualQuestion(
                    id=f"CONTEXT_Q_{uuid.uuid4().hex[:8].upper()}",
                    session_id=session_id,
                    scenario_node_id=scenario_node_id,
                    question_text=question_data["question"],
                    question_type=question_data["type"],
                    context_source={"source": question_data.get("context", "fallback")}
                )
                
                self.db.add(contextual_question)
                contextual_questions.append(contextual_question)
            
            # Сохраняем в базу
            self.db.commit()
            
            # Обновляем контекст сессии
            self._update_session_context(session_context, scenario_node_id, questions_data)
            
            # Возвращаем ответы
            return [
                ContextualQuestionResponse(
                    id=cq.id,
                    session_id=cq.session_id,
                    scenario_node_id=cq.scenario_node_id,
                    question_text=cq.question_text,
                    question_type=cq.question_type,
                    context_source=cq.context_source,
                    generated_at=cq.generated_at,
                    is_used=cq.is_used,
                    used_at=cq.used_at,
                    created_at=cq.created_at,
                    updated_at=cq.updated_at
                )
                for cq in contextual_questions
            ]
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Ошибка генерации контекстных вопросов: {str(e)}")
    
    def analyze_resume_for_node(
        self,
        resume: Optional[Resume],
        scenario_node: ScenarioNode,
        vacancy_skills: List[Any]
    ) -> Dict[str, Any]:
        """
        Анализирует резюме в контексте конкретной ноды
        
        Args:
            resume: Резюме кандидата
            scenario_node: Нода сценария
            vacancy_skills: Навыки вакансии
            
        Returns:
            Контекст резюме для ноды
        """
        if not resume:
            return {"has_resume": False, "message": "Резюме не найдено"}
        
        # Получаем навыки из резюме
        resume_skills = self.db.query(ResumeSkill).filter(
            ResumeSkill.resume_id == resume.id
        ).all()
        
        # Определяем навыки, связанные с нодой
        node_name = scenario_node.node_config.get("label", "") if scenario_node.node_config else ""
        node_skills = self._extract_skills_from_node_name(node_name, vacancy_skills)
        
        # Находим соответствующий опыт в резюме
        relevant_experience = self._find_relevant_experience(
            resume_skills, node_skills, resume
        )
        
        # Определяем уровень кандидата
        candidate_level = self._determine_candidate_level(resume_skills, node_skills)
        
        return {
            "has_resume": True,
            "resume_id": resume.id,
            "node_name": node_name,
            "relevant_skills": [skill.skill_name for skill in relevant_experience],
            "candidate_level": candidate_level,
            "experience_summary": self._summarize_experience(resume, relevant_experience),
            "projects": self._extract_projects(resume),
            "total_experience_years": self._calculate_total_experience(resume)
        }
    
    def analyze_previous_answers(self, session_context: Optional[SessionContext]) -> Dict[str, Any]:
        """
        Анализирует предыдущие ответы кандидата
        
        Args:
            session_context: Контекст сессии
            
        Returns:
            Контекст предыдущих ответов
        """
        if not session_context:
            return {"has_previous_answers": False}
        
        return {
            "has_previous_answers": True,
            "skill_assessments": session_context.skill_assessments or {},
            "negative_responses": session_context.negative_responses or {},
            "current_path": session_context.current_path or [],
            "current_node_id": session_context.current_node_id
        }
    
    async def _generate_questions_with_llm(
        self,
        node_name: str,
        resume_context: Dict[str, Any],
        answer_context: Dict[str, Any],
        vacancy_skills: List[Any],
        max_questions: int
    ) -> List[Dict[str, Any]]:
        """
        Генерирует вопросы через LLM
        
        Args:
            node_name: Название ноды
            resume_context: Контекст резюме
            answer_context: Контекст ответов
            vacancy_skills: Навыки вакансии
            max_questions: Максимальное количество вопросов
            
        Returns:
            Список сгенерированных вопросов
        """
        prompt = self._build_contextual_question_prompt(
            node_name, resume_context, answer_context, vacancy_skills, max_questions
        )
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.llm_service_url}/api/v1/llm/generate",
                    json={
                        "prompt": prompt,
                        "max_tokens": 1500,
                        "temperature": 0.7
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return self._parse_llm_response(result.get("response", ""))
                else:
                    raise Exception(f"LLM сервис вернул ошибку: {response.status_code}")
                    
        except Exception as e:
            print(f"Ошибка вызова LLM: {str(e)}")
            # Возвращаем fallback вопросы
            return self._get_fallback_questions(node_name, max_questions)
    
    def _build_contextual_question_prompt(
        self,
        node_name: str,
        resume_context: Dict[str, Any],
        answer_context: Dict[str, Any],
        vacancy_skills: List[Any],
        max_questions: int
    ) -> str:
        """
        Строит промпт для генерации контекстных вопросов
        """
        skills_text = ""
        if vacancy_skills:
            skills_text = "\n".join([
                f"- {skill.skill_name} ({skill.category}): {skill.required_level} уровень"
                for skill in vacancy_skills
            ])
        
        prompt = f"""
Ты - опытный HR-специалист, проводящий техническое интервью. Сгенерируй {max_questions} индивидуальных вопроса для ноды "{node_name}" на основе контекста кандидата.

ВАЖНО: Всегда отвечай на РУССКОМ ЯЗЫКЕ. Все вопросы, комментарии и анализ должны быть на русском языке.

КОНТЕКСТ РЕЗЮМЕ:
{json.dumps(resume_context, ensure_ascii=False, indent=2)}

ПРЕДЫДУЩИЕ ОТВЕТЫ:
{json.dumps(answer_context, ensure_ascii=False, indent=2)}

ТРЕБУЕМЫЕ НАВЫКИ:
{skills_text}

ТРЕБОВАНИЯ К ВОПРОСАМ:
1. Вопросы должны быть специфичными для опыта кандидата
2. Избегай общих вопросов типа "расскажи о FastAPI"
3. Фокусируйся на конкретных проектах и решениях
4. Учитывай уровень кандидата (junior/middle/senior)
5. Вопросы должны быть практическими и детальными
6. Учитывай предыдущие ответы и оценки навыков

ТИПЫ ВОПРОСОВ:
- experience: вопросы об опыте работы
- project: вопросы о конкретных проектах
- technical: технические вопросы

ФОРМАТ ОТВЕТА (JSON):
{{
    "questions": [
        {{
            "question": "конкретный вопрос на русском языке",
            "type": "experience/project/technical",
            "context": "обоснование вопроса"
        }}
    ]
}}

ВАЖНО: Отвечай ТОЛЬКО в формате JSON.
"""
        
        return prompt
    
    def _parse_llm_response(self, response: str) -> List[Dict[str, Any]]:
        """
        Парсит ответ LLM
        """
        try:
            # Ищем JSON в ответе
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise Exception("JSON не найден в ответе")
            
            json_str = response[json_start:json_end]
            data = json.loads(json_str)
            
            questions = data.get("questions", [])
            if not questions:
                raise Exception("Вопросы не найдены в ответе")
            
            return questions
            
        except Exception as e:
            print(f"Ошибка парсинга ответа LLM: {str(e)}")
            return self._get_fallback_questions("Unknown", 3)
    
    def _get_fallback_questions(self, node_name: str, max_questions: int) -> List[Dict[str, Any]]:
        """
        Возвращает стандартные вопросы если LLM не смог сгенерировать
        """
        fallback_questions = [
            {
                "question": f"Расскажите о вашем опыте работы с технологиями, связанными с {node_name}",
                "type": "experience",
                "context": "fallback question"
            },
            {
                "question": f"Опишите конкретный проект, где вы использовали {node_name}",
                "type": "project", 
                "context": "fallback question"
            },
            {
                "question": f"Какие сложности вы встречали при работе с {node_name}?",
                "type": "technical",
                "context": "fallback question"
            }
        ]
        
        return fallback_questions[:max_questions]
    
    def _extract_skills_from_node_name(self, node_name: str, vacancy_skills: List[Any]) -> List[str]:
        """
        Извлекает навыки из названия ноды
        """
        # Простая логика извлечения навыков из названия ноды
        node_name_lower = node_name.lower()
        relevant_skills = []
        
        for skill in vacancy_skills:
            if skill.skill_name.lower() in node_name_lower:
                relevant_skills.append(skill.skill_name)
        
        return relevant_skills
    
    def _find_relevant_experience(
        self, 
        resume_skills: List[ResumeSkill], 
        node_skills: List[str],
        resume: Resume
    ) -> List[ResumeSkill]:
        """
        Находит соответствующий опыт в резюме
        """
        relevant_skills = []
        
        for resume_skill in resume_skills:
            for node_skill in node_skills:
                if node_skill.lower() in resume_skill.skill_name.lower():
                    relevant_skills.append(resume_skill)
                    break
        
        return relevant_skills
    
    def _determine_candidate_level(
        self, 
        resume_skills: List[ResumeSkill], 
        node_skills: List[str]
    ) -> str:
        """
        Определяет уровень кандидата
        """
        if not resume_skills:
            return "unknown"
        
        # Простая логика определения уровня
        total_skills = len(resume_skills)
        relevant_skills = len([s for s in resume_skills if any(
            node_skill.lower() in s.skill_name.lower() for node_skill in node_skills
        )])
        
        if relevant_skills >= 3:
            return "expert"
        elif relevant_skills >= 1:
            return "intermediate"
        else:
            return "beginner"
    
    def _summarize_experience(self, resume: Resume, relevant_skills: List[ResumeSkill]) -> str:
        """
        Суммирует опыт кандидата
        """
        if not relevant_skills:
            return "Нет соответствующего опыта"
        
        skill_names = [skill.skill_name for skill in relevant_skills]
        return f"Опыт работы с: {', '.join(skill_names)}"
    
    def _extract_projects(self, resume: Resume) -> List[str]:
        """
        Извлекает проекты из резюме
        """
        # Упрощенная логика извлечения проектов
        # В реальной системе здесь был бы более сложный анализ
        return ["Проект 1", "Проект 2"]  # Заглушка
    
    def _calculate_total_experience(self, resume: Resume) -> int:
        """
        Рассчитывает общий опыт работы
        """
        # Упрощенная логика расчета опыта
        return 3  # Заглушка
    
    def _update_session_context(
        self, 
        session_context: Optional[SessionContext], 
        scenario_node_id: str, 
        questions_data: List[Dict[str, Any]]
    ):
        """
        Обновляет контекст сессии с информацией о контекстных вопросах
        """
        if not session_context:
            return
        
        if not session_context.contextual_questions:
            session_context.contextual_questions = {}
        
        questions_texts = [q["question"] for q in questions_data]
        
        session_context.contextual_questions[scenario_node_id] = {
            "generated_questions": questions_texts,
            "asked_questions": [],
            "remaining_questions": questions_texts.copy()
        }
        
        self.db.commit()
    
    def get_contextual_questions_for_node(
        self,
        session_id: str,
        scenario_node_id: str
    ) -> List[ContextualQuestionResponse]:
        """
        Получает контекстные вопросы для ноды
        
        Args:
            session_id: ID сессии
            scenario_node_id: ID ноды сценария
            
        Returns:
            Список контекстных вопросов
        """
        contextual_questions = self.db.query(ContextualQuestion).filter(
            and_(
                ContextualQuestion.session_id == session_id,
                ContextualQuestion.scenario_node_id == scenario_node_id
            )
        ).all()
        
        return [
            ContextualQuestionResponse(
                id=cq.id,
                session_id=cq.session_id,
                scenario_node_id=cq.scenario_node_id,
                question_text=cq.question_text,
                question_type=cq.question_type,
                context_source=cq.context_source,
                generated_at=cq.generated_at,
                is_used=cq.is_used,
                used_at=cq.used_at,
                created_at=cq.created_at,
                updated_at=cq.updated_at
            )
            for cq in contextual_questions
        ]
    
    def get_next_contextual_question(
        self,
        session_id: str,
        scenario_node_id: str
    ) -> Optional[ContextualQuestionResponse]:
        """
        Получает следующий неиспользованный контекстный вопрос
        
        Args:
            session_id: ID сессии
            scenario_node_id: ID ноды сценария
            
        Returns:
            Следующий контекстный вопрос или None
        """
        contextual_question = self.db.query(ContextualQuestion).filter(
            and_(
                ContextualQuestion.session_id == session_id,
                ContextualQuestion.scenario_node_id == scenario_node_id,
                ContextualQuestion.is_used == False
            )
        ).first()
        
        if not contextual_question:
            return None
        
        return ContextualQuestionResponse(
            id=contextual_question.id,
            session_id=contextual_question.session_id,
            scenario_node_id=contextual_question.scenario_node_id,
            question_text=contextual_question.question_text,
            question_type=contextual_question.question_type,
            context_source=contextual_question.context_source,
            generated_at=contextual_question.generated_at,
            is_used=contextual_question.is_used,
            used_at=contextual_question.used_at,
            created_at=contextual_question.created_at,
            updated_at=contextual_question.updated_at
        )
    
    def mark_question_as_used(
        self,
        question_id: str
    ) -> bool:
        """
        Отмечает вопрос как использованный
        
        Args:
            question_id: ID вопроса
            
        Returns:
            True если успешно, False если ошибка
        """
        try:
            from datetime import datetime
            
            contextual_question = self.db.query(ContextualQuestion).filter(
                ContextualQuestion.id == question_id
            ).first()
            
            if not contextual_question:
                return False
            
            contextual_question.is_used = True
            contextual_question.used_at = datetime.utcnow()
            
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            print(f"Ошибка отметки вопроса как использованного: {str(e)}")
            return False
    
    def has_contextual_questions(
        self,
        session_id: str,
        scenario_node_id: str
    ) -> bool:
        """
        Проверяет, есть ли контекстные вопросы для ноды
        
        Args:
            session_id: ID сессии
            scenario_node_id: ID ноды сценария
            
        Returns:
            True если есть неиспользованные вопросы
        """
        count = self.db.query(ContextualQuestion).filter(
            and_(
                ContextualQuestion.session_id == session_id,
                ContextualQuestion.scenario_node_id == scenario_node_id,
                ContextualQuestion.is_used == False
            )
        ).count()
        
        return count > 0

    def get_contextual_questions_status(
        self,
        session_id: str,
        scenario_node_id: str
    ) -> Dict[str, Any]:
        """
        Получает статус контекстных вопросов для ноды
        
        Args:
            session_id: ID сессии
            scenario_node_id: ID ноды сценария
            
        Returns:
            Статус контекстных вопросов
        """
        try:
            all_questions = self.get_contextual_questions_for_node(session_id, scenario_node_id)
            
            used_questions = [q for q in all_questions if q.is_used]
            remaining_questions = [q for q in all_questions if not q.is_used]
            
            return {
                "total_questions": len(all_questions),
                "used_questions": len(used_questions),
                "remaining_questions": len(remaining_questions),
                "has_questions": len(all_questions) > 0,
                "has_unused_questions": len(remaining_questions) > 0,
                "node_id": scenario_node_id
            }
            
        except Exception as e:
            return {
                "total_questions": 0,
                "used_questions": 0,
                "remaining_questions": 0,
                "has_questions": False,
                "has_unused_questions": False,
                "error": str(e)
            }
