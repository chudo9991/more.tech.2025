<template>
  <div class="hr-panel">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>HR Панель - Управление интервью</h1>
          <BaseButton variant="primary" @click="refreshData" :icon="Refresh">
            Обновить
          </BaseButton>
        </div>
      </el-header>
      
      <el-main>
        <el-row :gutter="20" class="stats-row">
          <!-- Statistics Cards -->
          <el-col :span="6" v-for="stat in statistics" :key="stat.title">
            <BaseMetricCard
              :title="stat.title"
              :value="stat.value"
              :icon="stat.icon"
              :variant="stat.type"
            />
          </el-col>
        </el-row>

        <!-- Filters -->
        <el-card class="filter-card" shadow="never">
          <el-form :model="filters" inline>
            <el-form-item label="Вакансия">
              <el-select v-model="filters.vacancy_id" placeholder="Все вакансии" clearable style="width: 250px">
                <el-option
                  v-for="vacancy in vacancies"
                  :key="vacancy.id"
                  :label="vacancy.title"
                  :value="vacancy.id"
                >
                  <div class="vacancy-option">
                    <div class="vacancy-title">{{ vacancy.title }}</div>
                    <div class="vacancy-code" v-if="vacancy.vacancy_code">{{ vacancy.vacancy_code }}</div>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Статус">
              <el-select v-model="filters.status" placeholder="Все статусы" clearable style="width: 150px">
                <el-option label="Создано" value="created" />
                <el-option label="В процессе" value="in_progress" />
                <el-option label="Завершено" value="completed" />
                <el-option label="Неудачно" value="failed" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <BaseButton variant="primary" @click="applyFilters" :loading="loading" :icon="Search" style="margin-right: 1rem;">
                Применить
              </BaseButton>
              <BaseButton @click="clearFilters" variant="ghost" :icon="Refresh">
                Очистить
              </BaseButton>
            </el-form-item>
          </el-form>
        </el-card>

        <!-- Sessions Table -->
        <el-card shadow="never">
          <template #header>
            <div class="table-header">
              <span>Сессии интервью</span>
              <div class="table-actions">
                <BaseButton variant="primary" @click="showCreateSession" size="small" :icon="Plus">
                  Новая сессия
                </BaseButton>
                <BaseButton @click="refreshData" :loading="loading" size="small" variant="secondary" :icon="Refresh">
                  Обновить
                </BaseButton>
                <BaseButton variant="secondary" @click="exportAllSessions" size="small" :icon="Download">
                  Экспорт всех
                </BaseButton>
              </div>
            </div>
          </template>
          
          <el-table
            :data="sessions"
            v-loading="loading"
            @row-click="viewSession"
            class="sessions-table"
          >
            <el-table-column prop="id" label="ID Сессии" width="200" />
            <el-table-column prop="vacancy_title" label="Вакансия" min-width="200">
              <template #default="{ row }">
                <div class="vacancy-info">
                  <div class="vacancy-title">{{ row.vacancy_title || '—' }}</div>
                  <div class="vacancy-code" v-if="row.vacancy_code">{{ row.vacancy_code }}</div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="phone" label="Телефон" width="150" />
            <el-table-column prop="status" label="Статус" width="120">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ getStatusLabel(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="current_step" label="Прогресс" width="120">
              <template #default="{ row }">
                {{ row.current_step }}/{{ row.total_steps }}
              </template>
            </el-table-column>
            <el-table-column prop="total_score" label="Балл" width="100">
              <template #default="{ row }">
                <span v-if="row.total_score !== null">
                  {{ (row.total_score * 100).toFixed(1) }}%
                </span>
                <span v-else>-</span>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="Создано" width="180">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="Действия" width="250" fixed="right">
              <template #default="{ row }">
                <BaseButton size="small" @click.stop="viewSession(row)" variant="primary">
                  Просмотр
                </BaseButton>
                <BaseButton 
                  size="small" 
                  variant="secondary" 
                  @click.stop="exportSession(row)"
                  :disabled="row.status !== 'completed'"
                >
                  Экспорт
                </BaseButton>
                <BaseButton 
                  size="small" 
                  variant="danger" 
                  @click.stop="deleteSession(row)"
                  :icon="Delete"
                />
              </template>
            </el-table-column>
          </el-table>
          
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="pagination.page"
              v-model:page-size="pagination.limit"
              :total="pagination.total"
              :page-sizes="[10, 25, 50, 100]"
              layout="total, sizes, prev, pager, next"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </el-card>
      </el-main>
    </el-container>

    <!-- Session Detail Dialog -->
    <el-dialog
      v-model="sessionDialog.visible"
      title="Детали сессии"
      width="80%"
      :before-close="closeSessionDialog"
    >
      <SessionDetail
        v-if="sessionDialog.visible"
        :session-id="sessionDialog.sessionId"
        @close="closeSessionDialog"
      />
    </el-dialog>

    <!-- Create Session Dialog -->
    <CreateSession
      v-model:visible="createSessionDialog"
      @created="handleSessionCreated"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh, Download, Delete, Search, Plus, Document, Check, Clock, Star } from '@element-plus/icons-vue'
