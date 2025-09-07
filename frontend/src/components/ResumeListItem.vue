<template>
  <BaseCard class="resume-list-item hover:shadow-md transition-all duration-200">
    <div class="p-4">
      <div class="flex items-center gap-4">
        <!-- File Icon -->
        <div 
          :class="[
            'w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0',
            getFileTypeColor(resume.file_type)
          ]"
        >
          <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
          </svg>
        </div>
        
        <!-- File Info -->
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-3 mb-1">
            <h3 class="font-medium text-neutral-900 dark:text-white truncate">
              {{ resume.original_filename }}
            </h3>
            <span 
              :class="[
                'px-2 py-1 text-xs font-medium rounded-full flex-shrink-0',
                getFileTypeBadgeColor(resume.file_type)
              ]"
            >
              {{ resume.file_type.toUpperCase() }}
            </span>
          </div>
          
          <div class="flex items-center gap-4 text-sm text-neutral-600 dark:text-neutral-400">
            <span>{{ resume.vacancy_title || 'Нет вакансии' }}</span>
            <span>•</span>
            <span>{{ formatDate(resume.upload_date) }}</span>
            <span v-if="resume.file_size">•</span>
            <span v-if="resume.file_size">{{ formatFileSize(resume.file_size) }}</span>
          </div>
        </div>
        
        <!-- Score -->
        <div v-if="resume.total_score !== null && resume.total_score !== undefined" class="flex items-center gap-3 flex-shrink-0">
          <div class="text-right">
            <div class="text-sm font-medium text-neutral-900 dark:text-white">
              {{ resume.total_score }}%
            </div>
            <div class="text-xs text-neutral-500 dark:text-neutral-400">
              Соответствие
            </div>
          </div>
          <div class="w-16 bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
            <div 
              :class="[
                'h-2 rounded-full transition-all duration-300',
                getScoreColor(resume.total_score)
              ]"
              :style="{ width: `${resume.total_score}%` }"
            ></div>
          </div>
        </div>
        
        <!-- Status -->
        <div class="flex-shrink-0">
          <BaseButton
            :variant="getStatusVariant(resume.status)"
            size="sm"
            class="pointer-events-none"
          >
            {{ getStatusLabel(resume.status) }}
          </BaseButton>
        </div>
        
        <!-- Actions -->
        <div class="flex items-center gap-2 flex-shrink-0">
          <BaseButton
            variant="primary"
            size="sm"
            @click="$emit('view', resume.id)"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
          </BaseButton>
          
          <BaseButton
            v-if="resume.status === 'uploaded'"
            variant="warning"
            size="sm"
            @click="$emit('process', resume.id)"
            :loading="processing"
            :disabled="processing"
          >
            <svg v-if="!processing" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h8m-9-4V8a3 3 0 016 0v2M7 16a3 3 0 006 0v-2" />
            </svg>
          </BaseButton>
          
          <BaseButton
            v-if="resume.status === 'analyzed' && !resume.total_score"
            variant="success"
            size="sm"
            @click="$emit('calculate-score', resume.id)"
            :loading="calculating"
            :disabled="calculating"
          >
            <svg v-if="!calculating" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </BaseButton>
          
          <!-- More Actions Dropdown -->
          <div class="relative">
            <BaseButton
              variant="secondary"
              size="sm"
              @click="showActions = !showActions"
              class="px-2"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
              </svg>
            </BaseButton>
            
            <!-- Dropdown Menu -->
            <div 
              v-if="showActions"
              v-click-outside="() => showActions = false"
              class="absolute right-0 top-full mt-1 w-48 bg-white dark:bg-neutral-800 rounded-lg shadow-lg border border-neutral-200 dark:border-neutral-700 py-1 z-10"
            >
              <button
                @click="handleDownload"
                class="w-full px-4 py-2 text-left text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 flex items-center gap-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Скачать
              </button>
              
              <button
                @click="handleGenerateCode"
                class="w-full px-4 py-2 text-left text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700 flex items-center gap-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                </svg>
                Создать код
              </button>
              
              <hr class="my-1 border-neutral-200 dark:border-neutral-700">
              
              <button
                @click="handleDelete"
                class="w-full px-4 py-2 text-left text-sm text-error-600 dark:text-error-400 hover:bg-error-50 dark:hover:bg-error-900/20 flex items-center gap-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Удалить
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </BaseCard>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseButton from '@/components/base/BaseButton.vue'

