<template>
  <div class="hr-panel">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>HR Панель - Управление интервью</h1>
          <el-button type="primary" @click="refreshData">
            <el-icon><Refresh /></el-icon>
            Обновить
          </el-button>
        </div>
      </el-header>
      
      <el-main>
        <el-row :gutter="20">
          <!-- Statistics Cards -->
          <el-col :span="6" v-for="stat in statistics" :key="stat.title">
            <el-card class="stat-card" shadow="hover">
              <div class="stat-content">
                <div class="stat-icon" :class="stat.type">
                  <el-icon><component :is="stat.icon" /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stat.value }}</div>
                  <div class="stat-title">{{ stat.title }}</div>
                  <div class="stat-change" :class="stat.trend">
                    {{ stat.change }}
                  </div>
                </div>
              </div>
            </el-card>
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
              <el-button type="primary" @click="applyFilters" :loading="loading">
                <el-icon><Search /></el-icon>
                Применить
              </el-button>
              <el-button @click="clearFilters">
                <el-icon><Refresh /></el-icon>
                Очистить
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <!-- Sessions Table -->
        <el-card shadow="never">
          <template #header>
            <div class="table-header">
              <span>Сессии интервью</span>
              <div class="table-actions">
                <el-button type="primary" @click="showCreateSession" size="small">
                  <el-icon><Plus /></el-icon>
                  Новая сессия
                </el-button>
                <el-button @click="refreshData" :loading="loading" size="small">
                  <el-icon><Refresh /></el-icon>
                  Обновить
                </el-button>
                <el-button type="success" @click="exportAllSessions" size="small">
                  <el-icon><Download /></el-icon>
                  Экспорт всех
                </el-button>
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
                <el-button size="small" @click.stop="viewSession(row)">
                  Просмотр
                </el-button>
                <el-button 
                  size="small" 
                  type="success" 
                  @click.stop="exportSession(row)"
                  :disabled="row.status !== 'completed'"
                >
                  Экспорт
                </el-button>
                <el-button 
                  size="small" 
                  type="danger" 
                  @click.stop="deleteSession(row)"
                  :icon="Delete"
                  circle
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
import { Refresh, Download, Delete, Search, Document, Check, Clock, Star, Plus } from '@element-plus/icons-vue'
import SessionDetail from '@/components/SessionDetail.vue'
import CreateSession from '@/components/CreateSession.vue'
import { useHRStore } from '@/stores/hr'

const hrStore = useHRStore()

// Reactive data
const loading = ref(false)
const statistics = ref([
  { title: 'Всего сессий', value: 0, change: '+0%', trend: 'neutral', icon: 'Document', type: 'primary' },
  { title: 'Завершено', value: 0, change: '+0%', trend: 'positive', icon: 'Check', type: 'success' },
  { title: 'В процессе', value: 0, change: '+0%', trend: 'neutral', icon: 'Clock', type: 'warning' },
  { title: 'Средний балл', value: '0%', change: '+0%', trend: 'positive', icon: 'Star', type: 'info' }
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
    statistics.value = [
      { title: 'Total Sessions', value: stats.total_sessions, change: stats.sessions_change, trend: 'neutral' },
      { title: 'Completed', value: stats.completed_sessions, change: stats.completed_change, trend: 'positive' },
      { title: 'In Progress', value: stats.in_progress_sessions, change: stats.progress_change, trend: 'neutral' },
      { title: 'Avg Score', value: `${(stats.avg_score * 100).toFixed(1)}%`, change: stats.score_change, trend: 'positive' }
    ]
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
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.header-content h1 {
  margin: 0;
  color: #303133;
}

.stat-card {
  margin-bottom: 20px;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stat-icon.primary { background-color: #409eff; }
.stat-icon.success { background-color: #67c23a; }
.stat-icon.warning { background-color: #e6a23c; }
.stat-icon.info { background-color: #909399; }

.stat-info {
  flex: 1;
}

.stat-content {
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-title {
  font-size: 0.9rem;
  color: #606266;
  margin-bottom: 4px;
}

.stat-change {
  font-size: 0.8rem;
  font-weight: 500;
}

.stat-change.positive {
  color: #67c23a;
}

.stat-change.negative {
  color: #f56c6c;
}

.stat-change.neutral {
  color: #909399;
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
</style>
