"""
API endpoints for dynamic interview scenarios
"""
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Vacancy, InterviewScenario, DynamicCriteria, ScenarioCriteriaMapping, ScenarioNode, ScenarioTransition
from app.services.scenario_generation_service import ScenarioGenerationService
from app.services.scenario_image_generator import ScenarioImageGenerator
from app.schemas.dynamic_criteria import (
    ScenarioGenerationRequest, ScenarioGenerationResponse,
    ScenarioPreviewRequest, ScenarioPreviewResponse,
    DynamicCriteriaListResponse, VacancyDynamicCriteriaResponse,
    DynamicCriteriaResponse
)

router = APIRouter()


@router.get("/by-vacancy/{vacancy_id}")
async def get_scenario_by_vacancy(
    vacancy_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Получение активного сценария для конкретной вакансии
    """
    try:
        # Проверяем существование вакансии
        vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
        if not vacancy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Вакансия {vacancy_id} не найдена"
            )
        
        # Получаем активный сценарий
        scenario = db.query(InterviewScenario).filter(
            InterviewScenario.vacancy_id == vacancy_id,
            InterviewScenario.is_active == True
        ).first()
        
        if not scenario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Активный сценарий для вакансии {vacancy_id} не найден"
            )
        
        # Подсчитываем узлы
        nodes_count = db.query(ScenarioNode).filter(
            ScenarioNode.scenario_id == scenario.id
        ).count()
        
        return {
            "id": scenario.id,
            "name": scenario.name,
            "description": scenario.description,
            "is_active": scenario.is_active,
            "version": scenario.version,
            "total_nodes": nodes_count,
            "created_at": scenario.created_at.isoformat() if scenario.created_at else None,
            "updated_at": scenario.updated_at.isoformat() if scenario.updated_at else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения сценария: {str(e)}"
        )


@router.get("/")
async def get_scenarios(
    vacancy_id: Optional[str] = Query(None, description="Фильтр по ID вакансии"),
    name: Optional[str] = Query(None, description="Поиск по названию"),
    status: Optional[str] = Query(None, description="Фильтр по статусу"),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """
    Получение списка сценариев с фильтрацией
    """
    try:
        query = db.query(InterviewScenario)
        
        # Применяем фильтры
        if vacancy_id:
            query = query.filter(InterviewScenario.vacancy_id == vacancy_id)
        
        if name:
            query = query.filter(InterviewScenario.name.ilike(f"%{name}%"))
        
        if status:
            # Здесь можно добавить логику фильтрации по статусу
            pass
        
        # Получаем сценарии
        scenarios = query.order_by(InterviewScenario.created_at.desc()).all()
        
        # Получаем узлы и переходы для каждого сценария
        result = []
        for scenario in scenarios:
            nodes = db.query(ScenarioNode).filter(ScenarioNode.scenario_id == scenario.id).all()
            transitions = db.query(ScenarioTransition).filter(ScenarioTransition.scenario_id == scenario.id).all()
            
            result.append({
                "id": scenario.id,
                "name": scenario.name,
                "description": scenario.description,
                "vacancy_id": scenario.vacancy_id,
                "nodes_count": len(nodes),
                "transitions_count": len(transitions),
                "created_at": scenario.created_at,
                "updated_at": scenario.updated_at
            })
        
        return result
        
    except Exception as e:
                            raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Ошибка получения списка сценариев: {str(e)}"
                    )

@router.post("/{scenario_id}/recreate-transitions")
async def recreate_scenario_transitions(
    scenario_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Пересоздание переходов для сценария
    """
    try:
        from app.services.scenario_generation_service import ScenarioGenerationService
        
        # Создаем сервис
        scenario_service = ScenarioGenerationService(db)
        
        # Пересоздаем переходы
        result = await scenario_service.recreate_transitions_for_scenario(scenario_id)
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка пересоздания переходов: {str(e)}"
        )