import { BaseButton, BaseMetricCard } from '@/components/base'
import SessionDetail from '@/components/SessionDetail.vue'
import CreateSession from '@/components/CreateSession.vue'
import { useHRStore } from '@/stores/hr'

const hrStore = useHRStore()

// Reactive data
const loading = ref(false)
const statistics = ref([
  { title: 'Всего сессий', value: 42, icon: 'Document', type: 'primary' },
  { title: 'Завершено', value: 28, icon: 'User', type: 'success' },
  { title: 'В процессе', value: 14, icon: 'Briefcase', type: 'warning' },
  { title: 'Средний балл', value: 85, icon: 'Money', type: 'info' }
])

// Use store data
const sessions = computed(() => hrStore.sessions)
const vacancies = computed(() => hrStore.vacancies)

const filters = reactive({
  vacancy_id: null,
  status: null
})

const pagination = reactive({
  page: 1,
  limit: 25,
  total: 0
})

const sessionDialog = reactive({
  visible: false,
  sessionId: null
})

const createSessionDialog = ref(false)

// Computed
const queryParams = computed(() => ({
  skip: (pagination.page - 1) * pagination.limit,
  limit: pagination.limit,
  vacancy_id: filters.vacancy_id || undefined,
  status: filters.status || undefined
}))

// Methods
const loadSessions = async () => {
  try {
    loading.value = true
    const response = await hrStore.fetchSessions(queryParams.value)
    pagination.total = response.total || response.length || 0
  } catch (error) {
    ElMessage.error('Failed to load sessions')
    console.error('Error loading sessions:', error)
  } finally {
    loading.value = false
  }
}

const loadVacancies = async () => {
  try {
    await hrStore.fetchVacancies()
  } catch (error) {
    console.error('Error loading vacancies:', error)
  }
}

const loadStatistics = async () => {
  try {
    const stats = await hrStore.fetchStatistics()
    statistics.value[0].value = stats.total_sessions
    statistics.value[1].value = stats.completed_sessions
    statistics.value[2].value = stats.in_progress_sessions
    statistics.value[3].value = Math.round(stats.avg_score * 100)
  } catch (error) {
    console.error('Error loading statistics:', error)
  }
}

const refreshData = async () => {
  await loadSessions()
  await loadStatistics()
      ElMessage.success('Данные обновлены')
}

const applyFilters = () => {
  pagination.page = 1
  loadSessions()
}

const clearFilters = () => {
  filters.vacancy_id = null
  filters.status = null
  pagination.page = 1
  loadSessions()
}

const handleSizeChange = (size) => {
  pagination.limit = size
  pagination.page = 1
  loadSessions()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  loadSessions()
}

const viewSession = (session) => {
  sessionDialog.sessionId = session.id
  sessionDialog.visible = true
}

const closeSessionDialog = () => {
  sessionDialog.visible = false
  sessionDialog.sessionId = null
}

const showCreateSession = () => {
  createSessionDialog.value = true
}

const handleSessionCreated = (session) => {
  // Refresh sessions list
  loadSessions()
  loadStatistics()
  ElMessage.success('Сессия успешно создана')
}

const exportSession = async (session) => {
  try {
    const response = await hrStore.exportSession(session.id, 'csv')
    downloadFile(response.content, response.filename)
    ElMessage.success('Сессия успешно экспортирована')
  } catch (error) {
    ElMessage.error('Не удалось экспортировать сессию')
    console.error('Error exporting session:', error)
  }
}

const deleteSession = async (session) => {
  try {
    // Show confirmation dialog
    await ElMessageBox.confirm(
      `Вы уверены, что хотите удалить сессию "${session.id}"? Это действие нельзя отменить.`,
      'Подтверждение удаления',
      {
        confirmButtonText: 'Удалить',
        cancelButtonText: 'Отмена',
        type: 'warning',
      }
    )
    
    await hrStore.deleteSession(session.id)
    ElMessage.success('Сессия успешно удалена')
    
    // Refresh data
    await loadSessions()
    await loadStatistics()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Не удалось удалить сессию')
      console.error('Error deleting session:', error)
    }
  }
}

const exportAllSessions = async () => {
  try {
    const response = await hrStore.exportAllSessions('csv')
    downloadFile(response.content, response.filename)
    ElMessage.success('Все сессии успешно экспортированы')
  } catch (error) {
    ElMessage.error('Не удалось экспортировать сессии')
    console.error('Error exporting sessions:', error)
  }
}

const downloadFile = (content, filename) => {
  const blob = new Blob([content], { type: 'text/csv' })
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  window.URL.revokeObjectURL(url)
  document.body.removeChild(a)
}

const getStatusType = (status) => {
  const types = {
    created: 'info',
    in_progress: 'warning',
    completed: 'success',
    failed: 'danger'
  }
  return types[status] || 'info'
}

