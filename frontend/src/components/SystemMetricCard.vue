<template>
  <BaseMetricCard
    :title="title"
    :value="value"
    :icon="getIconClass()"
    :variant="getVariant()"
    :status="status"
    show-status
  >
    <template #icon>
      <!-- Clock Icon -->
      <svg v-if="icon === 'clock'" fill="currentColor" viewBox="0 0 20 20" class="w-5 h-5 text-white">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
      </svg>
      <!-- CPU Icon -->
      <svg v-else-if="icon === 'cpu'" fill="currentColor" viewBox="0 0 20 20" class="w-5 h-5 text-white">
        <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z" />
      </svg>
      <!-- Zap Icon -->
      <svg v-else-if="icon === 'zap'" fill="currentColor" viewBox="0 0 20 20" class="w-5 h-5 text-white">
        <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd" />
      </svg>
      <!-- Alert Icon -->
      <svg v-else-if="icon === 'alert'" fill="currentColor" viewBox="0 0 20 20" class="w-5 h-5 text-white">
        <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
      </svg>
    </template>
  </BaseMetricCard>
</template>

<script setup lang="ts">
import BaseMetricCard from '@/components/base/BaseMetricCard.vue'

// Props
interface Props {
  title: string
  value: string | number
  icon: 'clock' | 'cpu' | 'zap' | 'alert'
  status: 'success' | 'warning' | 'error'
}

const props = defineProps<Props>()

// Computed properties
const getIconClass = (): string => {
  const icons: Record<Props['icon'], string> = {
    clock: 'mdi mdi-clock-outline',
    cpu: 'mdi mdi-cpu-64-bit',
    zap: 'mdi mdi-flash',
    alert: 'mdi mdi-alert'
  }
  return icons[props.icon as keyof typeof icons]
}

const getVariant = (): 'primary' | 'success' | 'warning' | 'error' => {
  const variants: Record<Props['status'], 'primary' | 'success' | 'warning' | 'error'> = {
    success: 'success',
    warning: 'warning',
    error: 'error'
  }
  return variants[props.status as keyof typeof variants]
}
</script>

