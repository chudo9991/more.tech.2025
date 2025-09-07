<template>
  <div class="hr-panel">
    <!-- Header -->
    <PageHeader
      title="HR Панель"
      subtitle="Управление интервью и аналитика"
    >
      <template #actions>
        <BaseButton
          variant="secondary"
          icon="mdi mdi-refresh"
          :loading="loading"
          @click="refreshData"
        >
          Обновить
        </BaseButton>
        <BaseButton
          variant="primary"
          icon="mdi mdi-plus"
          @click="showCreateSession"
        >
          Новая сессия
        </BaseButton>
      </template>
    </PageHeader>

    <!-- Main Content -->
    <div class="panel-content">
      <!-- Statistics Dashboard -->
      <section class="stats-section">
        <div class="stats-grid">
          <BaseMetricCard
            v-for="(stat, index) in statistics"
            :key="stat.title"
            :title="stat.title"
            :value="stat.value"
            :icon="stat.icon"
            :variant="stat.type"
            :change="stat.change"
            :trend="stat.trend"
            :class="{ 'animate-fade-in-up': statsVisible }"
            :style="{ animationDelay: `${index * 100}ms` }"
          />
        </div>
      </section>

      <!-- Filters Section -->
      <section class="filters-section">
        <BaseCard padding="md" variant="outlined" class="filters-card">
          <template #header>
            <div class="filters-header">
              <h3 class="filters-title">Фильтры и поиск</h3>
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
              <label class="filter-label">Поиск по телефону или ID</label>
              <BaseInput
                v-model="filters.search"
                placeholder="Введите телефон или ID сессии"
                icon="mdi mdi-magnify"
                @input="debouncedSearch"
              />
            </div>

            <div class="filter-group">
              <label class="filter-label">Вакансия</label>
              <BaseSelect
                v-model="filters.vacancy_id"
                placeholder="Все вакансии"
                :options="vacancyOptions"
                clearable
              />
            </div>

            <div class="filter-group">
              <label class="filter-label">Статус</label>
              <BaseSelect
                v-model="filters.status"
                placeholder="Все статусы"
                :options="statusOptions"
                clearable
              />
            </div>

            <div class="filter-group">
              <label class="filter-label">Период</label>
              <BaseSelect
                v-model="filters.period"
                placeholder="Все время"
                :options="periodOptions"
                clearable
              />
            </div>

            <div class="filter-actions">
              <BaseButton
                variant="primary"
                icon="mdi mdi-filter-check"
                :loading="loading"
                @click="applyFilters"
              >
                Применить фильтры
              </BaseButton>
            </div>
          </div>
        </BaseCard>
      </section>

      <!-- Sessions Table -->
      <section class="table-section">
        <BaseCard padding="md" variant="elevated" class="table-card">
          <template #header>
            <div class="table-header">
              <div class="table-title-section">
                <h3 class="table-title">Сессии интервью</h3>
                <div class="table-meta">
                  <span class="sessions-count">{{ pagination.total }} сессий</span>
                  <div class="view-options">
                    <BaseButton
                      variant="secondary"
                      size="sm"
                      :icon="viewMode === 'table' ? 'mdi mdi-view-grid' : 'mdi mdi-view-list'"
                      @click="toggleViewMode"
                    >
                      {{ viewMode === 'table' ? 'Карточки' : 'Таблица' }}
                    </BaseButton>
                  </div>
                </div>
              </div>
              <div class="table-actions">
                <BaseButton
                  variant="secondary"
                  size="sm"
                  icon="mdi mdi-download"
                  @click="exportAllSessions"
                  :loading="exportLoading"
                >
                  Экспорт всех
                </BaseButton>
                <BaseButton
                  variant="secondary"
                  size="sm"
                  icon="mdi mdi-refresh"
                  :loading="loading"
                  @click="refreshData"
                >
                  Обновить
                </BaseButton>
              </div>
            </div>
          </template>

          <!-- Table View -->
          <div v-if="viewMode === 'table'" class="table-container">
            <div v-if="loading" class="loading-container">
              <div class="loading-spinner">
                <i class="mdi mdi mdi-loading animate-spin text-4xl text-primary-500"></i>
                <p class="loading-text">Загрузка сессий...</p>
              </div>
            </div>

            <div v-else-if="sessions.length === 0" class="empty-state">
              <div class="empty-icon">
                <i class="mdi mdi mdi-clipboard-text-outline text-6xl text-neutral-400"></i>
              </div>
              <h3 class="empty-title">Сессии не найдены</h3>
              <p class="empty-description">
                {{ hasActiveFilters ? 'Попробуйте изменить фильтры поиска' : 'Создайте первую сессию интервью' }}
              </p>
              <BaseButton
                v-if="!hasActiveFilters"
                variant="primary"
                icon="mdi mdi-plus"
                @click="showCreateSession"
              >
                Создать сессию
              </BaseButton>
            </div>

            <div v-else class="sessions-table">
              <div class="table-responsive">
                <table class="data-table">
                  <thead>
                    <tr>
                      <th class="sortable" @click="sortBy('id')">
                        ID Сессии
                        <i :class="getSortIcon('id')"></i>
                      </th>
                      <th class="sortable" @click="sortBy('vacancy_title')">
                        Вакансия
                        <i :class="getSortIcon('vacancy_title')"></i>
                      </th>
                      <th>Кандидат</th>
                      <th class="sortable" @click="sortBy('status')">
                        Статус
                        <i :class="getSortIcon('status')"></i>
                      </th>
                      <th>Прогресс</th>
                      <th class="sortable" @click="sortBy('total_score')">
                        Оценка
                        <i :class="getSortIcon('total_score')"></i>
                      </th>
                      <th class="sortable" @click="sortBy('created_at')">
                        Создано
                        <i :class="getSortIcon('created_at')"></i>
                      </th>
                      <th class="actions-column">Действия</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="session in sessions"
                      :key="session.id"
                      class="table-row"
                      @click="viewSession(session)"
                    >
                      <td class="session-id">
                        <span class="id-text">{{ session.id }}</span>
                      </td>
                      <td class="vacancy-cell">
                        <div class="vacancy-info">
                          <div class="vacancy-title">{{ session.vacancy_title || '—' }}</div>
                          <div v-if="session.vacancy_code" class="vacancy-code">{{ session.vacancy_code }}</div>
                        </div>
                      </td>
                      <td class="candidate-cell">
                        <div class="candidate-info">
                          <div class="candidate-phone">{{ session.phone }}</div>
                          <div v-if="session.candidate_name" class="candidate-name">{{ session.candidate_name }}</div>
                        </div>
                      </td>
                      <td class="status-cell">
                        <div class="status-badge" :class="getStatusClass(session.status)">
                          <i :class="getStatusIcon(session.status)"></i>
                          {{ getStatusLabel(session.status) }}
                        </div>
                      </td>
                      <td class="progress-cell">
                        <div class="progress-info">
                          <div class="progress-text">{{ session.current_step }}/{{ session.total_steps }}</div>
                          <div class="progress-bar">
                            <div 
                              class="progress-fill" 
                              :style="{ width: `${(session.current_step / session.total_steps) * 100}%` }"
                            ></div>
                          </div>
                        </div>
                      </td>
                      <td class="score-cell">
                        <div v-if="session.total_score !== null" class="score-info">
                          <div class="score-value" :class="getScoreClass(session.total_score)">
                            {{ (session.total_score * 100).toFixed(1) }}%
                          </div>
                          <div class="score-bar">
                            <div 
                              class="score-fill" 
                              :class="getScoreClass(session.total_score)"
                              :style="{ width: `${session.total_score * 100}%` }"
                            ></div>
                          </div>
                        </div>
                        <span v-else class="no-score">—</span>
                      </td>
                      <td class="date-cell">
                        <div class="date-info">
                          <div class="date-text">{{ formatDate(session.created_at) }}</div>
                          <div class="time-text">{{ formatTime(session.created_at) }}</div>
                        </div>
                      </td>
                      <td class="actions-cell" @click.stop>
                        <div class="action-buttons">
                          <BaseButton
                            variant="secondary"
                            size="sm"
                            icon="mdi mdi-eye"
                            @click="viewSession(session)"
                          />
                          <BaseButton
                            variant="secondary"
                            size="sm"
                            icon="mdi mdi-download"
                            :disabled="session.status !== 'completed'"
                            @click="exportSession(session)"
                          />
                          <BaseButton
                            variant="secondary"
                            size="sm"
                            icon="mdi mdi-delete"
                            @click="deleteSession(session)"
                          />
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Card View -->
          <div v-else class="cards-container">
            <div v-if="loading" class="loading-container">
              <div class="loading-spinner">
                <i class="mdi mdi mdi-loading animate-spin text-4xl text-primary-500"></i>
                <p class="loading-text">Загрузка сессий...</p>
              </div>
            </div>

            <div v-else-if="sessions.length === 0" class="empty-state">
              <div class="empty-icon">
                <i class="mdi mdi mdi-clipboard-text-outline text-6xl text-neutral-400"></i>
              </div>
              <h3 class="empty-title">Сессии не найдены</h3>
              <p class="empty-description">
                {{ hasActiveFilters ? 'Попробуйте изменить фильтры поиска' : 'Создайте первую сессию интервью' }}
              </p>
            </div>

            <div v-else class="sessions-grid">
              <SessionCard
                v-for="session in sessions"
                :key="session.id"
                :session="session"
                @view="viewSession"
                @export="exportSession"
                @delete="deleteSession"
              />
            </div>
          </div>

          <!-- Pagination -->
          <div v-if="sessions.length > 0" class="pagination-container">
            <div class="pagination-info">
              <span class="pagination-text">
                Показано {{ ((pagination.page - 1) * pagination.limit) + 1 }}-{{ Math.min(pagination.page * pagination.limit, pagination.total) }} 
                из {{ pagination.total }} сессий
              </span>
            </div>
            <div class="pagination-controls">
              <BaseButton
                variant="secondary"
                size="sm"
                icon="mdi mdi-chevron-left"
                :disabled="pagination.page === 1"
                @click="handleCurrentChange(pagination.page - 1)"
              />
              <div class="page-numbers">
                <BaseButton
                  v-for="page in visiblePages"
                  :key="page"
                  :variant="page === pagination.page ? 'primary' : 'ghost'"
                  size="sm"
                  @click="handleCurrentChange(page)"
                >
                  {{ page }}
                </BaseButton>
              </div>
              <BaseButton
                variant="secondary"
                size="sm"
                icon="mdi mdi-chevron-right"
                :disabled="pagination.page === totalPages"
                @click="handleCurrentChange(pagination.page + 1)"
              />
              <BaseSelect
                v-model="pagination.limit"
                :options="pageSizeOptions"
                size="sm"
                @change="handleSizeChange"
              />
            </div>
          </div>
        </BaseCard>
      </section>
    </div>

    <!-- Session Detail Modal -->
    <HRModal
      v-model="sessionDialog.visible"
      title="Детали сессии"
      size="xl"
      @close="closeSessionDialog"
    >
      <SessionDetail
        v-if="sessionDialog.visible"
        :session-id="sessionDialog.sessionId"
        @close="closeSessionDialog"
      />
    </HRModal>

    <!-- Create Session Modal -->
    <HRModal
      v-model="createSessionDialog"
      title="Создание новой сессии"
      size="lg"
      @close="createSessionDialog = false"
    >
      <CreateSession
        v-if="createSessionDialog"
        @created="handleSessionCreated"
        @close="createSessionDialog = false"
      />
    </HRModal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch } from 'vue'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import BaseSelect from '@/components/base/BaseSelect.vue'