// Props
interface Props {
  resume: {
    id: string
    original_filename: string
    file_type: string
    file_size?: number
    vacancy_title?: string
    status: 'uploaded' | 'processing' | 'analyzed' | 'error'
    total_score?: number
    upload_date: string
  }
  processing?: boolean
  calculating?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  processing: false,
  calculating: false
})

// Emits
const emit = defineEmits<{
  view: [id: string]
  process: [id: string]
  'calculate-score': [id: string]
  download: [id: string]
  'generate-code': [id: string]
  delete: [id: string]
}>()

// Local state
const showActions = ref(false)

// Methods (same as ResumeCard)
const getFileTypeColor = (fileType: string): string => {
  const colors: Record<string, string> = {
    pdf: 'bg-error-500',
    docx: 'bg-primary-500',
    rtf: 'bg-warning-500',
    txt: 'bg-info-500'
  }
  return colors[fileType?.toLowerCase()] || 'bg-neutral-500'
}

const getFileTypeBadgeColor = (fileType: string): string => {
  const colors: Record<string, string> = {
    pdf: 'bg-error-100 text-error-800 dark:bg-error-900/20 dark:text-error-400',
    docx: 'bg-primary-100 text-primary-800 dark:bg-primary-900/20 dark:text-primary-400',
    rtf: 'bg-warning-100 text-warning-800 dark:bg-warning-900/20 dark:text-warning-400',
    txt: 'bg-info-100 text-info-800 dark:bg-info-900/20 dark:text-info-400'
  }
  return colors[fileType?.toLowerCase()] || 'bg-neutral-100 text-neutral-800 dark:bg-neutral-800 dark:text-neutral-300'
}

const getStatusVariant = (status: string): 'primary' | 'secondary' | 'success' | 'warning' | 'danger' => {
  const variants: Record<string, 'primary' | 'secondary' | 'success' | 'warning' | 'danger'> = {
    uploaded: 'secondary',
    processing: 'warning',
    analyzed: 'success',
    error: 'danger'
  }
  return variants[status] || 'secondary'
}

const getStatusLabel = (status: string): string => {
  const labels: Record<string, string> = {
    uploaded: 'Загружено',
    processing: 'Обработка',
    analyzed: 'Проанализировано',
    error: 'Ошибка'
  }
  return labels[status] || status
}

const getScoreColor = (score: number): string => {
  if (score >= 80) return 'bg-success-500'
  if (score >= 60) return 'bg-warning-500'
  return 'bg-error-500'
}

const formatDate = (dateString: string): string => {
  if (!dateString) return 'Unknown'
  try {
    const date = new Date(dateString)
    const now = new Date()
    const diffTime = Math.abs(now.getTime() - date.getTime())
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays === 1) return 'today'
    if (diffDays === 2) return 'yesterday'
    if (diffDays <= 7) return `${diffDays - 1} days ago`
    
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  } catch (error) {
    console.error('Date formatting error:', error)
    return 'Invalid date'
  }
}

const formatFileSize = (bytes?: number): string => {
  if (!bytes) return ''
  
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  
  return `${Math.round(bytes / Math.pow(1024, i) * 100) / 100} ${sizes[i]}`
}

const handleDownload = (): void => {
  showActions.value = false
  emit('download', props.resume.id)
}

const handleGenerateCode = (): void => {
  showActions.value = false
  emit('generate-code', props.resume.id)
}

const handleDelete = (): void => {
  showActions.value = false
  emit('delete', props.resume.id)
}

// Click outside directive
const vClickOutside = {
  mounted(el: HTMLElement & { clickOutsideEvent?: (event: Event) => void }, binding: any) {
    el.clickOutsideEvent = (event: Event) => {
      if (!(el === event.target || el.contains(event.target as Node))) {
        binding.value()
      }
    }
    document.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el: HTMLElement & { clickOutsideEvent?: (event: Event) => void }) {
    if (el.clickOutsideEvent) {
      document.removeEventListener('click', el.clickOutsideEvent)
    }
  }
}
</script>

<style scoped>
.resume-list-item {
  @apply cursor-pointer;
}

/* Smooth transitions */
.resume-list-item * {
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, backdrop-filter;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}
</style>