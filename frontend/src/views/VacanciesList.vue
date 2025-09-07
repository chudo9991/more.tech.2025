<template>
  <div class="vacancies-list">
    <!-- Header -->
    <PageHeader
      title="Управление вакансиями"
      subtitle="Создавайте и управляйте вакансиями для автоматизированных интервью"
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
          @click="createVacancy"
        >
          Создать вакансию
        </BaseButton>
      </template>
    </PageHeader>

    <!-- Main Content -->
    <div class="page-content">
      <!-- Statistics Dashboard -->
      <section class="stats-section">
        <div class="stats-grid">
          <BaseMetricCard
            v-for="(stat, index) in statistics"
            :key="stat.title"
            :title="stat.title"
            :value="stat.value"
            :icon="getStatIcon(stat.type)"
            :variant="stat.type"
            :change="stat.change"
            :trend="stat.trend"
            :class="{ 'animate-fade-in-up': statsVisible }"
            :style="{ animationDelay: `${index * 100}ms` }"
          />
        </div>
      </section>

      <!-- Filters and Search -->
      <section class="filters-section">
        <div class="filters-layout">
          <!-- Sidebar Filters -->
          <div class="filters-sidebar" :class="{ 'sidebar-collapsed': !showFilters }">
            <BaseCard padding="lg" variant="outlined">
              <template #header>
                <div class="filters-header">
                  <h3 class="filters-title">Фильтры</h3>
                  <BaseButton
                    variant="secondary"
                    size="sm"
                    :icon="showFilters ? 'mdi mdi-chevron-left' : 'mdi mdi-chevron-right'"
                    @click="toggleFilters"
                  />
                </div>
              </template>

              <div v-show="showFilters" class="filters-content">
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
                  <label class="filter-label">Тип занятости</label>
                  <BaseSelect
                    v-model="filters.employment_type"
                    placeholder="Все типы"
                    :options="employmentTypeOptions"
                    clearable
                  />
                </div>

                <div class="filter-group">
                  <label class="filter-label">Уровень опыта</label>
                  <BaseSelect
                    v-model="filters.experience_level"
                    placeholder="Любой уровень"
                    :options="experienceLevelOptions"
                    clearable
                  />
                </div>

                <div class="filter-group">
                  <label class="filter-label">Регион</label>
                  <BaseInput
                    v-model="filters.region"
                    placeholder="Поиск по региону"
                    icon="mdi mdi-map-marker"
                  />
                </div>

                <div class="filter-group">
                  <label class="filter-label">Город</label>
                  <BaseInput
                    v-model="filters.city"
                    placeholder="Поиск по городу"
                    icon="mdi mdi-city"
                  />
                </div>

                <div class="filter-group">
                  <label class="filter-label">Зарплата от</label>
                  <BaseInput
                    v-model="filters.salary_min"
                    type="number"
                    placeholder="0"
                    icon="mdi mdi-currency-rub"
                  />
                </div>

                <div class="filter-actions">
                  <BaseButton
                    variant="primary"
                    size="sm"
                    icon="mdi mdi-filter-check"
                    :loading="loading"
                    @click="applyFilters"
                  >
                    Применить
                  </BaseButton>
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
              </div>
            </BaseCard>
          </div>

          <!-- Main Content Area -->
          <div class="content-area">
            <!-- Search and View Controls -->
            <div class="search-controls">
              <div class="search-input">
                <BaseInput
                  v-model="filters.search"
                  placeholder="Поиск по названию, требованиям, обязанностям..."
                  icon="mdi mdi-magnify"
                  @input="debouncedSearch"
                />
              </div>
              <div class="view-controls">
                <BaseButton
                  :variant="viewMode === 'grid' ? 'primary' : 'secondary'"
                  size="sm"
                  icon="mdi mdi-view-grid"
                  @click="setViewMode('grid')"
                >
                  Карточки
                </BaseButton>
                <BaseButton
                  :variant="viewMode === 'list' ? 'primary' : 'secondary'"
                  size="sm"
                  icon="mdi mdi-view-list"
                  @click="setViewMode('list')"
                >
                  Список
                </BaseButton>
              </div>
            </div>

            <!-- Results Header -->
            <div class="results-header">
              <div class="results-info">
                <h3 class="results-title">Вакансии</h3>
                <span class="results-count">{{ pagination.total }} {{ getPluralForm(pagination.total, ['вакансия', 'вакансии', 'вакансий']) }}</span>
              </div>
              <div class="results-actions">
                <BaseSelect
                  v-model="sortBy"
                  :options="sortOptions"
                  size="sm"
                  @change="handleSortChange"
                />
                <BaseButton
                  variant="secondary"
                  size="sm"
                  icon="mdi mdi-download"
                  @click="exportVacancies"
                  :loading="exportLoading"
                >
                  Экспорт
                </BaseButton>
              </div>
            </div>

            <!-- Vacancies Content -->
            <div class="vacancies-content">
              <!-- Loading State -->
              <div v-if="loading" class="loading-container">
                <div class="loading-spinner">
                  <i class="mdi mdi mdi-loading animate-spin text-4xl text-primary-500"></i>
                  <p class="loading-text">Загрузка вакансий...</p>
                </div>
              </div>

              <!-- Empty State -->
              <div v-else-if="vacancies.length === 0" class="empty-state">
                <div class="empty-icon">
                  <i class="mdi mdi mdi-briefcase-outline text-6xl text-neutral-400"></i>
                </div>
                <h3 class="empty-title">Вакансии не найдены</h3>
                <p class="empty-description">
                  {{ hasActiveFilters ? 'Попробуйте изменить фильтры поиска' : 'Создайте первую вакансию' }}
                </p>
                <BaseButton
                  v-if="!hasActiveFilters"
                  variant="primary"
                  icon="mdi mdi-plus"
                  @click="createVacancy"
                >
                  Создать вакансию
                </BaseButton>
              </div>

              <!-- Grid View -->
              <div v-else-if="viewMode === 'grid'" class="vacancies-grid">
                <VacancyCard
                  v-for="vacancy in vacancies"
                  :key="vacancy.id"
                  :vacancy="vacancy"
                  @view="viewVacancy"
                  @edit="editVacancy"
                  @delete="deleteVacancy"
                />
              </div>

              <!-- List View -->
              <div v-else class="vacancies-list-view">
                <BaseCard padding="none" variant="elevated">
                  <div class="table-container">
                    <table class="vacancies-table">
                      <thead>
                        <tr>
                          <th class="sortable" @click="sortByField('vacancy_code')">
                            Код
                            <i :class="getSortIcon('vacancy_code')"></i>
                          </th>
                          <th class="sortable" @click="sortByField('title')">
                            Название
                            <i :class="getSortIcon('title')"></i>
                          </th>
                          <th class="sortable" @click="sortByField('status')">
                            Статус
                            <i :class="getSortIcon('status')"></i>
                          </th>
                          <th>Тип занятости</th>
                          <th class="sortable" @click="sortByField('salary_min')">
                            Зарплата
                            <i :class="getSortIcon('salary_min')"></i>
                          </th>
                          <th class="sortable" @click="sortByField('created_at')">
                            Создано
                            <i :class="getSortIcon('created_at')"></i>
                          </th>
                          <th class="actions-column">Действия</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="vacancy in vacancies"
                          :key="vacancy.id"
                          class="table-row"
                          @click="viewVacancy(vacancy)"
                        >
                          <td class="code-cell">
                            <div v-if="vacancy.vacancy_code" class="vacancy-code">
                              {{ vacancy.vacancy_code }}
                            </div>
                            <span v-else class="no-code">—</span>
                          </td>
                          <td class="title-cell">
                            <div class="vacancy-info">
                              <div class="vacancy-title">{{ vacancy.title }}</div>
                              <div class="vacancy-location">
                                <i class="mdi mdi mdi-map-marker text-neutral-400"></i>
                                {{ getLocationText(vacancy) }}
                              </div>
                            </div>
                          </td>
                          <td class="status-cell">
                            <div class="status-badge" :class="getStatusClass(vacancy.status)">
                              <i :class="getStatusIcon(vacancy.status)"></i>
                              {{ getStatusLabel(vacancy.status) }}
                            </div>
                          </td>
                          <td class="employment-cell">
                            <div class="employment-type">
                              {{ getEmploymentTypeLabel(vacancy.employment_type) }}
                            </div>
                          </td>
                          <td class="salary-cell">
                            <div v-if="vacancy.salary_min || vacancy.salary_max" class="salary-info">
                              <div class="salary-range">
                                {{ getSalaryRange(vacancy) }}
                              </div>
                              <div class="salary-period">₽/мес</div>
                            </div>
                            <span v-else class="no-salary">Не указана</span>
                          </td>
                          <td class="date-cell">
                            <div class="date-info">
                              <div class="date-text">{{ formatDate(vacancy.created_at) }}</div>
                              <div class="time-text">{{ formatTime(vacancy.created_at) }}</div>
                            </div>
                          </td>
                          <td class="actions-cell" @click.stop>
                            <div class="action-buttons">
                              <BaseButton
                                variant="secondary"
                                size="sm"
                                icon="mdi mdi-eye"
                                @click="viewVacancy(vacancy)"
                              />
                              <BaseButton
                                variant="secondary"
                                size="sm"
                                icon="mdi mdi-pencil"
                                @click="editVacancy(vacancy)"
                              />
                              <BaseButton
                                variant="secondary"
                                size="sm"
                                icon="mdi mdi-delete"
                                @click="deleteVacancy(vacancy)"
                              />
                            </div>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </BaseCard>
              </div>
            </div>

            <!-- Pagination -->
            <div v-if="vacancies.length > 0" class="pagination-container">
              <div class="pagination-info">
                <span class="pagination-text">
                  Показано {{ ((pagination.page - 1) * pagination.size) + 1 }}-{{ Math.min(pagination.page * pagination.size, pagination.total) }} 
                  из {{ pagination.total }} вакансий
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
                  v-model="pagination.size"
                  :options="pageSizeOptions"
                  size="sm"
                  @change="handleSizeChange"
                />
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch } from 'vue'
// @ts-ignore
import { useRouter } from 'vue-router'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import BaseSelect from '@/components/base/BaseSelect.vue'
import BaseMetricCard from '@/components/base/BaseMetricCard.vue'
import VacancyCard from '@/components/VacancyCard.vue'
import PageHeader from '@/components/layout/PageHeader.vue'