@router.post("/generate", response_model=ScenarioGenerationResponse)
async def generate_scenario(
    request: ScenarioGenerationRequest,
    db: Session = Depends(get_db)
) -> ScenarioGenerationResponse:
    """
    Генерация сценария интервью для вакансии с динамическими критериями
    """
    try:
        # Проверяем существование вакансии
        vacancy = db.query(Vacancy).filter(Vacancy.id == request.vacancy_id).first()
        if not vacancy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Вакансия {request.vacancy_id} не найдена"
            )
        
        # Создаем сервис генерации
        scenario_service = ScenarioGenerationService(db)
        
        # Генерируем сценарий
        result = await scenario_service.generate_scenario_for_vacancy(
            vacancy_id=request.vacancy_id,
            scenario_name=request.scenario_name,
            description=request.description
        )
        
        if not result.get("success", False):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Неизвестная ошибка генерации")
            )
        
        return ScenarioGenerationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка генерации сценария: {str(e)}"
        )


@router.post("/preview", response_model=ScenarioPreviewResponse)
async def preview_scenario(
    request: ScenarioPreviewRequest,
    db: Session = Depends(get_db)
) -> ScenarioPreviewResponse:
    """
    Предварительный просмотр сценария без сохранения в БД
    """
    try:
        # Проверяем существование вакансии
        vacancy = db.query(Vacancy).filter(Vacancy.id == request.vacancy_id).first()
        if not vacancy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Вакансия {request.vacancy_id} не найдена"
            )
        
        # Создаем сервис генерации
        scenario_service = ScenarioGenerationService(db)
        
        # Генерируем сценарий для предварительного просмотра
        from app.services.vacancy_skills_extractor import VacancySkillsExtractor
        skills_extractor = VacancySkillsExtractor()
        
        # Извлекаем навыки
        vacancy_skills = await skills_extractor.extract_skills_from_vacancy(
            vacancy=vacancy,
            force_reload=False
        )
        
        if not vacancy_skills or not vacancy_skills.skills:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удалось извлечь навыки из вакансии"
            )
        
        # Создаем динамические критерии
        dynamic_criteria = await scenario_service._create_dynamic_criteria_from_skills(
            vacancy_skills.skills, request.vacancy_id
        )
        
        # Генерируем сценарий
        scenario_data = await scenario_service._generate_scenario_with_llm(
            vacancy, vacancy_skills.skills, dynamic_criteria
        )
        
        # Формируем ответ
        return ScenarioPreviewResponse(
            scenario_name=scenario_data.get("scenario_name", f"Сценарий для {vacancy.title}"),
            description=scenario_data.get("description", ""),
            nodes=scenario_data.get("nodes", []),
            transitions=scenario_data.get("transitions", []),
            criteria=[DynamicCriteriaResponse.from_orm(c) for c in dynamic_criteria],
            skills_used=[skill.skill_name for skill in vacancy_skills.skills]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка предварительного просмотра: {str(e)}"
        )


@router.post("/{scenario_id}/regenerate", response_model=ScenarioGenerationResponse)
async def regenerate_scenario(
    scenario_id: str,
    db: Session = Depends(get_db)
) -> ScenarioGenerationResponse:
    """
    Перегенерация существующего сценария
    """
    try:
        # Проверяем существование сценария
        scenario = db.query(InterviewScenario).filter(InterviewScenario.id == scenario_id).first()
        if not scenario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Сценарий {scenario_id} не найден"
            )
        
        # Создаем сервис генерации
        scenario_service = ScenarioGenerationService(db)
        
        # Перегенерируем сценарий
        result = await scenario_service.regenerate_scenario(scenario_id)
        
        if not result.get("success", False):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Неизвестная ошибка перегенерации")
            )
        
        return ScenarioGenerationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка перегенерации сценария: {str(e)}"
        )


