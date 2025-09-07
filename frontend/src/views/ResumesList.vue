<template>
  <div class="resumes-list">
    <!-- Header -->
    <PageHeader
      title="Управление резюме"
      subtitle="Управляйте резюме кандидатов и кодами интервью"
    >
      <template #actions>
        <BaseButton
          variant="secondary"
          @click="$router.push('/resumes/upload')"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Загрузить резюме
        </BaseButton>
        <BaseButton
          variant="primary"
          @click="$router.push('/resumes/batch-upload')"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
          </svg>
          Массовая загрузка
        </BaseButton>
      </template>
    </PageHeader>

      <!-- Statistics Dashboard -->
      <section class="stats-section">
        <div class="stats-grid">
          <BaseMetricCard
            v-for="(stat, index) in statisticsCards"
            :key="stat.title"
            :title="stat.title"
            :value="stat.value"
            :icon="stat.icon"
            :variant="stat.variant"
            :change="stat.change"
            :trend="stat.trend"
            :class="{ 'animate-fade-in-up': statsVisible }"
            :style="{ animationDelay: `${index * 100}ms` }"
          />
        </div>
      </section>

    <!-- Main Content -->
    <div class="panel-content">
      <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        
        <!-- Filters Sidebar -->
        <aside class="lg:col-span-1">
          <BaseCard>
            <template #header>
              <div class="flex items-center justify-between">
                <h2 class="text-lg font-semibold text-neutral-900 dark:text-white">
                  Фильтры
                </h2>
                <BaseButton
                  variant="secondary"
                  size="sm"
                  @click="clearFilters"
                  :disabled="!hasActiveFilters"
                >
                  Очистить
                </BaseButton>
              </div>
            </template>
            
            <div class="space-y-6">
              <!-- Search -->
              <div>
                <label for="search" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                  Поиск
                </label>
                <BaseInput
                  id="search"
                  v-model="filters.search"
                  placeholder="Поиск по имени файла..."
                  @input="debouncedSearch"
                />
              </div>
              
              <!-- Vacancy Filter -->
              <div>
                <label for="vacancy" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                  Вакансия
                </label>
                <BaseSelect
                  id="vacancy"
                  v-model="filters.vacancy_id"
                  :items="vacancyOptions"
                  placeholder="Все вакансии"
                  @update:model-value="applyFilters"
                />
              </div>
              
              <!-- Status Filter -->
              <div>
                <label for="status" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                  Статус
                </label>
                <BaseSelect
                  id="status"
                  v-model="filters.status"
                  :items="statusOptions"
                  placeholder="Все статусы"
                  @update:model-value="applyFilters"
                />
              </div>
              
              <!-- File Type Filter -->
              <div>
                <label class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                  Тип файла
                </label>
                <div class="space-y-2">
                  <label v-for="type in fileTypes" :key="type.value" class="flex items-center">
                    <BaseCheckbox
                      :model-value="filters.file_types.includes(type.value)"
                      @update:model-value="toggleFileType(type.value)"
                    />
                    <span class="ml-2 text-sm text-neutral-700 dark:text-neutral-300">
                      {{ type.label }}
                    </span>
                  </label>
                </div>
              </div>
              
              <!-- Score Range Filter -->
              <div>
                <label class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                  Диапазон баллов
                </label>
                <div class="space-y-2">
                  <label v-for="range in scoreRanges" :key="range.value" class="flex items-center">
                    <BaseCheckbox
                      :model-value="filters.score_ranges.includes(range.value)"
                      @update:model-value="toggleScoreRange(range.value)"
                    />
                    <span class="ml-2 text-sm text-neutral-700 dark:text-neutral-300">
                      {{ range.label }}
                    </span>
                  </label>
                </div>
              </div>
              
              <!-- Date Range Filter -->
              <div>
                <label class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                  Дата загрузки
                </label>
                <div class="space-y-2">
                  <BaseInput
                    v-model="filters.date_from"
                    type="date"
                    placeholder="С даты"
                    @change="applyFilters"
                  />
                  <BaseInput
                    v-model="filters.date_to"
                    type="date"
                    placeholder="По дату"
                    @change="applyFilters"
                  />
                </div>
              </div>
            </div>
          </BaseCard>
        </aside>
        
        <!-- Resume Cards -->
        <div class="lg:col-span-3">
          <!-- View Toggle and Sort -->
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
            <div class="flex items-center gap-2">
              <span class="text-sm text-neutral-600 dark:text-neutral-400">
                Найдено резюме: {{ pagination.total }}
              </span>
              <div v-if="hasActiveFilters" class="flex items-center gap-2">
                <span class="text-xs text-neutral-500">•</span>
                <BaseButton
                  variant="secondary"
                  size="sm"
                  @click="clearFilters"
                >
                  Очистить фильтры
                </BaseButton>
              </div>
            </div>
            
            <div class="flex items-center gap-3">
              <!-- View Toggle -->
              <div class="flex items-center gap-1">
                <BaseButton
                  :variant="viewMode === 'grid' ? 'primary' : 'secondary'"
                  size="sm"
                  @click="viewMode = 'grid'"
                  aria-label="Вид карточками"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                  </svg>
                </BaseButton>
                <BaseButton
                  :variant="viewMode === 'list' ? 'primary' : 'secondary'"
                  size="sm"
                  @click="viewMode = 'list'"
                  aria-label="Вид списком"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd" />
                  </svg>
                </BaseButton>
              </div>
              
              <!-- Sort -->
              <BaseSelect
                v-model="sortBy"
                :items="sortOptions"
                placeholder="Сортировка"
                @update:model-value="applyFilters"
                size="sm"
              />
              
              <!-- Refresh -->
              <BaseButton
                variant="secondary"
                size="sm"
                @click="loadResumes"
                :loading="loading"
                aria-label="Обновить"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </BaseButton>
            </div>
          </div>
          
          <!-- Loading State -->
          <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
            <div v-for="i in 6" :key="i" class="animate-pulse">
              <BaseCard>
                <div class="p-6">
                  <div class="h-4 bg-neutral-200 dark:bg-neutral-700 rounded mb-4"></div>
                  <div class="h-3 bg-neutral-200 dark:bg-neutral-700 rounded mb-2"></div>
                  <div class="h-3 bg-neutral-200 dark:bg-neutral-700 rounded w-2/3"></div>
                </div>
              </BaseCard>
            </div>
          </div>
          
          <!-- Grid View -->
          <div 
            v-else-if="viewMode === 'grid'" 
            class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6"
          >
            <ResumeCard
              v-for="resume in resumes"
              :key="resume.id"
              :resume="resume"
              @view="viewResume"
              @process="processResume"
              @calculate-score="calculateScore"
              @download="downloadResume"
              @generate-code="generateInterviewCode"
              @delete="deleteResume"
              :processing="processingResume === resume.id"
              :calculating="calculatingScore === resume.id"
            />
          </div>
          
          <!-- List View -->
          <div v-else-if="viewMode === 'list'" class="space-y-4">
            <ResumeListItem
              v-for="resume in resumes"
              :key="resume.id"
              :resume="resume"
              @view="viewResume"
              @process="processResume"
              @calculate-score="calculateScore"
              @download="downloadResume"
              @generate-code="generateInterviewCode"
              @delete="deleteResume"
              :processing="processingResume === resume.id"
              :calculating="calculatingScore === resume.id"
            />
          </div>
          
          <!-- Empty State -->
          <div v-else-if="resumes.length === 0" class="text-center py-12">
            <div class="text-neutral-400 dark:text-neutral-500">
              <svg class="w-16 h-16 mx-auto mb-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
              </svg>
              <h3 class="text-lg font-medium text-neutral-900 dark:text-white mb-2">
                Резюме не найдены
              </h3>
              <p class="text-neutral-500 dark:text-neutral-400 mb-6">
                {{ hasActiveFilters ? 'Попробуйте изменить фильтры или' : 'Начните с загрузки первого резюме.' }}
              </p>
              <BaseButton
                v-if="hasActiveFilters"
                variant="secondary"
                @click="clearFilters"
              >
                Очистить фильтры
              </BaseButton>
              <BaseButton
                v-else
                variant="primary"
                @click="$router.push('/resumes/upload')"
              >
                Загрузить резюме
              </BaseButton>
            </div>
          </div>
          
          <!-- Pagination -->
          <div v-if="resumes.length > 0" class="mt-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div class="text-sm text-neutral-600 dark:text-neutral-400">
              Показано {{ ((pagination.page - 1) * pagination.limit) + 1 }} - 
              {{ Math.min(pagination.page * pagination.limit, pagination.total) }} из 
              {{ pagination.total }} результатов
            </div>
            
            <div class="flex items-center gap-2">
              <BaseButton
                variant="secondary"
                size="sm"
                @click="previousPage"
                :disabled="pagination.page <= 1"
              >
                Назад
              </BaseButton>
              
              <div class="flex items-center gap-1">
                <button
                  v-for="page in visiblePages"
                  :key="page"
                  @click="goToPage(page)"
                  :class="[
                    'px-3 py-1 text-sm rounded-md transition-colors',
                    page === pagination.page
                      ? 'bg-primary-500 text-white'
                      : 'text-neutral-600 dark:text-neutral-400 hover:bg-neutral-100 dark:hover:bg-neutral-800'
                  ]"
                >
                  {{ page }}
                </button>
              </div>
              
              <BaseButton
                variant="secondary"
                size="sm"
                @click="nextPage"
                :disabled="pagination.page >= totalPages"
              >
                Далее
              </BaseButton>
            </div>
          </div>
        </div>
      </div>
      </main>
    </div>
    
    <!-- Interview Code Modal -->
    <BaseModal v-model="showCodeDialog" title="Код интервью сгенерирован">
      <div class="text-center space-y-6">
        <div class="p-6 bg-neutral-50 dark:bg-neutral-800 rounded-lg">
          <div class="text-4xl font-mono font-bold text-primary-600 dark:text-primary-400 tracking-widest">
            {{ generatedCode }}
          </div>
        </div>
        
        <div class="text-left space-y-4">
          <h3 class="font-semibold text-neutral-900 dark:text-white">
            Инструкции для кандидата:
          </h3>
          <ol class="list-decimal list-inside space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
            <li>Перейдите на страницу интервью</li>
            <li>Введите код: <strong class="text-neutral-900 dark:text-white">{{ generatedCode }}</strong></li>
            <li>Начните интервью с ИИ-аватаром</li>
          </ol>
          
          <div class="p-4 bg-warning-50 dark:bg-warning-900/20 border border-warning-200 dark:border-warning-800 rounded-lg">
            <p class="text-sm text-warning-800 dark:text-warning-200">
              <strong>Важно:</strong> Этот код можно использовать только один раз. После использования интервью будет привязано к данному резюме.
            </p>
          </div>
        </div>
        
        <div class="flex gap-3">
          <BaseButton
            variant="secondary"
            @click="copyToClipboard"
            class="flex-1"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            Копировать код
          </BaseButton>
          <BaseButton
            variant="primary"
            @click="showCodeDialog = false"
            class="flex-1"
          >
            Понятно
          </BaseButton>
        </div>
      </div>
    </BaseModal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive, watch } from 'vue'