// Types
interface VacancyFilters {
  search: string
  status: string | null
  region: string
  city: string
  employment_type: string | null
  experience_level: string | null
  salary_min: string
}

interface Pagination {
  page: number
  size: number
  total: number
}

interface Statistic {
  title: string
  value: string | number
  change: string
  trend: 'positive' | 'negative' | 'neutral'
  icon: string
  type: 'primary' | 'success' | 'warning' | 'info'
}

interface Vacancy {
  id: string
  title: string
  vacancy_code?: string
  status: string
  employment_type: string
  experience_level: string
  region?: string
  city?: string
  salary_min?: number
  salary_max?: number
  created_at: string
}
const router = useRouter()

// Reactive data
const loading = ref(false)
const exportLoading = ref(false)
const statsVisible = ref(false)
const showFilters = ref(true)
const viewMode = ref<'grid' | 'list'>('grid')
const sortField = ref<string>('created_at')
const sortDirection = ref<'asc' | 'desc'>('desc')

const vacancies = ref<Vacancy[]>([])

const filters = reactive<VacancyFilters>({
  search: '',
  status: null,
  region: '',
  city: '',
  employment_type: null,
  experience_level: null,
  salary_min: ''
})

const pagination = reactive<Pagination>({
  page: 1,
  size: 20,
  total: 0
})

