"""
Negative response analyzer service
"""
import re
from typing import Dict, List, Any, Tuple
from sqlalchemy.orm import Session
from app.models import SessionContext, Criteria


class NegativeResponseAnalyzer:
    """Анализатор негативных ответов для умного сценария"""
    
    def __init__(self, db: Session):
        self.db = db
        
        # Паттерны для определения негативных ответов
        self.negative_patterns = [
            r'\bне\s+знаю\b',
            r'\bне\s+работал\b',
            r'\bне\s+знаком\b',
            r'\bне\s+использовал\b',
            r'\bне\s+изучал\b',
            r'\bне\s+имею\s+опыта\b',
            r'\bне\s+понимаю\b',
            r'\bне\s+умею\b',
            r'\bне\s+могу\b',
            r'\bне\s+слышал\b',
            r'\bне\s+встречал\b',
            r'\bне\s+сталкивался\b',
            r'\bне\s+применял\b',
            r'\bне\s+практиковал\b',
            r'\bне\s+изучал\b',
            r'\bне\s+знаком\s+с\b',
            r'\bне\s+работал\s+с\b',
            r'\bне\s+использовал\s+в\s+практике\b',
            r'\bне\s+имею\s+практического\s+опыта\b',
            r'\bне\s+могу\s+ответить\b',
            r'\bне\s+знаю\s+как\b',
            r'\bне\s+понимаю\s+как\b',
            r'\bне\s+уверен\b',
            r'\bсомневаюсь\b',
            r'\bне\s+помню\b',
            r'\bзабыл\b',
            r'\bне\s+могу\s+вспомнить\b'
        ]
        
        # Паттерны для определения уровня уверенности
        self.confidence_patterns = {
            'high': [
                r'\bточно\b',
                r'\bопределенно\b',
                r'\bконечно\b',
                r'\bбезусловно\b',
                r'\bуверен\b',
                r'\bзнаю\b',
                r'\bработал\b',
                r'\bиспользовал\b',
                r'\bпрактиковал\b',
                r'\bизучал\b',
                r'\bзнаком\b',
                r'\bимею\s+опыт\b',
                r'\bмогу\s+объяснить\b',
                r'\bпонимаю\b',
                r'\bумею\b'
            ],
            'medium': [
                r'\bвроде\b',
                r'\bкажется\b',
                r'\bвозможно\b',
                r'\bнаверное\b',
                r'\bдумаю\b',
                r'\bполагаю\b',
                r'\bпредполагаю\b',
                r'\bмогу\s+быть\b',
                r'\bскорее\s+всего\b',
                r'\bв\s+принципе\b',
                r'\bв\s+общем\b',
                r'\bв\s+целом\b'
            ],
            'low': [
                r'\bне\s+уверен\b',
                r'\bсомневаюсь\b',
                r'\bне\s+знаю\b',
                r'\bзабыл\b',
                r'\bне\s+помню\b',
                r'\bне\s+могу\s+вспомнить\b',
                r'\bне\s+понимаю\b',
                r'\bне\s+умею\b',
                r'\bне\s+могу\b'
            ]
        }
        
        # Маппинг навыков для определения связанных вопросов
        self.skill_mapping = {
            'FASTAPI': ['Python', 'Async', 'Web Development', 'API Development'],
            'PYTHON': ['FastAPI', 'Django', 'Flask', 'Async Programming'],
            'DATABASE': ['SQL', 'PostgreSQL', 'MySQL', 'ORM', 'Migrations'],
            'TESTING': ['Unit Tests', 'Integration Tests', 'TDD', 'BDD'],
            'MICROSERVICES': ['Docker', 'Kubernetes', 'Service Communication', 'API Gateway'],
            'DEPLOYMENT': ['CI/CD', 'Docker', 'Kubernetes', 'Cloud Platforms'],
            'ASYNC': ['FastAPI', 'asyncio', 'Concurrent Programming', 'Performance'],
            'SQL': ['Database Design', 'Query Optimization', 'Indexing', 'Transactions']
        }

    def analyze_negative_patterns(self, text: str) -> Dict[str, Any]:
        """
        Анализ текста на наличие отрицательных паттернов
        
        Args:
            text: Текст ответа кандидата
            
        Returns:
            Dict с результатами анализа
        """
        if not text:
            return {
                'is_negative': False,
                'confidence_level': 'unknown',
                'negative_patterns_found': [],
                'confidence_score': 0.0
            }
        
        text_lower = text.lower()
        
        # Поиск негативных паттернов
        negative_patterns_found = []
        for pattern in self.negative_patterns:
            if re.search(pattern, text_lower):
                negative_patterns_found.append(pattern)
        
        # Определение уровня уверенности
        confidence_scores = {'high': 0, 'medium': 0, 'low': 0}
        
        for level, patterns in self.confidence_patterns.items():
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                confidence_scores[level] += matches
        
        # Определение доминирующего уровня уверенности
        max_score = max(confidence_scores.values())
        if max_score == 0:
            confidence_level = 'unknown'
            confidence_score = 0.0
        else:
            if confidence_scores['high'] > confidence_scores['low']:
                confidence_level = 'high'
                confidence_score = min(1.0, confidence_scores['high'] / 10.0)
            elif confidence_scores['low'] > confidence_scores['high']:
                confidence_level = 'low'
                confidence_score = max(0.0, 1.0 - (confidence_scores['low'] / 10.0))
            else:
                confidence_level = 'medium'
                confidence_score = 0.5
        
        return {
            'is_negative': len(negative_patterns_found) > 0,
            'confidence_level': confidence_level,
            'negative_patterns_found': negative_patterns_found,
            'confidence_score': confidence_score,
            'text_length': len(text),
            'word_count': len(text.split())
        }

    def detect_skill_gaps(self, text: str, required_skills: List[str]) -> List[str]:
        """
        Определение недостающих навыков на основе ответа
        
        Args:
            text: Текст ответа
            required_skills: Список требуемых навыков
            
        Returns:
            Список недостающих навыков
        """
        if not text or not required_skills:
            return []
        
        text_lower = text.lower()
        missing_skills = []
        
        for skill in required_skills:
            skill_lower = skill.lower()
            
            # Проверяем наличие упоминания навыка
            skill_mentioned = skill_lower in text_lower
            
            # Проверяем наличие негативных паттернов для этого навыка
            skill_negative = False
            for pattern in self.negative_patterns:
                if re.search(pattern, text_lower):
                    # Проверяем, относится ли негативный ответ к данному навыку
                    # Ищем контекст вокруг негативного паттерна
                    matches = re.finditer(pattern, text_lower)
                    for match in matches:
                        start = max(0, match.start() - 50)
                        end = min(len(text_lower), match.end() + 50)
                        context = text_lower[start:end]
                        
                        if skill_lower in context:
                            skill_negative = True
                            break
                    if skill_negative:
                        break
            
            # Если навык не упомянут или упомянут негативно
            if not skill_mentioned or skill_negative:
                missing_skills.append(skill)
        
        return missing_skills

    def extract_confidence_level(self, text: str) -> float:
        """
        Извлечение уровня уверенности из ответа
        
        Args:
            text: Текст ответа
            
        Returns:
            Уровень уверенности от 0.0 до 1.0
        """
        analysis = self.analyze_negative_patterns(text)
        return analysis['confidence_score']

    def should_skip_related_questions(self, skill_name: str, session_id: str) -> bool:
        """
        Определение необходимости пропуска связанных вопросов
        
        Args:
            skill_name: Название навыка
            session_id: ID сессии
            
        Returns:
            True если нужно пропустить связанные вопросы
        """
        # Получаем контекст сессии
        session_context = self.db.query(SessionContext).filter(
            SessionContext.session_id == session_id
        ).first()
        
        if not session_context or not session_context.negative_responses:
            return False
        
        # Проверяем, есть ли негативные ответы по данному навыку
        negative_responses = session_context.negative_responses
        
        # Прямая проверка навыка
        if skill_name in negative_responses:
            return True
        
        # Проверка связанных навыков
        related_skills = self.skill_mapping.get(skill_name, [])
        for related_skill in related_skills:
            if related_skill in negative_responses:
                return True
        
        return False

    def update_session_context(self, session_id: str, question_id: str, answer_text: str, answer_score: float) -> Dict[str, Any]:
        """
        Обновление контекста сессии на основе ответа
        
        Args:
            session_id: ID сессии
            question_id: ID вопроса
            answer_text: Текст ответа
            answer_score: Оценка ответа
            
        Returns:
            Обновленный контекст
        """
        # Получаем или создаем контекст сессии
        session_context = self.db.query(SessionContext).filter(
            SessionContext.session_id == session_id
        ).first()
        
        if not session_context:
            session_context = SessionContext(
                id=f"ctx_{session_id}",
                session_id=session_id,
                skill_assessments={},
                negative_responses={},
                current_path=[],
                context_data={}
            )
            self.db.add(session_context)
        
        # Анализируем ответ
        analysis = self.analyze_negative_patterns(answer_text)
        
        # Обновляем оценки навыков
        if not session_context.skill_assessments:
            session_context.skill_assessments = {}
        
        # Получаем критерии для вопроса
        from app.models import QuestionCriterion, Criteria
        criteria_data = self.db.query(Criteria, QuestionCriterion).join(
            QuestionCriterion, Criteria.id == QuestionCriterion.criterion_id
        ).filter(
            QuestionCriterion.question_id == question_id
        ).all()
        
        # Обновляем оценки по критериям
        for criteria, qc in criteria_data:
            criteria_name = criteria.name
            weight = float(qc.weight)
            
            # Рассчитываем взвешенную оценку
            weighted_score = answer_score * weight
            
            if criteria_name not in session_context.skill_assessments:
                session_context.skill_assessments[criteria_name] = {
                    'total_score': 0.0,
                    'count': 0,
                    'average_score': 0.0,
                    'last_score': 0.0
                }
            
            skill_data = session_context.skill_assessments[criteria_name]
            skill_data['total_score'] += weighted_score
            skill_data['count'] += 1
            skill_data['average_score'] = skill_data['total_score'] / skill_data['count']
            skill_data['last_score'] = weighted_score
        
        # Обновляем негативные ответы
        if not session_context.negative_responses:
            session_context.negative_responses = {}
        
        if analysis['is_negative']:
            # Определяем, к каким навыкам относится негативный ответ
            for criteria, qc in criteria_data:
                criteria_name = criteria.name
                if criteria_name not in session_context.negative_responses:
                    session_context.negative_responses[criteria_name] = []
                
                session_context.negative_responses[criteria_name].append({
                    'question_id': question_id,
                    'answer_text': answer_text,
                    'patterns_found': analysis['negative_patterns_found'],
                    'confidence_level': analysis['confidence_level']
                })
        
        # Обновляем путь
        if not session_context.current_path:
            session_context.current_path = []
        
        session_context.current_path.append({
            'question_id': question_id,
            'answer_score': answer_score,
            'is_negative': analysis['is_negative'],
            'confidence_level': analysis['confidence_level'],
            'timestamp': session_context.updated_at.isoformat() if session_context.updated_at else None
        })
        
        # Обновляем контекстные вопросы в SessionContext
        self._update_contextual_questions_context(session_context, question_id, answer_text, answer_score)
        
        # Если это был контекстный вопрос, обновляем его статус
        from app.models import ContextualQuestion
        contextual_question = self.db.query(ContextualQuestion).filter(
            ContextualQuestion.id == question_id
        ).first()
        
        if contextual_question:
            # Отмечаем контекстный вопрос как использованный
            contextual_question.is_used = True
            from datetime import datetime
            contextual_question.used_at = datetime.utcnow()
        
        self.db.commit()
        
        return {
            'skill_assessments': session_context.skill_assessments,
            'negative_responses': session_context.negative_responses,
            'current_path': session_context.current_path,
            'analysis': analysis
        }

    def _update_contextual_questions_context(
        self,
        session_context: SessionContext,
        question_id: str,
        answer_text: str,
        answer_score: float
    ):
        """
        Обновляет контекст контекстных вопросов в SessionContext
        
        Args:
            session_context: Контекст сессии
            question_id: ID вопроса
            answer_text: Текст ответа
            answer_score: Оценка ответа
        """
        try:
            # Проверяем, является ли вопрос контекстным
            from app.models import ContextualQuestion
            contextual_question = self.db.query(ContextualQuestion).filter(
                ContextualQuestion.id == question_id
            ).first()
            
            if contextual_question:
                # Если это контекстный вопрос, обновляем контекст
                if not session_context.contextual_questions:
                    session_context.contextual_questions = {}
                
                node_id = contextual_question.scenario_node_id
                
                if node_id not in session_context.contextual_questions:
                    session_context.contextual_questions[node_id] = {
                        "generated_questions": [],
                        "asked_questions": [],
                        "remaining_questions": []
                    }
                
                # Добавляем вопрос в список использованных
                if contextual_question.question_text not in session_context.contextual_questions[node_id]["asked_questions"]:
                    session_context.contextual_questions[node_id]["asked_questions"].append(
                        contextual_question.question_text
                    )
                
                # Удаляем из списка оставшихся
                if contextual_question.question_text in session_context.contextual_questions[node_id]["remaining_questions"]:
                    session_context.contextual_questions[node_id]["remaining_questions"].remove(
                        contextual_question.question_text
                    )
                
                # Добавляем информацию об ответе
                if "answers" not in session_context.contextual_questions[node_id]:
                    session_context.contextual_questions[node_id]["answers"] = []
                
                session_context.contextual_questions[node_id]["answers"].append({
                    "question_id": question_id,
                    "question_text": contextual_question.question_text,
                    "answer_text": answer_text,
                    "answer_score": answer_score,
                    "timestamp": session_context.updated_at.isoformat() if session_context.updated_at else None
                })
                
        except Exception as e:
            print(f"Ошибка обновления контекста контекстных вопросов: {str(e)}")