import BaseMetricCard from '@/components/base/BaseMetricCard.vue'
import HRModal from '@/components/HRModal.vue'
import SessionCard from '@/components/SessionCard.vue'
import SessionDetail from '@/components/SessionDetail.vue'
import CreateSession from '@/components/CreateSession.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import { useHRStore } from '@/stores/hr'

// Types
interface SessionFilters {
  search: string
  vacancy_id: string | null
  status: string | null
  period: string | null
}

interface Pagination {
  page: number
  limit: number
  total: number
}

interface SessionDialog {
  visible: boolean
  sessionId: string | null
}

interface Statistic {
  title: string
  value: string | number
  change: string
  trend: 'positive' | 'negative' | 'neutral'
  icon: string
  type: 'primary' | 'success' | 'warning' | 'info'
}

const hrStore = useHRStore()

// Reactive data
const loading = ref(false)
const exportLoading = ref(false)
const statsVisible = ref(false)
const viewMode = ref<'table' | 'cards'>('table')
const sortField = ref<string>('')
const sortDirection = ref<'asc' | 'desc'>('desc')

const statistics = ref<Statistic[]>([
  { 
    title: 'Всего сессий', 
    value: 0, 
    change: '+0%', 
    trend: 'neutral', 
    icon: 'mdi mdi-clipboard-text-multiple', 
    type: 'primary' 
  },
  { 
    title: 'Завершено', 
    value: 0, 
    change: '+0%', 
    trend: 'positive', 
    icon: 'mdi mdi-check-circle', 
    type: 'success' 
  },
  { 
    title: 'В процессе', 
    value: 0, 
    change: '+0%', 
    trend: 'neutral', 
    icon: 'mdi mdi-clock-outline', 
    type: 'warning' 
  },
  { 
    title: 'Средний балл', 
    value: '0.0%', 
    change: '+0%', 
    trend: 'positive', 
    icon: 'mdi mdi-star', 
    type: 'info' 
  }
])

