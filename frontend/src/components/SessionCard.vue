<template>
  <BaseCard 
    :class="[
      'session-card',
      'transition-all duration-200 hover:shadow-lg',
      { 'border-l-4': true },
      statusBorderClass
    ]"
    :hoverable="true"
  >
    <!-- Header with status and actions -->
    <div class="flex items-start justify-between mb-4">
      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-2 mb-1">
          <h3 class="text-lg font-semibold text-gray-900 truncate">
            {{ vacancyTitle }}
          </h3>
          <span 
            :class="[
              'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
              statusBadgeClass
            ]"
          >
            {{ statusLabel }}
          </span>
        </div>
        <p class="text-sm text-gray-600">
          Кандидат: {{ session.candidateInfo.phone }}
          <span v-if="session.candidateInfo.name" class="ml-1">
            ({{ session.candidateInfo.name }})
          </span>
        </p>
      </div>
      
      <!-- Actions dropdown -->
      <div class="flex items-center gap-2 ml-4">
        <BaseButton
          v-if="session.status === 'completed' && session.scores?.overall"
          variant="secondary"
          size="sm"
          class="text-blue-600"
        >
          {{ Math.round(session.scores.overall * 100) }}%
        </BaseButton>
        
        <div class="relative" ref="actionsRef">
          <BaseButton
            variant="secondary"
            size="sm"
            @click="showActions = !showActions"
            class="p-1"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
            </svg>
          </BaseButton>
          
          <!-- Actions dropdown menu -->
          <div 
            v-if="showActions"
            class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 z-10"
          >
            <div class="py-1">
              <button
                v-for="action in availableActions"
                :key="action.id"
                @click="handleAction(action)"
                :disabled="action.disabled"
                class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span v-if="action.icon" class="mr-2">{{ action.icon }}</span>
                {{ action.label }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Progress bar for in-progress sessions -->
    <div v-if="session.status === 'in_progress'" class="mb-4">
      <div class="flex items-center justify-between text-sm text-gray-600 mb-1">
        <span>Прогресс интервью</span>
        <span>{{ session.currentStep }}/{{ session.totalSteps }}</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div 
          class="bg-blue-500 h-2 rounded-full transition-all duration-300"
          :style="{ width: `${progressPercentage}%` }"
        ></div>
      </div>
    </div>

    <!-- Score visualization for completed sessions -->
    <div v-if="session.status === 'completed' && session.scores" class="mb-4">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div 
          v-for="(score, category) in scoreCategories"
          :key="category"
          class="text-center"
        >
          <div class="text-xs text-gray-500 mb-1">{{ getCategoryLabel(category) }}</div>
          <div class="text-lg font-semibold" :class="getScoreColor(score)">
            {{ Math.round(score * 100) }}%
          </div>
        </div>
      </div>
    </div>

    <!-- Session metadata -->
    <div class="flex flex-wrap items-center gap-4 text-sm text-gray-500">
      <div class="flex items-center gap-1">
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"/>
        </svg>
        {{ formatDate(session.createdAt) }}
      </div>
      
      <div v-if="session.metadata?.sessionDuration" class="flex items-center gap-1">
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
        </svg>
        {{ formatDuration(session.metadata.sessionDuration) }}
      </div>
      
      <div v-if="session.responses?.length" class="flex items-center gap-1">
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd"/>
        </svg>
        {{ session.responses.length }} ответов
      </div>
    </div>
  </BaseCard>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue'
import type { InterviewSession, SessionAction } from '@/types/session'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseButton from '@/components/base/BaseButton.vue'

interface Props {
  session: InterviewSession
  vacancyTitle?: string
  actions?: SessionAction[]
  showProgress?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  vacancyTitle: 'Неизвестная вакансия',
  actions: () => [],
  showProgress: true
})

const emit = defineEmits<{
  action: [action: SessionAction, session: InterviewSession]
}>()

const showActions = ref(false)
const actionsRef = ref<HTMLElement>()

// Status styling
const statusBorderClass = computed(() => {
  switch (props.session.status) {
    case 'completed': return 'border-l-green-500'
    case 'in_progress': return 'border-l-blue-500'
    case 'failed': return 'border-l-red-500'
    case 'cancelled': return 'border-l-gray-500'
    default: return 'border-l-yellow-500'
  }
})

const statusBadgeClass = computed(() => {
  switch (props.session.status) {
    case 'completed': return 'bg-green-100 text-green-800'
    case 'in_progress': return 'bg-blue-100 text-blue-800'
    case 'failed': return 'bg-red-100 text-red-800'
    case 'cancelled': return 'bg-gray-100 text-gray-800'
    default: return 'bg-yellow-100 text-yellow-800'
  }
})

const statusLabel = computed(() => {
  switch (props.session.status) {
    case 'completed': return 'Завершено'
    case 'in_progress': return 'В процессе'
    case 'failed': return 'Ошибка'
    case 'cancelled': return 'Отменено'
    default: return 'Создано'
  }
})

// Progress calculation
const progressPercentage = computed(() => {
  if (props.session.totalSteps === 0) return 0
  return Math.round((props.session.currentStep / props.session.totalSteps) * 100)
})

// Score categories for display
const scoreCategories = computed(() => {
  if (!props.session.scores) return {}
  
  return {
    technical: props.session.scores.technical,
    communication: props.session.scores.communication,
    experience: props.session.scores.experience,
    cultural: props.session.scores.cultural
  }
})