// @ts-ignore
import { useRouter } from 'vue-router'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import BaseSelect from '@/components/base/BaseSelect.vue'
import BaseCheckbox from '@/components/base/BaseCheckbox.vue'
import BaseModal from '@/components/base/BaseModal.vue'
import BaseMetricCard from '@/components/base/BaseMetricCard.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import ResumeCard from '@/components/ResumeCard.vue'
import ResumeListItem from '@/components/ResumeListItem.vue'
import type { SelectItem } from '@/types/components'

// Types
interface Resume {
  id: string
  original_filename: string
  file_type: string
  vacancy_id?: string
  vacancy_title?: string
  status: 'uploaded' | 'processing' | 'analyzed' | 'error'
  total_score?: number
  upload_date: string
}

interface Vacancy {
  id: string
  title: string
}

interface Statistics {
  total_resumes: number
  processed_resumes: number
  average_score: number
  error_resumes: number
}

interface Filters {
  search: string
  vacancy_id: string | null
  status: string | null
  file_types: string[]
  score_ranges: string[]
  date_from: string
  date_to: string
}

interface Pagination {
  page: number
  limit: number
  total: number
}

// Reactive data
const router = useRouter()
const resumes = ref<Resume[]>([])
const vacancies = ref<Vacancy[]>([])
const loading = ref(false)
const processingResume = ref<string | null>(null)
const calculatingScore = ref<string | null>(null)
const viewMode = ref<'grid' | 'list'>('grid')
const sortBy = ref('upload_date_desc')
const statsVisible = ref(false)

