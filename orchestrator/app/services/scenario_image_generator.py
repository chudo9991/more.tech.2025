"""
Сервис для генерации изображений сценариев интервью
"""
import os
import tempfile
import subprocess
from typing import List, Dict, Any, Optional
from pathlib import Path

from app.models import InterviewScenario, ScenarioNode, ScenarioTransition
from app.services.scenario_generation_service import ScenarioGenerationService


class ScenarioImageGenerator:
    """
    Генератор изображений для сценариев интервью
    """
    
    def __init__(self, db_session=None):
        self.db_session = db_session
        self.scenario_service = ScenarioGenerationService(db_session) if db_session else None
    
    def generate_dot_code(self, scenario: InterviewScenario, nodes: List[ScenarioNode], transitions: List[ScenarioTransition]) -> str:
        """
        Генерирует DOT код для Graphviz из данных сценария
        """
        dot_lines = [
            "digraph scenario {",
            "    rankdir=TB;",
            "    node [shape=box, style=filled, fontname=\"Arial\", fontsize=10];",
            "    edge [fontname=\"Arial\", fontsize=8];",
            "",
            f"    // Сценарий: {scenario.name}",
            ""
        ]
        
        # Добавляем узлы
        for node in nodes:
            node_id = self._sanitize_id(node.id)
            node_config = node.node_config or {}
            label = node_config.get("label", f"Узел {node.id}")
            
            # Определяем стиль узла
            if node.node_type == "start":
                dot_lines.append(f'    {node_id} [label="🎬 {label}", fillcolor="#e1f5fe", color="#0277bd"];')
            elif node.node_type == "end":
                dot_lines.append(f'    {node_id} [label="🏁 {label}", fillcolor="#f3e5f5", color="#7b1fa2"];')
            elif node.node_type == "question":
                # Добавляем информацию о навыках
                target_skills = node_config.get("target_skills", [])
                skills_text = ", ".join(target_skills[:2])  # Показываем первые 2 навыка
                if len(target_skills) > 2:
                    skills_text += "..."
                
                weight = node_config.get("weight", 0.5)
                must_have = node_config.get("must_have", False)
                
                icon = "🔴" if must_have else "🟡"
                color = "#ffebee" if must_have else "#fff3e0"
                border_color = "#c62828" if must_have else "#ef6c00"
                
                dot_lines.append(f'    {node_id} [label="\\n{icon} {label}\\n💡 {skills_text}\\n⚖️ {weight}", fillcolor="{color}", color="{border_color}"];')
            else:
                dot_lines.append(f'    {node_id} [label="❓ {label}", fillcolor="#f5f5f5", color="#757575"];')
        
        dot_lines.append("")
        
        # Добавляем переходы
        if transitions:
            for transition in transitions:
                from_id = self._sanitize_id(transition.from_node_id)
                to_id = self._sanitize_id(transition.to_node_id)
                
                condition_type = transition.condition_type
                label = transition.transition_label or ""
                
                if condition_type == "always":
                    dot_lines.append(f"    {from_id} -> {to_id};")
                elif condition_type == "score_threshold":
                    condition_value = transition.condition_value or {}
                    min_score = condition_value.get("min_score", 0.7)
                    criterion = condition_value.get("criterion", "")
                    dot_lines.append(f'    {from_id} -> {to_id} [label="📊 ≥{min_score}"];')
                elif condition_type == "negative_response":
                    dot_lines.append(f'    {from_id} -> {to_id} [label="❌ Нет"];')
                else:
                    dot_lines.append(f'    {from_id} -> {to_id} [label="{label}"];')
        else:
            # Если переходов нет, создаем последовательные переходы между узлами
            node_ids = []
            for node in nodes:
                node_id = self._sanitize_id(node.id)
                node_ids.append(node_id)
            
            # Создаем последовательные переходы
            for i in range(len(node_ids) - 1):
                dot_lines.append(f"    {node_ids[i]} -> {node_ids[i+1]};")
        
        dot_lines.append("}")
        
        return "\n".join(dot_lines)
    
    def _sanitize_id(self, node_id: str) -> str:
        """
        Очищает ID узла для использования в DOT
        """
        return node_id.replace("-", "_").replace(" ", "_").replace(".", "_")
    
    def generate_image(self, scenario: InterviewScenario, nodes: List[ScenarioNode], transitions: List[ScenarioTransition], 
                      format: str = "png", output_path: Optional[str] = None) -> str:
        """
        Генерирует изображение сценария
        
        Args:
            scenario: Сценарий интервью
            nodes: Узлы сценария
            transitions: Переходы между узлами
            format: Формат изображения (png, svg, pdf)
            output_path: Путь для сохранения (если None, создается временный файл)
            
        Returns:
            Путь к сгенерированному изображению
        """
        try:
            # Генерируем DOT код
            dot_code = self.generate_dot_code(scenario, nodes, transitions)
            
            # Создаем временный DOT файл
            with tempfile.NamedTemporaryFile(mode='w', suffix='.dot', delete=False) as dot_file:
                dot_file.write(dot_code)
                dot_file_path = dot_file.name
            
            # Определяем путь для выходного файла
            if output_path is None:
                with tempfile.NamedTemporaryFile(suffix=f'.{format}', delete=False) as output_file:
                    output_path = output_file.name
            
            # Запускаем Graphviz
            cmd = ["dot", "-T", format, "-o", output_path, dot_file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Удаляем временный DOT файл
            os.unlink(dot_file_path)
            
            if result.returncode != 0:
                raise Exception(f"Graphviz error: {result.stderr}")
            
            return output_path
            
        except subprocess.TimeoutExpired:
            raise Exception("Timeout generating image")
        except Exception as e:
            raise Exception(f"Error generating image: {str(e)}")
    
    def generate_scenario_image(self, scenario_id: str, format: str = "png", db_session=None) -> str:
        """
        Генерирует изображение для сценария по ID
        
        Args:
            scenario_id: ID сценария
            format: Формат изображения
            db_session: Сессия базы данных
            
        Returns:
            Путь к сгенерированному изображения
        """
        if not db_session:
            raise Exception("Database session is required")
        
        # Получаем данные сценария напрямую из БД
        scenario = db_session.query(InterviewScenario).filter(InterviewScenario.id == scenario_id).first()
        if not scenario:
            raise Exception(f"Scenario {scenario_id} not found")
        
        nodes = db_session.query(ScenarioNode).filter(ScenarioNode.scenario_id == scenario_id).all()
        transitions = db_session.query(ScenarioTransition).filter(ScenarioTransition.scenario_id == scenario_id).all()
        
        # Генерируем изображение
        return self.generate_image(scenario, nodes, transitions, format)
    
    def get_image_as_bytes(self, scenario_id: str, format: str = "png", db_session=None) -> bytes:
        """
        Возвращает изображение сценария как bytes
        
        Args:
            scenario_id: ID сценария
            format: Формат изображения
            db_session: Сессия базы данных
            
        Returns:
            Байты изображения
        """
        image_path = self.generate_scenario_image(scenario_id, format, db_session)
        
        try:
            with open(image_path, 'rb') as f:
                return f.read()
        finally:
            # Удаляем временный файл
            if os.path.exists(image_path):
                os.unlink(image_path)