// Available actions based on session status
const availableActions = computed(() => {
  const baseActions = [...props.actions]
  
  // Add default actions based on status
  if (props.session.status === 'completed') {
    baseActions.unshift({
      id: 'view-results',
      label: 'Посмотреть результаты',
      icon: '',
      action: () => {},
      variant: 'primary'
    })
  }
  
  if (props.session.status === 'in_progress') {
    baseActions.unshift({
      id: 'monitor',
      label: 'Мониторить',
      icon: '',
      action: () => {},
      variant: 'primary'
    })
  }
  
  baseActions.push({
    id: 'export',
    label: 'Экспорт',
    icon: '',
    action: () => {},
    variant: 'secondary'
  })
  
  return baseActions
})

// Helper functions
const getCategoryLabel = (category: string): string => {
  const labels: Record<string, string> = {
    technical: 'Техн.',
    communication: 'Комм.',
    experience: 'Опыт',
    cultural: 'Культ.'
  }
  return labels[category] || category
}

const getScoreColor = (score: number): string => {
  if (score >= 0.8) return 'text-green-600'
  if (score >= 0.6) return 'text-yellow-600'
  return 'text-red-600'
}

const formatDate = (date: Date): string => {
  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(new Date(date))
}

const formatDuration = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

const handleAction = (action: SessionAction) => {
  showActions.value = false
  emit('action', action, props.session)
  action.action()
}

// Close dropdown when clicking outside
const handleClickOutside = (event: Event) => {
  if (actionsRef.value && !actionsRef.value.contains(event.target as Node)) {
    showActions.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.session-card {
  background: rgba(15, 23, 42, 0.4) !important;
  border: 1px solid rgba(0, 255, 255, 0.2) !important;
  backdrop-filter: blur(20px);
  transition: all 0.4s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.session-card:hover {
  transform: translateY(-4px);
  border-color: rgba(0, 255, 255, 0.4) !important;
  box-shadow: 
    0 8px 40px rgba(0, 0, 0, 0.4),
    0 0 30px rgba(0, 255, 255, 0.2);
}

/* Override text colors */
.session-card :deep(.text-gray-900) {
  color: #00ffff !important;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
}

.session-card :deep(.text-gray-600),
.session-card :deep(.text-gray-500) {
  color: #e2e8f0 !important;
}

.session-card :deep(.text-blue-600) {
  color: #8a2be2 !important;
  text-shadow: 0 0 3px rgba(138, 43, 226, 0.3);
}

/* Status badges */
.session-card :deep(.bg-green-100) {
  background: rgba(0, 255, 255, 0.2) !important;
  color: #00ffff !important;
  border: 1px solid rgba(0, 255, 255, 0.4);
  backdrop-filter: blur(10px);
}

.session-card :deep(.bg-blue-100) {
  background: rgba(138, 43, 226, 0.2) !important;
  color: #8a2be2 !important;
  border: 1px solid rgba(138, 43, 226, 0.4);
  backdrop-filter: blur(10px);
}

.session-card :deep(.bg-red-100) {
  background: rgba(255, 20, 147, 0.2) !important;
  color: #ff1493 !important;
  border: 1px solid rgba(255, 20, 147, 0.4);
  backdrop-filter: blur(10px);
}

.session-card :deep(.bg-yellow-100) {
  background: rgba(255, 193, 7, 0.2) !important;
  color: #ffc107 !important;
  border: 1px solid rgba(255, 193, 7, 0.4);
  backdrop-filter: blur(10px);
}

.session-card :deep(.bg-gray-100) {
  background: rgba(156, 163, 175, 0.2) !important;
  color: #e2e8f0 !important;
  border: 1px solid rgba(156, 163, 175, 0.4);
  backdrop-filter: blur(10px);
}

/* Progress bar */
.session-card :deep(.bg-gray-200) {
  background: rgba(15, 23, 42, 0.6) !important;
  border: 1px solid rgba(0, 255, 255, 0.2);
}

.session-card :deep(.bg-blue-500) {
  background: linear-gradient(90deg, #00ffff, #8a2be2) !important;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
}

/* Score colors */
.session-card :deep(.text-green-600) {
  color: #00ffff !important;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.5);
}

.session-card :deep(.text-yellow-600) {
  color: #ffc107 !important;
  text-shadow: 0 0 5px rgba(255, 193, 7, 0.5);
}

.session-card :deep(.text-red-600) {
  color: #ff1493 !important;
  text-shadow: 0 0 5px rgba(255, 20, 147, 0.5);
}

/* Border colors */
.session-card :deep(.border-l-green-500) {
  border-left-color: #00ffff !important;
  box-shadow: -4px 0 10px rgba(0, 255, 255, 0.3);
}

.session-card :deep(.border-l-blue-500) {
  border-left-color: #8a2be2 !important;
  box-shadow: -4px 0 10px rgba(138, 43, 226, 0.3);
}

.session-card :deep(.border-l-red-500) {
  border-left-color: #ff1493 !important;
  box-shadow: -4px 0 10px rgba(255, 20, 147, 0.3);
}

.session-card :deep(.border-l-yellow-500) {
  border-left-color: #ffc107 !important;
  box-shadow: -4px 0 10px rgba(255, 193, 7, 0.3);
}

.session-card :deep(.border-l-gray-500) {
  border-left-color: #e2e8f0 !important;
  box-shadow: -4px 0 10px rgba(226, 232, 240, 0.3);
}

/* Dropdown menu */
.session-card :deep(.bg-white) {
  background: rgba(15, 23, 42, 0.9) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.2) !important;
}

.session-card :deep(.text-gray-700) {
  color: #e2e8f0 !important;
}

.session-card :deep(.hover\\:bg-gray-50:hover) {
  background: rgba(0, 255, 255, 0.1) !important;
}
</style>