// Interview code modal
const showCodeDialog = ref(false)
const generatedCode = ref('')
const selectedResumeId = ref('')

// Statistics
const statistics = reactive<Statistics>({
  total_resumes: 0,
  processed_resumes: 0,
  average_score: 0,
  error_resumes: 0
})

// Filters
const filters = reactive<Filters>({
  search: '',
  vacancy_id: null,
  status: null,
  file_types: [],
  score_ranges: [],
  date_from: '',
  date_to: ''
})

// Pagination
const pagination = reactive<Pagination>({
  page: 1,
  limit: 12,
  total: 0
})

// Computed properties
const statisticsCards = computed(() => [
  {
    title: 'Всего резюме',
    value: statistics.total_resumes,
    icon: 'mdi mdi-file-document-multiple',
    variant: 'primary',
    change: '+0%',
    trend: 'neutral'
  },
  {
    title: 'Обработано',
    value: statistics.processed_resumes,
    icon: 'mdi mdi-check-circle',
    variant: 'success',
    change: '+0%',
    trend: 'positive'
  },
  {
    title: 'Средний балл',
    value: `${statistics.average_score}%`,
    icon: 'mdi mdi-star',
    variant: 'info',
    change: '+0%',
    trend: 'positive'
  },
  {
    title: 'Ошибки',
    value: statistics.error_resumes,
    icon: 'mdi mdi-alert-circle',
    variant: 'error',
    change: '+0%',
    trend: 'negative'
  }
])

