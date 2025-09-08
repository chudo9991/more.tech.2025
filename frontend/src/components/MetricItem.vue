<template>
  <div class="metric-item">
    <div class="metric-item-content">
      <span class="metric-label">
        {{ label }}
      </span>
      <div class="metric-value-container">
        <span class="metric-value" :class="getValueColorClass()">
          {{ value }}
        </span>
        <div 
          v-if="status"
          class="metric-status-dot"
          :class="getStatusColorClass()"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  label: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  status: {
    type: String,
    default: '',
    validator: (value) => !value || ['success', 'warning', 'error'].includes(value)
  }
})

// Methods
const getValueColorClass = () => {
  if (!props.status) return 'value-default'
  
  const colors = {
    success: 'value-success',
    warning: 'value-warning',
    error: 'value-error'
  }
  return colors[props.status]
}

const getStatusColorClass = () => {
  if (!props.status) return ''
  
  const colors = {
    success: 'status-success',
    warning: 'status-warning',
    error: 'status-error'
  }
  return colors[props.status]
}
</script>

<style scoped>
.metric-item {
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(0, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.metric-item:last-child {
  border-bottom: none;
}

.metric-item:hover {
  background: rgba(0, 255, 255, 0.05);
  border-radius: 0.5rem;
  padding-left: 0.5rem;
  padding-right: 0.5rem;
}

.metric-item-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.metric-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #e2e8f0;
}

.metric-value-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.metric-value {
  font-size: 0.875rem;
  font-weight: 600;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
}

.value-default {
  color: #00ffff;
}

.value-success {
  color: #22c55e;
}

.value-warning {
  color: #f59e0b;
}

.value-error {
  color: #ef4444;
}

.metric-status-dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-success {
  background: #22c55e;
  box-shadow: 0 0 8px rgba(34, 197, 94, 0.5);
}

.status-warning {
  background: #f59e0b;
  box-shadow: 0 0 8px rgba(245, 158, 11, 0.5);
}

.status-error {
  background: #ef4444;
  box-shadow: 0 0 8px rgba(239, 68, 68, 0.5);
}
</style>