const statistics = ref<Statistic[]>([
  { 
    title: 'Всего вакансий', 
    value: 0, 
    change: '+0%', 
    trend: 'neutral', 
    icon: 'mdi mdi-briefcase', 
    type: 'primary' 
  },
  { 
    title: 'Активные', 
    value: 0, 
    change: '+0%', 
    trend: 'positive', 
    icon: 'mdi mdi-check-circle', 
    type: 'success' 
  },
  { 
    title: 'Закрытые', 
    value: 0, 
    change: '+0%', 
    trend: 'negative', 
    icon: 'mdi mdi-close-circle', 
    type: 'warning' 
  },
  { 
    title: 'Черновики', 
    value: 0, 
    change: '+0%', 
    trend: 'neutral', 
    icon: 'mdi mdi-file-document-outline', 
    type: 'info' 
  }
])

// Debounced search
let searchTimeout: NodeJS.Timeout | null = null
const debouncedSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    applyFilters()
  }, 500)
}

// Options for selects
const statusOptions = [
  { value: 'active', label: 'Активные' },
  { value: 'closed', label: 'Закрытые' },
  { value: 'draft', label: 'Черновики' },
  { value: 'paused', label: 'Приостановленные' }
]

const employmentTypeOptions = [
  { value: 'full_time', label: 'Полная занятость' },
  { value: 'part_time', label: 'Частичная занятость' },
  { value: 'contract', label: 'Контракт' },
  { value: 'internship', label: 'Стажировка' }
]