const vacancyOptions = computed<SelectItem[]>(() => [
  { title: 'Все вакансии', value: null },
  ...vacancies.value.map(vacancy => ({
    title: vacancy.title,
    value: vacancy.id
  }))
])

const statusOptions = computed<SelectItem[]>(() => [
  { title: 'Все статусы', value: null },
  { title: 'Загружено', value: 'uploaded' },
  { title: 'Обрабатывается', value: 'processing' },
  { title: 'Проанализировано', value: 'analyzed' },
  { title: 'Ошибка', value: 'error' }
])

const fileTypes = computed(() => [
  { label: 'PDF', value: 'pdf' },
  { label: 'DOCX', value: 'docx' },
  { label: 'RTF', value: 'rtf' },
  { label: 'TXT', value: 'txt' }
])

const scoreRanges = computed(() => [
  { label: '90-100%', value: '90-100' },
  { label: '80-89%', value: '80-89' },
  { label: '70-79%', value: '70-79' },
  { label: '60-69%', value: '60-69' },
  { label: 'Below 60%', value: '0-59' }
])

const sortOptions = computed<SelectItem[]>(() => [
  { title: 'Сначала новые', value: 'upload_date_desc' },
  { title: 'Сначала старые', value: 'upload_date_asc' },
  { title: 'Высокий балл', value: 'score_desc' },
  { title: 'Низкий балл', value: 'score_asc' },
  { title: 'Имя файла А-Я', value: 'filename_asc' },
  { title: 'Имя файла Я-А', value: 'filename_desc' }
])

