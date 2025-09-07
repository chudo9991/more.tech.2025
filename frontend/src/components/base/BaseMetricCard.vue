<template>
  <BaseCard class="metric-card" :class="variant">
    <div class="metric-content">
      <div class="metric-icon" :class="iconColorClass">
        <slot name="icon">
          <i :class="icon" class="metric-icon-default"></i>
        </slot>
      </div>
      <div class="metric-info">
        <div class="metric-value">{{ value }}</div>
        <div class="metric-title">{{ title }}</div>
        <div v-if="change" class="metric-change" :class="trendClass">
          <i :class="trendIcon"></i>
          {{ change }}
        </div>
      </div>
      <div v-if="showStatus" class="metric-status" :class="statusColorClass"></div>
    </div>
  </BaseCard>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import BaseCard from './BaseCard.vue'

interface Props {
  title: string
  value: string | number
  icon?: string
  change?: string
  trend?: 'positive' | 'negative' | 'neutral'
  status?: 'success' | 'warning' | 'error' | 'info'
  variant?: 'primary' | 'success' | 'warning' | 'info' | 'error'
  showStatus?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  trend: 'neutral',
  status: 'info',
  variant: 'primary',
  showStatus: false
})

const iconColorClass = computed(() => {
  const colors = {
    primary: 'icon-primary',
    success: 'icon-success', 
    warning: 'icon-warning',
    info: 'icon-info',
    error: 'icon-error'
  }
  return colors[props.variant as keyof typeof colors]
})

const statusColorClass = computed(() => {
  const colors = {
    success: 'status-success',
    warning: 'status-warning',
    error: 'status-error',
    info: 'status-info'
  }
  return colors[props.status as keyof typeof colors]
})

const trendClass = computed(() => {
  const classes = {
    positive: 'trend-positive',
    negative: 'trend-negative',
    neutral: 'trend-neutral'
  }
  return classes[props.trend as keyof typeof classes]
})

const trendIcon = computed(() => {
  const icons = {
    positive: 'mdi mdi-trending-up',
    negative: 'mdi mdi-trending-down',
    neutral: 'mdi mdi-trending-neutral'
  }
  return icons[props.trend as keyof typeof icons]
})
</script>

<style scoped>
.metric-card {
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

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.1), transparent);
  transition: left 0.6s ease;
}

.metric-card:hover {
  transform: translateY(-4px);
  border-color: rgba(0, 255, 255, 0.4) !important;
  box-shadow: 
    0 8px 40px rgba(0, 0, 0, 0.4),
    0 0 30px rgba(0, 255, 255, 0.2);
}

.metric-card:hover::before {
  left: 100%;
}

.metric-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  position: relative;
  z-index: 1;
}

.metric-icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.metric-icon::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), transparent);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: xor;
}

.metric-icon-default {
  font-size: 1.25rem;
  color: white;
}

/* Icon color variants */
.icon-primary {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.3), rgba(0, 200, 200, 0.3));
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}

.icon-success {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.3), rgba(22, 163, 74, 0.3));
  box-shadow: 0 0 20px rgba(34, 197, 94, 0.3);
}

.icon-warning {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.3), rgba(245, 158, 11, 0.3));
  box-shadow: 0 0 20px rgba(251, 191, 36, 0.3);
}

.icon-info {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(37, 99, 235, 0.3));
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
}

.icon-error {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.3), rgba(220, 38, 38, 0.3));
  box-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
}

.metric-info {
  flex: 1;
}

.metric-value {
  font-size: 1.875rem;
  font-weight: 700;
  color: #00ffff;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
  margin-bottom: 0.125rem;
  line-height: 1;
}

.metric-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: #e2e8f0;
  margin-bottom: 0.125rem;
}

.metric-change {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.trend-positive {
  color: #22c55e;
}

.trend-negative {
  color: #ef4444;
}

.trend-neutral {
  color: #94a3b8;
}

.metric-status {
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-success {
  background: #22c55e;
  box-shadow: 0 0 10px rgba(34, 197, 94, 0.5);
}

.status-warning {
  background: #f59e0b;
  box-shadow: 0 0 10px rgba(245, 158, 11, 0.5);
}

.status-error {
  background: #ef4444;
  box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
}

.status-info {
  background: #3b82f6;
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
}

/* Variant styles */
.metric-card.primary .metric-value {
  color: #00ffff;
}

.metric-card.success .metric-value {
  color: #22c55e;
}

.metric-card.warning .metric-value {
  color: #f59e0b;
}

.metric-card.info .metric-value {
  color: #3b82f6;
}

.metric-card.error .metric-value {
  color: #ef4444;
}
</style>