const experienceLevelOptions = [
  { value: 'entry', label: 'Без опыта' },
  { value: 'junior', label: 'Junior (1-3 года)' },
  { value: 'middle', label: 'Middle (3-5 лет)' },
  { value: 'senior', label: 'Senior (5+ лет)' },
  { value: 'lead', label: 'Lead/Principal' }
]

const sortOptions = [
  { value: 'created_at_desc', label: 'Сначала новые' },
  { value: 'created_at_asc', label: 'Сначала старые' },
  { value: 'title_asc', label: 'По названию (А-Я)' },
  { value: 'title_desc', label: 'По названию (Я-А)' },
  { value: 'salary_desc', label: 'По зарплате (убыв.)' },
  { value: 'salary_asc', label: 'По зарплате (возр.)' }
]

const pageSizeOptions = [
  { value: 10, label: '10 на странице' },
  { value: 20, label: '20 на странице' },
  { value: 50, label: '50 на странице' },
  { value: 100, label: '100 на странице' }
]

const sortBy = ref('created_at_desc')

// Computed properties
const hasActiveFilters = computed(() => 
  filters.search || filters.status || filters.region || filters.city || 
  filters.employment_type || filters.experience_level || filters.salary_min
)

const totalPages = computed(() => 
  Math.ceil(pagination.total / pagination.size)
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
const loadVacancies = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      skip: ((pagination.page - 1) * pagination.size).toString(),
      limit: pagination.size.toString(),
      ...(filters.search && { search: filters.search }),
      ...(filters.status && { status: filters.status }),
      ...(filters.region && { region: filters.region }),
      ...(filters.city && { city: filters.city }),
      ...(filters.employment_type && { employment_type: filters.employment_type }),
      ...(filters.experience_level && { experience_level: filters.experience_level }),
      ...(filters.salary_min && { salary_min: filters.salary_min }),
      ...(sortField.value && { sort_field: sortField.value }),
      ...(sortDirection.value && { sort_direction: sortDirection.value })
    })
    
    const response = await fetch(`/api/v1/vacancies/?${params}`)
    if (!response.ok) throw new Error('Ошибка загрузки вакансий')
    
    const data = await response.json()
    vacancies.value = data.items || data
    pagination.total = data.total || data.length || 0
  } catch (error) {
    console.error('Error loading vacancies:', error)
    // Mock data for development
    vacancies.value = []
    pagination.total = 0
  } finally {
    loading.value = false
  }
}

const loadStatistics = async () => {
  try {
    const response = await fetch('/api/v1/vacancies/statistics')
    if (!response.ok) throw new Error('Ошибка загрузки статистики')
    
    const data = await response.json()
    statistics.value = [
      { 
        title: 'Всего вакансий', 
        value: data.total || 0, 
        change: data.total_change || '+0%', 
        trend: 'neutral',
        icon: 'mdi mdi-briefcase',
        type: 'primary'
      },
      { 
        title: 'Активные', 
        value: data.active || 0, 
        change: data.active_change || '+0%', 
        trend: 'positive',
        icon: 'mdi mdi-check-circle',
        type: 'success'
      },
      { 
        title: 'Закрытые', 
        value: data.closed || 0, 
        change: data.closed_change || '+0%', 
        trend: 'negative',
        icon: 'mdi mdi-close-circle',
        type: 'warning'
      },
      { 
        title: 'Черновики', 
        value: data.draft || 0, 
        change: data.draft_change || '+0%', 
        trend: 'neutral',
        icon: 'mdi mdi-file-document-outline',
        type: 'info'
      }
    ]
  } catch (error) {
    console.error('Error loading statistics:', error)
  }
}