// Use store data
const sessions = computed(() => hrStore.sessions)
const vacancies = computed(() => hrStore.vacancies)

const filters = reactive<SessionFilters>({
  search: '',
  vacancy_id: null,
  status: null,
  period: null
})

const pagination = reactive<Pagination>({
  page: 1,
  limit: 25,
  total: 0
})

const sessionDialog = reactive<SessionDialog>({
  visible: false,
  sessionId: null
})

const createSessionDialog = ref(false)

// Debounced search
let searchTimeout: NodeJS.Timeout | null = null
const debouncedSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    applyFilters()
  }, 500)
}

// Options for selects
const vacancyOptions = computed(() => 
  vacancies.value.map((vacancy: any) => ({
    value: vacancy.id,
    label: vacancy.title,
    description: vacancy.vacancy_code
  }))
)

const statusOptions = [
  { value: 'created', label: 'Создано' },
  { value: 'in_progress', label: 'В процессе' },
  { value: 'completed', label: 'Завершено' },
  { value: 'failed', label: 'Неудачно' }
]

const periodOptions = [
  { value: 'today', label: 'Сегодня' },
  { value: 'week', label: 'Эта неделя' },
  { value: 'month', label: 'Этот месяц' },
  { value: 'quarter', label: 'Этот квартал' },
  { value: 'year', label: 'Этот год' }
]

const pageSizeOptions = [
  { value: 10, label: '10 на странице' },
  { value: 25, label: '25 на странице' },
  { value: 50, label: '50 на странице' },
  { value: 100, label: '100 на странице' }
]

// Computed
const queryParams = computed(() => ({
  skip: (pagination.page - 1) * pagination.limit,
  limit: pagination.limit,
  vacancy_id: filters.vacancy_id || undefined,
  status: filters.status || undefined,
  search: filters.search || undefined,
  period: filters.period || undefined,
  sort_field: sortField.value || undefined,
  sort_direction: sortDirection.value || undefined
}))

const hasActiveFilters = computed(() => 
  filters.search || filters.vacancy_id || filters.status || filters.period
)

const totalPages = computed(() => 
  Math.ceil(pagination.total / pagination.limit)
)

const visiblePages = computed(() => {
  const current = pagination.page
  const total = totalPages.value
  const delta = 2
  const range = []
  
  for (let i = Math.max(2, current - delta); i <= Math.min(total - 1, current + delta); i++) {
    range.push(i)
  }
  
  if (current - delta > 2) {
    range.unshift('...')
  }
  if (current + delta < total - 1) {
    range.push('...')
  }
  
  range.unshift(1)
  if (total > 1) {
    range.push(total)
  }
  
  return range.filter((item, index, arr) => arr.indexOf(item) === index)
})

// Methods
const loadSessions = async () => {
  try {
    loading.value = true
    const response = await hrStore.fetchSessions(queryParams.value)
    pagination.total = response.total || response.length || 0
  } catch (error) {
    console.error('Error loading sessions:', error)
    // Show user-friendly error message
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
      { 
        title: 'Всего сессий', 
        value: stats.total_sessions || 0, 
        change: stats.sessions_change || '+0%', 
        trend: 'neutral',
        icon: 'mdi mdi-clipboard-text-multiple',
        type: 'primary'
      },
      { 
        title: 'Завершено', 
        value: stats.completed_sessions || 0, 
        change: stats.completed_change || '+0%', 
        trend: 'positive',
        icon: 'mdi mdi-check-circle',
        type: 'success'
      },
      { 
        title: 'В процессе', 
        value: stats.in_progress_sessions || 0, 
        change: stats.progress_change || '+0%', 
        trend: 'neutral',
        icon: 'mdi mdi-clock-outline',
        type: 'warning'
      },
      { 
        title: 'Средний балл', 
        value: `${((stats.avg_score || 0) * 100).toFixed(1)}%`, 
        change: stats.score_change || '+0%', 
        trend: 'positive',
        icon: 'mdi mdi-star',
        type: 'info'
      }
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
}

const applyFilters = () => {
  pagination.page = 1
  loadSessions()
}

const clearFilters = () => {
  filters.search = ''
  filters.vacancy_id = null
  filters.status = null
  filters.period = null
  pagination.page = 1
  loadSessions()
}

const handleSizeChange = (size: number) => {
  pagination.limit = size
  pagination.page = 1
  loadSessions()
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  loadSessions()
}

const sortBy = (field: string) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortDirection.value = 'desc'
  }
  loadSessions()
}