const hasActiveFilters = computed(() => {
  return filters.search !== '' ||
         filters.vacancy_id !== null ||
         filters.status !== null ||
         filters.file_types.length > 0 ||
         filters.score_ranges.length > 0 ||
         filters.date_from !== '' ||
         filters.date_to !== ''
})

const totalPages = computed(() => {
  return Math.ceil(pagination.total / pagination.limit)
})

const visiblePages = computed(() => {
  const current = pagination.page
  const total = totalPages.value
  const delta = 2
  
  let start = Math.max(1, current - delta)
  let end = Math.min(total, current + delta)
  
  if (end - start < 4) {
    if (start === 1) {
      end = Math.min(total, start + 4)
    } else {
      start = Math.max(1, end - 4)
    }
  }
  
  const pages = []
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

// Debounced search
let searchTimeout: NodeJS.Timeout
const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    applyFilters()
  }, 300)
}

// Methods
const loadResumes = async (): Promise<void> => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      skip: ((pagination.page - 1) * pagination.limit).toString(),
      limit: pagination.limit.toString()
    })
    
    // Add filters
    if (filters.search) params.append('search', filters.search)
    if (filters.vacancy_id) params.append('vacancy_id', filters.vacancy_id)
    if (filters.status) params.append('status', filters.status)
    if (filters.file_types.length > 0) params.append('file_types', filters.file_types.join(','))
    if (filters.score_ranges.length > 0) params.append('score_ranges', filters.score_ranges.join(','))
    if (filters.date_from) params.append('date_from', filters.date_from)
    if (filters.date_to) params.append('date_to', filters.date_to)
    if (sortBy.value) params.append('sort_by', sortBy.value)
    
    const response = await fetch(`/api/v1/resumes/?${params}`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    
    resumes.value = data.resumes || []
    pagination.total = data.total || 0
    pagination.page = data.page || 1
    pagination.limit = data.size || 12
  } catch (error) {
    console.error('Error loading resumes:', error)
    // Show user-friendly error message
  } finally {
    loading.value = false
  }
}

const loadStatistics = async (): Promise<void> => {
  try {
    const response = await fetch('/api/v1/resumes/statistics')
    const data = await response.json()
    Object.assign(statistics, data)
  } catch (error) {
    console.error('Error loading statistics:', error)
  }
}

const loadVacancies = async (): Promise<void> => {
  try {
    const response = await fetch('/api/v1/vacancies/')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    vacancies.value = data || []
  } catch (error) {
    console.error('Error loading vacancies:', error)
  }
}

const applyFilters = (): void => {
  pagination.page = 1
  loadResumes()
}

const clearFilters = (): void => {
  filters.search = ''
  filters.vacancy_id = null
  filters.status = null
  filters.file_types = []
  filters.score_ranges = []
  filters.date_from = ''
  filters.date_to = ''
  sortBy.value = 'upload_date_desc'
  applyFilters()
}

const toggleFileType = (type: string): void => {
  const index = filters.file_types.indexOf(type)
  if (index > -1) {
    filters.file_types.splice(index, 1)
  } else {
    filters.file_types.push(type)
  }
  applyFilters()
}

const toggleScoreRange = (range: string): void => {
  const index = filters.score_ranges.indexOf(range)
  if (index > -1) {
    filters.score_ranges.splice(index, 1)
  } else {
    filters.score_ranges.push(range)
  }
  applyFilters()
}

// Pagination methods
const previousPage = (): void => {
  if (pagination.page > 1) {
    pagination.page--
    loadResumes()
  }
}

const nextPage = (): void => {
  if (pagination.page < totalPages.value) {
    pagination.page++
    loadResumes()
  }
}

const goToPage = (page: number): void => {
  pagination.page = page
  loadResumes()
}

// Resume actions
const viewResume = (resumeId: string): void => {
  router.push(`/resumes/${resumeId}`)
}

