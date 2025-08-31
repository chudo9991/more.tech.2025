<template>
  <div class="scenarios-list">
    <!-- Фильтры -->
    <div class="filters-section">
      <el-card class="filter-card">
        <template #header>
          <div class="filter-header">
            <span>Фильтры</span>
            <el-button type="text" @click="clearFilters">Очистить</el-button>
          </div>
        </template>
        
        <el-form :model="filters" label-width="120px" class="filter-form">
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="Вакансия:">
                <el-select 
                  v-model="filters.vacancy_id" 
                  placeholder="Все вакансии"
                  clearable
                  @change="loadScenarios"
                >
                  <el-option 
                    v-for="vacancy in vacancies" 
                    :key="vacancy.id" 
                    :label="vacancy.title" 
                    :value="vacancy.id"
                  />
                </el-select>
              </el-form-item>
            </el-col>
            
            <el-col :span="8">
              <el-form-item label="Название:">
                <el-input 
                  v-model="filters.name" 
                  placeholder="Поиск по названию"
                  clearable
                  @input="debouncedSearch"
                />
              </el-form-item>
            </el-col>
            
            <el-col :span="8">
              <el-form-item label="Статус:">
                <el-select 
                  v-model="filters.status" 
                  placeholder="Все статусы"
                  clearable
                  @change="loadScenarios"
                >
                  <el-option label="Активные" value="active" />
                  <el-option label="Архивные" value="archived" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </el-card>
    </div>

    <!-- Таблица сценариев -->
    <div class="table-section">
      <el-card>
        <template #header>
          <div class="table-header">
            <div class="header-left">
              <h3>Сценарии интервью</h3>
              <el-tag type="info">{{ scenarios.length }} сценариев</el-tag>
            </div>
            <div class="header-actions">
              <el-button type="primary" @click="createScenario">
                <el-icon><Plus /></el-icon>
                Создать сценарий
              </el-button>
            </div>
          </div>
        </template>

        <el-table 
          :data="scenarios" 
          v-loading="loading"
          stripe
          class="scenarios-table"
        >
          <el-table-column prop="name" label="Название" min-width="200">
            <template #default="{ row }">
              <div class="scenario-name">
                <strong>{{ row.name }}</strong>
                <div class="scenario-description">{{ row.description }}</div>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="vacancy_title" label="Вакансия" width="200">
            <template #default="{ row }">
              <el-tag type="primary">{{ row.vacancy_title }}</el-tag>
            </template>
          </el-table-column>

          <el-table-column label="Статистика" width="150">
            <template #default="{ row }">
              <div class="scenario-stats">
                <div class="stat-item">
                  <el-icon><CircleCheck /></el-icon>
                  <span>{{ row.nodes_count }} узлов</span>
                </div>
                <div class="stat-item">
                  <el-icon><Connection /></el-icon>
                  <span>{{ row.transitions_count }} переходов</span>
                </div>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="created_at" label="Создан" width="150">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>

          <el-table-column label="Действия" width="200" fixed="right">
            <template #default="{ row }">
              <el-button-group>
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="viewScenario(row)"
                  title="Просмотр"
                >
                  <el-icon><View /></el-icon>
                </el-button>
                
                                 <el-button 
                   type="warning" 
                   size="small" 
                   @click="recreateTransitions(row)"
                   title="Пересоздать переходы"
                 >
                   <el-icon><Refresh /></el-icon>
                 </el-button>
                 
                 <el-button 
                   type="danger" 
                   size="small" 
                   @click="deleteScenario(row)"
                   title="Удалить"
                 >
                   <el-icon><Delete /></el-icon>
                 </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <!-- Диалог создания сценария -->
    <el-dialog 
      v-model="createDialogVisible" 
      title="Создать сценарий"
      width="600px"
    >
      <el-form :model="newScenario" label-width="120px">
        <el-form-item label="Вакансия:" required>
          <el-select 
            v-model="newScenario.vacancy_id" 
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
        
        <el-form-item label="Название:" required>
          <el-input 
            v-model="newScenario.name" 
            placeholder="Введите название сценария"
          />
        </el-form-item>
        
        <el-form-item label="Описание:">
          <el-input 
            v-model="newScenario.description" 
            type="textarea" 
            :rows="3"
            placeholder="Введите описание сценария"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="createDialogVisible = false">Отмена</el-button>
        <el-button type="primary" @click="submitCreateScenario" :loading="creating">
          Создать
        </el-button>
      </template>
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import ScenarioVisualizer from './ScenarioVisualizer.vue'
import { 
  Plus, View, Delete, Refresh,
  CircleCheck, Connection 
} from '@element-plus/icons-vue'