const getSortIcon = (field: string) => {
  if (sortField.value !== field) return 'mdi mdi mdi-sort text-neutral-400'
  return sortDirection.value === 'asc' 
    ? 'mdi mdi mdi-sort-ascending text-primary-500' 
    : 'mdi mdi mdi-sort-descending text-primary-500'
}

const toggleViewMode = () => {
  viewMode.value = viewMode.value === 'table' ? 'cards' : 'table'
}

const viewSession = (session: any) => {
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

const handleSessionCreated = () => {
  createSessionDialog.value = false
  loadSessions()
  loadStatistics()
}

const exportSession = async (session: any) => {
  try {
    exportLoading.value = true
    const response = await hrStore.exportSession(session.id, 'csv')
    downloadFile(response.content, response.filename)
  } catch (error) {
    console.error('Error exporting session:', error)
  } finally {
    exportLoading.value = false
  }
}

const deleteSession = async (session: any) => {
  try {
    // Show confirmation - in a real app, use a proper confirmation modal
    if (confirm(`Вы уверены, что хотите удалить сессию "${session.id}"?`)) {
      await hrStore.deleteSession(session.id)
      await loadSessions()
      await loadStatistics()
    }
  } catch (error) {
    console.error('Error deleting session:', error)
  }
}

const exportAllSessions = async () => {
  try {
    exportLoading.value = true
    const response = await hrStore.exportAllSessions('csv')
    downloadFile(response.content, response.filename)
  } catch (error) {
    console.error('Error exporting sessions:', error)
  } finally {
    exportLoading.value = false
  }
}

const downloadFile = (content: string, filename: string) => {
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

const getStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    created: 'status-created',
    in_progress: 'status-progress',
    completed: 'status-completed',
    failed: 'status-failed'
  }
  return classes[status] || 'status-created'
}

const getStatusIcon = (status: string) => {
  const icons: Record<string, string> = {
    created: 'mdi mdi mdi-clock-outline',
    in_progress: 'mdi mdi mdi-play-circle',
    completed: 'mdi mdi mdi-check-circle',
    failed: 'mdi mdi mdi-alert-circle'
  }
  return icons[status] || 'mdi mdi mdi-help-circle'
}

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    created: 'Создана',
    in_progress: 'В процессе',
    completed: 'Завершена',
    failed: 'Ошибка'
  }
  return labels[status] || status
}

const getScoreClass = (score: number) => {
  if (score >= 0.8) return 'score-excellent'
  if (score >= 0.6) return 'score-good'
  if (score >= 0.4) return 'score-average'
  return 'score-poor'
}

const getTrendIcon = (trend: string) => {
  const icons: Record<string, string> = {
    positive: 'mdi mdi mdi-trending-up',
    negative: 'mdi mdi mdi-trending-down',
    neutral: 'mdi mdi mdi-trending-neutral'
  }
  return icons[trend] || 'mdi mdi mdi-trending-neutral'
}

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('ru-RU')
}

const formatTime = (dateString: string) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleTimeString('ru-RU', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

// Watchers
watch(() => filters.vacancy_id, () => {
  if (filters.vacancy_id !== null) {
    applyFilters()
  }
})

watch(() => filters.status, () => {
  if (filters.status !== null) {
    applyFilters()
  }
})

watch(() => filters.period, () => {
  if (filters.period !== null) {
    applyFilters()
  }
})

// Lifecycle
onMounted(async () => {
  // Trigger stats animation
  setTimeout(() => {
    statsVisible.value = true
  }, 200)
  
  // Load data
  await loadVacancies()
  await loadSessions()
  await loadStatistics()
})
</script>

<style scoped>
/* HR Panel Styles */
.hr-panel {
  min-height: 100vh;
  background: #f8fafc;
}

/* Main Content */
.panel-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}


/* Statistics Section */
.stats-section {
  margin-bottom: 1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}



.stat-content {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.stat-icon {
  width: 4rem;
  height: 4rem;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  font-size: 1.75rem;
  position: relative;
  overflow: hidden;
}

.stat-icon::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: inherit;
  filter: blur(8px);
  opacity: 0.3;
  z-index: -1;
}

.stat-icon.primary { 
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.3), rgba(138, 43, 226, 0.3)); 
  border: 1px solid rgba(0, 255, 255, 0.4);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}
.stat-icon.success { 
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.3), rgba(0, 200, 150, 0.3)); 
  border: 1px solid rgba(0, 255, 255, 0.4);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}
.stat-icon.warning { 
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.3), rgba(255, 152, 0, 0.3)); 
  border: 1px solid rgba(255, 193, 7, 0.4);
  box-shadow: 0 0 20px rgba(255, 193, 7, 0.3);
}
.stat-icon.info { 
  background: linear-gradient(135deg, rgba(138, 43, 226, 0.3), rgba(75, 0, 130, 0.3)); 
  border: 1px solid rgba(138, 43, 226, 0.4);
  box-shadow: 0 0 20px rgba(138, 43, 226, 0.3);
}

