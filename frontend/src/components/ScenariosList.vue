<template>
  <div class="scenarios-list">
    <!-- Header -->
    <PageHeader
      title="Сценарии интервью"
      :subtitle="`${scenarios.length} сценариев`"
    >
      <template #actions>
        <BaseButton
          variant="secondary"
          icon="mdi mdi-refresh"
          :loading="loading"
          @click="loadScenarios"
        >
          Обновить
        </BaseButton>
        <BaseButton
          variant="primary"
          icon="mdi mdi-plus"
          @click="createScenario"
        >
          Создать сценарий
        </BaseButton>
      </template>
    </PageHeader>

    <!-- Main Content -->
    <div class="page-content">
      <!-- Фильтры -->
      <section class="filters-section">
        <BaseCard padding="lg" variant="outlined">
          <template #header>
            <div class="filters-header">
              <h3 class="filters-title">Фильтры</h3>
              <BaseButton
                variant="secondary"
                size="sm"
                icon="mdi mdi-filter-off"
                @click="clearFilters"
                :disabled="!hasActiveFilters"
              >
                Очистить
              </BaseButton>
            </div>
          </template>

          <div class="filters-content">
            <div class="filter-group">
              <label class="filter-label">Вакансия</label>
              <BaseSelect
                v-model="filters.vacancy_id"
                placeholder="Все вакансии"
                :options="vacancyOptions"
                clearable
                @change="loadScenarios"
              />
            </div>

            <div class="filter-group">
              <label class="filter-label">Поиск по названию</label>
              <BaseInput
                v-model="filters.name"
                placeholder="Введите название..."
                icon="mdi mdi-magnify"
                @input="debouncedSearch"
              />
            </div>

            <div class="filter-group">
              <label class="filter-label">Статус</label>
              <BaseSelect
                v-model="filters.status"
                placeholder="Все статусы"
                :options="statusOptions"
                clearable
                @change="loadScenarios"
              />
            </div>
          </div>
        </BaseCard>
      </section>

      <!-- Список сценариев -->
      <section class="scenarios-section">
        <!-- Loading State -->
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner">
            <i class="mdi mdi-loading animate-spin text-4xl text-cyan-400"></i>
            <p class="loading-text">Загрузка сценариев...</p>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="scenarios.length === 0" class="empty-state">
          <div class="empty-icon">
            <i class="mdi mdi-script-text-outline text-6xl text-slate-400"></i>
          </div>
          <h3 class="empty-title">Сценарии не найдены</h3>
          <p class="empty-description">
            {{ hasActiveFilters ? 'Попробуйте изменить фильтры поиска' : 'Создайте первый сценарий для начала работы' }}
          </p>
          <BaseButton
            v-if="!hasActiveFilters"
            variant="primary"
            icon="mdi mdi-plus"
            @click="createScenario"
          >
            Создать сценарий
          </BaseButton>
        </div>

        <!-- Scenarios Grid -->
        <div v-else class="scenarios-grid">
          <BaseCard
            v-for="scenario in scenarios"
            :key="scenario.id"
            class="scenario-card"
            padding="lg"
            variant="elevated"
          >
            <template #header>
              <div class="scenario-header">
                <div class="scenario-info">
                  <h3 class="scenario-title">{{ scenario.name }}</h3>
                  <p class="scenario-description">
                    {{ scenario.description || 'Описание отсутствует' }}
                  </p>
                </div>
                <div class="scenario-status">
                  <span 
                    class="status-badge"
                    :class="scenario.is_active ? 'status-active' : 'status-inactive'"
                  >
                    {{ scenario.is_active ? 'Активный' : 'Неактивный' }}
                  </span>
                </div>
              </div>
            </template>

            <div class="scenario-content">
              <!-- Вакансия -->
              <div class="scenario-vacancy">
                <div class="vacancy-icon">
                  <i class="mdi mdi-briefcase text-cyan-400"></i>
                </div>
                <div class="vacancy-info">
                  <p class="vacancy-title">{{ scenario.vacancy_title }}</p>
                  <p class="vacancy-label">Вакансия</p>
                </div>
              </div>

              <!-- Статистика -->
              <div class="scenario-stats">
                <div class="stat-item">
                  <div class="stat-value">{{ scenario.nodes_count || 0 }}</div>
                  <div class="stat-label">Узлов</div>
                </div>
                <div class="stat-item">
                  <div class="stat-value">{{ scenario.transitions_count || 0 }}</div>
                  <div class="stat-label">Переходов</div>
                </div>
              </div>

              <!-- Дата создания -->
              <div class="scenario-date">
                <i class="mdi mdi-calendar text-slate-400"></i>
                <span>Создан: {{ formatDate(scenario.created_at) }}</span>
              </div>

              <!-- Действия -->
              <div class="scenario-actions">
                <BaseButton
                  variant="primary"
                  size="sm"
                  icon="mdi mdi-eye"
                  @click="viewScenario(scenario)"
                >
                  Просмотр
                </BaseButton>
                <BaseButton
                  variant="secondary"
                  size="sm"
                  icon="mdi mdi-refresh"
                  @click="recreateTransitions(scenario)"
                  :loading="regenerating === scenario.id"
                />
                <BaseButton
                  variant="secondary"
                  size="sm"
                  icon="mdi mdi-delete"
                  @click="deleteScenario(scenario)"
                />
              </div>
            </div>
          </BaseCard>
        </div>
      </section>
    </div>

    <!-- Модальное окно создания сценария -->
    <div v-if="createDialogVisible" class="modal-overlay" @click="createDialogVisible = false">
      <div class="modal-container" @click.stop>
        <BaseCard padding="lg" variant="elevated">
          <template #header>
            <div class="modal-header">
              <h3 class="modal-title">Создать сценарий</h3>
              <BaseButton
                variant="secondary"
                size="sm"
                icon="mdi mdi-close"
                @click="createDialogVisible = false"
              />
            </div>
          </template>

          <div class="modal-content">
            <div class="form-group">
              <label class="form-label">Вакансия <span class="required">*</span></label>
              <BaseSelect
                v-model="newScenario.vacancy_id"
                placeholder="Выберите вакансию"
                :options="vacancyOptions"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Название <span class="required">*</span></label>
              <BaseInput
                v-model="newScenario.name"
                placeholder="Введите название сценария"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Описание</label>
              <BaseInput
                v-model="newScenario.description"
                type="textarea"
                :rows="3"
                placeholder="Введите описание сценария"
              />
            </div>
          </div>

          <div class="modal-actions">
            <BaseButton
              variant="secondary"
              @click="createDialogVisible = false"
            >
              Отмена
            </BaseButton>
            <BaseButton
              variant="primary"
              @click="submitCreateScenario"
              :loading="creating"
            >
              Создать
            </BaseButton>
          </div>
        </BaseCard>
      </div>
    </div>

    <!-- Модальное окно визуализации -->
    <div v-if="showVisualizeDialog" class="modal-overlay" @click="showVisualizeDialog = false">
      <div class="modal-container modal-large" @click.stop>
        <BaseCard padding="lg" variant="elevated">
          <template #header>
            <div class="modal-header">
              <h3 class="modal-title">Визуализация сценария</h3>
              <BaseButton
                variant="secondary"
                size="sm"
                icon="mdi mdi-close"
                @click="showVisualizeDialog = false"
              />
            </div>
          </template>

          <div class="modal-content">
            <ScenarioVisualizer 
              v-if="selectedScenarioForVisualization"
              :scenario-id="selectedScenarioForVisualization.id"
              @error="handleVisualizationError"
            />
          </div>
        </BaseCard>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
