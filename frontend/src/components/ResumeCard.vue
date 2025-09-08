<template>
  <BaseCard 
    class="resume-card group hover:shadow-lg transition-all duration-200"
    :class="{ 'ring-2 ring-primary-500': selected }"
  >
    <div class="p-6">
      <!-- Header -->
      <div class="flex items-start justify-between mb-4">
        <div class="flex items-center gap-3 flex-1 min-w-0">
          <!-- File Icon -->
          <div 
            :class="[
              'w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0',
              getFileTypeColor(resume.file_type)
            ]"
          >
            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
            </svg>
          </div>
          
          <!-- File Info -->
          <div class="flex-1 min-w-0">
            <h3 class="font-medium text-neutral-900 truncate">
              {{ resume.original_filename }}
            </h3>
            <div class="flex items-center gap-2 mt-1">
              <span 
                :class="[
                  'px-2 py-1 text-xs font-medium rounded-full',
                  getFileTypeBadgeColor(resume.file_type)
                ]"
              >
                {{ resume.file_type.toUpperCase() }}
              </span>
              <span class="text-xs text-neutral-500">
                {{ formatFileSize(resume.file_size) }}
              </span>
            </div>
          </div>
        </div>
        
        <!-- Status Badge -->
        <BaseButton
          :variant="getStatusVariant(resume.status)"
          size="sm"
          class="pointer-events-none flex-shrink-0"
        >
          {{ getStatusLabel(resume.status) }}
        </BaseButton>
      </div>
      
      <!-- Vacancy Info -->
      <div class="mb-4">
        <div class="text-sm text-neutral-600 mb-1">
          Вакансия
        </div>
        <div class="font-medium text-neutral-900">
          {{ resume.vacancy_title || 'Не указана' }}
        </div>
      </div>
      
      <!-- Score -->
      <div v-if="resume.total_score !== null && resume.total_score !== undefined" class="mb-4">
        <div class="flex items-center justify-between text-sm mb-2">
          <span class="text-neutral-600">Соответствие</span>
          <span class="font-medium text-neutral-900">{{ resume.total_score }}%</span>
        </div>
        <div class="w-full bg-neutral-200 rounded-full h-2">
          <div 
            :class="[
              'h-2 rounded-full transition-all duration-300',
              getScoreColor(resume.total_score)
            ]"
            :style="{ width: `${resume.total_score}%` }"
          ></div>
        </div>
      </div>
      
      <!-- Upload Date -->
      <div class="mb-6">
        <div class="text-sm text-neutral-500">
          Загружено {{ formatDate(resume.upload_date) }}
        </div>
      </div>
      
      <!-- Actions -->
      <div class="flex flex-wrap gap-2">
        <BaseButton
          variant="primary"
          size="sm"
          @click="$emit('view', resume.id)"
          class="flex-1"
        >
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          Просмотр
        </BaseButton>
        
        <BaseButton
          v-if="resume.status === 'uploaded'"
          variant="secondary"
          size="sm"
          @click="$emit('process', resume.id)"
          :loading="processing"
          :disabled="processing"
        >
          <svg v-if="!processing" class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h8m-9-4V8a3 3 0 016 0v2M7 16a3 3 0 006 0v-2" />
          </svg>
          Обработать
        </BaseButton>
        
        <BaseButton
          v-if="resume.status === 'analyzed' && !resume.total_score"
          variant="secondary"
          size="sm"
          @click="$emit('calculate-score', resume.id)"
          :loading="calculating"
          :disabled="calculating"
        >
          <svg v-if="!calculating" class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          Оценить
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
            class="absolute right-0 top-full mt-1 w-48 bg-white rounded-lg shadow-lg border border-neutral-200 py-1 z-10"
          >
            <button
              @click="handleDownload"
              class="w-full px-4 py-2 text-left text-sm text-neutral-700 hover:bg-neutral-100 flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Скачать
            </button>
            
            <button
              @click="handleGenerateCode"
              class="w-full px-4 py-2 text-left text-sm text-neutral-700 hover:bg-neutral-100 flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1721 9z" />
              </svg>
              Создать код
            </button>
            
            <hr class="my-1 border-neutral-200">
            
            <button
              @click="handleDelete"
              class="w-full px-4 py-2 text-left text-sm text-error-600 hover:bg-error-50 flex items-center gap-2"
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
  </BaseCard>