.stat-info {
  flex: 1;
  min-width: 0;
}

.stat-value {
  font-size: 1.875rem;
  font-weight: 700;
  color: #00ffff;
  margin-bottom: 0.25rem;
  line-height: 1;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
}

.stat-title {
  font-size: 0.875rem;
  color: #e2e8f0;
  margin-bottom: 0.25rem;
  font-weight: 500;
}

.stat-change {
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.stat-change.positive { color: #00ffff; }
.stat-change.negative { color: #ff1493; }
.stat-change.neutral { color: #e2e8f0; }

/* Filters Section */
.filters-section {
  margin-bottom: 1rem;
}

.filters-card {
  background: rgba(15, 23, 42, 0.4) !important;
  border: 1px solid rgba(0, 255, 255, 0.2) !important;
  backdrop-filter: blur(20px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.filters-card :deep(.card-header) {
  background: rgba(0, 255, 255, 0.05) !important;
  border-bottom: 1px solid rgba(0, 255, 255, 0.1) !important;
  padding: 1.5rem !important;
}

.filters-card :deep(.card-content) {
  background: transparent !important;
  padding: 2.5rem !important;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0;
  padding: 0 0.5rem;
}

.filters-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0;
}

.table-card {
  background: rgba(15, 23, 42, 0.4) !important;
  border: 1px solid rgba(0, 255, 255, 0.2) !important;
  backdrop-filter: blur(20px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.table-card :deep(.card-header) {
  background: rgba(0, 255, 255, 0.05) !important;
  border-bottom: 1px solid rgba(0, 255, 255, 0.1) !important;
  padding: 2.5rem !important;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
  padding: 0 0.5rem;
}

.table-title-section {
  flex: 1;
}

.table-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0 0 0.5rem 0;
}

.table-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.sessions-count {
  font-size: 0.875rem;
  color: #94a3b8;
}

.table-actions {
  padding-top: 0.5rem;
  display: flex;
  gap: 0.75rem;
}

.table-card :deep(.card-content) {
  background: transparent !important;
  padding: 0 !important;
}

/* Override BaseInput styles in HR Panel */
.hr-panel :deep(input),
.hr-panel :deep(select) {
  background: rgba(15, 23, 42, 0.8) !important;
  border: 1px solid rgba(0, 255, 255, 0.3) !important;
  color: #e2e8f0 !important;
  border-radius: 8px !important;
  padding: 0.75rem 1rem !important;
  font-size: 0.875rem !important;
}

.hr-panel :deep(input::placeholder) {
  color: #94a3b8 !important;
  opacity: 1 !important;
}

.hr-panel :deep(input:focus),
.hr-panel :deep(select:focus) {
  border-color: rgba(0, 255, 255, 0.6) !important;
  box-shadow: 0 0 0 2px rgba(0, 255, 255, 0.2) !important;
  outline: none !important;
}

.hr-panel :deep(.bg-white) {
  background: rgba(15, 23, 42, 0.8) !important;
  border-color: rgba(0, 255, 255, 0.3) !important;
  color: #e2e8f0 !important;
}

.hr-panel :deep(.text-neutral-900) {
  color: #e2e8f0 !important;
}

.hr-panel :deep(.placeholder-neutral-500) {
  color: #94a3b8 !important;
}

.hr-panel :deep(.border-neutral-300) {
  border-color: rgba(0, 255, 255, 0.3) !important;
}

/* Override BaseSelect styles */
.hr-panel :deep(option) {
  background: rgba(15, 23, 42, 0.95) !important;
  color: #e2e8f0 !important;
}

.hr-panel :deep(select option) {
  background: rgba(15, 23, 42, 0.95) !important;
  color: #e2e8f0 !important;
}

/* Fix button text colors */
.hr-panel :deep(.text-gray-700) {
  color: #e2e8f0 !important;
}

.hr-panel :deep(.text-gray-600) {
  color: #e2e8f0 !important;
}

.hr-panel :deep(.text-gray-500) {
  color: #94a3b8 !important;
}

.hr-panel :deep(.text-gray-400) {
  color: #94a3b8 !important;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filters-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #00ffff;
  margin: 0;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
}

.filters-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 0.5rem;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #e2e8f0;
}

.filter-actions {
  display: flex;
  justify-content: flex-end;
}

/* Table Section */
.table-section {
  flex: 1;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.table-title-section {
  flex: 1;
}

.table-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #00ffff;
  margin: 0 0 0.5rem 0;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
}

.table-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.sessions-count {
  font-size: 0.875rem;
  color: #e2e8f0;
}

.table-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

/* Loading and Empty States */
.loading-container,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  background: transparent;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-text {
  color: #e2e8f0;
  font-size: 0.875rem;
}

.empty-icon {
  margin-bottom: 1rem;
  color: #8a2be2;
}

.empty-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #00ffff;
  margin: 0 0 0.5rem 0;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
}

.empty-description {
  color: #e2e8f0;
  margin: 0 0 1.5rem 0;
  max-width: 400px;
}

/* Data Table */
.table-container {
  overflow: hidden;
  background: transparent;
}

.table-responsive {
  overflow-x: auto;
  background: transparent;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
  background: rgba(15, 23, 42, 0.3);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  overflow: hidden;
}

.data-table th {
  background: rgba(0, 255, 255, 0.1);
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  color: #00ffff;
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
  white-space: nowrap;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
}

.data-table th.sortable {
  cursor: pointer;
  user-select: none;
  transition: all 0.3s ease;
}

.data-table th.sortable:hover {
  background: rgba(0, 255, 255, 0.15);
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);
}

.data-table td {
  padding: 1rem;
  border-bottom: 1px solid rgba(0, 255, 255, 0.1);
  vertical-align: top;
  color: #e2e8f0;
}

.table-row {
  cursor: pointer;
  transition: all 0.3s ease;
}

.table-row:hover {
  background: rgba(0, 255, 255, 0.05);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
}

.session-id .id-text {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: #8a2be2;
  text-shadow: 0 0 3px rgba(138, 43, 226, 0.3);
}

.vacancy-info,
.candidate-info,
.date-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.vacancy-title,
.candidate-phone,
.date-text {
  font-weight: 500;
  color: #e2e8f0;
}

.vacancy-code,
.candidate-name,
.time-text {
  font-size: 0.75rem;
  color: #94a3b8;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  backdrop-filter: blur(10px);
  border: 1px solid;
}

.status-created {
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  border-color: rgba(138, 43, 226, 0.4);
  box-shadow: 0 0 10px rgba(138, 43, 226, 0.2);
}

.status-progress {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
  border-color: rgba(255, 193, 7, 0.4);
  box-shadow: 0 0 10px rgba(255, 193, 7, 0.2);
}

.status-completed {
  background: rgba(0, 255, 255, 0.2);
  color: #00ffff;
  border-color: rgba(0, 255, 255, 0.4);
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);
}

.status-failed {
  background: rgba(255, 20, 147, 0.2);
  color: #ff1493;
  border-color: rgba(255, 20, 147, 0.4);
  box-shadow: 0 0 10px rgba(255, 20, 147, 0.2);
}

.progress-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.progress-text {
  font-size: 0.75rem;
  color: #e2e8f0;
}

.progress-bar {
  width: 100%;
  height: 4px;
  background: rgba(15, 23, 42, 0.8);
  border: none;
  border-radius: 0;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #00ffff, #8a2be2);
  transition: width 0.3s ease;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
}

.score-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.score-value {
  font-weight: 600;
  font-size: 0.875rem;
}

.score-excellent { 
  color: #00ffff; 
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.5);
}
.score-good { 
  color: #8a2be2; 
  text-shadow: 0 0 5px rgba(138, 43, 226, 0.5);
}
.score-average { 
  color: #ffc107; 
  text-shadow: 0 0 5px rgba(255, 193, 7, 0.5);
}
.score-poor { 
  color: #ff1493; 
  text-shadow: 0 0 5px rgba(255, 20, 147, 0.5);
}

.score-bar {
  width: 100%;
  height: 0.25rem;
  background: #e5e7eb;
  border-radius: 9999px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.score-fill.score-excellent { background: #059669; }
.score-fill.score-good { background: #0ea5e9; }
.score-fill.score-average { background: #f59e0b; }
.score-fill.score-poor { background: #ef4444; }

.no-score {
  color: #9ca3af;
}

.action-buttons {
  display: flex;
  gap: 0.25rem;
}

.actions-column {
  width: 120px;
}

/* Cards View */
.cards-container {
  padding: 1.5rem;
  background: transparent;
}

.sessions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
  padding: 0;
  margin: 0;
}

/* Pagination */
.pagination-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-top: 1px solid rgba(0, 255, 255, 0.2);
  background: rgba(15, 23, 42, 0.3);
  backdrop-filter: blur(10px);
}

.pagination-info {
  flex: 1;
}

.pagination-text {
  font-size: 0.875rem;
  color: #e2e8f0;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.page-numbers {
  display: flex;
  gap: 0.25rem;
}

/* Animations */
.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive Design */
@media (max-width: 1024px) {
  .panel-content {
    padding: 1.5rem;
  }
  
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
  
  .filters-content {
    grid-template-columns: 1fr;
  }
  
  .table-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .table-actions {
    justify-content: flex-start;
  }
}

@media (max-width: 768px) {
  .panel-header {
    padding: 1rem;
  }
  
  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .header-actions {
    justify-content: flex-end;
  }
  
  .panel-content {
    padding: 1rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .sessions-grid {
    grid-template-columns: 1fr;
  }
  
  .pagination-container {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .pagination-controls {
    justify-content: center;
  }
  
  .table-responsive {
    margin: 0 -1rem;
  }
  
  .data-table {
    font-size: 0.75rem;
  }
  
  .data-table th,
  .data-table td {
    padding: 0.5rem;
  }
}

@media (max-width: 640px) {
  .panel-title {
    font-size: 1.5rem;
  }
  
  .header-actions {
    flex-direction: column;
  }
  
  .table-actions {
    flex-direction: column;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}

/* Button Styles - Override BaseButton Tailwind Classes */
.hr-panel :deep(.bg-primary-500) {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(138, 43, 226, 0.2)) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(0, 255, 255, 0.5) !important;
  color: #00ffff !important;
  box-shadow: 0 8px 32px rgba(0, 255, 255, 0.3) !important;
  position: relative !important;
  overflow: hidden !important;
  padding: 1rem 2rem !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  min-width: 180px !important;
}

.hr-panel :deep(.bg-primary-500::before) {
  content: '' !important;
  position: absolute !important;
  top: 0 !important;
  left: -100% !important;
  width: 100% !important;
  height: 100% !important;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.4), transparent) !important;
  transition: left 0.6s ease !important;
}

.hr-panel :deep(.bg-primary-500:hover) {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.35), rgba(138, 43, 226, 0.35)) !important;
  transform: translateY(-3px) !important;
  box-shadow: 0 12px 40px rgba(0, 255, 255, 0.5) !important;
  text-shadow: 0 0 15px rgba(0, 255, 255, 1) !important;
}

.hr-panel :deep(.bg-primary-500:hover::before) {
  left: 100% !important;
}

/* Outline Button Style */
.hr-panel :deep(.bg-transparent) {
  background: rgba(15, 23, 42, 0.7) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(138, 43, 226, 0.5) !important;
  color: #8a2be2 !important;
  box-shadow: 0 8px 32px rgba(138, 43, 226, 0.2) !important;
  padding: 1rem 2rem !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  min-width: 180px !important;
}

.hr-panel :deep(.bg-transparent:hover) {
  background: rgba(138, 43, 226, 0.2) !important;
  border-color: rgba(138, 43, 226, 0.7) !important;
  transform: translateY(-3px) !important;
  box-shadow: 0 12px 40px rgba(138, 43, 226, 0.4) !important;
  text-shadow: 0 0 15px rgba(138, 43, 226, 1) !important;
}

/* Ghost Button Style */
.hr-panel :deep(.text-neutral-700) {
  background: rgba(15, 23, 42, 0.6) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(0, 255, 255, 0.3) !important;
  color: #00ffff !important;
  box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1) !important;
  padding: 0.75rem 1.5rem !important;
  font-size: 0.875rem !important;
  font-weight: 600 !important;
  min-width: 120px !important;
}

.hr-panel :deep(.text-neutral-700:hover) {
  background: rgba(0, 255, 255, 0.1) !important;
  border-color: rgba(0, 255, 255, 0.5) !important;
  color: #00ffff !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 12px 40px rgba(0, 255, 255, 0.3) !important;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.8) !important;
}

/* Filter and Form Styles */
.filters-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #e2e8f0;
  margin-bottom: 0.25rem;
}