@router.get("/vacancies/{vacancy_id}/dynamic-criteria", response_model=VacancyDynamicCriteriaResponse)
async def get_vacancy_dynamic_criteria(
    vacancy_id: str,
    db: Session = Depends(get_db)
) -> VacancyDynamicCriteriaResponse:
    """
    Получение динамических критериев для вакансии
    """
    try:
        # Проверяем существование вакансии
        vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
        if not vacancy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Вакансия {vacancy_id} не найдена"
            )
        
        # Получаем динамические критерии
        criteria = db.query(DynamicCriteria).filter(
            DynamicCriteria.vacancy_id == vacancy_id
        ).all()
        
        # Вычисляем статистику
        skills_count = len(criteria)
        mandatory_skills_count = len([c for c in criteria if c.is_mandatory])
        average_importance = sum(c.importance for c in criteria) / skills_count if skills_count > 0 else 0.0
        
        return VacancyDynamicCriteriaResponse(
            vacancy_id=vacancy_id,
            vacancy_title=vacancy.title,
            criteria=[DynamicCriteriaResponse.from_orm(c) for c in criteria],
            skills_count=skills_count,
            mandatory_skills_count=mandatory_skills_count,
            average_importance=average_importance
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения критериев: {str(e)}"
        )





@router.get("/vacancies/{vacancy_id}/scenarios")
async def get_vacancy_scenarios(
    vacancy_id: str,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """
    Получение сценариев для конкретной вакансии
    """
    try:
        # Проверяем существование вакансии
        vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
        if not vacancy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Вакансия {vacancy_id} не найдена"
            )
        
        # Получаем сценарии
        scenarios = db.query(InterviewScenario).filter(
            InterviewScenario.vacancy_id == vacancy_id
        ).all()
        
        # Формируем ответ с дополнительной информацией
        result = []
        for scenario in scenarios:
            # Подсчитываем узлы и переходы
            nodes_count = db.query(ScenarioNode).filter(
                ScenarioNode.scenario_id == scenario.id
            ).count()
            
            transitions_count = db.query(ScenarioTransition).filter(
                ScenarioTransition.scenario_id == scenario.id
            ).count()
            
            # Подсчитываем критерии
            criteria_count = db.query(ScenarioCriteriaMapping).filter(
                ScenarioCriteriaMapping.scenario_id == scenario.id
            ).count()
            
            result.append({
                "id": scenario.id,
                "name": scenario.name,
                "description": scenario.description,
                "is_active": scenario.is_active,
                "version": scenario.version,
                "created_at": scenario.created_at.isoformat() if scenario.created_at else None,
                "updated_at": scenario.updated_at.isoformat() if scenario.updated_at else None,
                "nodes_count": nodes_count,
                "transitions_count": transitions_count,
                "criteria_count": criteria_count,
                "skills_count": criteria_count  # Пока используем количество критериев
            })
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения сценариев: {str(e)}"
        )


@router.get("/{scenario_id}/criteria", response_model=DynamicCriteriaListResponse)
async def get_scenario_criteria(
    scenario_id: str,
    db: Session = Depends(get_db)
) -> DynamicCriteriaListResponse:
    """
    Получение критериев для конкретного сценария
    """
    try:
        # Проверяем существование сценария
        scenario = db.query(InterviewScenario).filter(InterviewScenario.id == scenario_id).first()
        if not scenario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Сценарий {scenario_id} не найден"
            )
        
        # Получаем критерии через маппинги
        criteria_mappings = db.query(ScenarioCriteriaMapping).filter(
            ScenarioCriteriaMapping.scenario_id == scenario_id
        ).all()
        
        criteria_ids = [m.criterion_id for m in criteria_mappings]
        criteria = db.query(DynamicCriteria).filter(
            DynamicCriteria.id.in_(criteria_ids)
        ).all()
        
        return DynamicCriteriaListResponse(
            criteria=[DynamicCriteriaResponse.from_orm(c) for c in criteria],
            total_count=len(criteria),
            vacancy_id=scenario.vacancy_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения критериев сценария: {str(e)}"
        )