</template>

<script setup>
import { ref } from 'vue'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseButton from '@/components/base/BaseButton.vue'

// Props
const props = defineProps({
  resume: {
    type: Object,
    required: true
  },
  processing: {
    type: Boolean,
    default: false
  },
  calculating: {
    type: Boolean,
    default: false
  },
  selected: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits([
  'view',
  'process',
  'calculate-score',
  'download',
  'generate-code',
  'delete'
])

// Local state
const showActions = ref(false)

// Methods
const getFileTypeColor = (fileType) => {
  const colors = {
    pdf: 'bg-error-500',
    docx: 'bg-primary-500',
    rtf: 'bg-warning-500',
    txt: 'bg-info-500'
  }
  return colors[fileType?.toLowerCase()] || 'bg-neutral-500'
}

const getFileTypeBadgeColor = (fileType) => {
  const colors = {
    pdf: 'bg-error-100 text-error-800',
    docx: 'bg-primary-100 text-primary-800',
    rtf: 'bg-warning-100 text-warning-800',
    txt: 'bg-info-100 text-info-800'
  }
  return colors[fileType?.toLowerCase()] || 'bg-neutral-100 text-neutral-800'
}

const getStatusVariant = (status) => {
  const variants = {
    uploaded: 'secondary',
    processing: 'secondary',
    analyzed: 'primary',
    error: 'danger'
  }
  return variants[status] || 'secondary'
}

const getStatusLabel = (status) => {
  const labels = {
    uploaded: 'Загружено',
    processing: 'Обработка',
    analyzed: 'Проанализировано',
    error: 'Ошибка'
  }
  return labels[status] || status
}

const getScoreColor = (score) => {
  if (score >= 80) return 'bg-success-500'
  if (score >= 60) return 'bg-warning-500'
  return 'bg-error-500'
}

const formatDate = (dateString) => {
  if (!dateString) return 'Неизвестно'
  try {
    const date = new Date(dateString)
    const now = new Date()
    const diffTime = Math.abs(now.getTime() - date.getTime())
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays === 1) return 'сегодня'
    if (diffDays === 2) return 'вчера'
    if (diffDays <= 7) return `${diffDays - 1} дн. назад`
    
    return date.toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  } catch (error) {
    console.error('Date formatting error:', error)
    return 'Неверная дата'
  }
}

const formatFileSize = (bytes) => {
  if (!bytes) return ''
  
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  
  return `${Math.round(bytes / Math.pow(1024, i) * 100) / 100} ${sizes[i]}`
}

const handleDownload = () => {
  showActions.value = false
  emit('download', props.resume.id)
}

const handleGenerateCode = () => {
  showActions.value = false
  emit('generate-code', props.resume.id)
}

const handleDelete = () => {
  showActions.value = false
  emit('delete', props.resume.id)
}

// Click outside directive
const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value()
      }
    }
    document.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el) {
    if (el.clickOutsideEvent) {
      document.removeEventListener('click', el.clickOutsideEvent)
    }
  }
}
</script>

<style scoped>
.resume-card {
  cursor: pointer;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.6)) !important;
  border: 1px solid rgba(0, 255, 255, 0.2) !important;
  backdrop-filter: blur(20px);
  transition: all 0.4s ease;
  box-shadow: 
    0 4px 20px rgba(0, 0, 0, 0.3),
    0 0 20px rgba(0, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}

.resume-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.1), transparent);
  transition: left 0.6s ease;
}

