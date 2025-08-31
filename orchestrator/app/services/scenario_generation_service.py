"""
Scenario Generation Service
"""
import uuid
import json
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from app.models import (
    Vacancy, InterviewScenario, ScenarioNode, ScenarioTransition,
    DynamicCriteria, ScenarioCriteriaMapping
)
from app.services.vacancy_skills_extractor import VacancySkillsExtractor
from app.schemas.dynamic_criteria import DynamicCriteriaCreate
from app.core.config import settings
import httpx


class ScenarioGenerationService:
    """Сервис генерации сценариев интервью с динамическими критериями"""
    
    def __init__(self, db: Session):
        self.db = db
        self.vacancy_skills_extractor = VacancySkillsExtractor()
        self.llm_service_url = settings.LLM_SERVICE_URL

    async def generate_scenario_for_vacancy(
        self, 
        vacancy_id: str, 
        scenario_name: str = None,
        description: str = None
    ) -> Dict[str, Any]:
        """
        Генерация сценария интервью для вакансии с динамическими критериями
        
        Args:
            vacancy_id: ID вакансии
            scenario_name: Название сценария (опционально)
            description: Описание сценария (опционально)
            
        Returns:
            Сгенерированный сценарий с динамическими критериями
        """
        try:
            # Получаем вакансию
            vacancy = self.db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
            if not vacancy:
                raise Exception("Вакансия не найдена")
            
            # Извлекаем навыки из вакансии
            print(f"Извлекаем навыки для вакансии {vacancy_id}")
            vacancy_skills = await self.vacancy_skills_extractor.extract_skills_from_vacancy(
                vacancy=vacancy,
                force_reload=False
            )
            
            if not vacancy_skills or not vacancy_skills.skills:
                raise Exception("Не удалось извлечь навыки из вакансии")
            
            print(f"Извлечено {len(vacancy_skills.skills)} навыков")
            
            # Создаем динамические критерии на основе навыков
            dynamic_criteria = await self._create_dynamic_criteria_from_skills(
                vacancy_skills.skills, vacancy_id
            )
            
            # Генерируем сценарий через LLM
            scenario_data = await self._generate_scenario_with_llm(
                vacancy, vacancy_skills.skills, dynamic_criteria
            )
            
            # Создаем сценарий в базе данных
            scenario = await self._create_scenario_in_db(
                vacancy_id, scenario_data, scenario_name, description
            )
            
            # Создаем узлы сценария
            nodes = await self._create_scenario_nodes(scenario.id, scenario_data)
            
            # Создаем переходы между узлами
            transitions = await self._create_scenario_transitions(
                scenario.id, nodes, scenario_data
            )
            
            # Связываем критерии со сценарием
            await self._link_criteria_to_scenario(scenario.id, dynamic_criteria)
            
            return {
                "success": True,
                "scenario_id": scenario.id,
                "scenario_name": scenario.name,
                "nodes_count": len(nodes),
                "transitions_count": len(transitions),
                "criteria_count": len(dynamic_criteria),
                "skills_used": [skill.skill_name for skill in vacancy_skills.skills]
            }
            
        except Exception as e:
            print(f"Ошибка генерации сценария: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def recreate_transitions_for_scenario(self, scenario_id: str) -> Dict[str, Any]:
        """
        Пересоздание переходов для существующего сценария
        
        Args:
            scenario_id: ID сценария
            
        Returns:
            Результат пересоздания переходов
        """
        try:
            # Получаем сценарий
            scenario = self.db.query(InterviewScenario).filter(
                InterviewScenario.id == scenario_id
            ).first()
            
            if not scenario:
                raise Exception("Сценарий не найден")
            
            # Получаем узлы сценария
            nodes = self.db.query(ScenarioNode).filter(
                ScenarioNode.scenario_id == scenario_id
            ).order_by(ScenarioNode.created_at).all()
            
            if not nodes:
                raise Exception("Узлы сценария не найдены")
            
            # Удаляем существующие переходы
            self.db.query(ScenarioTransition).filter(
                ScenarioTransition.scenario_id == scenario_id
            ).delete()
            
            # Создаем новые переходы
            transitions = await self._create_sequential_transitions(scenario_id, nodes)
            
            # Сохраняем изменения
            self.db.commit()
            
            return {
                "success": True,
                "scenario_id": scenario_id,
                "scenario_name": scenario.name,
                "nodes_count": len(nodes),
                "transitions_count": len(transitions),
                "message": f"Создано {len(transitions)} переходов для сценария '{scenario.name}'"
            }
            
        except Exception as e:
            self.db.rollback()
            print(f"Ошибка пересоздания переходов: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _create_sequential_transitions(self, scenario_id: str, nodes: List[ScenarioNode]) -> List[ScenarioTransition]:
        """
        Создание последовательных переходов между узлами
        
        Args:
            scenario_id: ID сценария
            nodes: Список узлов в порядке создания
            
        Returns:
            Список созданных переходов
        """
        transitions = []
        
        # Сортируем узлы по типу: start -> questions -> end
        start_nodes = [n for n in nodes if n.node_type == "start"]
        question_nodes = [n for n in nodes if n.node_type == "question"]
        end_nodes = [n for n in nodes if n.node_type == "end"]
        
        # Создаем переходы от start к первому вопросу
        if start_nodes and question_nodes:
            transition = ScenarioTransition(
                id=f"TRANSITION_{uuid.uuid4().hex[:8].upper()}",
                scenario_id=scenario_id,
                from_node_id=start_nodes[0].id,
                to_node_id=question_nodes[0].id,
                condition_type="always",
                transition_label="Начать интервью"
            )
            transitions.append(transition)
            self.db.add(transition)
        
        # Создаем переходы между вопросами
        for i in range(len(question_nodes) - 1):
            current_node = question_nodes[i]
            next_node = question_nodes[i + 1]
            
            # Определяем тип перехода на основе веса вопроса
            node_config = current_node.node_config or {}
            weight = node_config.get("weight", 0.5)
            must_have = node_config.get("must_have", False)
            
            if must_have:
                # Для обязательных вопросов - переход по порогу оценки
                transition = ScenarioTransition(
                    id=f"TRANSITION_{uuid.uuid4().hex[:8].upper()}",
                    scenario_id=scenario_id,
                    from_node_id=current_node.id,
                    to_node_id=next_node.id,
                    condition_type="score_threshold",
                    condition_value={
                        "min_score": 0.7,
                        "criterion": "overall_score"
                    },
                    transition_label=f"Переход к следующему вопросу (порог: 0.7)"
                )
            else:
                # Для необязательных вопросов - всегда переходим
                transition = ScenarioTransition(
                    id=f"TRANSITION_{uuid.uuid4().hex[:8].upper()}",
                    scenario_id=scenario_id,
                    from_node_id=current_node.id,
                    to_node_id=next_node.id,
                    condition_type="always",
                    transition_label="Переход к следующему вопросу"
                )
            
            transitions.append(transition)
            self.db.add(transition)
        
        # Создаем переход от последнего вопроса к end
        if question_nodes and end_nodes:
            last_question = question_nodes[-1]
            transition = ScenarioTransition(
                id=f"TRANSITION_{uuid.uuid4().hex[:8].upper()}",
                scenario_id=scenario_id,
                from_node_id=last_question.id,
                to_node_id=end_nodes[0].id,
                condition_type="always",
                transition_label="Завершить интервью"
            )
            transitions.append(transition)
            self.db.add(transition)
        
        return transitions

    async def _create_dynamic_criteria_from_skills(
        self, 
        skills: List[Any], 
        vacancy_id: str
    ) -> List[DynamicCriteria]:
        """
        Создание динамических критериев на основе навыков вакансии
        """
        dynamic_criteria = []
        
        for skill in skills:
            criterion_id = f"DC_{uuid.uuid4().hex[:8].upper()}"
            
            criterion = DynamicCriteria(
                id=criterion_id,
                vacancy_id=vacancy_id,
                skill_name=skill.skill_name,
                category=skill.category,
                importance=skill.importance,
                required_level=skill.required_level,
                is_mandatory=skill.is_mandatory,
                description=skill.description or f"Оценка навыка {skill.skill_name}",
                alternatives=skill.alternatives or []
            )
            
            self.db.add(criterion)
            dynamic_criteria.append(criterion)
        
        self.db.commit()
        return dynamic_criteria

    async def _generate_scenario_with_llm(
        self, 
        vacancy: Vacancy, 
        skills: List[Any], 
        dynamic_criteria: List[DynamicCriteria]
    ) -> Dict[str, Any]:
        """
        Генерация сценария интервью через LLM
        """
        # Формируем промпт для LLM
        prompt = self._build_scenario_generation_prompt(vacancy, skills, dynamic_criteria)
        
        # Вызываем LLM
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.llm_service_url}/api/v1/llm/generate",
                    json={
                        "prompt": prompt,
                        "max_tokens": 2000,
                        "temperature": 0.7
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return self._parse_scenario_response(result.get("response", ""))
                else:
                    raise Exception(f"LLM сервис вернул ошибку: {response.status_code}")
                    
        except Exception as e:
            print(f"Ошибка вызова LLM: {str(e)}")
            # Возвращаем базовый сценарий
            return self._create_fallback_scenario(vacancy, skills)

    def _build_scenario_generation_prompt(
        self, 
        vacancy: Vacancy, 
        skills: List[Any], 
        dynamic_criteria: List[DynamicCriteria]
    ) -> str:
        """
        Формирование промпта для генерации сценария
        """
        skills_text = "\n".join([
            f"- {skill.skill_name} ({skill.category}): {skill.required_level} уровень, важность {skill.importance}"
            for skill in skills
        ])
        
        criteria_text = "\n".join([
            f"- {criterion.skill_name}: {criterion.description}"
            for criterion in dynamic_criteria
        ])
        
        prompt = f"""
Ты - эксперт по созданию сценариев технических интервью. Создай адаптивный сценарий интервью для вакансии.

ВАКАНСИЯ: {vacancy.title}
ТРЕБОВАНИЯ: {vacancy.requirements or 'Не указаны'}
ОБЯЗАННОСТИ: {vacancy.responsibilities or 'Не указаны'}
ОПЫТ: {vacancy.experience_required or 'Не указан'}

НАВЫКИ ДЛЯ ОЦЕНКИ:
{skills_text}

КРИТЕРИИ ОЦЕНКИ:
{criteria_text}

СОЗДАЙ СЦЕНАРИЙ ИНТЕРВЬЮ В ФОРМАТЕ JSON:
{{
    "scenario_name": "название сценария",
    "description": "описание сценария",
    "nodes": [
        {{
            "id": "уникальный_id",
            "node_type": "start/question/condition/end",
            "question_text": "текст вопроса (для узлов типа question)",
            "position_x": 100,
            "position_y": 100,
            "node_config": {{
                "label": "метка узла",
                "weight": 1.0,
                "must_have": true/false,
                "target_skills": ["список навыков для оценки"]
            }}
        }}
    ],
    "transitions": [
        {{
            "from_node_id": "id_исходного_узла",
            "to_node_id": "id_целевого_узла",
            "condition_type": "always/score_threshold/negative_response",
            "condition_value": {{
                "min_score": 0.7,
                "criterion": "название_критерия"
            }},
            "priority": 1,
            "transition_label": "метка перехода"
        }}
    ]
}}

ВАЖНО:
1. Создай логичную последовательность вопросов
2. Учитывай важность навыков при определении весов
3. Добавь условия переходов на основе оценок
4. Включи обработку негативных ответов
5. Сделай сценарий адаптивным

Отвечай ТОЛЬКО в формате JSON.
"""
        
        return prompt

    def _parse_scenario_response(self, response: str) -> Dict[str, Any]:
        """
        Парсинг ответа LLM в структуру сценария
        """
        try:
            # Ищем JSON в ответе
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("JSON не найден в ответе")
            
            json_str = response[json_start:json_end]
            scenario_data = json.loads(json_str)
            
            # Генерируем уникальный префикс для ID узлов
            scenario_prefix = f"SCENARIO_{uuid.uuid4().hex[:8].upper()}"
            
            # Обновляем ID узлов, чтобы избежать конфликтов
            if 'nodes' in scenario_data:
                for i, node in enumerate(scenario_data['nodes']):
                    if node.get('id') in ['start', 'end']:
                        node['id'] = f"{scenario_prefix}_{node['id']}"
                    elif node.get('id', '').startswith('question_'):
                        node['id'] = f"{scenario_prefix}_{node['id']}"
                    else:
                        # Генерируем уникальный ID для остальных узлов
                        node['id'] = f"{scenario_prefix}_node_{i}"
            
            # Обновляем переходы, чтобы они ссылались на правильные ID
            if 'transitions' in scenario_data:
                for transition in scenario_data['transitions']:
                    from_id = transition.get('from_node_id', '')
                    to_id = transition.get('to_node_id', '')
                    
                    # Обновляем from_node_id
                    if from_id in ['start', 'end']:
                        transition['from_node_id'] = f"{scenario_prefix}_{from_id}"
                    elif from_id.startswith('question_'):
                        transition['from_node_id'] = f"{scenario_prefix}_{from_id}"
                    
                    # Обновляем to_node_id
                    if to_id in ['start', 'end']:
                        transition['to_node_id'] = f"{scenario_prefix}_{to_id}"
                    elif to_id.startswith('question_'):
                        transition['to_node_id'] = f"{scenario_prefix}_{to_id}"
            
            return scenario_data
            
        except Exception as e:
            print(f"Ошибка парсинга ответа LLM: {str(e)}")
            raise Exception("Не удалось распарсить ответ LLM")

    def _create_fallback_scenario(
        self, 
        vacancy: Vacancy, 
        skills: List[Any]
    ) -> Dict[str, Any]:
        """
        Создание базового сценария при недоступности LLM
        """
        scenario_id = f"SCENARIO_{uuid.uuid4().hex[:8].upper()}"
        
        nodes = [
            {
                "id": f"{scenario_id}_start",
                "node_type": "start",
                "question_text": "",
                "position_x": 100,
                "position_y": 100,
                "node_config": {
                    "label": "Начало интервью",
                    "weight": 1.0,
                    "must_have": False
                }
            }
        ]
        
        # Создаем узлы для каждого навыка
        for i, skill in enumerate(skills[:8]):  # Максимум 8 вопросов
            node_id = f"{scenario_id}_question_{i+1}"
            nodes.append({
                "id": node_id,
                "node_type": "question",
                "question_text": f"Расскажите о вашем опыте работы с {skill.skill_name}",
                "position_x": 300 + i * 200,
                "position_y": 100,
                "node_config": {
                    "label": f"Вопрос по {skill.skill_name}",
                    "weight": skill.importance,
                    "must_have": skill.is_mandatory,
                    "target_skills": [skill.skill_name]
                }
            })
        
        nodes.append({
            "id": f"{scenario_id}_end",
            "node_type": "end",
            "question_text": "",
            "position_x": 300 + len(skills) * 200,
            "position_y": 100,
            "node_config": {
                "label": "Завершение интервью",
                "weight": 1.0,
                "must_have": False
            }
        })
        
        # Создаем переходы
        transitions = []
        for i in range(len(nodes) - 1):
            transitions.append({
                "from_node_id": nodes[i]["id"],
                "to_node_id": nodes[i+1]["id"],
                "condition_type": "always",
                "condition_value": {},
                "priority": 1,
                "transition_label": f"Переход {i+1}"
            })
        
        return {
            "scenario_name": f"Базовый сценарий для {vacancy.title}",
            "description": f"Автоматически созданный сценарий для вакансии {vacancy.title}",
            "nodes": nodes,
            "transitions": transitions
        }

    async def _create_scenario_in_db(
        self, 
        vacancy_id: str, 
        scenario_data: Dict[str, Any],
        scenario_name: str = None,
        description: str = None
    ) -> InterviewScenario:
        """
        Создание сценария в базе данных
        """
        scenario = InterviewScenario(
            id=f"SCENARIO_{uuid.uuid4().hex[:8].upper()}",
            vacancy_id=vacancy_id,
            name=scenario_name or scenario_data.get("scenario_name", "Новый сценарий"),
            description=description or scenario_data.get("description", ""),
            is_active=True,
            version="1.0"
        )
        
        self.db.add(scenario)
        self.db.commit()
        self.db.refresh(scenario)
        
        return scenario

    async def _create_scenario_nodes(
        self, 
        scenario_id: str, 
        scenario_data: Dict[str, Any]
    ) -> List[ScenarioNode]:
        """
        Создание узлов сценария в базе данных
        """
        nodes = []
        
        for node_data in scenario_data.get("nodes", []):
            node = ScenarioNode(
                id=node_data["id"],
                scenario_id=scenario_id,
                question_id=None,  # Будет заполнено позже
                node_type=node_data["node_type"],
                position_x=node_data.get("position_x", 0),
                position_y=node_data.get("position_y", 0),
                node_config=node_data.get("node_config", {})
            )
            
            self.db.add(node)
            nodes.append(node)
        
        self.db.commit()
        return nodes

    async def _create_scenario_transitions(
        self, 
        scenario_id: str, 
        nodes: List[ScenarioNode],
        scenario_data: Dict[str, Any]
    ) -> List[ScenarioTransition]:
        """
        Создание переходов между узлами
        """
        transitions = []
        
        # Создаем словарь существующих узлов для проверки
        existing_nodes = {node.id: node for node in nodes}
        
        for transition_data in scenario_data.get("transitions", []):
            from_node_id = transition_data["from_node_id"]
            to_node_id = transition_data["to_node_id"]
            
            # Проверяем, что оба узла существуют
            if from_node_id not in existing_nodes:
                print(f"Предупреждение: узел {from_node_id} не найден, пропускаем переход")
                continue
                
            if to_node_id not in existing_nodes:
                print(f"Предупреждение: узел {to_node_id} не найден, пропускаем переход")
                continue
            
            transition = ScenarioTransition(
                id=f"TRANS_{uuid.uuid4().hex[:8].upper()}",
                scenario_id=scenario_id,
                from_node_id=from_node_id,
                to_node_id=to_node_id,
                condition_type=transition_data.get("condition_type", "always"),
                condition_value=transition_data.get("condition_value", {}),
                priority=transition_data.get("priority", 1),
                transition_label=transition_data.get("transition_label", "")
            )
            
            self.db.add(transition)
            transitions.append(transition)
        
        self.db.commit()
        return transitions

    async def _link_criteria_to_scenario(
        self, 
        scenario_id: str, 
        dynamic_criteria: List[DynamicCriteria]
    ) -> None:
        """
        Связывание динамических критериев со сценарием
        """
        for criterion in dynamic_criteria:
            mapping = ScenarioCriteriaMapping(
                id=f"MAPPING_{uuid.uuid4().hex[:8].upper()}",
                scenario_id=scenario_id,
                criterion_id=criterion.id,
                weight=criterion.importance,
                is_mandatory=criterion.is_mandatory
            )
            
            self.db.add(mapping)
        
        self.db.commit()

    async def regenerate_scenario(self, scenario_id: str) -> Dict[str, Any]:
        """
        Перегенерация существующего сценария
        """
        try:
            # Получаем существующий сценарий
            scenario = self.db.query(InterviewScenario).filter(
                InterviewScenario.id == scenario_id
            ).first()
            
            if not scenario:
                raise Exception("Сценарий не найден")
            
            # Сначала удаляем переходы, потом узлы (из-за foreign key constraints)
            self.db.query(ScenarioTransition).filter(
                ScenarioTransition.scenario_id == scenario_id
            ).delete()
            
            self.db.query(ScenarioNode).filter(
                ScenarioNode.scenario_id == scenario_id
            ).delete()
            
            self.db.commit()
            
            # Генерируем новый сценарий
            return await self.generate_scenario_for_vacancy(
                scenario.vacancy_id,
                scenario.name,
                scenario.description
            )
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