@router.delete("/{scenario_id}")
async def delete_scenario(
    scenario_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Удаление сценария интервью
    """
    try:
        # Проверяем существование сценария
        scenario = db.query(InterviewScenario).filter(InterviewScenario.id == scenario_id).first()
        if not scenario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Сценарий {scenario_id} не найден"
            )
        
        # Удаляем сценарий (каскадное удаление узлов, переходов и маппингов)
        db.delete(scenario)
        db.commit()
        
        return {
            "success": True,
            "message": f"Сценарий {scenario_id} успешно удален"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка удаления сценария: {str(e)}"
        )


@router.get("/{scenario_id}/mermaid")
async def get_scenario_mermaid(
    scenario_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Получение сценария в формате Mermaid для визуализации
    """
    try:
        scenario = db.query(InterviewScenario).filter(
            InterviewScenario.id == scenario_id
        ).first()
        
        if not scenario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Сценарий {scenario_id} не найден"
            )
        
        # Получаем узлы сценария
        nodes = db.query(ScenarioNode).filter(
            ScenarioNode.scenario_id == scenario_id
        ).order_by(ScenarioNode.position_x).all()
        
        print(f"DEBUG: Найдено узлов: {len(nodes)}")
        for node in nodes:
            print(f"DEBUG: Узел {node.id} типа {node.node_type}")
        
        # Получаем переходы
        transitions = db.query(ScenarioTransition).filter(
            ScenarioTransition.scenario_id == scenario_id
        ).all()
        
        print(f"DEBUG: Найдено переходов: {len(transitions)}")
        for transition in transitions:
            print(f"DEBUG: Переход {transition.from_node_id} -> {transition.to_node_id}")
        
        # Создаем Mermaid диаграмму
        mermaid_code = _generate_mermaid_diagram(nodes, transitions, scenario)
        print(f"DEBUG: Сгенерированный Mermaid код:\n{mermaid_code}")
        
        return {
            "scenario_id": scenario_id,
            "scenario_name": scenario.name,
            "mermaid_code": mermaid_code,
            "nodes_count": len(nodes),
            "transitions_count": len(transitions)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка генерации диаграммы: {str(e)}"
        )

def _generate_mermaid_diagram(
    nodes: List[ScenarioNode], 
    transitions: List[ScenarioTransition],
    scenario: InterviewScenario
) -> str:
    """
    Генерация Mermaid диаграммы из узлов и переходов
    """
    mermaid_lines = [
        "graph TD",
        f"    %% Сценарий: {scenario.name}",
        ""
    ]
    
    # Добавляем узлы
    for node in nodes:
        node_id = node.id.replace("-", "_").replace(" ", "_")
        node_config = node.node_config or {}
        label = node_config.get("label", f"Узел {node.id}")
        
        if node.node_type == "start":
            safe_label = label.replace("<br/>", "\\n").replace("<", "&lt;").replace(">", "&gt;").replace('"', '&quot;')
            mermaid_lines.append(f'    {node_id}["🎬 {safe_label}"]')
        elif node.node_type == "end":
            safe_label = label.replace("<br/>", "\\n").replace("<", "&lt;").replace(">", "&gt;").replace('"', '&quot;')
            mermaid_lines.append(f'    {node_id}["🏁 {safe_label}"]')
        elif node.node_type == "question":
            # Добавляем информацию о навыках
            target_skills = node_config.get("target_skills", [])
            skills_text = ", ".join(target_skills[:2])  # Показываем первые 2 навыка
            if len(target_skills) > 2:
                skills_text += "..."
            
            weight = node_config.get("weight", 0.5)
            must_have = node_config.get("must_have", False)
            
            icon = "🔴" if must_have else "🟡"
            # Экранируем специальные символы для Mermaid и заменяем HTML теги
            safe_label = label.replace("<br/>", "\\n").replace("<", "&lt;").replace(">", "&gt;").replace('"', '&quot;')
            safe_skills = skills_text.replace("<br/>", "\\n").replace("<", "&lt;").replace(">", "&gt;").replace('"', '&quot;')
            mermaid_lines.append(f'    {node_id}["{icon} {safe_label}\\n💡 {safe_skills}\\n⚖️ {weight}"]')
        else:
            safe_label = label.replace("<br/>", "\\n").replace("<", "&lt;").replace(">", "&gt;").replace('"', '&quot;')
            mermaid_lines.append(f'    {node_id}["❓ {safe_label}"]')
    
    mermaid_lines.append("")
    
    # Добавляем переходы
    if transitions:
        for transition in transitions:
            from_id = transition.from_node_id.replace("-", "_").replace(" ", "_")
            to_id = transition.to_node_id.replace("-", "_").replace(" ", "_")
            
            condition_type = transition.condition_type
            label = transition.transition_label or ""
            safe_label = label.replace("<br/>", "\\n").replace("<", "&lt;").replace(">", "&gt;").replace('"', '&quot;')
            
            if condition_type == "always":
                mermaid_lines.append(f"    {from_id} --> {to_id}")
            elif condition_type == "score_threshold":
                condition_value = transition.condition_value or {}
                min_score = condition_value.get("min_score", 0.7)
                criterion = condition_value.get("criterion", "")
                mermaid_lines.append(f'    {from_id} -->|"{safe_label}\\n📊 ≥{min_score}"| {to_id}')
            elif condition_type == "negative_response":
                mermaid_lines.append(f'    {from_id} -->|"{safe_label}\\n❌ Нет"| {to_id}')
            else:
                mermaid_lines.append(f'    {from_id} -->|"{safe_label}"| {to_id}')
    else:
        # Если переходов нет, создаем последовательные переходы между узлами
        node_ids = []
        for node in nodes:
            node_id = node.id.replace("-", "_").replace(" ", "_")
            node_ids.append(node_id)
        
        # Создаем последовательные переходы
        for i in range(len(node_ids) - 1):
            mermaid_lines.append(f"    {node_ids[i]} --> {node_ids[i+1]}")
    
    return "\n".join(mermaid_lines)