// @ts-ignore
import { useRouter } from 'vue-router'
import BaseCard from './base/BaseCard.vue'
import BaseButton from './base/BaseButton.vue'
import BaseSelect from './base/BaseSelect.vue'
import BaseInput from './base/BaseInput.vue'
import PageHeader from './layout/PageHeader.vue'
import ScenarioVisualizer from './ScenarioVisualizer.vue'

const router = useRouter()

// Reactive data
const loading = ref(false)
const creating = ref(false)
const regenerating = ref<string | null>(null)
const scenarios = ref([])
const vacancies = ref([])
const createDialogVisible = ref(false)
const showVisualizeDialog = ref(false)
const selectedScenarioForVisualization = ref(null)

const filters = reactive({
  vacancy_id: '',
  name: '',
  status: ''
})

const newScenario = reactive({
  vacancy_id: '',
  name: '',
  description: ''
})

// Computed properties
const vacancyOptions = computed(() => 
  vacancies.value.map((vacancy: any) => ({
    value: vacancy.id,
    label: vacancy.title
  }))
)

const statusOptions = [
  { value: 'active', label: 'Активные' },
  { value: 'archived', label: 'Архивные' }
]

const hasActiveFilters = computed(() => 
  filters.vacancy_id || filters.name || filters.status
)