const processResume = async (resumeId: string): Promise<void> => {
  processingResume.value = resumeId
  try {
    const response = await fetch(`/api/v1/resumes/${resumeId}/process`, {
      method: 'POST'
    })
    const data = await response.json()
    
    if (data.success) {
      console.log('Resume processed successfully')
      await loadResumes()
      await loadStatistics()
    } else {
      console.error(data.error || 'Processing error')
    }
  } catch (error) {
    console.error('Error processing resume:', error)
  } finally {
    processingResume.value = null
  }
}

const calculateScore = async (resumeId: string): Promise<void> => {
  calculatingScore.value = resumeId
  try {
    const response = await fetch(`/api/v1/resumes/${resumeId}/calculate-score`, {
      method: 'POST'
    })
    const data = await response.json()
    
    if (data.success) {
      console.log('Score calculated successfully')
      await loadResumes()
      await loadStatistics()
    } else {
      console.error(data.error || 'Score calculation error')
    }
  } catch (error) {
    console.error('Error calculating score:', error)
  } finally {
    calculatingScore.value = null
  }
}

const downloadResume = async (resumeId: string): Promise<void> => {
  try {
    const response = await fetch(`/api/v1/resumes/${resumeId}/download`)
    const data = await response.json()
    
    if (data.download_url) {
      window.open(data.download_url, '_blank')
    }
  } catch (error) {
    console.error('Error downloading resume:', error)
  }
}

const generateInterviewCode = async (resumeId: string): Promise<void> => {
  try {
    const response = await fetch(`/api/v1/interview-codes/generate/${resumeId}`, {
      method: 'POST'
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    generatedCode.value = data.code
    selectedResumeId.value = resumeId
    showCodeDialog.value = true
    
    console.log('Interview code generated successfully')
  } catch (error) {
    console.error('Error generating interview code:', error)
  }
}

const deleteResume = async (resumeId: string): Promise<void> => {
  if (!confirm('Вы уверены, что хотите удалить это резюме?')) {
    return
  }
  
  try {
    const response = await fetch(`/api/v1/resumes/${resumeId}`, {
      method: 'DELETE'
    })
    
    if (response.ok) {
      console.log('Resume deleted successfully')
      await loadResumes()
      await loadStatistics()
    } else {
      console.error('Error deleting resume')
    }
  } catch (error) {
    console.error('Error deleting resume:', error)
  }
}

const copyToClipboard = async (): Promise<void> => {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(generatedCode.value)
      console.log('Code copied to clipboard')
    } else {
      // Fallback for older browsers
      const textArea = document.createElement('textarea')
      textArea.value = generatedCode.value
      textArea.style.position = 'fixed'
      textArea.style.left = '-999999px'
      textArea.style.top = '-999999px'
      document.body.appendChild(textArea)
      textArea.focus()
      textArea.select()
      
      try {
        document.execCommand('copy')
        console.log('Code copied to clipboard')
      } catch (err) {
        console.error('Copy failed:', err)
      }
      
      document.body.removeChild(textArea)
    }
  } catch (error) {
    console.error('Copy to clipboard error:', error)
  }
}

// Lifecycle
onMounted(() => {
  // Trigger stats animation
  setTimeout(() => {
    statsVisible.value = true
  }, 200)
  
  loadResumes()
  loadStatistics()
  loadVacancies()
})

// Watch for view mode changes in localStorage
watch(viewMode, (newMode) => {
  localStorage.setItem('resumesViewMode', newMode)
})

// Load view mode from localStorage
onMounted(() => {
  const savedViewMode = localStorage.getItem('resumesViewMode') as 'grid' | 'list'
  if (savedViewMode) {
    viewMode.value = savedViewMode
  }
})
</script>



<style scoped>
/* Resumes List Styles */
.resumes-list {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  position: relative;
  overflow-x: hidden;
}

