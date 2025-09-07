<template>
  <div class="metrics-showcase">
    <div class="showcase-header">
      <h2 class="showcase-title">Унифицированные карточки метрик</h2>
      <p class="showcase-subtitle">Все карточки используют единый стиль HR панели</p>
    </div>

    <!-- Base Metric Cards -->
    <section class="showcase-section">
      <h3 class="section-title">Базовые карточки метрик</h3>
      <div class="metrics-grid">
        <BaseMetricCard
          title="Всего сессий"
          :value="142"
          icon="mdi mdi-clipboard-text-multiple"
          variant="primary"
          change="+12%"
          trend="positive"
        />
        <BaseMetricCard
          title="Завершено"
          :value="89"
          icon="mdi mdi-check-circle"
          variant="success"
          change="+8%"
          trend="positive"
        />
        <BaseMetricCard
          title="В процессе"
          :value="23"
          icon="mdi mdi-clock-outline"
          variant="warning"
          change="+3%"
          trend="neutral"
        />
        <BaseMetricCard
          title="Средний балл"
          value="87.5%"
          icon="mdi mdi-star"
          variant="info"
          change="+2.1%"
          trend="positive"
        />
      </div>
    </section>

    <!-- System Metric Cards -->
    <section class="showcase-section">
      <h3 class="section-title">Системные метрики</h3>
      <div class="metrics-grid">
        <SystemMetricCard
          title="Время работы"
          value="24h 15m"
          icon="clock"
          status="success"
        />
        <SystemMetricCard
          title="Активные модели"
          value="4/8"
          icon="cpu"
          status="warning"
        />
        <SystemMetricCard
          title="Время отклика"
          value="125ms"
          icon="zap"
          status="success"
        />
        <SystemMetricCard
          title="Частота ошибок"
          value="0.2%"
          icon="alert"
          status="error"
        />
      </div>
    </section>

    <!-- Service Status Cards -->
    <section class="showcase-section">
      <h3 class="section-title">Статус сервисов</h3>
      <div class="services-grid">
        <ServiceStatusCard
          title="API Gateway"
          status="healthy"
          last-updated="2025-01-07T10:30:00Z"
        >
          <template #metrics>
            <MetricItem label="Запросов в минуту" value="1,247" status="success" />
            <MetricItem label="Среднее время ответа" value="89ms" status="success" />
            <MetricItem label="Ошибки 5xx" value="0.1%" status="success" />
          </template>
        </ServiceStatusCard>

        <ServiceStatusCard
          title="База данных"
          status="degraded"
          last-updated="2025-01-07T10:25:00Z"
        >
          <template #metrics>
            <MetricItem label="Соединения" value="45/100" status="warning" />
            <MetricItem label="Время запроса" value="250ms" status="warning" />
            <MetricItem label="Свободное место" value="15GB" status="success" />
          </template>
        </ServiceStatusCard>

        <ServiceStatusCard
          title="Redis Cache"
          status="healthy"
          last-updated="2025-01-07T10:32:00Z"
        >
          <template #metrics>
            <MetricItem label="Использование памяти" value="2.1GB" status="success" />
            <MetricItem label="Hit Rate" value="94.2%" status="success" />
            <MetricItem label="Подключения" value="12" status="success" />
          </template>
        </ServiceStatusCard>
      </div>
    </section>

    <!-- Metric Items -->
    <section class="showcase-section">
      <h3 class="section-title">Элементы метрик</h3>
      <BaseCard class="metrics-list-card">
        <div class="metrics-list">
          <MetricItem label="Общее количество резюме" value="1,247" />
          <MetricItem label="Обработано сегодня" value="89" status="success" />
          <MetricItem label="Средняя оценка" value="87.5%" status="success" />
          <MetricItem label="Ошибки обработки" value="3" status="error" />
          <MetricItem label="Время обработки" value="2.3s" status="warning" />
          <MetricItem label="Активные сессии" value="12" status="success" />
        </div>
      </BaseCard>
    </section>
  </div>
</template>

<script setup lang="ts">
import BaseMetricCard from '@/components/base/BaseMetricCard.vue'
import BaseCard from '@/components/base/BaseCard.vue'
import SystemMetricCard from '@/components/SystemMetricCard.vue'
import ServiceStatusCard from '@/components/ServiceStatusCard.vue'
import MetricItem from '@/components/MetricItem.vue'
</script>

<style scoped>
.metrics-showcase {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  padding: 2rem;
  position: relative;
  overflow-x: hidden;
}

.metrics-showcase::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 80%, rgba(0, 255, 255, 0.1) 0%, transparent 60%),
    radial-gradient(circle at 80% 20%, rgba(138, 43, 226, 0.1) 0%, transparent 60%),
    radial-gradient(circle at 40% 40%, rgba(75, 0, 130, 0.08) 0%, transparent 50%);
  pointer-events: none;
  z-index: -1;
}

.showcase-header {
  text-align: center;
  margin-bottom: 3rem;
}

.showcase-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #00ffff;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
  margin-bottom: 0.5rem;
}

.showcase-subtitle {
  font-size: 1.125rem;
  color: #e2e8f0;
  margin: 0;
}

.showcase-section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #00ffff;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
  margin-bottom: 1.5rem;
  text-align: center;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.metrics-list-card {
  max-width: 600px;
  margin: 0 auto;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.6)) !important;
  border: 1px solid rgba(0, 255, 255, 0.2) !important;
  backdrop-filter: blur(20px);
  box-shadow: 
    0 4px 20px rgba(0, 0, 0, 0.3),
    0 0 20px rgba(0, 255, 255, 0.1);
}

.metrics-list {
  padding: 1.5rem;
}
</style>