const createVacancy = () => {
  router.push('/vacancies/create')
}

const viewVacancy = (vacancy: Vacancy) => {
  router.push(`/vacancies/${vacancy.id}`)
}

const editVacancy = (vacancy: Vacancy) => {
  router.push(`/vacancies/${vacancy.id}/edit`)
}

const deleteVacancy = async (vacancy: Vacancy) => {
  try {
    if (confirm(`Удалить вакансию "${vacancy.title}"?`)) {
      const response = await fetch(`/api/v1/vacancies/${vacancy.id}`, { 
        method: 'DELETE' 
      })
      
      if (!response.ok) throw new Error('Ошибка удаления вакансии')
      
      await loadVacancies()
      await loadStatistics()
    }
  } catch (error) {
    console.error('Error deleting vacancy:', error)
  }
}

const applyFilters = () => {
  pagination.page = 1
  loadVacancies()
}

const clearFilters = () => {
  filters.search = ''
  filters.status = null
  filters.region = ''
  filters.city = ''
  filters.employment_type = null
  filters.experience_level = null
  filters.salary_min = ''
  pagination.page = 1
  loadVacancies()
}

const refreshData = async () => {
  await Promise.all([
    loadVacancies(),
    loadStatistics()
  ])
}

const exportVacancies = async () => {
  try {
    exportLoading.value = true
    // Mock export functionality
    console.log('Exporting vacancies...')
  } catch (error) {
    console.error('Error exporting vacancies:', error)
  } finally {
    exportLoading.value = false
  }
}

const handleSizeChange = (size: number) => {
  pagination.size = size
  pagination.page = 1
  loadVacancies()
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  loadVacancies()
}

const handleSortChange = (value: string) => {
  const [field, direction] = value.split('_')
  sortField.value = field
  sortDirection.value = direction as 'asc' | 'desc'
  loadVacancies()
}

const sortByField = (field: string) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortDirection.value = 'desc'
  }
  loadVacancies()
}

const getSortIcon = (field: string) => {
  if (sortField.value !== field) return 'mdi mdi mdi-sort text-neutral-400'
  return sortDirection.value === 'asc' 
    ? 'mdi mdi mdi-sort-ascending text-primary-500' 
    : 'mdi mdi mdi-sort-descending text-primary-500'
}

const toggleFilters = () => {
  showFilters.value = !showFilters.value
}

const setViewMode = (mode: 'grid' | 'list') => {
  viewMode.value = mode
}

const getStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    active: 'status-active',
    closed: 'status-closed',
    draft: 'status-draft',
    paused: 'status-paused'
  }
  return classes[status] || 'status-draft'
}

const getStatusIcon = (status: string) => {
  const icons: Record<string, string> = {
    active: 'mdi mdi mdi-check-circle',
    closed: 'mdi mdi mdi-close-circle',
    draft: 'mdi mdi mdi-file-document-outline',
    paused: 'mdi mdi mdi-pause-circle'
  }
  return icons[status] || 'mdi mdi mdi-help-circle'
}

const getStatusLabel = (status: string) => {
  const labels = {
    active: 'Активная',
    closed: 'Закрытая',
    draft: 'Черновик',
    paused: 'Приостановлена'
  }
  return labels[status as keyof typeof labels] || status
}

const getEmploymentTypeLabel = (type: string) => {
  const labels = {
    full_time: 'Полная занятость',
    part_time: 'Частичная занятость',
    contract: 'Контракт',
    internship: 'Стажировка'
  }
  return labels[type as keyof typeof labels] || type
}

const getLocationText = (vacancy: Vacancy) => {
  const parts = []
  if (vacancy.region) parts.push(vacancy.region)
  if (vacancy.city) parts.push(vacancy.city)
  return parts.length > 0 ? parts.join(', ') : 'Не указано'
}

const getSalaryRange = (vacancy: Vacancy) => {
  if (vacancy.salary_min && vacancy.salary_max) {
    return `${formatSalary(vacancy.salary_min)} — ${formatSalary(vacancy.salary_max)}`
  } else if (vacancy.salary_min) {
    return `от ${formatSalary(vacancy.salary_min)}`
  } else if (vacancy.salary_max) {
    return `до ${formatSalary(vacancy.salary_max)}`
  }
  return 'Не указана'
}

