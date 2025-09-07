<template>
  <BaseCard class="service-status-card">
    <template #header>
      <div class="service-header">
        <div class="service-title-section">
          <div 
            class="service-status-indicator"
            :class="[
              getStatusColor(),
              { 'animate-pulse': loading }
            ]"
          ></div>
          <h3 class="service-title">
            {{ title }}
          </h3>
        </div>
        
        <div class="service-actions">
          <span class="last-updated">
            {{ formatLastUpdated() }}
          </span>
          <BaseButton
            variant="secondary"
            size="sm"
            @click="$emit('refresh')"
            :loading="loading"
            class="refresh-button"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </BaseButton>
        </div>
      </div>
    </template>
    
    <div class="service-content">
      <!-- Status Badge -->
      <div class="status-section">
        <span class="status-label">Status</span>
        <BaseButton
          :variant="getStatusVariant()"
          size="sm"
          class="status-badge"
        >
          {{ getStatusLabel() }}
        </BaseButton>
      </div>
      
      <!-- Metrics Slot -->
      <div v-if="$slots.metrics" class="metrics-section">
        <h4 class="metrics-title">
          Metrics
        </h4>
        <slot name="metrics" />
      </div>
      
      <!-- Actions Slot -->
      <div v-if="$slots.actions" class="actions-section">
        <slot name="actions" />
      </div>
    </div>
  </BaseCard>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseButton from '@/components/base/BaseButton.vue'

// Props
interface Props {
  title: string
  status: 'healthy' | 'degraded' | 'down' | 'unknown'
  lastUpdated?: string
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

// Emits
const emit = defineEmits<{
  refresh: []
}>()

// Computed properties
const getStatusColor = (): string => {
  const colors = {
    healthy: 'bg-success-500',
    degraded: 'bg-warning-500',
    down: 'bg-error-500',
    unknown: 'bg-neutral-400'
  }
  return colors[props.status as keyof typeof colors]
}

const getStatusVariant = (): 'success' | 'warning' | 'danger' | 'secondary' => {
  const variants = {
    healthy: 'success' as const,
    degraded: 'warning' as const,
    down: 'danger' as const,
    unknown: 'secondary' as const
  }
  return variants[props.status as keyof typeof variants]
}

const getStatusLabel = (): string => {
  const labels = {
    healthy: 'Operational',
    degraded: 'Degraded',
    down: 'Down',
    unknown: 'Unknown'
  }
  return labels[props.status as keyof typeof labels]
}

const formatLastUpdated = (): string => {
  if (!props.lastUpdated) return 'Never updated'
  
  const date = new Date(props.lastUpdated)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  
  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m ago`
  
  const diffHours = Math.floor(diffMins / 60)
  if (diffHours < 24) return `${diffHours}h ago`
  
  const diffDays = Math.floor(diffHours / 24)
  return `${diffDays}d ago`
}
</script>

<style scoped>
.service-status-card {
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

.service-status-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.1), transparent);
  transition: left 0.6s ease;
}

.service-status-card:hover {
  transform: translateY(-4px);
  border-color: rgba(0, 255, 255, 0.4) !important;
  box-shadow: 
    0 8px 40px rgba(0, 0, 0, 0.4),
    0 0 30px rgba(0, 255, 255, 0.2);
}

.service-status-card:hover::before {
  left: 100%;
}

.service-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  z-index: 1;
}

.service-title-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.service-status-indicator {
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
  flex-shrink: 0;
}

.service-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #00ffff;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.service-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.last-updated {
  font-size: 0.75rem;
  color: #94a3b8;
}

.refresh-button {
  padding: 0.5rem;
  color: #e2e8f0;
}

.service-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  position: relative;
  z-index: 1;
}

.status-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.status-label {
  font-size: 0.875rem;
  color: #e2e8f0;
}

.status-badge {
  pointer-events: none;
}

.metrics-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.metrics-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: #e2e8f0;
}

.actions-section {
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 255, 255, 0.2);
}

/* Status indicator colors */
.service-status-indicator.bg-success-500 {
  background: #22c55e;
  box-shadow: 0 0 10px rgba(34, 197, 94, 0.5);
}

.service-status-indicator.bg-warning-500 {
  background: #f59e0b;
  box-shadow: 0 0 10px rgba(245, 158, 11, 0.5);
}

.service-status-indicator.bg-error-500 {
  background: #ef4444;
  box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
}

.service-status-indicator.bg-neutral-400 {
  background: #94a3b8;
  box-shadow: 0 0 10px rgba(148, 163, 184, 0.5);
}
</style>