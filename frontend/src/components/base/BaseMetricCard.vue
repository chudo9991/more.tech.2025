<template>
  <div class="metric-card" :class="[variant, { 'has-change': change }]">
    <div class="metric-content">
      <div class="metric-info">
        <div class="metric-value">{{ value }}</div>
        <div class="metric-title">{{ title }}</div>
      </div>
      <div class="metric-icon" :class="iconColorClass">
        <slot name="icon">
          <component v-if="iconComponent" :is="iconComponent" class="metric-icon-default" />
          <span v-else class="metric-icon-symbol">{{ iconSymbol }}</span>
        </slot>
      </div>
    </div>
    <div v-if="change" class="metric-change" :class="trendClass">
      <component :is="trendIcon" />
      {{ change }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { 
  Document, 
  Check, 
  Clock, 
  TrendCharts, 
  User, 
  Briefcase, 
  Money,
  Star,
  Warning
} from '@element-plus/icons-vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  icon: {
    type: [String, Object],
    default: null
  },
  change: {
    type: String,
    default: null
  },
  trend: {
    type: String,
    default: 'neutral',
    validator: (value) => ['positive', 'negative', 'neutral'].includes(value)
  },
  status: {
    type: String,
    default: 'info',
    validator: (value) => ['success', 'warning', 'error', 'info'].includes(value)
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'success', 'warning', 'info', 'error'].includes(value)
  },
  showStatus: {
    type: Boolean,
    default: false
  }
})

const iconColorClass = computed(() => {
  const colors = {
    primary: 'icon-primary',
    success: 'icon-success', 
    warning: 'icon-warning',
    info: 'icon-info',
    error: 'icon-error'
  }
  return colors[props.variant]
})



const trendClass = computed(() => {
  const classes = {
    positive: 'trend-positive',
    negative: 'trend-negative',
    neutral: 'trend-neutral'
  }
  return classes[props.trend]
})

const trendIcon = computed(() => {
  // Используем Element Plus иконки вместо MDI
  const icons = {
    positive: TrendCharts,
    negative: TrendCharts,
    neutral: TrendCharts
  }
  return icons[props.trend]
})

const iconComponent = computed(() => {
  if (!props.icon) return null

  // Если передан Vue компонент напрямую
  if (typeof props.icon === 'object') {
    return props.icon
  }

  // Если передана строка, ищем в мапе
  const iconMap = {
    Document,
    Check,
    Clock,
    TrendCharts,
    User,
    Briefcase,
    Money,
    Star,
    Warning
  }

  return iconMap[props.icon] || null
})

const iconSymbol = computed(() => {
  const symbolMap = {
    Document: '📄',
    Check: '✅',
    Clock: '🕐',
    TrendCharts: '📈',
    User: '👤',
    Briefcase: '💼',
    Money: '💰',
    Star: '⭐',
    Warning: '⚠️'
  }

  return symbolMap[props.icon] || '📊'
})
</script>

<style scoped>
.metric-card {
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 1.25rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: all 0.4s ease;
  border: 1px solid rgba(0, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
  height: 100px;
  z-index: 100;
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.05), rgba(255, 0, 255, 0.05));
  opacity: 0;
  transition: opacity 0.4s ease;
}

.metric-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 255, 255, 0.2);
  border-color: rgba(0, 255, 255, 0.4);
  z-index: 200;
}

.metric-card:hover::before {
  opacity: 1;
}

.metric-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  z-index: 1;
  height: 100%;
}

.metric-info {
  text-align: left;
}

.metric-icon {
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.metric-icon-default {
  font-size: 1.5rem;
}

.metric-icon-symbol {
  font-size: 1.75rem;
  filter: drop-shadow(0 0 8px rgba(0, 255, 255, 0.6));
}

/* Icon color variants */
.icon-primary .metric-icon-default {
  color: #00ffff;
}

.icon-success .metric-icon-default {
  color: #22c55e;
}

.icon-warning .metric-icon-default {
  color: #f59e0b;
}

.icon-info .metric-icon-default {
  color: #3b82f6;
}

.icon-error .metric-icon-default {
  color: #ef4444;
}

.metric-value {
  font-size: 1.875rem;
  font-weight: 800;
  background: linear-gradient(135deg, #00ffff, #8a2be2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.25rem;
  text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
  line-height: 1;
}

.metric-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: #cbd5e1;
  opacity: 0.9;
}

.metric-change {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  margin-top: 0.5rem;
  position: relative;
  z-index: 1;
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