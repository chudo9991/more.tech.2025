<template>
  <div class="button-showcase">
    <div class="showcase-container">
      <h2 class="showcase-title">Демонстрация кнопок</h2>
      
      <div class="button-groups">
        <!-- Primary Buttons (как на главной странице) -->
        <div class="button-group">
          <h3 class="group-title">Primary кнопки (точно как cta-primary)</h3>
          <div class="buttons-row">
            <BaseButton variant="primary" size="lg">Начать интервью с AI-аватаром</BaseButton>
            <BaseButton variant="primary" icon="mdi mdi-plus" size="md">Новая сессия</BaseButton>
            <BaseButton variant="primary" size="md">Создать вакансию</BaseButton>
            <BaseButton variant="primary" icon="mdi mdi-loading" loading size="md">Загрузка</BaseButton>
          </div>
          
          <!-- Сравнение с оригиналом -->
          <div class="comparison-section">
            <h4 class="comparison-title">Сравнение с оригиналом (должны быть АБСОЛЮТНО одинаковые):</h4>
            <div class="comparison-buttons">
              <div class="cta-button cta-primary">
                Начать интервью с AI-аватаром (ОРИГИНАЛ)
              </div>
              <BaseButton variant="primary" size="lg">Начать интервью с AI-аватаром (BaseButton)</BaseButton>
            </div>
          </div>
        </div>

        <!-- Secondary Buttons (как на главной странице) -->
        <div class="button-group">
          <h3 class="group-title">Secondary кнопки (стиль cta-secondary)</h3>
          <div class="buttons-row">
            <BaseButton variant="secondary" size="sm">Отмена</BaseButton>
            <BaseButton variant="secondary" size="md">Открыть HR панель</BaseButton>
            <BaseButton variant="secondary" size="lg">Назад к списку</BaseButton>
            <BaseButton variant="secondary" icon="mdi mdi-cog" size="md">Настройки</BaseButton>
          </div>
        </div>

        <!-- Outline Buttons -->
        <div class="button-group">
          <h3 class="group-title">Outline кнопки</h3>
          <div class="buttons-row">
            <BaseButton variant="secondary" size="sm">Маленькая</BaseButton>
            <BaseButton variant="secondary" size="md">Средняя</BaseButton>
            <BaseButton variant="secondary" size="lg">Большая</BaseButton>
            <BaseButton variant="secondary" icon="mdi mdi-download">С иконкой</BaseButton>
          </div>
        </div>

        <!-- Ghost Buttons -->
        <div class="button-group">
          <h3 class="group-title">Ghost кнопки</h3>
          <div class="buttons-row">
            <BaseButton variant="secondary" size="sm">Маленькая</BaseButton>
            <BaseButton variant="secondary" size="md">Средняя</BaseButton>
            <BaseButton variant="secondary" size="lg">Большая</BaseButton>
            <BaseButton variant="secondary" icon="mdi mdi-eye">С иконкой</BaseButton>
          </div>
        </div>

        <!-- Danger Buttons -->
        <div class="button-group">
          <h3 class="group-title">Danger кнопки</h3>
          <div class="buttons-row">
            <BaseButton variant="danger" size="sm">Маленькая</BaseButton>
            <BaseButton variant="danger" size="md">Средняя</BaseButton>
            <BaseButton variant="danger" size="lg">Большая</BaseButton>
            <BaseButton variant="danger" icon="mdi mdi-delete">С иконкой</BaseButton>
          </div>
        </div>

        <!-- Icon Only Buttons -->
        <div class="button-group">
          <h3 class="group-title">Только иконки</h3>
          <div class="buttons-row">
            <BaseButton variant="primary" icon="mdi mdi-plus" icon-only size="sm" />
            <BaseButton variant="secondary" icon="mdi mdi-cog" icon-only size="md" />
            <BaseButton variant="secondary" icon="mdi mdi-download" icon-only size="lg" />
            <BaseButton variant="secondary" icon="mdi mdi-eye" icon-only />
            <BaseButton variant="danger" icon="mdi mdi-delete" icon-only />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import BaseButton from '@/components/base/BaseButton.vue'
</script>

<style scoped>
.button-showcase {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  position: relative;
  padding: 2rem;
}

.button-showcase::before {
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

.showcase-container {
  max-width: 1200px;
  margin: 0 auto;
}

.showcase-title {
  font-size: 2rem;
  font-weight: 700;
  color: #00ffff;
  text-align: center;
  margin-bottom: 3rem;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
}

.button-groups {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.button-group {
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 16px;
  padding: 2rem;
}

.group-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 1rem;
}

.buttons-row {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: center;
}

/* Comparison section */
.comparison-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(0, 255, 255, 0.2);
}

.comparison-title {
  font-size: 1rem;
  font-weight: 500;
  color: #cbd5e1;
  margin-bottom: 1rem;
}

.comparison-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: center;
}

/* Original cta-button styles for comparison */
.cta-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.1rem;
  text-decoration: none;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  cursor: pointer;
  min-width: 200px;
}

.cta-button.cta-primary {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(138, 43, 226, 0.2)) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.5) !important;
  color: #00ffff !important;
  box-shadow: 0 8px 32px rgba(0, 255, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.cta-button.cta-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.4), transparent);
  transition: left 0.6s ease;
}

.cta-button.cta-primary:hover {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.35), rgba(138, 43, 226, 0.35)) !important;
  transform: translateY(-3px);
  box-shadow: 0 12px 40px rgba(0, 255, 255, 0.5);
  text-shadow: 0 0 15px rgba(0, 255, 255, 1);
}

.cta-button.cta-primary:hover::before {
  left: 100%;
}

@media (max-width: 768px) {
  .buttons-row,
  .comparison-buttons {
    flex-direction: column;
    align-items: stretch;
  }
  
  .buttons-row > *,
  .comparison-buttons > * {
    width: 100%;
  }
}
</style>