const router = useRouter()

// Reactive data
const loading = ref(false)
const creating = ref(false)
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
    ElMessage.error('Не удалось загрузить вакансии')
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
    scenarios.value = data.map(scenario => ({
      ...scenario,
      vacancy_title: vacancies.value.find(v => v.id === scenario.vacancy_id)?.title || 'Неизвестная вакансия'
    }))
    console.log('Загружено сценариев:', data.length)
  } catch (error) {
    console.error('Ошибка загрузки сценариев:', error)
    ElMessage.error('Не удалось загрузить сценарии')
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

const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    loadScenarios()
  }, 500)
}

let searchTimeout = null

const createScenario = () => {
  newScenario.vacancy_id = ''
  newScenario.name = ''
  newScenario.description = ''
  createDialogVisible.value = true
}

const submitCreateScenario = async () => {
  if (!newScenario.vacancy_id || !newScenario.name) {
    ElMessage.warning('Заполните обязательные поля')
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
    ElMessage.success('Сценарий успешно создан')
    createDialogVisible.value = false
    loadScenarios()
    
    // Переходим к редактированию созданного сценария
    if (result.scenario_id) {
      router.push(`/scenarios/${result.scenario_id}/edit`)
    }
  } catch (error) {
    console.error('Ошибка создания сценария:', error)
    ElMessage.error(error.message || 'Не удалось создать сценарий')
  } finally {
    creating.value = false
  }
}

const viewScenario = (scenario) => {
  // Открываем визуализацию в диалоге
  selectedScenarioForVisualization.value = scenario
  showVisualizeDialog.value = true
}

const recreateTransitions = async (scenario) => {
  try {
    const confirmed = await ElMessageBox.confirm(
      `Пересоздать переходы для сценария "${scenario.name}"?`,
      'Подтверждение',
      {
        confirmButtonText: 'Да',
        cancelButtonText: 'Отмена',
        type: 'warning'
      }
    )
    
    if (!confirmed) return
    
    const response = await fetch(
      `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/scenarios/${scenario.id}/recreate-transitions`,
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
    
    ElMessage.success(result.message || 'Переходы успешно пересозданы')
    
    // Перезагружаем список сценариев
    await loadScenarios()
    
  } catch (error) {
    console.error('Ошибка пересоздания переходов:', error)
    ElMessage.error(error.message || 'Не удалось пересоздать переходы')
  }
}

const deleteScenario = async (scenario) => {
  try {
    await ElMessageBox.confirm(
      `Вы уверены, что хотите удалить сценарий "${scenario.name}"?`,
      'Подтверждение удаления',
      {
        confirmButtonText: 'Удалить',
        cancelButtonText: 'Отмена',
        type: 'warning'
      }
    )
    
    const response = await fetch(`/api/v1/scenarios/${scenario.id}`, {
      method: 'DELETE'
    })
    
    if (!response.ok) throw new Error('Ошибка удаления сценария')
    
    ElMessage.success('Сценарий успешно удален')
    loadScenarios()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Ошибка удаления сценария:', error)
      ElMessage.error('Не удалось удалить сценарий')
    }
  }
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('ru-RU')
}

// Lifecycle
onMounted(() => {
  loadVacancies()
  loadScenarios()
})
</script>

<style scoped>
.scenarios-list {
  padding: 20px;
}

.filters-section {
  margin-bottom: 20px;
}

.filter-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.filter-card :deep(.el-card__header) {
  background: transparent;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-form {
  margin-top: 10px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-left h3 {
  margin: 0;
  color: #303133;
}

.scenarios-table {
  margin-top: 10px;
}

.scenario-name {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.scenario-description {
  font-size: 12px;
  color: #909399;
  line-height: 1.4;
}

.scenario-stats {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #606266;
}

.stat-item .el-icon {
  font-size: 14px;
  color: #409EFF;
}

/* Responsive design */
@media (max-width: 768px) {
  .scenarios-list {
    padding: 10px;
  }
  
  .table-header {
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
  }
  
  .header-actions {
    display: flex;
    justify-content: center;
  }
}
</style>
