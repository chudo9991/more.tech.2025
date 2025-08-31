"""
Smart scenario navigation service
"""
import json
from typing import Dict, List, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models import (
    SessionContext, InterviewScenario, ScenarioNode, 
    ScenarioTransition, Session as SessionModel, Question
)
from app.services.negative_response_analyzer import NegativeResponseAnalyzer
from app.services.contextual_question_generator import ContextualQuestionGenerator


class ScenarioNavigationService:
    """Сервис умной навигации по сценарию интервью"""
    
    def __init__(self, db: Session):
        self.db = db
        self.negative_analyzer = NegativeResponseAnalyzer(db)
        self.contextual_generator = ContextualQuestionGenerator(db)

    def get_scenario_for_vacancy(self, vacancy_id: str) -> Optional[InterviewScenario]:
        """
        Получение активного сценария для вакансии
        
        Args:
            vacancy_id: ID вакансии
            
        Returns:
            Активный сценарий или None
        """
        return self.db.query(InterviewScenario).filter(
            and_(
                InterviewScenario.vacancy_id == vacancy_id,
                InterviewScenario.is_active == True
            )
        ).first()

    def get_session_context(self, session_id: str) -> Optional[SessionContext]:
        """
        Получение контекста сессии
        
        Args:
            session_id: ID сессии
            
        Returns:
            Контекст сессии или None
        """
        return self.db.query(SessionContext).filter(
            SessionContext.session_id == session_id
        ).first()

    def get_next_question(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает следующий вопрос (базовый или контекстный)
        Логика:
        1. Проверяем есть ли неиспользованные контекстные вопросы для текущей ноды
        2. Если есть - возвращаем следующий контекстный вопрос
        3. Если нет - возвращаем базовый вопрос из сценария
        4. Если базовых вопросов нет - завершаем интервью
        
        Args:
            session_id: ID сессии
            
        Returns:
            Информация о следующем вопросе или None
        """
        # Получаем сессию
        session = self.db.query(SessionModel).filter(
            SessionModel.id == session_id
        ).first()
        
        if not session:
            return None
        
        # Получаем контекст сессии
        session_context = self.get_session_context(session_id)
        
        # Если нет контекста, инициализируем его
        if not session_context:
            session_context = self._initialize_session_context(session_id, session.vacancy_id)
        
        # Получаем текущий узел
        current_node = None
        if session_context.current_node_id:
            current_node = self.db.query(ScenarioNode).filter(
                ScenarioNode.id == session_context.current_node_id
            ).first()
        
        # Если нет текущего узла, начинаем с начала сценария
        if not current_node:
            current_node = self._get_start_node(session_context.scenario_id)
            if current_node:
                session_context.current_node_id = current_node.id
                self.db.commit()
        
        # Проверяем контекстные вопросы для текущей ноды
        current_node_id = session_context.current_node_id
        if current_node_id:
            contextual_questions = self.get_contextual_questions_status(session_id, current_node_id)
        else:
            contextual_questions = {"has_unused_questions": False}
        
        if current_node_id and contextual_questions.get('has_unused_questions', False):
            # Возвращаем следующий контекстный вопрос
            next_contextual_question = self.contextual_generator.get_next_contextual_question(
                session_id, current_node_id
            )
            if next_contextual_question:
                return {
                    'question_text': next_contextual_question.question_text,
                    'node_id': current_node_id,
                    'is_contextual': True,
                    'contextual_question_id': next_contextual_question.id,
                    'question_type': next_contextual_question.question_type,
                    'should_terminate': False
                }
        
        # Возвращаем базовый вопрос из сценария
        return self._get_basic_scenario_question(session_id, session_context)

    def _initialize_session_context(self, session_id: str, vacancy_id: str) -> SessionContext:
        """
        Инициализация контекста сессии
        
        Args:
            session_id: ID сессии
            vacancy_id: ID вакансии
            
        Returns:
            Созданный контекст сессии
        """
        # Получаем сценарий для вакансии
        scenario = self.get_scenario_for_vacancy(vacancy_id)
        
        if not scenario:
            # Если нет сценария, создаем базовый контекст
            session_context = SessionContext(
                id=f"ctx_{session_id}",
                session_id=session_id,
                skill_assessments={},
                negative_responses={},
                current_path=[],
                context_data={},
                scenario_id=None,
                current_node_id=None
            )
        else:
            # Создаем контекст с привязкой к сценарию
            session_context = SessionContext(
                id=f"ctx_{session_id}",
                session_id=session_id,
                skill_assessments={},
                negative_responses={},
                current_path=[],
                context_data={},
                scenario_id=scenario.id,
                current_node_id=None
            )
        
        self.db.add(session_context)
        self.db.commit()
        
        return session_context

    def _get_start_node(self, scenario_id: str) -> Optional[ScenarioNode]:
        """
        Получение начального узла сценария
        
        Args:
            scenario_id: ID сценария
            
        Returns:
            Начальный узел или None
        """
        return self.db.query(ScenarioNode).filter(
            and_(
                ScenarioNode.scenario_id == scenario_id,
                ScenarioNode.node_type == 'start'
            )
        ).first()

    def _get_next_node(self, current_node: ScenarioNode, session_context: SessionContext) -> Optional[ScenarioNode]:
        """
        Получение следующего узла на основе условий
        
        Args:
            current_node: Текущий узел
            session_context: Контекст сессии
            
        Returns:
            Следующий узел или None
        """
        # Получаем все возможные переходы из текущего узла
        transitions = self.db.query(ScenarioTransition).filter(
            ScenarioTransition.from_node_id == current_node.id
        ).order_by(ScenarioTransition.priority).all()
        
        if not transitions:
            return None
        
        # Оцениваем каждый переход
        valid_transitions = []
        for transition in transitions:
            if self._evaluate_transition(transition, session_context):
                valid_transitions.append(transition)
        
        if not valid_transitions:
            return None
        
        # Выбираем переход с наивысшим приоритетом
        best_transition = min(valid_transitions, key=lambda t: t.priority)
        
        # Получаем целевой узел
        return self.db.query(ScenarioNode).filter(
            ScenarioNode.id == best_transition.to_node_id
        ).first()

    def _evaluate_transition(self, transition: ScenarioTransition, session_context: SessionContext) -> bool:
        """
        Оценка условия перехода
        
        Args:
            transition: Переход для оценки
            session_context: Контекст сессии
            
        Returns:
            True если переход возможен
        """
        if not transition.condition_type or transition.condition_type == 'always':
            return True
        
        if not transition.condition_value:
            return True
        
        condition_value = transition.condition_value
        
        if transition.condition_type == 'score_threshold':
            return self._evaluate_score_threshold(condition_value, session_context)
        
        elif transition.condition_type == 'negative_response':
            return self._evaluate_negative_response(condition_value, session_context)
        
        elif transition.condition_type == 'skill_missing':
            return self._evaluate_skill_missing(condition_value, session_context)
        
        return True

    def _evaluate_score_threshold(self, condition_value: Dict[str, Any], session_context: SessionContext) -> bool:
        """
        Оценка условия по порогу оценки
        
        Args:
            condition_value: Значение условия
            session_context: Контекст сессии
            
        Returns:
            True если условие выполнено
        """
        if not session_context.skill_assessments:
            return False
        
        criterion = condition_value.get('criterion')
        min_score = condition_value.get('min_score')
        max_score = condition_value.get('max_score')
        
        if criterion and criterion in session_context.skill_assessments:
            skill_data = session_context.skill_assessments[criterion]
            average_score = skill_data.get('average_score', 0.0)
            
            if min_score is not None and average_score < min_score:
                return False
            
            if max_score is not None and average_score > max_score:
                return False
            
            return True
        
        return False

    def _evaluate_negative_response(self, condition_value: Dict[str, Any], session_context: SessionContext) -> bool:
        """
        Оценка условия по негативному ответу
        
        Args:
            condition_value: Значение условия
            session_context: Контекст сессии
            
        Returns:
            True если есть негативный ответ
        """
        if not session_context.negative_responses:
            return False
        
        patterns = condition_value.get('patterns', [])
        
        # Проверяем последний ответ в пути
        if session_context.current_path:
            last_answer = session_context.current_path[-1]
            answer_text = last_answer.get('answer_text', '').lower()
            
            for pattern in patterns:
                if pattern.lower() in answer_text:
                    return True
        
        return False

    def _evaluate_skill_missing(self, condition_value: Dict[str, Any], session_context: SessionContext) -> bool:
        """
        Оценка условия по отсутствию навыка
        
        Args:
            condition_value: Значение условия
            session_context: Контекст сессии
            
        Returns:
            True если навык отсутствует
        """
        skill_name = condition_value.get('skill_name')
        
        if not skill_name:
            return False
        
        # Проверяем наличие навыка в негативных ответах
        if session_context.negative_responses and skill_name in session_context.negative_responses:
            return True
        
        # Проверяем низкую оценку навыка
        if session_context.skill_assessments and skill_name in session_context.skill_assessments:
            skill_data = session_context.skill_assessments[skill_name]
            average_score = skill_data.get('average_score', 0.0)
            
            if average_score < 0.3:  # Порог для определения отсутствия навыка
                return True
        
        return False

    def should_terminate_interview(self, session_id: str) -> bool:
        """
        Определение необходимости завершения интервью
        
        Args:
            session_id: ID сессии
            
        Returns:
            True если интервью нужно завершить
        """
        session_context = self.get_session_context(session_id)
        
        if not session_context:
            return False
        
        # Проверяем, достигли ли мы конечного узла
        if session_context.current_node_id:
            current_node = self.db.query(ScenarioNode).filter(
                ScenarioNode.id == session_context.current_node_id
            ).first()
            
            if current_node and current_node.node_type == 'end':
                return True
        
        # Проверяем условия досрочного завершения
        if session_context.negative_responses:
            # Если кандидат отрицает базовые навыки программирования
            critical_skills = ['Python', 'Programming', 'Development']
            for skill in critical_skills:
                if skill in session_context.negative_responses:
                    return True
        
        return False

    def get_available_transitions(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Получение доступных переходов для текущего состояния
        
        Args:
            session_id: ID сессии
            
        Returns:
            Список доступных переходов
        """
        session_context = self.get_session_context(session_id)
        
        if not session_context or not session_context.current_node_id:
            return []
        
        current_node = self.db.query(ScenarioNode).filter(
            ScenarioNode.id == session_context.current_node_id
        ).first()
        
        if not current_node:
            return []
        
        transitions = self.db.query(ScenarioTransition).filter(
            ScenarioTransition.from_node_id == current_node.id
        ).all()
        
        available_transitions = []
        for transition in transitions:
            is_valid = self._evaluate_transition(transition, session_context)
            
            available_transitions.append({
                'transition_id': transition.id,
                'to_node_id': transition.to_node_id,
                'condition_type': transition.condition_type,
                'condition_value': transition.condition_value,
                'priority': transition.priority,
                'transition_label': transition.transition_label,
                'is_valid': is_valid
            })
        
        return available_transitions

    def update_context_after_answer(self, session_id: str, question_id: str, answer_text: str, answer_score: float) -> Dict[str, Any]:
        """
        Обновление контекста после ответа
        
        Args:
            session_id: ID сессии
            question_id: ID вопроса
            answer_text: Текст ответа
            answer_score: Оценка ответа
            
        Returns:
            Обновленный контекст
        """
        return self.negative_analyzer.update_session_context(
            session_id, question_id, answer_text, answer_score
        )

    def _get_contextual_questions_count(self, session_id: str, node_id: str) -> int:
        """
        Получает количество неиспользованных контекстных вопросов для ноды
        
        Args:
            session_id: ID сессии
            node_id: ID ноды
            
        Returns:
            Количество неиспользованных контекстных вопросов
        """
        try:
            from app.models import ContextualQuestion
            from sqlalchemy import and_
            
            count = self.db.query(ContextualQuestion).filter(
                and_(
                    ContextualQuestion.session_id == session_id,
                    ContextualQuestion.scenario_node_id == node_id,
                    ContextualQuestion.is_used == False
                )
            ).count()
            
            return count
            
        except Exception as e:
            print(f"Ошибка подсчета контекстных вопросов: {str(e)}")
            return 0

    async def generate_contextual_questions_for_current_node(
        self,
        session_id: str,
        max_questions: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Генерирует контекстные вопросы для текущего узла
        
        Args:
            session_id: ID сессии
            max_questions: Максимальное количество вопросов
            
        Returns:
            Список сгенерированных контекстных вопросов
        """
        try:
            session_context = self.get_session_context(session_id)
            
            if not session_context or not session_context.current_node_id:
                raise Exception("Текущий узел не найден")
            
            contextual_questions = await self.contextual_generator.generate_contextual_questions(
                session_id=session_id,
                scenario_node_id=session_context.current_node_id,
                max_questions=max_questions
            )
            
            return [
                {
                    "id": cq.id,
                    "question_text": cq.question_text,
                    "question_type": cq.question_type,
                    "context_source": cq.context_source,
                    "is_contextual": True
                }
                for cq in contextual_questions
            ]
            
        except Exception as e:
            raise Exception(f"Ошибка генерации контекстных вопросов: {str(e)}")

    def get_contextual_questions_status(
        self,
        session_id: str,
        node_id: str = None
    ) -> Dict[str, Any]:
        """
        Получает статус контекстных вопросов
        
        Args:
            session_id: ID сессии
            node_id: ID ноды (если None, используется текущий узел)
            
        Returns:
            Статус контекстных вопросов
        """
        try:
            if not node_id:
                session_context = self.get_session_context(session_id)
                print(f"DEBUG: session_context = {session_context}")
                if not session_context:
                    return {"has_questions": False, "error": "Контекст сессии не найден"}
                if not session_context.current_node_id:
                    return {"has_questions": False, "error": "Текущий узел не найден"}
                node_id = session_context.current_node_id
                print(f"DEBUG: node_id = {node_id}")
            
            all_questions = self.contextual_generator.get_contextual_questions_for_node(
                session_id, node_id
            )
            
            used_questions = [q for q in all_questions if q.is_used]
            remaining_questions = [q for q in all_questions if not q.is_used]
            
            return {
                "total_questions": len(all_questions),
                "used_questions": len(used_questions),
                "remaining_questions": len(remaining_questions),
                "has_questions": len(all_questions) > 0,
                "has_remaining": len(remaining_questions) > 0,
                "node_id": node_id
            }
            
        except Exception as e:
            return {
                "total_questions": 0,
                "used_questions": 0,
                "remaining_questions": 0,
                "has_questions": False,
                "has_remaining": False,
                "error": str(e)
            }

    def _get_basic_scenario_question(self, session_id: str, session_context: SessionContext) -> Optional[Dict[str, Any]]:
        """
        Получает базовый вопрос из сценария
        
        Args:
            session_id: ID сессии
            session_context: Контекст сессии
            
        Returns:
            Информация о базовом вопросе или None
        """
        # Получаем сессию
        session = self.db.query(SessionModel).filter(
            SessionModel.id == session_id
        ).first()
        
        if not session:
            return None
        
        # Получаем текущий узел
        current_node = None
        if session_context.current_node_id:
            current_node = self.db.query(ScenarioNode).filter(
                ScenarioNode.id == session_context.current_node_id
            ).first()
        
        # Если нет текущего узла, начинаем с начала сценария
        if not current_node:
            current_node = self._get_start_node(session_context.scenario_id)
            if current_node:
                session_context.current_node_id = current_node.id
                self.db.commit()
        
        # Получаем следующий узел
        next_node = self._get_next_node(current_node, session_context)
        
        if not next_node:
            return None
        
        # Обновляем контекст
        session_context.current_node_id = next_node.id
        self.db.commit()
        
        # Если это конечный узел, завершаем сессию
        if next_node.node_type == 'end':
            session.status = 'completed'
            self.db.commit()
            return {
                'should_terminate': True,
                'node_type': 'end',
                'message': 'Интервью завершено'
            }
        
        # Если это узел-пропуск, получаем следующий после него
        if next_node.node_type == 'skip':
            next_node = self._get_next_node(next_node, session_context)
            if next_node:
                session_context.current_node_id = next_node.id
                self.db.commit()
        
        # Получаем вопрос
        if next_node.question_id:
            question = self.db.query(Question).filter(
                Question.id == next_node.question_id
            ).first()
            
            if question:
                return {
                    'node_id': next_node.id,
                    'question_id': question.id,
                    'question_text': question.text,
                    'question_type': question.type,
                    'node_type': next_node.node_type,
                    'node_config': next_node.node_config,
                    'is_contextual': False,
                    'should_terminate': False
                }
        
        return None
