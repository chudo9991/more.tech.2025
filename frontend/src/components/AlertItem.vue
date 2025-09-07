<template>
  <div 
    :class="[
      'alert-item p-4 rounded-lg border-l-4 transition-all duration-200',
      getAlertStyles()
    ]"
  >
    <div class="flex items-start justify-between">
      <div class="flex items-start gap-3 flex-1">
        <!-- Alert Icon -->
        <div 
          :class="[
            'w-5 h-5 flex-shrink-0 mt-0.5',
            getIconColor()
          ]"
        >
          <svg fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" :d="getIconComponent()" clip-rule="evenodd" />
          </svg>
        </div>
        
        <!-- Alert Content -->
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 mb-1">
            <h4 class="text-sm font-medium text-neutral-900 dark:text-white">
              {{ alert.title }}
            </h4>
            <span 
              v-if="alert.service"
              :class="[
                'px-2 py-1 text-xs font-medium rounded-full',
                'bg-neutral-100 text-neutral-600 dark:bg-neutral-800 dark:text-neutral-400'
              ]"
            >
              {{ alert.service }}
            </span>
          </div>
          
          <p class="text-sm text-neutral-600 dark:text-neutral-400 mb-2">
            {{ alert.message }}
          </p>
          
          <div class="text-xs text-neutral-500 dark:text-neutral-500">
            {{ formatTimestamp(alert.timestamp) }}
          </div>
        </div>
      </div>
      
      <!-- Dismiss Button -->
      <BaseButton
        variant="secondary"
        size="sm"
        @click="$emit('dismiss', alert.id)"
        class="px-2 ml-2 flex-shrink-0"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </BaseButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import BaseButton from '@/components/base/BaseButton.vue'

// Props
interface Alert {
  id: string
  type: 'error' | 'warning' | 'info'
  title: string
  message: string
  timestamp: Date
  service?: string
}

interface Props {
  alert: Alert
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  dismiss: [id: string]
}>()

// Methods
const getAlertStyles = (): string => {
  const styles: Record<Alert['type'], string> = {
    error: 'bg-error-50 border-error-500 dark:bg-error-900/20 dark:border-error-500',
    warning: 'bg-warning-50 border-warning-500 dark:bg-warning-900/20 dark:border-warning-500',
    info: 'bg-info-50 border-info-500 dark:bg-info-900/20 dark:border-info-500'
  }
  return styles[props.alert.type as Alert['type']]
}

const getIconColor = (): string => {
  const colors: Record<Alert['type'], string> = {
    error: 'text-error-500',
    warning: 'text-warning-500',
    info: 'text-info-500'
  }
  return colors[props.alert.type as Alert['type']]
}

const getIconComponent = (): string => {
  const icons: Record<Alert['type'], string> = {
    error: 'M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z',
    warning: 'M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z',
    info: 'M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z'
  }
  
  return icons[props.alert.type as Alert['type']]
}

const formatTimestamp = (timestamp: Date): string => {
  const now = new Date()
  const diffMs = now.getTime() - timestamp.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  
  if (diffMins < 1) return 'Только что'
  if (diffMins < 60) return `${diffMins} минут назад`
  
  const diffHours = Math.floor(diffMins / 60)
  if (diffHours < 24) return `${diffHours} часов назад`
  
  return timestamp.toLocaleDateString('ru-RU', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.alert-item {
  @apply hover:shadow-sm;
}
</style>