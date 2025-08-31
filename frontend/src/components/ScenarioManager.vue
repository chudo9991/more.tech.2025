<template>
  <div class="scenario-manager">
    <!-- Заголовок -->
    <div class="scenario-header">
      <h2>Управление сценариями интервью</h2>
      <div class="scenario-actions">
        <el-button 
          type="primary" 
          :icon="Plus"
          @click="showGenerateDialog = true"
          :loading="generating"
        >
          Создать сценарий
        </el-button>
        <el-button 
          type="info" 
          :icon="View"
          @click="previewScenario"
          :disabled="!selectedVacancy"
        >
          Предварительный просмотр
        </el-button>
      </div>
    </div>

    <!-- Выбор вакансии -->
    <div class="vacancy-selector">
      <el-form :model="form" label-width="120px">
        <el-form-item label="Вакансия:">
          <el-select 
            v-model="selectedVacancy" 
            placeholder="Выберите вакансию"
            @change="loadScenarios"
            style="width: 100%"
          >
            <el-option
              v-for="vacancy in vacancies"
              :key="vacancy.id"
              :label="vacancy.title"
              :value="vacancy.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
    </div>

    <!-- Список сценариев -->
    <div class="scenarios-list" v-if="selectedVacancy">
      <el-card v-if="scenarios.length === 0" class="empty-state">
        <el-empty description="Сценарии не найдены">
          <el-button type="primary" @click="showGenerateDialog = true">
            Создать первый сценарий
          </el-button>
        </el-empty>
      </el-card>

      <el-card 
        v-for="scenario in scenarios" 
        :key="scenario.id" 
        class="scenario-card"
        :class="{ 'active': scenario.is_active }"
      >
        <template #header>
          <div class="scenario-card-header">
            <div class="scenario-info">
              <h3>{{ scenario.name }}</h3>
              <p class="scenario-description">{{ scenario.description || 'Описание отсутствует' }}</p>
              <div class="scenario-meta">
                <el-tag :type="scenario.is_active ? 'success' : 'info'">
                  {{ scenario.is_active ? 'Активный' : 'Неактивный' }}
                </el-tag>
                <el-tag type="info">Версия {{ scenario.version }}</el-tag>
                <span class="scenario-date">
                  Создан: {{ formatDate(scenario.created_at) }}
                </span>
              </div>
            </div>
            <div class="scenario-actions">
              <el-button-group>
                <el-button 
                  size="small" 
                  type="primary" 
                  :icon="View"
                  @click="viewScenario(scenario)"
                >
                  Просмотр
                </el-button>
                <el-button 
                  size="small" 
                  type="success" 
                  :icon="DataAnalysis"
                  @click="visualizeScenario(scenario)"
                >
                  Визуализация
                </el-button>
                <el-button 
                  size="small" 
                  type="warning" 
                  :icon="Refresh"
                  @click="regenerateScenario(scenario)"
                  :loading="regenerating === scenario.id"
                >
                  Перегенерировать
                </el-button>
                <el-button 
                  size="small" 
                  type="danger" 
                  :icon="Delete"
                  @click="deleteScenario(scenario)"
                >
                  Удалить
                </el-button>
              </el-button-group>
            </div>
          </div>
        </template>

        <div class="scenario-stats">
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="stat-item">
                <div class="stat-value">{{ scenario.nodes_count || 0 }}</div>
                <div class="stat-label">Узлов</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-item">
                <div class="stat-value">{{ scenario.transitions_count || 0 }}</div>
                <div class="stat-label">Переходов</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-item">
                <div class="stat-value">{{ scenario.criteria_count || 0 }}</div>
                <div class="stat-label">Критериев</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-item">
                <div class="stat-value">{{ scenario.skills_count || 0 }}</div>
                <div class="stat-label">Навыков</div>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-card>
    </div>

    <!-- Диалог генерации сценария -->
    <el-dialog 
      v-model="showGenerateDialog" 
      title="Создание сценария интервью"
      width="600px"
    >
      <el-form :model="generateForm" label-width="140px">
        <el-form-item label="Вакансия:" required>
          <el-select 
            v-model="generateForm.vacancy_id" 
            placeholder="Выберите вакансию"
            style="width: 100%"
          >
            <el-option
              v-for="vacancy in vacancies"
              :key="vacancy.id"
              :label="vacancy.title"
              :value="vacancy.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Название сценария:">
          <el-input 
            v-model="generateForm.scenario_name" 
            placeholder="Введите название сценария"
          />
        </el-form-item>
        <el-form-item label="Описание:">
          <el-input 
            v-model="generateForm.description" 
            type="textarea" 
            :rows="3"
            placeholder="Введите описание сценария"
          />
        </el-form-item>
        <el-form-item label="Принудительная перегенерация:">
          <el-switch v-model="generateForm.force_regenerate" />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showGenerateDialog = false">Отмена</el-button>
          <el-button 
            type="primary" 
            @click="generateScenario"
            :loading="generating"
          >
            Создать сценарий
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- Диалог предварительного просмотра -->
    <el-dialog 
      v-model="showPreviewDialog" 
      title="Предварительный просмотр сценария"
      width="800px"
    >
      <div v-if="previewData" class="preview-content">
        <h3>{{ previewData.scenario_name }}</h3>
        <p>{{ previewData.description }}</p>
        
        <el-divider>Навыки для оценки</el-divider>
        <el-tag 
          v-for="skill in previewData.skills_used" 
          :key="skill"
          class="skill-tag"
        >
          {{ skill }}
        </el-tag>

        <el-divider>Критерии оценки</el-divider>
        <div class="criteria-list">
          <el-card 
            v-for="criterion in previewData.criteria" 
            :key="criterion.id"
            class="criterion-card"
          >
            <div class="criterion-header">
              <h4>{{ criterion.skill_name }}</h4>
              <el-tag :type="criterion.is_mandatory ? 'danger' : 'info'">
                {{ criterion.is_mandatory ? 'Обязательный' : 'Дополнительный' }}
              </el-tag>
            </div>
            <p>{{ criterion.description }}</p>
            <div class="criterion-meta">
              <span>Важность: {{ (criterion.importance * 100).toFixed(0) }}%</span>
              <span>Уровень: {{ criterion.required_level }}</span>
              <span>Категория: {{ criterion.category }}</span>
            </div>
          </el-card>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showPreviewDialog = false">Закрыть</el-button>
          <el-button 
            type="primary" 
            @click="generateFromPreview"
            :loading="generating"
          >
            Создать сценарий
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- Диалог просмотра сценария -->
    <el-dialog 
      v-model="showViewDialog" 
      title="Просмотр сценария"
      width="1000px"
    >
      <div v-if="selectedScenario" class="scenario-view">
        <h3>{{ selectedScenario.name }}</h3>
        <p>{{ selectedScenario.description }}</p>
        
        <el-divider>Структура сценария</el-divider>
        <div class="scenario-structure">
          <!-- Здесь будет визуализация узлов и переходов -->
          <el-alert
            title="Визуализация сценария"
            description="Функция визуализации структуры сценария будет добавлена в следующих этапах"
            type="info"
            show-icon
          />
        </div>
      </div>
    </el-dialog>

    <!-- Диалог визуализации сценария -->
    <el-dialog 
      v-model="showVisualizeDialog" 
      title="Визуализация сценария"
      width="90%"
      :fullscreen="true"
    >
      <ScenarioVisualizer 
        v-if="selectedScenarioForVisualization"
        :scenario-id="selectedScenarioForVisualization.id"
        @error="(error) => ElMessage.error(error)"
      />
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showVisualizeDialog = false">Закрыть</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, View, Refresh, Delete, DataAnalysis } from '@element-plus/icons-vue'
import { useHRStore } from '@/stores/hr'
import ScenarioVisualizer from './ScenarioVisualizer.vue'