// Methods
const loadVacancies = async () => {
  try {
    const response = await fetch('/api/v1/vacancies/')
    if (!response.ok) throw new Error('Ошибка загрузки вакансий')
    
    const data = await response.json()
    vacancies.value = data
    console.log('Загружено вакансий:', data.length)
  } catch (error) {
    console.error('Ошибка загрузки вакансий:', error)
    showErrorMessage('Не удалось загрузить вакансии')
  }
}

const loadScenarios = async () => {
  loading.value = true
  try {
    let url = '/api/v1/scenarios/'
    const params = new URLSearchParams()
    
    if (filters.vacancy_id) {
      params.append('vacancy_id', filters.vacancy_id)
    }
    if (filters.name) {
      params.append('name', filters.name)
    }
    if (filters.status) {
      params.append('status', filters.status)
    }
    
    if (params.toString()) {
      url += '?' + params.toString()
    }
    
    const response = await fetch(url)
    if (!response.ok) throw new Error('Ошибка загрузки сценариев')
    
    const data = await response.json()
    scenarios.value = data.map((scenario: any) => ({
      ...scenario,
      vacancy_title: (vacancies.value.find((v: any) => v.id === scenario.vacancy_id) as any)?.title || 'Неизвестная вакансия'
    }))
    console.log('Загружено сценариев:', data.length)
  } catch (error) {
    console.error('Ошибка загрузки сценариев:', error)
    showErrorMessage('Не удалось загрузить сценарии')
  } finally {
    loading.value = false
  }
}

const clearFilters = () => {
  filters.vacancy_id = ''
  filters.name = ''
  filters.status = ''
  loadScenarios()
}

let searchTimeout: NodeJS.Timeout | null = null
const debouncedSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    loadScenarios()
  }, 500)
}

const createScenario = () => {
  newScenario.vacancy_id = ''
  newScenario.name = ''
  newScenario.description = ''
  createDialogVisible.value = true
}

const submitCreateScenario = async () => {
  if (!newScenario.vacancy_id || !newScenario.name) {
    showErrorMessage('Заполните обязательные поля')
    return
  }
  
  creating.value = true
  try {
    const response = await fetch('/api/v1/scenarios/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        vacancy_id: newScenario.vacancy_id,
        scenario_name: newScenario.name,
        description: newScenario.description
      })
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Ошибка создания сценария')
    }
    
    const result = await response.json()
    showSuccessMessage('Сценарий успешно создан')
    createDialogVisible.value = false
    loadScenarios()
    
    // Переходим к редактированию созданного сценария
    if (result.scenario_id) {
      router.push(`/scenarios/${result.scenario_id}/edit`)
    }
  } catch (error) {
    console.error('Ошибка создания сценария:', error)
    showErrorMessage((error as Error).message || 'Не удалось создать сценарий')
  } finally {
    creating.value = false
  }
}

const viewScenario = (scenario: any) => {
  // Открываем визуализацию в диалоге
  selectedScenarioForVisualization.value = scenario
  showVisualizeDialog.value = true
}