const getStatIcon = (type: string) => {
  const icons = {
    primary: 'mdi mdi-briefcase',
    success: 'mdi mdi-check-circle',
    warning: 'mdi mdi-close-circle',
    info: 'mdi mdi-file-document-outline'
  }
  return icons[type as keyof typeof icons] || 'mdi mdi-briefcase'
}

const getTrendIcon = (trend: 'positive' | 'negative' | 'neutral') => {
  const icons: Record<'positive' | 'negative' | 'neutral', string> = {
    positive: 'mdi mdi mdi-trending-up',
    negative: 'mdi mdi mdi-trending-down',
    neutral: 'mdi mdi mdi-trending-neutral'
  }
  return icons[trend] || 'mdi mdi mdi-trending-neutral'
}

const formatSalary = (salary: number) => {
  return new Intl.NumberFormat('ru-RU').format(salary)
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

const getPluralForm = (count: number, forms: string[]) => {
  const cases = [2, 0, 1, 1, 1, 2]
  return forms[(count % 100 > 4 && count % 100 < 20) ? 2 : cases[Math.min(count % 10, 5)]]
}

// Watchers
watch(() => filters.status, () => {
  if (filters.status !== null) {
    applyFilters()
  }
})

watch(() => filters.employment_type, () => {
  if (filters.employment_type !== null) {
    applyFilters()
  }
})

watch(() => filters.experience_level, () => {
  if (filters.experience_level !== null) {
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
  await loadStatistics()
})
</script>

<style scoped>
/* Vacancies List Styles */
.vacancies-list {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #0f172a 50%, #1e293b 75%, #0f172a 100%);
  position: relative;
  overflow-x: hidden;
}

.vacancies-list::before {
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

.vacancies-list::after {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(45deg, rgba(0, 255, 255, 0.02) 25%, transparent 25%),
    linear-gradient(-45deg, rgba(138, 43, 226, 0.02) 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, rgba(0, 255, 255, 0.02) 75%),
    linear-gradient(-45deg, transparent 75%, rgba(138, 43, 226, 0.02) 75%);
  background-size: 60px 60px;
  background-position: 0 0, 0 30px, 30px -30px, -30px 0px;
  pointer-events: none;
  z-index: -1;
  opacity: 0.3;
}

/* Header */
.page-header {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.6));
  backdrop-filter: blur(30px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 20px;
  padding: 2.5rem;
  position: relative;
  z-index: 10;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.4),
    0 0 40px rgba(0, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  margin: 2rem 2rem 0 2rem;
  overflow: hidden;
}

.header-content {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-info {
  flex: 1;
}

.page-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #00ffff;
  margin: 0 0 0.25rem 0;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.page-subtitle {
  color: #e2e8f0;
  margin: 0;
  font-size: 1rem;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

/* Main Content */
.page-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem 2rem 2rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Statistics Section */
.stats-section {
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon.primary {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(0, 255, 255, 0.1));
  color: #00ffff;
}

.stat-icon.success {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1));
  color: #10b981;
}

.stat-icon.warning {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.1));
  color: #f59e0b;
}

.stat-icon.info {
  background: linear-gradient(135deg, rgba(138, 43, 226, 0.2), rgba(138, 43, 226, 0.1));
  color: #8a2be2;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 1.875rem;
  font-weight: 700;
  color: #e2e8f0;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stat-title {
  font-size: 0.875rem;
  color: #94a3b8;
  margin-bottom: 0.25rem;
}

.stat-change {
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.stat-change.positive {
  color: #10b981;
}

.stat-change.negative {
  color: #ef4444;
}

.stat-change.neutral {
  color: #6b7280;
}

/* Filters Section */
.filters-section {
  margin-bottom: 2rem;
}

.filters-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
}

.filters-sidebar {
  transition: all 0.3s ease;
}

.filters-sidebar.sidebar-collapsed {
  grid-template-columns: 60px 1fr;
}

.filters-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.filters-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #00ffff;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
}

.filters-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #94a3b8;
}

.filter-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 255, 255, 0.2);
}