.filter-actions {
  grid-column: 1 / -1;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 255, 255, 0.1);
}

/* Table Improvements */
.table-container {
  padding: 0;
}

.table-responsive {
  padding: 2rem;
}

.data-table {
  background: transparent !important;
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  padding: 1.5rem 2rem !important;
  background: rgba(0, 255, 255, 0.05) !important;
  border-bottom: 1px solid rgba(0, 255, 255, 0.1) !important;
  color: #e2e8f0 !important;
  font-weight: 600 !important;
  font-size: 0.875rem !important;
  text-align: left !important;
}

.data-table td {
  padding: 1.5rem 2rem !important;
  border-bottom: 1px solid rgba(0, 255, 255, 0.05) !important;
  color: #e2e8f0 !important;
}

.data-table tr:hover {
  background: rgba(0, 255, 255, 0.02) !important;
}

.sortable {
  cursor: pointer;
  user-select: none;
  transition: all 0.2s ease;
}

.sortable:hover {
  background: rgba(0, 255, 255, 0.1) !important;
}

/* Pagination Improvements */
.pagination-container {
  padding: 2rem 2.5rem;
  border-top: 1px solid rgba(0, 255, 255, 0.1);
}

/* Loading and Empty States */
.loading-container,
.empty-state {
  padding: 4rem 2.5rem;
}