const getStatusLabel = (status) => {
  const labels = {
    created: 'Создана',
    in_progress: 'В процессе',
    completed: 'Завершена',
    failed: 'Ошибка'
  }
  return labels[status] || status
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString()
}



// Lifecycle
onMounted(async () => {
  await loadVacancies()
  await loadSessions()
  await loadStatistics()
})
</script>

<style scoped>
.hr-panel {
  height: 100vh;
  /* overflow: visible; */
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.header-content {
  padding: 1rem 0;
  margin-bottom: 1rem;
}

.header-content h1 {
  margin: 0;
  color: #00ffff;
  font-size: 2rem;
  font-weight: 700;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}



.filter-card {
  margin-bottom: 20px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sessions-table {
  margin-bottom: 20px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

:deep(.el-table__row) {
  cursor: pointer;
}

:deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

.vacancy-option {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.vacancy-option .vacancy-title {
  font-weight: 500;
  color: #303133;
}

.vacancy-option .vacancy-code {
  font-size: 12px;
  color: #909399;
}

.vacancy-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.vacancy-info .vacancy-title {
  font-weight: 500;
  color: #303133;
}

.vacancy-info .vacancy-code {
  font-size: 12px;
  color: #909399;
}

.table-actions {
  display: flex;
  gap: 8px;
}
</style><style scoped>
/* Fix metric values visibility */
:deep(.metric-value) {
  color: #00ffff !important;
  -webkit-text-fill-color: #00ffff !important;
  background: none !important;
  -webkit-background-clip: unset !important;
  background-clip: unset !important;
}

/* Variant specific colors */
:deep(.metric-card.primary .metric-value) {
  color: #00ffff !important;
  -webkit-text-fill-color: #00ffff !important;
}

:deep(.metric-card.success .metric-value) {
  color: #22c55e !important;
  -webkit-text-fill-color: #22c55e !important;
}

:deep(.metric-card.warning .metric-value) {
  color: #f59e0b !important;
  -webkit-text-fill-color: #f59e0b !important;
}

:deep(.metric-card.info .metric-value) {
  color: #3b82f6 !important;
  -webkit-text-fill-color: #3b82f6 !important;
}
</style>/
* Fix primary button colors in HR Panel */
:deep(.base-button.primary),
:deep(.el-button--primary) {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(138, 43, 226, 0.2)) !important;
  border: 1px solid rgba(0, 255, 255, 0.5) !important;
  color: #00ffff !important;
  box-shadow: 0 8px 32px rgba(0, 255, 255, 0.3) !important;
}

:deep(.base-button.primary:hover),
:deep(.el-button--primary:hover) {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.35), rgba(138, 43, 226, 0.35)) !important;
  border-color: rgba(0, 255, 255, 0.7) !important;
  transform: translateY(-3px) !important;
  box-shadow: 0 12px 40px rgba(0, 255, 255, 0.5) !important;
  text-shadow: 0 0 15px rgba(0, 255, 255, 1) !important;
}

/* Fix ghost/secondary button colors */
:deep(.base-button.ghost),
:deep(.base-button.secondary) {
  background: rgba(15, 23, 42, 0.7) !important;
  border: 1px solid rgba(138, 43, 226, 0.5) !important;
  color: #8a2be2 !important;
  box-shadow: 0 8px 32px rgba(138, 43, 226, 0.2) !important;
}

:deep(.base-button.ghost:hover),
:deep(.base-button.secondary:hover) {
  background: rgba(138, 43, 226, 0.2) !important;
  border-color: rgba(138, 43, 226, 0.7) !important;
  transform: translateY(-3px) !important;
  box-shadow: 0 12px 40px rgba(138, 43, 226, 0.4) !important;
  text-shadow: 0 0 15px rgba(138, 43, 226, 1) !important;
}/* O
verride primary button colors with higher specificity */
.hr-panel :deep(.base-button--primary) {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(138, 43, 226, 0.2)) !important;
  border: 1px solid rgba(0, 255, 255, 0.5) !important;
  color: #00ffff !important;
  box-shadow: 0 8px 32px rgba(0, 255, 255, 0.3) !important;
}

.hr-panel :deep(.base-button--primary:hover) {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.35), rgba(138, 43, 226, 0.35)) !important;
  border-color: rgba(0, 255, 255, 0.7) !important;
  transform: translateY(-3px) !important;
  box-shadow: 0 12px 40px rgba(0, 255, 255, 0.5) !important;
  text-shadow: 0 0 15px rgba(0, 255, 255, 1) !important;
}/*
 Force primary button text color */
.hr-panel :deep(.base-button--primary),
.hr-panel :deep(.base-button--primary *),
.hr-panel :deep(.base-button--primary .button-text),
.hr-panel :deep(.base-button--primary span) {
  color: #00ffff !important;
}

.hr-panel :deep(.base-button--primary:hover),
.hr-panel :deep(.base-button--primary:hover *),
.hr-panel :deep(.base-button--primary:hover .button-text),
.hr-panel :deep(.base-button--primary:hover span) {
  color: #00ffff !important;
}