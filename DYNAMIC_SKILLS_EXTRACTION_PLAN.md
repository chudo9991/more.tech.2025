# План реализации динамического извлечения ключевых слов

## Обзор проблемы

**Текущее состояние:**
- Ключевые слова для оценки резюме берутся из **жестко заданного списка IT-навыков** в коде
- Простое текстовое сравнение без семантического анализа
- Ограниченный набор навыков (только IT-сфера)
- Нет весов важности навыков для конкретной вакансии

**Цель:**
- Динамическое извлечение навыков из описания вакансии через LLM
- Семантический анализ соответствия навыков
- Взвешенная оценка с учетом важности навыков
- Расширенная база навыков за пределы IT-сферы
- Контекстный анализ уровня владения навыками

---

## Этап 1: Создание LLM-сервиса для извлечения навыков из вакансии

### 1.1. Новый сервис `VacancySkillsExtractor`

**Файл:** `orchestrator/app/services/vacancy_skills_extractor.py`

```python
class VacancySkillsExtractor:
    async def extract_skills_from_vacancy(self, vacancy: Vacancy) -> Dict[str, Any]:
        """
        Извлекает навыки и требования из описания вакансии через LLM
        """
        # LLM анализирует vacancy.description, vacancy.requirements
        # Возвращает структурированный список навыков с весами важности
```

### 1.2. Расширенная схема навыков

**Файл:** `orchestrator/app/schemas/vacancy_skills.py`

```python
class VacancySkill(BaseModel):
    skill_name: str
    category: str  # "programming", "database", "devops", "soft_skills"
    importance: float  # 0.0-1.0 (важность для вакансии)
    required_level: str  # "beginner", "intermediate", "expert"
    is_mandatory: bool
    alternatives: List[str]  # альтернативные названия навыка
```

**Задачи:**
- [ ] Создать `VacancySkillsExtractor` сервис
- [ ] Создать Pydantic схемы для навыков
- [ ] Реализовать LLM-промпт для извлечения навыков
- [ ] Добавить валидацию извлеченных данных

---

## Этап 2: Улучшение анализа резюме

### 2.1. Расширенный `LLMResumeAnalyzer`

**Файл:** `orchestrator/app/services/llm_resume_analyzer.py` (дополнение)

```python
async def analyze_skill_levels(self, resume_text: str, required_skills: List[VacancySkill]) -> Dict[str, Any]:
    """
    Анализирует уровень владения каждым требуемым навыком
    """
    # LLM оценивает уровень владения каждым навыком
    # Возвращает детальную оценку по каждому навыку
```

### 2.2. Семантический анализ соответствия

```python
async def semantic_skills_matching(self, resume_skills: List[str], required_skills: List[VacancySkill]) -> Dict[str, Any]:
    """
    Семантический анализ соответствия навыков (не просто текстовое сравнение)
    """
    # LLM анализирует семантическое соответствие
    # Учитывает синонимы, альтернативные названия
```

**Задачи:**
- [ ] Добавить метод `analyze_skill_levels` в `LLMResumeAnalyzer`
- [ ] Добавить метод `semantic_skills_matching` в `LLMResumeAnalyzer`
- [ ] Создать промпты для анализа уровня навыков
- [ ] Создать промпты для семантического сопоставления

---

## Этап 3: Обновление системы оценки

### 3.1. Новый `DynamicRelevanceScoringService`

**Файл:** `orchestrator/app/services/dynamic_relevance_scoring_service.py`

```python
class DynamicRelevanceScoringService:
    def __init__(self):
        self.skills_extractor = VacancySkillsExtractor()
        self.llm_analyzer = LLMResumeAnalyzer()
    
    async def calculate_dynamic_score(self, resume: Resume, vacancy: Vacancy) -> Dict[str, Any]:
        # 1. Извлекаем навыки из вакансии
        vacancy_skills = await self.skills_extractor.extract_skills_from_vacancy(vacancy)
        
        # 2. Анализируем навыки в резюме
        resume_skills_analysis = await self.llm_analyzer.analyze_skill_levels(
            resume.extracted_text, vacancy_skills
        )
        
        # 3. Семантическое сопоставление
        skills_matching = await self.llm_analyzer.semantic_skills_matching(
            resume_skills_analysis.skills, vacancy_skills
        )
        
        # 4. Взвешенная оценка с учетом важности навыков
        return self._calculate_weighted_score(vacancy_skills, skills_matching)
```

