<template>
  <BaseCard 
    :class="[
      'vacancy-card',
      'transition-all duration-200 hover:shadow-lg',
      { 'opacity-75': vacancy.status === 'paused' || vacancy.status === 'closed' }
    ]"
    :hoverable="true"
  >
    <!-- Header with title and status -->
    <div class="flex items-start justify-between mb-2">
      <div class="flex-1 min-w-0">
        <h3 class="text-lg font-semibold text-gray-900 mb-1 line-clamp-2">
          {{ vacancy.title }}
        </h3>
        <div class="flex items-center gap-2 flex-wrap">
          <span 
            :class="[
              'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
              statusBadgeClass
            ]"
          >
            {{ statusLabel }}
          </span>
          <span class="text-sm text-gray-600">
            {{ departmentLabel }}
          </span>
        </div>
      </div>
      
      <!-- Actions -->
      <div v-if="showActions" class="flex items-center gap-2 ml-4">
        <div class="relative" ref="actionsRef">
          <BaseButton
            variant="secondary"
            size="sm"
            @click="showActionsMenu = !showActionsMenu"
            class="p-1"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
            </svg>
          </BaseButton>
          
          <!-- Actions dropdown menu -->
          <div 
            v-if="showActionsMenu"
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

    <!-- Description -->
    <div v-if="!compact" class="mb-3">
      <p class="text-sm text-gray-600 line-clamp-3">
        {{ vacancy.description }}
      </p>
    </div>

    <!-- Key details -->
    <div class="space-y-2 mb-3">
      <!-- Location and employment type -->
      <div class="flex items-center gap-3 text-sm">
        <div class="flex items-center gap-1 text-gray-600">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
          </svg>
          {{ vacancy.location }}
        </div>
        <div class="flex items-center gap-1 text-gray-600">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V8a2 2 0 012-2h2zm4-3a1 1 0 00-1 1v1h2V4a1 1 0 00-1-1z" clip-rule="evenodd"/>
          </svg>
          {{ employmentTypeLabel }}
        </div>
        <div class="flex items-center gap-1 text-gray-600">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          {{ experienceLevelLabel }}
        </div>
      </div>

      <!-- Salary range -->
      <div v-if="vacancy.salary" class="flex items-center gap-1 text-sm">
        <svg class="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
          <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z"/>
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clip-rule="evenodd"/>
        </svg>
        <span class="font-medium text-green-700">
          {{ formatSalary(vacancy.salary) }}
        </span>
      </div>

      <!-- Requirements preview -->
      <div v-if="!compact && vacancy.requirements?.length" class="text-sm">
        <div class="text-gray-700 font-medium mb-1">Ключевые требования:</div>
        <div class="flex flex-wrap gap-1">
          <span 
            v-for="(req, index) in vacancy.requirements.slice(0, 3)"
            :key="index"
            class="inline-flex items-center px-2 py-1 rounded-md text-xs bg-blue-50 text-blue-700"
          >
            {{ req }}
          </span>
          <span 
            v-if="vacancy.requirements.length > 3"
            class="inline-flex items-center px-2 py-1 rounded-md text-xs bg-gray-100 text-gray-600"
          >
            +{{ vacancy.requirements.length - 3 }} еще
          </span>
        </div>
      </div>
    </div>

    <!-- Footer with metadata -->
    <div class="flex items-center justify-between text-xs text-gray-500 pt-2 border-t border-gray-100">
      <div class="flex items-center gap-2">
        <span>Создано {{ formatDate(vacancy.createdAt) }}</span>
        <span v-if="vacancy.scenarioId" class="flex items-center gap-1">
          <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/>
          </svg>
          Сценарий настроен
        </span>
      </div>
      
      <div v-if="vacancy.updatedAt !== vacancy.createdAt">
        Обновлено {{ formatDate(vacancy.updatedAt) }}
      </div>
    </div>
  </BaseCard>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseButton from '@/components/base/BaseButton.vue'