const recreateTransitions = async (scenario: any) => {
  if (!confirm(`Пересоздать переходы для сценария "${scenario.name}"?`)) {
    return
  }

  regenerating.value = scenario.id
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL || ''}/api/v1/scenarios/${scenario.id}/recreate-transitions`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Ошибка пересоздания переходов')
    }
    
    const result = await response.json()
    showSuccessMessage(result.message || 'Переходы успешно пересозданы')
    
    // Перезагружаем список сценариев
    await loadScenarios()
    
  } catch (error) {
    console.error('Ошибка пересоздания переходов:', error)
    showErrorMessage((error as Error).message || 'Не удалось пересоздать переходы')
  } finally {
    regenerating.value = null
  }
}

const deleteScenario = async (scenario: any) => {
  if (!confirm(`Вы уверены, что хотите удалить сценарий "${scenario.name}"?`)) {
    return
  }

  try {
    const response = await fetch(`/api/v1/scenarios/${scenario.id}`, {
      method: 'DELETE'
    })
    
    if (!response.ok) throw new Error('Ошибка удаления сценария')
    
    showSuccessMessage('Сценарий успешно удален')
    loadScenarios()
  } catch (error) {
    console.error('Ошибка удаления сценария:', error)
    showErrorMessage('Не удалось удалить сценарий')
  }
}

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('ru-RU')
}

// Utility functions
const showSuccessMessage = (message: string) => {
  // Можно заменить на toast notification
  console.log('Success:', message)
}

const showErrorMessage = (message: string) => {
  // Можно заменить на toast notification
  console.error('Error:', message)
}

const handleVisualizationError = (error: string) => {
  showErrorMessage(error)
}

// Lifecycle
onMounted(() => {
  loadVacancies()
  loadScenarios()
})
</script>

<style scoped>
/* Scenarios List Styles */
.scenarios-list {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #0f172a 50%, #1e293b 75%, #0f172a 100%);
  position: relative;
  overflow-x: hidden;
}

.scenarios-list::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 80%, rgba(0, 255, 255, 0.1) 0%, transparent 60%),
    radial-gradient(circle at 80% 20%, rgba(138, 43, 226, 0.1) 0%, transparent 60%),
    radial-gradient(circle at 40% 40%, rgba(75, 0, 130, 0.08) 0%, transparent 50%);
  pointer-events: none;
  z-index: -1;
}

.page-content {
  position: relative;
  z-index: 2;
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
}

/* Filters Section */
.filters-section {
  margin-bottom: 2rem;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filters-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0;
}

.filters-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #cbd5e1;
}

/* Loading State */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-text {
  color: #94a3b8;
  font-size: 1rem;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(0, 255, 255, 0.1);
}

.empty-icon {
  margin-bottom: 1.5rem;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 0.5rem;
}

.empty-description {
  color: #94a3b8;
  margin-bottom: 2rem;
  font-size: 1rem;
}

/* Scenarios Grid */
.scenarios-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.scenario-card {
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 255, 255, 0.1);
}

.scenario-card:hover {
  transform: translateY(-4px);
  border-color: rgba(0, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
}

.scenario-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.scenario-info {
  flex: 1;
  min-width: 0;
}

.scenario-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
}

.scenario-description {
  font-size: 0.875rem;
  color: #94a3b8;
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.scenario-status {
  flex-shrink: 0;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-active {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.status-inactive {
  background: rgba(148, 163, 184, 0.1);
  color: #94a3b8;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.scenario-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.scenario-vacancy {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 8px;
  border: 1px solid rgba(0, 255, 255, 0.1);
}

.vacancy-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  background: rgba(0, 255, 255, 0.1);
  border-radius: 6px;
}

.vacancy-info {
  flex: 1;
  min-width: 0;
}

.vacancy-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: #e2e8f0;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.vacancy-label {
  font-size: 0.75rem;
  color: #94a3b8;
  margin: 0;
}

.scenario-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 8px;
  border: 1px solid rgba(0, 255, 255, 0.1);
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #00ffff;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.75rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.scenario-date {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: #94a3b8;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
}

.scenario-actions {
  display: flex;
  gap: 0.5rem;
  padding-top: 0.75rem;
}

.scenario-actions .btn {
  flex: 1;
}

.scenario-actions .btn:not(:first-child) {
  flex: 0 0 auto;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-container {
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-large {
  max-width: 1200px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0;
}

.modal-content {
  margin: 1.5rem 0;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #cbd5e1;
  margin-bottom: 0.5rem;
}

.required {
  color: #ef4444;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-content {
    padding: 1rem;
  }
  
  .filters-content {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .scenarios-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .scenario-actions {
    flex-direction: column;
  }
  
  .scenario-actions .btn {
    flex: 1;
  }
  
  .modal-container {
    margin: 0.5rem;
    max-width: none;
  }
}

@media (max-width: 480px) {
  .scenario-stats {
    grid-template-columns: 1fr;
  }
  
  .scenario-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
}

/* Animations */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>