/* Content Area */
.content-area {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.search-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-input {
  flex: 1;
}

.view-controls {
  display: flex;
  gap: 0.5rem;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 8px;
  padding: 0.25rem;
}

.results-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
}

.results-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.results-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #e2e8f0;
}

.results-count {
  font-size: 0.875rem;
  color: #94a3b8;
}

.results-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Vacancies Content */
.vacancies-content {
  min-height: 400px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
}

.loading-text {
  margin-top: 1rem;
  color: #94a3b8;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.empty-icon {
  margin-bottom: 1rem;
  color: #6b7280;
}

.empty-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 0.5rem;
}

.empty-description {
  color: #94a3b8;
  margin-bottom: 2rem;
}

/* Grid View */
.vacancies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

/* List View */
.vacancies-list-view {
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 16px;
  overflow: hidden;
}

.table-container {
  overflow-x: auto;
}

.vacancies-table {
  width: 100%;
  border-collapse: collapse;
}

.vacancies-table th {
  background: rgba(0, 255, 255, 0.1);
  color: #00ffff;
  font-weight: 600;
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
  font-size: 0.875rem;
}

.vacancies-table th.sortable {
  cursor: pointer;
  user-select: none;
  transition: all 0.2s ease;
}

.vacancies-table th.sortable:hover {
  background: rgba(0, 255, 255, 0.15);
}

.vacancies-table td {
  padding: 1rem;
  border-bottom: 1px solid rgba(0, 255, 255, 0.1);
  color: #e2e8f0;
  font-size: 0.875rem;
}

.table-row {
  cursor: pointer;
  transition: all 0.2s ease;
}

.table-row:hover {
  background: rgba(0, 255, 255, 0.05);
}

.vacancy-code {
  font-family: 'Monaco', 'Menlo', monospace;
  background: rgba(0, 255, 255, 0.1);
  color: #00ffff;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
}

.no-code {
  color: #6b7280;
}

.vacancy-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.vacancy-title {
  font-weight: 500;
  color: #e2e8f0;
}