@router.get("/{scenario_id}")
async def get_scenario(
    scenario_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Получение данных сценария интервью
    """
    try:
        # Проверяем существование сценария
        scenario = db.query(InterviewScenario).filter(InterviewScenario.id == scenario_id).first()
        if not scenario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Сценарий {scenario_id} не найден"
            )
        
        # Получаем узлы и переходы
        nodes = db.query(ScenarioNode).filter(ScenarioNode.scenario_id == scenario_id).all()
        transitions = db.query(ScenarioTransition).filter(ScenarioTransition.scenario_id == scenario_id).all()
        
        return {
            "id": scenario.id,
            "name": scenario.name,
            "description": scenario.description,
            "vacancy_id": scenario.vacancy_id,
            "nodes_count": len(nodes),
            "transitions_count": len(transitions),
            "created_at": scenario.created_at,
            "updated_at": scenario.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения данных сценария: {str(e)}"
        )


@router.get("/{scenario_id}/image")
async def get_scenario_image(
    scenario_id: str,
    format: str = Query("png", description="Формат изображения (png, svg, pdf)"),
    db: Session = Depends(get_db)
) -> Response:
    """
    Генерация изображения сценария интервью
    """
    try:
        # Проверяем существование сценария
        scenario = db.query(InterviewScenario).filter(InterviewScenario.id == scenario_id).first()
        if not scenario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Сценарий {scenario_id} не найден"
            )
        
        # Создаем генератор изображений
        image_generator = ScenarioImageGenerator()
        
        # Генерируем изображение
        image_bytes = image_generator.get_image_as_bytes(scenario_id, format, db)
        
        # Определяем MIME тип
        mime_types = {
            "png": "image/png",
            "svg": "image/svg+xml",
            "pdf": "application/pdf"
        }
        
        content_type = mime_types.get(format, "image/png")
        
        return Response(
            content=image_bytes,
            media_type=content_type,
            headers={
                "Content-Disposition": f"inline; filename=scenario_{scenario_id}.{format}"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка генерации изображения: {str(e)}"
        )
