<template>
  <div class="page-header">
    <div class="header-container">
      <div class="header-content">
        <div class="header-info">
          <h1 class="header-title">{{ title }}</h1>
          <p v-if="subtitle" class="header-subtitle">{{ subtitle }}</p>
        </div>
        <div class="header-actions">
          <slot name="actions" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
  subtitle?: string
}

defineProps<Props>()
</script>

<style scoped>
.page-header {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  position: relative;
  overflow: hidden;
  border-radius: 0 0 20px 20px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.4),
    0 0 40px rgba(0, 255, 255, 0.1);
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 80%, rgba(0, 255, 255, 0.15) 0%, transparent 60%),
    radial-gradient(circle at 80% 20%, rgba(138, 43, 226, 0.15) 0%, transparent 60%);
  pointer-events: none;
  z-index: 1;
}

.page-header::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.1), transparent);
  animation: shimmer 3s ease-in-out infinite;
  z-index: 2;
}

@keyframes shimmer {
  0% { left: -100%; }
  100% { left: 100%; }
}

.header-container {
  position: relative;
  z-index: 3;
}

.header-content {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.header-info {
  flex: 1;
}

.header-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #00ffff;
  margin: 0 0 0.25rem 0;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
  line-height: 1.2;
}

.header-subtitle {
  color: #e2e8f0;
  margin: 0;
  font-size: 1rem;
  opacity: 0.9;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  flex-shrink: 0;
}

/* Стили для кнопок внутри header-actions */
.header-actions :deep(.btn),
.header-actions :deep(button) {
  white-space: nowrap;
  min-width: fit-content;
}

/* Responsive */
@media (max-width: 768px) {
  .header-container {
    padding: 1.5rem 1rem 2rem 1rem;
  }
  
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
  }
  
  .header-title {
    font-size: 1.5rem;
  }
  
  .header-actions {
    width: 100%;
    justify-content: flex-end;
    flex-wrap: wrap;
  }
}

@media (max-width: 480px) {
  .header-container {
    padding: 1rem 0.75rem 1.5rem 0.75rem;
  }
  
  .header-content {
    gap: 1rem;
  }
  
  .header-title {
    font-size: 1.25rem;
  }
  
  .header-actions {
    gap: 0.5rem;
    /* Кнопки остаются в одну строку */
    flex-direction: row;
    flex-wrap: wrap;
  }
}
</style>