**Задачи:**
- [ ] Создать `DynamicRelevanceScoringService`
- [ ] Реализовать метод `calculate_dynamic_score`
- [ ] Реализовать метод `_calculate_weighted_score`
- [ ] Интегрировать с существующим `RelevanceScoringService`

---

## Этап 4: API endpoints для новой функциональности

### 4.1. Новые endpoints

**Файл:** `orchestrator/app/api/v1/endpoints/vacancy_skills.py`

```python
@router.post("/vacancies/{vacancy_id}/extract-skills")
async def extract_vacancy_skills(vacancy_id: str, db: Session = Depends(get_db)):
    """Извлекает навыки из описания вакансии"""

@router.post("/resumes/{resume_id}/analyze-skills")
async def analyze_resume_skills(resume_id: str, vacancy_id: str, db: Session = Depends(get_db)):
    """Анализирует навыки резюме относительно вакансии"""

@router.post("/resumes/{resume_id}/semantic-match")
async def semantic_skills_matching(resume_id: str, vacancy_id: str, db: Session = Depends(get_db)):
    """Семантическое сопоставление навыков"""
```

**Задачи:**
- [ ] Создать новый роутер `vacancy_skills.py`
- [ ] Реализовать endpoint для извлечения навыков вакансии
- [ ] Реализовать endpoint для анализа навыков резюме
- [ ] Реализовать endpoint для семантического сопоставления
- [ ] Добавить роутер в `orchestrator/app/api/v1/api.py`

---

## Этап 5: Кэширование и оптимизация

### 5.1. Кэширование извлеченных навыков

**Файл:** `orchestrator/app/services/cache_service.py` (дополнение)

```python
class VacancySkillsCache:
    async def get_vacancy_skills(self, vacancy_id: str) -> Optional[List[VacancySkill]]:
        """Получает кэшированные навыки вакансии"""
    
    async def cache_vacancy_skills(self, vacancy_id: str, skills: List[VacancySkill]):
        """Кэширует навыки вакансии"""
```

### 5.2. Batch обработка

**Файл:** `orchestrator/app/services/batch_skills_analyzer.py`

```python
class BatchSkillsAnalyzer:
    async def analyze_multiple_resumes(self, resume_ids: List[str], vacancy_id: str) -> Dict[str, Any]:
        """Анализирует навыки нескольких резюме одновременно"""
```

**Задачи:**
- [ ] Добавить методы кэширования навыков в `CacheService`
- [ ] Создать `BatchSkillsAnalyzer` для массовой обработки
- [ ] Интегрировать кэширование в `VacancySkillsExtractor`
- [ ] Добавить TTL для кэшированных навыков

---

## Этап 6: Frontend интеграция

### 6.1. Новые компоненты

**Файл:** `frontend/src/components/VacancySkillsDisplay.vue`

```vue
<template>
  <div class="vacancy-skills">
    <h3>Требуемые навыки</h3>
    <el-table :data="skills">
      <el-table-column prop="skill_name" label="Навык" />
      <el-table-column prop="importance" label="Важность" />
      <el-table-column prop="required_level" label="Уровень" />
    </el-table>
  </div>
</template>
```

### 6.2. Обновленная страница резюме

**Файл:** `frontend/src/views/ResumeDetail.vue` (дополнение)

```vue
<template>
  <!-- Добавить секцию анализа навыков -->
  <SkillsAnalysisSection 
    :resume-skills="resumeSkills" 
    :vacancy-skills="vacancySkills"
    :matching-results="matchingResults" 
  />
</template>
```

**Задачи:**
- [ ] Создать компонент `VacancySkillsDisplay.vue`
- [ ] Создать компонент `SkillsAnalysisSection.vue`
- [ ] Обновить `ResumeDetail.vue` для отображения анализа навыков
- [ ] Добавить API вызовы для получения навыков вакансии
- [ ] Добавить визуализацию соответствия навыков

---

## Этап 7: Тестирование и валидация

### 7.1. Unit тесты

**Файл:** `orchestrator/tests/test_vacancy_skills_extractor.py`

```python
class TestVacancySkillsExtractor:
    async def test_extract_skills_from_vacancy(self):
        """Тест извлечения навыков из вакансии"""
    
    async def test_semantic_matching(self):
        """Тест семантического сопоставления"""
```

### 7.2. Integration тесты

**Файл:** `orchestrator/tests/test_dynamic_scoring.py`

```python
class TestDynamicScoring:
    async def test_end_to_end_scoring(self):
        """End-to-end тест динамической оценки"""
```