const props = defineProps({
  vacancy: {
    type: Object,
    required: true
  },
  showActions: {
    type: Boolean,
    default: true
  },
  compact: {
    type: Boolean,
    default: false
  },
  actions: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['action'])

const showActionsMenu = ref(false)
const actionsRef = ref()

// Status styling
const statusBadgeClass = computed(() => {
  switch (props.vacancy.status) {
    case 'active': return 'bg-green-100 text-green-800'
    case 'draft': return 'bg-yellow-100 text-yellow-800'
    case 'paused': return 'bg-orange-100 text-orange-800'
    case 'closed': return 'bg-gray-100 text-gray-800'
    default: return 'bg-gray-100 text-gray-800'
  }
})

const statusLabel = computed(() => {
  switch (props.vacancy.status) {
    case 'active': return 'Активна'
    case 'draft': return 'Черновик'
    case 'paused': return 'Приостановлена'
    case 'closed': return 'Закрыта'
    default: return 'Неизвестно'
  }
})

// Labels
const departmentLabel = computed(() => {
  return props.vacancy.department || 'Не указан отдел'
})

const employmentTypeLabel = computed(() => {
  const labels = {
    full_time: 'Полная занятость',
    part_time: 'Частичная занятость',
    contract: 'Контракт',
    internship: 'Стажировка'
  }
  return labels[props.vacancy.employmentType] || props.vacancy.employmentType
})

const experienceLevelLabel = computed(() => {
  const labels = {
    entry: 'Без опыта',
    junior: 'Junior',
    middle: 'Middle',
    senior: 'Senior',
    lead: 'Lead'
  }
  return labels[props.vacancy.experienceLevel] || props.vacancy.experienceLevel
})

// Available actions based on vacancy status
const availableActions = computed(() => {
  const baseActions = [...props.actions]
  
  // Add default actions based on status
  if (props.vacancy.status === 'active') {
    baseActions.unshift({
      id: 'create-session',
      label: 'Создать интервью',
      icon: 'chat',
      action: () => {},
      variant: 'primary'
    })
  }
  
  baseActions.push(
    {
      id: 'edit',
      label: 'Редактировать',
      icon: 'edit',
      action: () => {},
      variant: 'secondary'
    },
    {
      id: 'duplicate',
      label: 'Дублировать',
      icon: 'duplicate',
      action: () => {},
      variant: 'secondary'
    }
  )
  
  if (props.vacancy.status === 'active') {
    baseActions.push({
      id: 'pause',
      label: 'Приостановить',
      icon: 'pause',
      action: () => {},
      variant: 'secondary'
    })
  } else if (props.vacancy.status === 'paused') {
    baseActions.push({
      id: 'activate',
      label: 'Активировать',
      icon: 'play',
      action: () => {},
      variant: 'primary'
    })
  }
  
  return baseActions
})

// Helper functions
const formatSalary = (salary) => {
  const periodLabels = {
    hour: 'час',
    month: 'мес',
    year: 'год'
  }
  
  const formatNumber = (num) => {
    return new Intl.NumberFormat('ru-RU').format(num)
  }
  
  if (salary.min === salary.max) {
    return `${formatNumber(salary.min)} ${salary.currency}/${periodLabels[salary.period]}`
  }
  
  return `${formatNumber(salary.min)} - ${formatNumber(salary.max)} ${salary.currency}/${periodLabels[salary.period]}`
}

const formatDate = (date) => {
  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  }).format(new Date(date))
}

const handleAction = (action) => {
  showActionsMenu.value = false
  emit('action', action, props.vacancy)
  action.action()
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  if (actionsRef.value && !actionsRef.value.contains(event.target)) {
    showActionsMenu.value = false
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
.vacancy-card {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.6)) !important;
  border: 1px solid rgba(0, 255, 255, 0.2) !important;
  backdrop-filter: blur(20px);
  transition: all 0.4s ease;
  box-shadow: 
    0 4px 20px rgba(0, 0, 0, 0.3),
    0 0 20px rgba(0, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
  padding: 1rem;
  border-radius: 0.75rem;
}

.vacancy-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.1), transparent);
  transition: left 0.6s ease;
}

.vacancy-card:hover {
  transform: translateY(-4px);
  border-color: rgba(0, 255, 255, 0.4) !important;
  box-shadow: 
    0 8px 40px rgba(0, 0, 0, 0.4),
    0 0 30px rgba(0, 255, 255, 0.2);
}

.vacancy-card:hover::before {
  left: 100%;
}

/* Override text colors for dark theme */
.vacancy-card :deep(.text-gray-900) {
  color: #00ffff !important;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.vacancy-card :deep(.text-gray-600),
.vacancy-card :deep(.text-gray-700) {
  color: #e2e8f0 !important;
}

.vacancy-card :deep(.text-gray-500) {
  color: #94a3b8 !important;
}

.vacancy-card :deep(.text-green-700) {
  color: #22c55e !important;
  text-shadow: 0 0 5px rgba(34, 197, 94, 0.3);
}

.vacancy-card :deep(.text-green-600) {
  color: #22c55e !important;
}

.vacancy-card :deep(.text-blue-700) {
  color: #3b82f6 !important;
}

/* Status badges with glow effect */
.vacancy-card :deep(.bg-green-100) {
  background: rgba(34, 197, 94, 0.2) !important;
  border: 1px solid rgba(34, 197, 94, 0.3);
  box-shadow: 0 0 10px rgba(34, 197, 94, 0.2);
}

.vacancy-card :deep(.text-green-800) {
  color: #22c55e !important;
}

.vacancy-card :deep(.bg-yellow-100) {
  background: rgba(251, 191, 36, 0.2) !important;
  border: 1px solid rgba(251, 191, 36, 0.3);
  box-shadow: 0 0 10px rgba(251, 191, 36, 0.2);
}

.vacancy-card :deep(.text-yellow-800) {
  color: #f59e0b !important;
}

.vacancy-card :deep(.bg-orange-100) {
  background: rgba(249, 115, 22, 0.2) !important;
  border: 1px solid rgba(249, 115, 22, 0.3);
  box-shadow: 0 0 10px rgba(249, 115, 22, 0.2);
}

.vacancy-card :deep(.text-orange-800) {
  color: #f97316 !important;
}

.vacancy-card :deep(.bg-gray-100) {
  background: rgba(148, 163, 184, 0.2) !important;
  border: 1px solid rgba(148, 163, 184, 0.3);
  box-shadow: 0 0 10px rgba(148, 163, 184, 0.2);
}

.vacancy-card :deep(.text-gray-800) {
  color: #94a3b8 !important;
}

.vacancy-card :deep(.bg-blue-50) {
  background: rgba(59, 130, 246, 0.2) !important;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.vacancy-card :deep(.border-gray-100) {
  border-color: rgba(0, 255, 255, 0.2) !important;
}

.vacancy-card :deep(.border-gray-200) {
  border-color: rgba(0, 255, 255, 0.2) !important;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>