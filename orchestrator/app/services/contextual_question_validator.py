"""
Contextual Question Validator Service
"""
import re
from typing import Dict, List, Any, Tuple
from sqlalchemy.orm import Session
from app.models import ScenarioNode, Resume


class ContextualQuestionValidator:
    """
    Валидирует сгенерированные контекстные вопросы
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # Паттерны для определения некачественных вопросов
        self.generic_patterns = [
            r'\bрасскажи\b.*\bо\b',
            r'\bчто\s+такое\b',
            r'\bобъясни\b.*\bчто\b',
            r'\bкак\s+работает\b',
            r'\bв\s+чем\s+разница\b',
            r'\bчто\s+означает\b',
            r'\bопиши\b.*\bпроцесс\b'
        ]
        
        # Паттерны для определения слишком личных вопросов
        self.personal_patterns = [
            r'\bзарплат[аы]\b',
            r'\bденьги\b',
            r'\bконфликт\b',
            r'\bссора\b',
            r'\bувольнение\b',
            r'\bпроблемы\s+с\s+начальством\b',
            r'\bличная\s+жизнь\b',
            r'\bсемья\b',
            r'\bздоровье\b'
        ]
        
        # Минимальная длина вопроса
        self.min_question_length = 20
        
        # Максимальная длина вопроса
        self.max_question_length = 300
    
    def validate_questions(
        self,
        questions: List[str],
        scenario_node: ScenarioNode,
        resume_context: Dict[str, Any]
    ) -> Tuple[List[str], List[str]]:
        """
        Валидирует вопросы:
        1. Не слишком личные
        2. Не дублируют базовые
        3. Релевантны ноде
        4. Соответствуют уровню кандидата
        
        Args:
            questions: Список вопросов для валидации
            scenario_node: Нода сценария
            resume_context: Контекст резюме
            
        Returns:
            Tuple[валидные_вопросы, причины_отклонения]
        """
        valid_questions = []
        rejection_reasons = []
        
        for i, question in enumerate(questions):
            is_valid, reason = self._validate_single_question(
                question, scenario_node, resume_context
            )
            
            if is_valid:
                valid_questions.append(question)
            else:
                rejection_reasons.append(f"Вопрос {i+1}: {reason}")
        
        return valid_questions, rejection_reasons
    
    def _validate_single_question(
        self,
        question: str,
        scenario_node: ScenarioNode,
        resume_context: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """
        Валидирует один вопрос
        
        Args:
            question: Вопрос для валидации
            scenario_node: Нода сценария
            resume_context: Контекст резюме
            
        Returns:
            Tuple[валиден_ли, причина_отклонения]
        """
        # Проверка длины
        if len(question) < self.min_question_length:
            return False, f"Слишком короткий вопрос ({len(question)} символов)"
        
        if len(question) > self.max_question_length:
            return False, f"Слишком длинный вопрос ({len(question)} символов)"
        
        # Проверка на слишком личные вопросы
        if self._is_too_personal(question):
            return False, "Содержит слишком личные темы"
        
        # Проверка на общие вопросы
        if self._is_too_generic(question):
            return False, "Слишком общий вопрос"
        
        # Проверка релевантности ноде
        if not self._is_relevant_to_node(question, scenario_node):
            return False, "Не релевантен ноде сценария"
        
        # Проверка соответствия уровню кандидата
        if not self._matches_candidate_level(question, resume_context):
            return False, "Не соответствует уровню кандидата"
        
        # Проверка на дублирование
        if self._is_duplicate_question(question):
            return False, "Дублирует существующий вопрос"
        
        return True, ""
    
    def _is_too_personal(self, question: str) -> bool:
        """
        Проверяет, не слишком ли личный вопрос
        """
        question_lower = question.lower()
        
        for pattern in self.personal_patterns:
            if re.search(pattern, question_lower):
                return True
        
        return False
    
    def _is_too_generic(self, question: str) -> bool:
        """
        Проверяет, не слишком ли общий вопрос
        """
        question_lower = question.lower()
        
        # Проверяем на общие паттерны
        for pattern in self.generic_patterns:
            if re.search(pattern, question_lower):
                return True
        
        # Проверяем на отсутствие конкретики
        if not self._has_specific_elements(question):
            return True
        
        return False
    
    def _has_specific_elements(self, question: str) -> bool:
        """
        Проверяет наличие конкретных элементов в вопросе
        """
        # Проверяем наличие конкретных технологий, проектов, решений
        specific_indicators = [
            r'\bпроект\b',
            r'\bзадача\b',
            r'\bрешение\b',
            r'\bопыт\b',
            r'\bслучай\b',
            r'\bситуация\b',
            r'\bпример\b',
            r'\bконкретно\b',
            r'\bдетально\b'
        ]
        
        question_lower = question.lower()
        specific_count = sum(1 for pattern in specific_indicators if re.search(pattern, question_lower))
        
        return specific_count >= 1
    
    def _is_relevant_to_node(self, question: str, scenario_node: ScenarioNode) -> bool:
        """
        Проверяет релевантность вопроса ноде
        """
        if not scenario_node.node_config:
            return True
        
        node_name = scenario_node.node_config.get("label", "").lower()
        if not node_name:
            return True
        
        # Извлекаем ключевые слова из названия ноды
        node_keywords = self._extract_keywords_from_node_name(node_name)
        
        # Проверяем наличие ключевых слов в вопросе
        question_lower = question.lower()
        relevant_keywords = [kw for kw in node_keywords if kw.lower() in question_lower]
        
        return len(relevant_keywords) > 0
    
    def _extract_keywords_from_node_name(self, node_name: str) -> List[str]:
        """
        Извлекает ключевые слова из названия ноды
        """
        # Простая логика извлечения ключевых слов
        keywords = []
        
        # Убираем общие слова
        common_words = ['вопросы', 'тема', 'раздел', 'часть', 'блок']
        
        words = node_name.split()
        for word in words:
            if word.lower() not in common_words and len(word) > 2:
                keywords.append(word)
        
        return keywords
    
    def _matches_candidate_level(self, question: str, resume_context: Dict[str, Any]) -> bool:
        """
        Проверяет соответствие вопроса уровню кандидата
        """
        candidate_level = resume_context.get("candidate_level", "unknown")
        
        # Определяем сложность вопроса
        question_complexity = self._assess_question_complexity(question)
        
        # Проверяем соответствие
        if candidate_level == "beginner" and question_complexity == "expert":
            return False
        elif candidate_level == "intermediate" and question_complexity == "expert":
            return False
        
        return True
    
    def _assess_question_complexity(self, question: str) -> str:
        """
        Оценивает сложность вопроса
        """
        question_lower = question.lower()
        
        # Индикаторы сложных вопросов
        expert_indicators = [
            r'\bархитектур\b',
            r'\bмасштабировани\b',
            r'\bоптимизаци\b',
            r'\bпроизводительност\b',
            r'\bбезопасност\b',
            r'\bмикросервис\b',
            r'\bконтейнеризаци\b',
            r'\bоркестраци\b',
            r'\bмониторинг\b',
            r'\bлогировани\b'
        ]
        
        # Индикаторы базовых вопросов
        beginner_indicators = [
            r'\bчто\s+такое\b',
            r'\bкак\s+использовать\b',
            r'\bбазовые\b',
            r'\bпростые\b',
            r'\bосновы\b'
        ]
        
        # Проверяем сложность
        expert_count = sum(1 for pattern in expert_indicators if re.search(pattern, question_lower))
        beginner_count = sum(1 for pattern in beginner_indicators if re.search(pattern, question_lower))
        
        if expert_count > 0:
            return "expert"
        elif beginner_count > 0:
            return "beginner"
        else:
            return "intermediate"
    
    def _is_duplicate_question(self, question: str) -> bool:
        """
        Проверяет на дублирование вопросов
        """
        # В реальной системе здесь была бы проверка в базе данных
        # Пока возвращаем False
        return False
    
    def get_question_quality_score(self, question: str) -> float:
        """
        Оценивает качество вопроса (0.0 - 1.0)
        """
        score = 1.0
        
        # Штраф за длину
        if len(question) < 30:
            score -= 0.2
        elif len(question) > 200:
            score -= 0.1
        
        # Штраф за общие паттерны
        question_lower = question.lower()
        generic_count = sum(1 for pattern in self.generic_patterns if re.search(pattern, question_lower))
        score -= generic_count * 0.3
        
        # Бонус за конкретность
        if self._has_specific_elements(question):
            score += 0.2
        
        # Бонус за релевантность
        if self._has_specific_elements(question):
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def suggest_improvements(self, question: str) -> List[str]:
        """
        Предлагает улучшения для вопроса
        """
        suggestions = []
        
        if len(question) < self.min_question_length:
            suggestions.append("Сделайте вопрос более детальным")
        
        if self._is_too_generic(question):
            suggestions.append("Добавьте конкретные детали или примеры")
        
        if not self._has_specific_elements(question):
            suggestions.append("Укажите конкретный проект или ситуацию")
        
        if self._is_too_personal(question):
            suggestions.append("Избегайте личных тем")
        
        return suggestions