.resumes-list::before {
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

.resumes-list::after {
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
.resumes-header {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.6));
  backdrop-filter: blur(30px);
  border-bottom: 1px solid rgba(0, 255, 255, 0.3);
  position: relative;
  z-index: 10;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.4),
    0 0 40px rgba(0, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.resumes-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #00ffff;
  margin: 0 0 0.25rem 0;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.resumes-subtitle {
  color: #e2e8f0;
  margin: 0;
  font-size: 1rem;
}

/* Override text colors for dark theme */
.resumes-list :deep(.text-neutral-900) {
  color: #00ffff !important;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.resumes-list :deep(.text-neutral-600),
.resumes-list :deep(.text-neutral-700) {
  color: #e2e8f0 !important;
}

.resumes-list :deep(.text-neutral-500) {
  color: #94a3b8 !important;
}

.resumes-list :deep(.text-neutral-400) {
  color: #94a3b8 !important;
}

.resumes-list :deep(.text-white) {
  color: #00ffff !important;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
}

/* Cards styling */
.resumes-list :deep(.bg-white) {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.6)) !important;
  border: 1px solid rgba(0, 255, 255, 0.2) !important;
  backdrop-filter: blur(20px);
  box-shadow: 
    0 4px 20px rgba(0, 0, 0, 0.3),
    0 0 20px rgba(0, 255, 255, 0.1);
}

.resumes-list :deep(.border-neutral-200) {
  border-color: rgba(0, 255, 255, 0.2) !important;
}

.resumes-list :deep(.bg-neutral-100) {
  background: rgba(0, 255, 255, 0.1) !important;
}

.resumes-list :deep(.bg-neutral-50) {
  background: rgba(0, 255, 255, 0.05) !important;
}

.resumes-list :deep(.bg-neutral-800) {
  background: rgba(15, 23, 42, 0.8) !important;
}

/* Primary colors */
.resumes-list :deep(.text-primary-600) {
  color: #00ffff !important;
}

.resumes-list :deep(.bg-primary-500) {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.8), rgba(0, 200, 200, 0.8)) !important;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}

/* Success colors */
.resumes-list :deep(.text-success-600) {
  color: #22c55e !important;
}

/* Info colors */
.resumes-list :deep(.text-info-600) {
  color: #3b82f6 !important;
}

/* Error colors */
.resumes-list :deep(.text-error-600) {
  color: #ef4444 !important;
}

/* Warning colors */
.resumes-list :deep(.text-warning-600) {
  color: #f59e0b !important;
}

.resumes-list :deep(.bg-warning-50) {
  background: rgba(251, 191, 36, 0.1) !important;
  border-color: rgba(251, 191, 36, 0.3) !important;
}

.resumes-list :deep(.text-warning-800) {
  color: #f59e0b !important;
}

.resumes-list :deep(.border-warning-200) {
  border-color: rgba(251, 191, 36, 0.3) !important;
}

/* Statistics Section */
.stats-section {
  max-width: 1280px;
  margin: 0 auto 2rem auto;
  padding: 0 2rem;
}

.resumes-list {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  position: relative;
}

.resumes-list::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 80%, rgba(0, 255, 255, 0.05) 0%, transparent 60%),
    radial-gradient(circle at 80% 20%, rgba(138, 43, 226, 0.05) 0%, transparent 60%);
  pointer-events: none;
  z-index: 1;
}

.panel-content {
  position: relative;
  z-index: 2;
}

/* Statistics Section */
.stats-section {
  padding: 2rem 2rem 0 2rem;
}

.stats-grid {
  max-width: 1280px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

/* Animation */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out forwards;
  opacity: 0;
}

/* Page Content */
.page-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem 2rem 2rem;
}

/* Smooth transitions for all interactive elements */
.transition-all {
  transition: all 0.2s ease-in-out;
}

/* Custom scrollbar for filters */
.space-y-6::-webkit-scrollbar {
  width: 4px;
}

.space-y-6::-webkit-scrollbar-track {
  background: transparent;
}

.space-y-6::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.3);
  border-radius: 2px;
}

.space-y-6::-webkit-scrollbar-thumb:hover {
  background: rgba(148, 163, 184, 0.5);
}

/* Responsive */
@media (max-width: 768px) {
  .stats-section {
    padding: 1.5rem 1rem 0 1rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .page-content {
    padding: 0 1rem 2rem 1rem;
  }
}
</style>