**Задачи:**
- [ ] Создать unit тесты для `VacancySkillsExtractor`
- [ ] Создать unit тесты для `DynamicRelevanceScoringService`
- [ ] Создать integration тесты для API endpoints
- [ ] Добавить тестовые данные для различных типов вакансий
- [ ] Настроить pytest для новых тестов

---

## Этап 8: Миграция данных

### 8.1. Новые таблицы

**Файл:** `orchestrator/alembic/versions/xxx_add_vacancy_skills.py`

```sql
CREATE TABLE vacancy_skills (
    id SERIAL PRIMARY KEY,
    vacancy_id VARCHAR(50) REFERENCES vacancies(id),
    skill_name VARCHAR(100),
    category VARCHAR(50),
    importance FLOAT,
    required_level VARCHAR(20),
    is_mandatory BOOLEAN,
    alternatives JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE resume_skill_analysis (
    id SERIAL PRIMARY KEY,
    resume_id VARCHAR(50) REFERENCES resumes(id),
    vacancy_id VARCHAR(50) REFERENCES vacancies(id),
    skill_name VARCHAR(100),
    confidence_level FLOAT,
    evidence TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Задачи:**
- [ ] Создать Alembic миграцию для новых таблиц
- [ ] Добавить индексы для оптимизации запросов
- [ ] Создать модели SQLAlchemy для новых таблиц
- [ ] Добавить связи между таблицами
- [ ] Протестировать миграцию на тестовых данных

---

## Этап 9: Документация и мониторинг

### 9.1. API документация

**Файл:** `API_DOCUMENTATION.md` (дополнение)

```markdown
# API_DOCUMENTATION.md
## Vacancy Skills Extraction
POST /api/v1/vacancies/{vacancy_id}/extract-skills
...

## Resume Skills Analysis  
POST /api/v1/resumes/{resume_id}/analyze-skills
...
```

### 9.2. Мониторинг производительности

**Файл:** `orchestrator/app/services/monitoring.py` (дополнение)

```python
class SkillsAnalysisMetrics:
    async def track_extraction_time(self, vacancy_id: str, duration: float):
        """Отслеживает время извлечения навыков"""
    
    async def track_analysis_accuracy(self, resume_id: str, accuracy: float):
        """Отслеживает точность анализа"""
```

**Задачи:**
- [ ] Обновить API документацию
- [ ] Добавить метрики производительности
- [ ] Создать дашборд для мониторинга
- [ ] Добавить логирование для отладки
- [ ] Создать руководство по использованию

---

## Приоритеты реализации

### Высокий приоритет (Этапы 1-3)
- Основная функциональность
- Критически важные компоненты
- Базовая интеграция

### Средний приоритет (Этапы 4-6)
- API endpoints
- Frontend интеграция
- Пользовательский интерфейс

### Низкий приоритет (Этапы 7-9)
- Тестирование
- Документация
- Мониторинг

---

## Ожидаемые результаты

### Функциональные улучшения
✅ **Динамическое извлечение** навыков из описания вакансии
✅ **Семантический анализ** соответствия навыков
✅ **Взвешенная оценка** с учетом важности навыков
✅ **Расширенная база навыков** за пределы IT-сферы
✅ **Контекстный анализ** уровня владения навыками

### Технические улучшения
✅ **Модульная архитектура** с разделением ответственности
✅ **Кэширование** для оптимизации производительности
✅ **Batch обработка** для массового анализа
✅ **Мониторинг** и метрики производительности
✅ **Полное тестирование** всех компонентов

### Пользовательский опыт
✅ **Более точная оценка** соответствия резюме вакансии
✅ **Детальная аналитика** по каждому навыку
✅ **Визуализация** соответствия навыков
✅ **Персонализированные рекомендации** для HR

---

## Следующие шаги

1. **Начать с Этапа 1** - создание `VacancySkillsExtractor`
2. **Создать базовые схемы** данных для навыков
3. **Реализовать LLM-промпты** для извлечения навыков
4. **Протестировать** на существующих вакансиях
5. **Постепенно интегрировать** с существующей системой

---

## Заметки по реализации

- **Совместимость:** Новая система должна работать параллельно со старой
- **Производительность:** Кэширование критически важно для скорости работы
- **Точность:** LLM-промпты должны быть тщательно протестированы
- **Масштабируемость:** Архитектура должна поддерживать рост нагрузки
- **Безопасность:** Валидация всех входных данных обязательна