.resume-card:hover {
  transform: translateY(-4px);
  border-color: rgba(0, 255, 255, 0.4) !important;
  box-shadow: 
    0 8px 40px rgba(0, 0, 0, 0.4),
    0 0 30px rgba(0, 255, 255, 0.2);
}

.resume-card:hover::before {
  left: 100%;
}

/* Override text colors for dark theme */
.resume-card :deep(.text-neutral-900) {
  color: #00ffff !important;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.resume-card :deep(.text-neutral-600),
.resume-card :deep(.text-neutral-700) {
  color: #e2e8f0 !important;
}

.resume-card :deep(.text-neutral-500) {
  color: #94a3b8 !important;
}

.resume-card :deep(.text-white) {
  color: #00ffff !important;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
}

/* File type icon backgrounds with glow */
.resume-card :deep(.bg-error-500) {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.8), rgba(220, 38, 38, 0.8)) !important;
  box-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
}

.resume-card :deep(.bg-primary-500) {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.8), rgba(0, 200, 200, 0.8)) !important;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}

.resume-card :deep(.bg-warning-500) {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.8), rgba(245, 158, 11, 0.8)) !important;
  box-shadow: 0 0 20px rgba(251, 191, 36, 0.3);
}

.resume-card :deep(.bg-info-500) {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.8), rgba(37, 99, 235, 0.8)) !important;
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
}

.resume-card :deep(.bg-neutral-500) {
  background: linear-gradient(135deg, rgba(148, 163, 184, 0.8), rgba(100, 116, 139, 0.8)) !important;
  box-shadow: 0 0 20px rgba(148, 163, 184, 0.3);
}

/* File type badges */
.resume-card :deep(.bg-error-100) {
  background: rgba(239, 68, 68, 0.2) !important;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.resume-card :deep(.text-error-800) {
  color: #ef4444 !important;
}

.resume-card :deep(.bg-primary-100) {
  background: rgba(0, 255, 255, 0.2) !important;
  border: 1px solid rgba(0, 255, 255, 0.3);
}

.resume-card :deep(.text-primary-800) {
  color: #00ffff !important;
}

.resume-card :deep(.bg-warning-100) {
  background: rgba(251, 191, 36, 0.2) !important;
  border: 1px solid rgba(251, 191, 36, 0.3);
}

.resume-card :deep(.text-warning-800) {
  color: #f59e0b !important;
}

.resume-card :deep(.bg-info-100) {
  background: rgba(59, 130, 246, 0.2) !important;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.resume-card :deep(.text-info-800) {
  color: #3b82f6 !important;
}

.resume-card :deep(.bg-neutral-100) {
  background: rgba(148, 163, 184, 0.2) !important;
  border: 1px solid rgba(148, 163, 184, 0.3);
}

.resume-card :deep(.text-neutral-800) {
  color: #94a3b8 !important;
}

/* Progress bars */
.resume-card :deep(.bg-neutral-200) {
  background: rgba(0, 255, 255, 0.2) !important;
}

.resume-card :deep(.bg-success-500) {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.8), rgba(22, 163, 74, 0.8)) !important;
  box-shadow: 0 0 10px rgba(34, 197, 94, 0.3);
}

/* Dropdown menu */
.resume-card :deep(.bg-white) {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95)) !important;
  border: 1px solid rgba(0, 255, 255, 0.3) !important;
  backdrop-filter: blur(20px);
}

.resume-card :deep(.border-neutral-200) {
  border-color: rgba(0, 255, 255, 0.3) !important;
}

.resume-card :deep(.hover\\:bg-neutral-100:hover) {
  background: rgba(0, 255, 255, 0.1) !important;
}

.resume-card :deep(.text-error-600) {
  color: #ef4444 !important;
}

.resume-card :deep(.hover\\:bg-error-50:hover) {
  background: rgba(239, 68, 68, 0.1) !important;
}

/* Smooth transitions */
.resume-card * {
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, backdrop-filter;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}
</style>