// Store
const hrStore = useHRStore()

// Reactive data
const selectedVacancy = ref(null)
const scenarios = ref([])
const vacancies = ref([])
const generating = ref(false)
const regenerating = ref(null)
const showGenerateDialog = ref(false)
const showPreviewDialog = ref(false)
const showViewDialog = ref(false)
const showVisualizeDialog = ref(false)
const selectedScenario = ref(null)
const selectedScenarioForVisualization = ref(null)
const previewData = ref(null)

// Forms
const form = reactive({})
const generateForm = reactive({
  vacancy_id: '',
  scenario_name: '',
  description: '',
  force_regenerate: false
})

// Methods
const loadVacancies = async () => {
  try {
    const response = await hrStore.fetchVacancies()
    vacancies.value = response || []
    console.log('Загружено вакансий:', vacancies.value.length)
  } catch (error) {
    console.error('Ошибка загрузки вакансий:', error)
    ElMessage.error('Не удалось загрузить вакансии')
  }
}

const loadScenarios = async () => {
  if (!selectedVacancy.value) return
  
  try {
    // Загружаем сценарии для выбранной вакансии
    const response = await hrStore.getVacancyScenarios(selectedVacancy.value)
    scenarios.value = response || []
    console.log('Загружено сценариев:', scenarios.value.length)
  } catch (error) {
    console.error('Ошибка загрузки сценариев:', error)
    // Если API еще не реализован, используем заглушку
    scenarios.value = []
  }
}

const generateScenario = async () => {
  if (!generateForm.vacancy_id) {
    ElMessage.warning('Выберите вакансию')
    return
  }

  generating.value = true
  try {
    const result = await hrStore.generateScenario(generateForm.vacancy_id, generateForm)

    if (result.success) {
      ElMessage.success('Сценарий успешно создан!')
      showGenerateDialog.value = false
      loadScenarios()
      
      // Обновляем форму
      generateForm.vacancy_id = ''
      generateForm.scenario_name = ''
      generateForm.description = ''
      generateForm.force_regenerate = false
    } else {
      ElMessage.error(result.error || 'Ошибка создания сценария')
    }
  } catch (error) {
    console.error('Ошибка генерации сценария:', error)
    ElMessage.error('Не удалось создать сценарий')
  } finally {
    generating.value = false
  }
}

