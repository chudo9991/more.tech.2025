<template>
  <div class="hr-panel">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>HR Panel - Interview Management</h1>
          <el-button type="primary" @click="refreshData">
            <el-icon><Refresh /></el-icon>
            Refresh
          </el-button>
        </div>
      </el-header>
      
      <el-main>
        <el-row :gutter="20">
          <!-- Statistics Cards -->
          <el-col :span="6" v-for="stat in statistics" :key="stat.title">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-value">{{ stat.value }}</div>
                <div class="stat-title">{{ stat.title }}</div>
                <div class="stat-change" :class="stat.trend">
                  {{ stat.change }}
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <!-- Filters -->
        <el-card class="filter-card">
          <el-form :model="filters" inline>
            <el-form-item label="Vacancy">
              <el-select v-model="filters.vacancy_id" placeholder="All vacancies" clearable>
                <el-option
                  v-for="vacancy in vacancies"
                  :key="vacancy.id"
                  :label="vacancy.title"
                  :value="vacancy.id"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="Status">
              <el-select v-model="filters.status" placeholder="All statuses" clearable>
                <el-option label="Created" value="created" />
                <el-option label="In Progress" value="in_progress" />
                <el-option label="Completed" value="completed" />
                <el-option label="Failed" value="failed" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="applyFilters">Apply Filters</el-button>
              <el-button @click="clearFilters">Clear</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <!-- Sessions Table -->
        <el-card>
          <template #header>
            <div class="table-header">
              <span>Interview Sessions</span>
              <el-button type="success" @click="exportAllSessions">
                <el-icon><Download /></el-icon>
                Export All
              </el-button>
            </div>
          </template>
          
          <el-table
            :data="sessions"
            v-loading="loading"
            @row-click="viewSession"
            class="sessions-table"
          >
            <el-table-column prop="id" label="Session ID" width="200" />
            <el-table-column prop="vacancy_title" label="Vacancy" />
            <el-table-column prop="phone" label="Phone" width="150" />
            <el-table-column prop="status" label="Status" width="120">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ getStatusLabel(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="current_step" label="Progress" width="120">
              <template #default="{ row }">
                {{ row.current_step }}/{{ row.total_steps }}
              </template>
            </el-table-column>
            <el-table-column prop="total_score" label="Score" width="100">
              <template #default="{ row }">
                <span v-if="row.total_score !== null">
                  {{ (row.total_score * 100).toFixed(1) }}%
                </span>
                <span v-else>-</span>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="Created" width="180">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="Actions" width="200" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click.stop="viewSession(row)">
                  View
                </el-button>
                <el-button 
                  size="small" 
                  type="success" 
                  @click.stop="exportSession(row)"
                  :disabled="row.status !== 'completed'"
                >
                  Export
                </el-button>
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
      title="Session Details"
      width="80%"
      :before-close="closeSessionDialog"
    >
      <SessionDetail
        v-if="sessionDialog.visible"
        :session-id="sessionDialog.sessionId"
        @close="closeSessionDialog"
      />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh, Download } from '@element-plus/icons-vue'
import SessionDetail from '@/components/SessionDetail.vue'
import { useHRStore } from '@/stores/hr'

const hrStore = useHRStore()

// Reactive data
const loading = ref(false)
const sessions = ref([])
const vacancies = ref([])
const statistics = ref([
  { title: 'Total Sessions', value: 0, change: '+0%', trend: 'neutral' },
  { title: 'Completed', value: 0, change: '+0%', trend: 'positive' },
  { title: 'In Progress', value: 0, change: '+0%', trend: 'neutral' },
  { title: 'Avg Score', value: '0%', change: '+0%', trend: 'positive' }
])

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
    sessions.value = response.sessions || []
    pagination.total = response.total || 0
  } catch (error) {
    ElMessage.error('Failed to load sessions')
    console.error('Error loading sessions:', error)
  } finally {
    loading.value = false
  }
}

const loadVacancies = async () => {
  try {
    const response = await hrStore.fetchVacancies()
    vacancies.value = response || []
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
  await Promise.all([
    loadSessions(),
    loadStatistics()
  ])
  ElMessage.success('Data refreshed')
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

const exportSession = async (session) => {
  try {
    const response = await hrStore.exportSession(session.id, 'csv')
    downloadFile(response.content, response.filename)
    ElMessage.success('Session exported successfully')
  } catch (error) {
    ElMessage.error('Failed to export session')
    console.error('Error exporting session:', error)
  }
}

const exportAllSessions = async () => {
  try {
    const response = await hrStore.exportAllSessions('csv')
    downloadFile(response.content, response.filename)
    ElMessage.success('All sessions exported successfully')
  } catch (error) {
    ElMessage.error('Failed to export sessions')
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
    created: 'Created',
    in_progress: 'In Progress',
    completed: 'Completed',
    failed: 'Failed'
  }
  return labels[status] || status
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString()
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    loadSessions(),
    loadVacancies(),
    loadStatistics()
  ])
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
</style>