.vacancy-location {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #94a3b8;
  font-size: 0.75rem;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge.status-active {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.status-badge.status-closed {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.status-badge.status-draft {
  background: rgba(107, 114, 128, 0.2);
  color: #6b7280;
  border: 1px solid rgba(107, 114, 128, 0.3);
}

.status-badge.status-paused {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.employment-type {
  color: #94a3b8;
}

.salary-info {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.salary-range {
  font-weight: 500;
  color: #e2e8f0;
}

.salary-period {
  color: #94a3b8;
  font-size: 0.75rem;
}

.no-salary {
  color: #6b7280;
}

.date-info {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.date-text {
  color: #e2e8f0;
}

.time-text {
  color: #94a3b8;
  font-size: 0.75rem;
}

.actions-cell {
  width: 120px;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

/* Pagination */
.pagination-container {
  display: flex;
  align-items: center;
  justify-content: between;
  padding: 1.5rem 0;
  border-top: 1px solid rgba(0, 255, 255, 0.2);
  margin-top: 2rem;
}

.pagination-info {
  flex: 1;
}

.pagination-text {
  color: #94a3b8;
  font-size: 0.875rem;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
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
  .filters-layout {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .filters-sidebar {
    order: 2;
  }
  
  .content-area {
    order: 1;
  }
  
  .search-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .results-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .vacancies-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .page-content {
    padding: 1rem;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .pagination-container {
    flex-direction: column;
    gap: 1rem;
  }
  
  .pagination-controls {
    flex-wrap: wrap;
    justify-content: center;
  }
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .table-container {
    font-size: 0.75rem;
  }
  
  .vacancies-table th,
  .vacancies-table td {
    padding: 0.5rem;
  }
}

.stat-card {
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.stat-icon.primary { background: linear-gradient(135deg, #0ea5e9, #0284c7); }
.stat-icon.success { background: linear-gradient(135deg, #10b981, #059669); }
.stat-icon.warning { background: linear-gradient(135deg, #f59e0b, #d97706); }
.stat-icon.info { background: linear-gradient(135deg, #3b82f6, #2563eb); }

.stat-info {
  flex: 1;
  min-width: 0;
}

.stat-value {
  font-size: 1.875rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.25rem;
  line-height: 1;
}

.stat-title {
  font-size: 0.875rem;
  color: #64748b;
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

.stat-change.positive { color: #10b981; }
.stat-change.negative { color: #ef4444; }
.stat-change.neutral { color: #64748b; }

/* Filters Section */
.filters-section {
  flex: 1;
}

.filters-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  align-items: start;
}

.filters-sidebar {
  position: sticky;
  top: 120px;
  transition: all 0.3s ease;
}

.sidebar-collapsed {
  grid-template-columns: 60px 1fr;
}

.sidebar-collapsed .filters-sidebar {
  width: 60px;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filters-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.filter-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* Content Area */
.content-area {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  min-width: 0;
}

.search-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-input {
  flex: 1;
}

.view-controls {
  display: flex;
  gap: 0.5rem;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
}

.results-info {
  display: flex;
  align-items: baseline;
  gap: 1rem;
}

.results-count {
  font-size: 0.875rem;
  color: #64748b;
}

.results-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
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
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-text {
  color: #64748b;
  font-size: 0.875rem;
}

.empty-icon {
  margin-bottom: 1rem;
}

.empty-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 0.5rem 0;
}

.empty-description {
  color: #64748b;
  margin: 0 0 1.5rem 0;
  max-width: 400px;
}

/* Grid View */
.vacancies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

/* List View */
.vacancies-list-view {
  width: 100%;
}

.table-container {
  overflow-x: auto;
}

.vacancies-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.vacancies-table th {
  background: #f8fafc;
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
  white-space: nowrap;
}

.vacancies-table th.sortable {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s;
}

.vacancies-table th.sortable:hover {
  background: #f1f5f9;
}

.vacancies-table td {
  padding: 1rem;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: top;
}

.table-row {
  cursor: pointer;
  transition: background-color 0.2s;
}

.table-row:hover {
  background: #f8fafc;
}

.code-cell .vacancy-code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  background: #e2e8f0;
  color: #475569;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
}

.no-code {
  color: #9ca3af;
}

.vacancy-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.vacancy-title {
  font-weight: 500;
  color: #0f172a;
}

.vacancy-location {
  font-size: 0.75rem;
  color: #6b7280;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-active {
  background: #d1fae5;
  color: #065f46;
}

.status-closed {
  background: #fee2e2;
  color: #991b1b;
}

.status-draft {
  background: #dbeafe;
  color: #1e40af;
}

.status-paused {
  background: #fef3c7;
  color: #92400e;
}

.employment-type {
  font-size: 0.875rem;
  color: #374151;
}

.salary-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.salary-range {
  font-weight: 500;
  color: #0f172a;
}

.salary-period {
  font-size: 0.75rem;
  color: #6b7280;
}

.no-salary {
  color: #9ca3af;
  font-style: italic;
}

.date-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.date-text {
  font-weight: 500;
  color: #0f172a;
}

.time-text {
  font-size: 0.75rem;
  color: #6b7280;
}

.action-buttons {
  display: flex;
  gap: 0.25rem;
}

.actions-column {
  width: 120px;
}

/* Pagination */
.pagination-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 0;
}

.pagination-info {
  flex: 1;
}

.pagination-text {
  font-size: 0.875rem;
  color: #6b7280;
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
  .page-content {
    padding: 1.5rem;
  }
  
  .filters-layout {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .filters-sidebar {
    position: static;
  }
  
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
  
  .search-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .results-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .results-actions {
    justify-content: flex-start;
  }
}

@media (max-width: 768px) {
  .page-header {
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
  
  .page-content {
    padding: 1rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .vacancies-grid {
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
  
  .table-container {
    margin: 0 -1rem;
  }
  
  .vacancies-table {
    font-size: 0.75rem;
  }
  
  .vacancies-table th,
  .vacancies-table td {
    padding: 0.5rem;
  }
}

@media (max-width: 640px) {
  .page-title {
    font-size: 1.5rem;
  }
  
  .header-actions {
    flex-direction: column;
  }
  
  .view-controls {
    flex-direction: column;
  }
  
  .results-actions {
    flex-direction: column;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .filters-content {
    gap: 1rem;
  }
  
  .filter-actions {
    flex-direction: row;
    gap: 0.5rem;
  }
}
</style>
