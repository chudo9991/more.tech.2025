<template>
  <div class="icon-test-container">
    <h2>Тест иконок BaseMetricCard</h2>
    <div class="test-grid">
      <BaseMetricCard
        title="Документы"
        value="42"
        icon="Document"
        variant="primary"
      />
      <BaseMetricCard
        title="Завершено"
        value="28"
        icon="Check"
        variant="success"
      />
      <BaseMetricCard
        title="В процессе"
        value="14"
        icon="Clock"
        variant="warning"
      />
      <BaseMetricCard
        title="Рейтинг"
        value="4.8"
        icon="Star"
        variant="info"
      />
    </div>
  </div>
</template>

<script setup>
import { BaseMetricCard } from '@/components/base'
</script>

<style scoped>
.icon-test-container {
  padding: 2rem;
}

.test-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}
</style>