/* Cards Grid */
.cards-container {
  padding: 2rem;
}

.sessions-grid {
  gap: 1.5rem;
}

/* Status Badges */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
  border: 1px solid;
}

.status-created {
  background: rgba(251, 191, 36, 0.1);
  border-color: rgba(251, 191, 36, 0.3);
  color: #fbbf24;
}

.status-progress {
  background: rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.3);
  color: #3b82f6;
}

.status-completed {
  background: rgba(34, 197, 94, 0.1);
  border-color: rgba(34, 197, 94, 0.3);
  color: #22c55e;
}

.status-failed {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.3);
  color: #ef4444;
}

/* Progress Bars */
.progress-bar {
  width: 100%;
  height: 4px;
  background: rgba(15, 23, 42, 0.8);
  border: none;
  border-radius: 0;
  overflow: hidden;
  margin-top: 0.25rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #00ffff, #8a2be2);
  border: none;
  border-radius: 0;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.75rem;
  color: #94a3b8;
  font-weight: 500;
}

/* Score Bars */
.score-bar {
  width: 100%;
  height: 6px;
  background: rgba(0, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
  margin-top: 0.25rem;
}

.score-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.score-excellent {
  background: linear-gradient(90deg, #22c55e, #16a34a);
  color: #22c55e !important;
}

.score-good {
  background: linear-gradient(90deg, #3b82f6, #2563eb);
  color: #3b82f6 !important;
}

.score-average {
  background: linear-gradient(90deg, #f59e0b, #d97706);
  color: #f59e0b !important;
}

.score-poor {
  background: linear-gradient(90deg, #ef4444, #dc2626);
  color: #ef4444 !important;
}

.score-value {
  font-size: 0.875rem;
  font-weight: 600;
}

.no-score {
  color: #6b7280;
  font-style: italic;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 0.5rem;
}

/* Date and Time */
.date-text {
  font-size: 0.875rem;
  color: #e2e8f0;
  font-weight: 500;
}

.time-text {
  font-size: 0.75rem;
  color: #94a3b8;
}

/* Vacancy and Candidate Info */
.vacancy-title {
  font-size: 0.875rem;
  color: #e2e8f0;
  font-weight: 500;
}

.vacancy-code {
  font-size: 0.75rem;
  color: #94a3b8;
}

.candidate-phone {
  font-size: 0.875rem;
  color: #e2e8f0;
  font-weight: 500;
}

.candidate-name {
  font-size: 0.75rem;
  color: #94a3b8;
}

/* Loading and Empty States */
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-text {
  color: #94a3b8;
  font-size: 0.875rem;
}

.empty-state {
  text-align: center;
}

.empty-icon {
  margin-bottom: 1rem;
  color: #6b7280;
}

.empty-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 0.5rem;
}

.empty-description {
  color: #94a3b8;
  margin-bottom: 1.5rem;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .panel-header {
    margin: 1rem;
    padding: 2rem;
  }
  
  .panel-content {
    padding: 1rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1.5rem;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
  
  .table-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .table-actions {
    width: 100%;
    justify-content: flex-end;
  }
}

@media (max-width: 768px) {
  .panel-header {
    margin: 0.5rem;
    padding: 1.5rem;
  }
  
  .panel-content {
    padding: 0.5rem;
  }
  
  .header-actions {
    justify-content: flex-end;
  }
  
  .panel-content {
    padding: 1rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .sessions-grid {
    grid-template-columns: 1fr;
  }
  
  .pagination-container {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .pagination-controls {
    justify-content: center;
  }
}/* Sm
all Button Overrides */
.hr-panel :deep(button.h-8) {
  min-width: 120px !important;
  padding: 0.5rem 1rem !important;
  font-size: 0.875rem !important;
}

.hr-panel :deep(button.h-10) {
  min-width: 160px !important;
  padding: 0.75rem 1.5rem !important;
  font-size: 1rem !important;
}



/* Filter form improvements */
.filter-group input,
.filter-group select {
  padding: 1rem 1.5rem !important;
  background: rgba(15, 23, 42, 0.6) !important;
  border: 1px solid rgba(0, 255, 255, 0.3) !important;
  border-radius: 8px !important;
  color: #e2e8f0 !important;
}

.filter-group input:focus,
.filter-group select:focus {
  border-color: rgba(0, 255, 255, 0.6) !important;
  box-shadow: 0 0 0 2px rgba(0, 255, 255, 0.2) !important;
}

.filter-group input::placeholder {
  color: #94a3b8 !important;
}

/* Small Button Overrides */
.hr-panel :deep(.h-8) {
  min-width: 120px !important;
  padding: 0.5rem 1rem !important;
  font-size: 0.875rem !important;
}

.hr-panel :deep(.h-10) {
  min-width: 160px !important;
  padding: 0.75rem 1.5rem !important;
  font-size: 1rem !important;
}

/* Icon-only buttons */
.hr-panel :deep(.w-8),
.hr-panel :deep(.w-10),
.hr-panel :deep(.w-12) {
  min-width: auto !important;
  padding: 0.5rem !important;
}

/* Small outline buttons */
.hr-panel :deep(.h-8.bg-transparent) {
  background: rgba(15, 23, 42, 0.7) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(138, 43, 226, 0.5) !important;
  color: #8a2be2 !important;
  box-shadow: 0 8px 32px rgba(138, 43, 226, 0.2) !important;
}

.hr-panel :deep(.h-8.bg-transparent:hover) {
  background: rgba(138, 43, 226, 0.2) !important;
  border-color: rgba(138, 43, 226, 0.7) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 12px 40px rgba(138, 43, 226, 0.4) !important;
  text-shadow: 0 0 15px rgba(138, 43, 226, 1) !important;
}
.hr-panel :deep(.bg-white) {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95)) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(0, 255, 255, 0.3) !important;
}

.hr-panel :deep(.dark\\:bg-neutral-800) {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95)) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(0, 255, 255, 0.3) !important;
}

.hr-panel :deep(.text-neutral-900) {
  color: #e2e8f0 !important;
}

.hr-panel :deep(.dark\\:text-neutral-100) {
  color: #e2e8f0 !important;
}

.hr-panel :deep(.border-neutral-200) {
  border-color: rgba(0, 255, 255, 0.2) !important;
}

.hr-panel :deep(.dark\\:border-neutral-700) {
  border-color: rgba(0, 255, 255, 0.2) !important;
}

.hr-panel :deep(.text-neutral-400) {
  color: #94a3b8 !important;
}

.hr-panel :deep(.dark\\:text-neutral-500) {
  color: #94a3b8 !important;
}

.hr-panel :deep(.hover\\:text-neutral-600:hover) {
  color: #00ffff !important;
}

.hr-panel :deep(.dark\\:hover\\:text-neutral-300:hover) {
  color: #00ffff !important;
}

.hr-panel :deep(.hover\\:bg-neutral-100:hover) {
  background: rgba(0, 255, 255, 0.1) !important;
}

.hr-panel :deep(.dark\\:hover\\:bg-neutral-700:hover) {
  background: rgba(0, 255, 255, 0.1) !important;
}

/* Modal backdrop */
.hr-panel :deep(.fixed.inset-0) {
  background: rgba(0, 0, 0, 0.8) !important;
  backdrop-filter: blur(8px) !important;
}
.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 0.5rem;
}

.filter-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #e2e8f0;
  margin-bottom: 0.5rem;
  padding-left: 0.25rem;
}

.filter-actions {
  grid-column: 1 / -1;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
  padding: 1.5rem 0.5rem 0.5rem 0.5rem;
  border-top: 1px solid rgba(0, 255, 255, 0.1);
}

/* Input field improvements */
.hr-panel :deep(.relative) input {
  padding-left: 2.5rem !important;
}

.hr-panel :deep(.absolute.left-3) {
  color: #94a3b8 !important;
}

/* Better text visibility */
.hr-panel :deep(input[type="text"]),
.hr-panel :deep(input[type="search"]) {
  background: rgba(15, 23, 42, 0.9) !important;
  border: 1px solid rgba(0, 255, 255, 0.4) !important;
  color: #ffffff !important;
  font-weight: 500 !important;
}

.hr-panel :deep(input[type="text"]:focus),
.hr-panel :deep(input[type="search"]:focus) {
  border-color: rgba(0, 255, 255, 0.8) !important;
  box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.2) !important;
  background: rgba(15, 23, 42, 0.95) !important;
}

/* Select improvements */
.hr-panel :deep(select) {
  background: rgba(15, 23, 42, 0.9) !important;
  border: 1px solid rgba(0, 255, 255, 0.4) !important;
  color: #ffffff !important;
  font-weight: 500 !important;
}

.hr-panel :deep(select:focus) {
  border-color: rgba(0, 255, 255, 0.8) !important;
  box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.2) !important;
  background: rgba(15, 23, 42, 0.95) !important;
}
</style>