const previewScenario = async () => {
  if (!selectedVacancy.value) {
    ElMessage.warning('Выберите вакансию')
    return
  }

  try {
    // Находим выбранную вакансию для получения названия
    const selectedVacancyData = vacancies.value.find(v => v.id === selectedVacancy.value)
    const scenarioName = selectedVacancyData ? `Сценарий для ${selectedVacancyData.title}` : 'Новый сценарий'
    
    const result = await hrStore.previewScenario(selectedVacancy.value, {
      scenario_name: scenarioName,
      description: `Автоматически сгенерированный сценарий для вакансии ${selectedVacancyData?.title || ''}`
    })
    previewData.value = result
    showPreviewDialog.value = true
  } catch (error) {
    console.error('Ошибка предварительного просмотра:', error)
    ElMessage.error('Не удалось загрузить предварительный просмотр')
  }
}

const generateFromPreview = async () => {
  if (!previewData.value) return

  generateForm.vacancy_id = selectedVacancy.value
  generateForm.scenario_name = previewData.value.scenario_name
  generateForm.description = previewData.value.description
  
  showPreviewDialog.value = false
  await generateScenario()
}

const regenerateScenario = async (scenario) => {
  try {
    await ElMessageBox.confirm(
      'Вы уверены, что хотите перегенерировать этот сценарий? Все существующие данные будут удалены.',
      'Подтверждение',
      {
        confirmButtonText: 'Да',
        cancelButtonText: 'Отмена',
        type: 'warning'
      }
    )

    regenerating.value = scenario.id
    const result = await hrStore.regenerateScenario(scenario.id)

    if (result.success) {
      ElMessage.success('Сценарий успешно перегенерирован!')
      loadScenarios()
    } else {
      ElMessage.error(result.error || 'Ошибка перегенерации сценария')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Ошибка перегенерации сценария:', error)
      ElMessage.error('Не удалось перегенерировать сценарий')
    }
  } finally {
    regenerating.value = null
  }
}

const visualizeScenario = (scenario) => {
  selectedScenarioForVisualization.value = scenario
  showVisualizeDialog.value = true
}

const deleteScenario = async (scenario) => {
  try {
    await ElMessageBox.confirm(
      'Вы уверены, что хотите удалить этот сценарий?',
      'Подтверждение',
      {
        confirmButtonText: 'Да',
        cancelButtonText: 'Отмена',
        type: 'warning'
      }
    )

    const result = await hrStore.deleteScenario(scenario.id)

    if (result.success) {
      ElMessage.success('Сценарий успешно удален!')
      loadScenarios()
    } else {
      ElMessage.error('Ошибка удаления сценария')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Ошибка удаления сценария:', error)
      ElMessage.error('Не удалось удалить сценарий')
    }
  }
}

const viewScenario = (scenario) => {
  selectedScenario.value = scenario
  showViewDialog.value = true
}

const formatDate = (dateString) => {
  if (!dateString) return 'Не указано'
  return new Date(dateString).toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Lifecycle
onMounted(() => {
  loadVacancies()
})
</script>

<style scoped>
.scenario-manager {
  padding: 20px;
}

.scenario-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.scenario-header h2 {
  margin: 0;
  color: #2c3e50;
}

.scenario-actions {
  display: flex;
  gap: 10px;
}

.vacancy-selector {
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.scenarios-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.empty-state {
  text-align: center;
  padding: 40px;
}

.scenario-card {
  transition: all 0.3s ease;
}

.scenario-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.scenario-card.active {
  border-left: 4px solid #67c23a;
}

.scenario-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.scenario-info h3 {
  margin: 0 0 10px 0;
  color: #2c3e50;
}

.scenario-description {
  margin: 0 0 15px 0;
  color: #666;
  font-size: 14px;
}

.scenario-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.scenario-date {
  font-size: 12px;
  color: #999;
}

.scenario-stats {
  margin-top: 15px;
}

.stat-item {
  text-align: center;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 6px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}

.stat-label {
  font-size: 12px;
  color: #666;
  margin-top: 5px;
}

.preview-content h3 {
  margin: 0 0 10px 0;
  color: #2c3e50;
}

.skill-tag {
  margin: 5px;
}

.criteria-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.criterion-card {
  margin-bottom: 10px;
}

.criterion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.criterion-header h4 {
  margin: 0;
  color: #2c3e50;
}

.criterion-meta {
  display: flex;
  gap: 20px;
  margin-top: 10px;
  font-size: 12px;
  color: #666;
}

.scenario-structure {
  margin-top: 20px;
}

.dialog-footer {
  text-align: right;
}
</style>
