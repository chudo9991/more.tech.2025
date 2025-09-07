<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-container">
        <div class="hero-content">
          <!-- Hero Text -->
          <div class="hero-text" :class="{ 'animate-fade-in-up': isVisible }">
            <h1 class="hero-title">
              Система ИИ-Интервью
              <span class="hero-title-accent">нового поколения</span>
            </h1>
            <p class="hero-description">
              Революционная платформа для проведения интеллектуальных интервью с использованием 
              искусственного интеллекта и современных технологий распознавания речи
            </p>
            
            <!-- CTA Buttons -->
            <div class="hero-actions">
              <router-link to="/interview" class="cta-button cta-primary">
                Начать интервью с AI-аватаром
              </router-link>
              <router-link to="/hr" class="cta-button cta-secondary">
                Открыть HR панель
              </router-link>
            </div>
          </div>

          <!-- Hero Visual -->
          <div class="hero-visual" :class="{ 'animate-fade-in-right': isVisible }">
            <div class="hero-image-container">
              <div class="hero-gradient-orb hero-gradient-orb-1"></div>
              <div class="hero-gradient-orb hero-gradient-orb-2"></div>
              <div class="hero-image-placeholder">
                <IconAIAvatar :size="120" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="features-container">
        <div class="features-header" :class="{ 'animate-fade-in-up': featuresVisible }">
          <h2 class="features-title">Возможности платформы</h2>
          <p class="features-description">
            Современные технологии для эффективного проведения интервью и оценки кандидатов
          </p>
        </div>

        <div class="features-grid">
          <div
            v-for="(feature, index) in features"
            :key="feature.id"
            :class="[
              'feature-card',
              { 'animate-fade-in-up': featuresVisible }
            ]"
            :style="{ animationDelay: `${index * 150}ms` }"
          >
            <div class="feature-content">
              <div class="feature-icon">
                <component :is="feature.icon" :size="48" :color="feature.color" />
              </div>
              <h3 class="feature-title">{{ feature.title }}</h3>
              <p class="feature-description">{{ feature.description }}</p>
              <ul class="feature-benefits">
                <li v-for="benefit in feature.benefits" :key="benefit">
                  <span class="benefit-check">✓</span> {{ benefit }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section">
      <div class="stats-container">
        <div class="stats-grid">
          <div
            v-for="(stat, index) in stats"
            :key="stat.label"
            class="stat-item"
            :class="{ 'animate-fade-in-up': statsVisible }"
            :style="{ animationDelay: `${index * 100}ms` }"
          >
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="cta-container">
        <div class="cta-content" :class="{ 'animate-fade-in-up': ctaVisible }">
          <h2 class="cta-title">Готовы начать?</h2>
          <p class="cta-description">
            Присоединяйтесь к компаниям, которые уже используют нашу платформу для поиска лучших кандидатов
          </p>
          <div class="cta-actions">
            <router-link to="/interview" class="cta-button cta-primary">
              Попробовать бесплатно
            </router-link>
            <button @click="scrollToFeatures" class="cta-button cta-ghost">
              Узнать больше
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import IconMicrophone from '@/components/icons/IconMicrophone.vue'
import IconBrain from '@/components/icons/IconBrain.vue'
import IconChart from '@/components/icons/IconChart.vue'
import IconRobot from '@/components/icons/IconRobot.vue'
import IconDocument from '@/components/icons/IconDocument.vue'
import IconBriefcase from '@/components/icons/IconBriefcase.vue'
import IconAIAvatar from '@/components/icons/IconAIAvatar.vue'

// Reactive state for animations
const isVisible = ref(false)
const featuresVisible = ref(false)
const statsVisible = ref(false)
const ctaVisible = ref(false)

// Features data
const features = ref([
  {
    id: 'speech-recognition',
    icon: IconMicrophone,
    color: '#00ffff',
    title: 'Распознавание речи',
    description: 'Передовые технологии преобразования речи в текст с высокой точностью',
    benefits: [
      'Поддержка множества языков',
      'Фильтрация шумов',
      'Реальное время обработки'
    ]
  },
  {
    id: 'ai-evaluation',
    icon: IconBrain,
    color: '#8a2be2',
    title: 'ИИ-Оценка',
    description: 'Интеллектуальный анализ ответов кандидатов с использованием машинного обучения',
    benefits: [
      'Объективная оценка',
      'Анализ эмоций',
      'Персонализированные рекомендации'
    ]
  },
  {
    id: 'analytics',
    icon: IconChart,
    color: '#1e90ff',
    title: 'Аналитика и отчеты',
    description: 'Подробная аналитика процесса интервью и результатов оценки',
    benefits: [
      'Детальные отчеты',
      'Сравнительный анализ',
      'Экспорт данных'
    ]
  },
  {
    id: 'avatar-integration',
    icon: IconRobot,
    color: '#00ffff',
    title: 'AI-Аватар',
    description: 'Интерактивный виртуальный интервьюер для естественного общения',
    benefits: [
      'Естественные диалоги',
      'Адаптивные сценарии',
      'Эмоциональный интеллект'
    ]
  },
  {
    id: 'resume-processing',
    icon: IconDocument,
    color: '#ff1493',
    title: 'Обработка резюме',
    description: 'Автоматический анализ и структурирование резюме кандидатов',
    benefits: [
      'Извлечение ключевых навыков',
      'Сопоставление с вакансиями',
      'Пакетная обработка'
    ]
  },
  {
    id: 'vacancy-management',
    icon: IconBriefcase,
    color: '#9932cc',
    title: 'Управление вакансиями',
    description: 'Комплексная система управления вакансиями и требованиями',
    benefits: [
      'Шаблоны вакансий',
      'Автоматическое сопоставление',
      'Статистика по вакансиям'
    ]
  }
])

// Statistics data
const stats = ref([
  { value: '10,000+', label: 'Проведенных интервью' },
  { value: '95%', label: 'Точность оценки' },
  { value: '500+', label: 'Довольных клиентов' },
  { value: '24/7', label: 'Поддержка' }
])

// Intersection Observer for scroll animations
let observer: IntersectionObserver | null = null

const setupScrollAnimations = () => {
  if (typeof window === 'undefined') return

  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const target = entry.target as HTMLElement
          
          if (target.classList.contains('hero-section')) {
            isVisible.value = true
          } else if (target.classList.contains('features-section')) {
            featuresVisible.value = true
          } else if (target.classList.contains('stats-section')) {
            statsVisible.value = true
          } else if (target.classList.contains('cta-section')) {
            ctaVisible.value = true
          }
        }
      })
    },
    {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    }
  )

  // Observe sections
  const sections = document.querySelectorAll('.hero-section, .features-section, .stats-section, .cta-section')
  sections.forEach((section) => observer?.observe(section))
}

const scrollToFeatures = () => {
  const featuresSection = document.querySelector('.features-section')
  if (featuresSection) {
    featuresSection.scrollIntoView({ 
      behavior: 'smooth',
      block: 'start'
    })
  }
}

onMounted(() => {
  // Trigger hero animation immediately
  setTimeout(() => {
    isVisible.value = true
  }, 100)
  
  // Setup scroll animations
  setTimeout(setupScrollAnimations, 200)
})

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
  }
})
</script>

<style scoped>
/* Home Page Styles */
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #0f172a 50%, #1e293b 75%, #0f172a 100%);
  position: relative;
  overflow-x: hidden;
}

.home::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 80%, rgba(0, 255, 255, 0.15) 0%, transparent 60%),
    radial-gradient(circle at 80% 20%, rgba(138, 43, 226, 0.15) 0%, transparent 60%),
    radial-gradient(circle at 40% 40%, rgba(75, 0, 130, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 90% 90%, rgba(255, 20, 147, 0.1) 0%, transparent 40%),
    radial-gradient(circle at 10% 10%, rgba(30, 144, 255, 0.08) 0%, transparent 50%);
  pointer-events: none;
  z-index: -1;
}

.home::after {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(45deg, rgba(0, 255, 255, 0.03) 25%, transparent 25%),
    linear-gradient(-45deg, rgba(138, 43, 226, 0.03) 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, rgba(0, 255, 255, 0.03) 75%),
    linear-gradient(-45deg, transparent 75%, rgba(138, 43, 226, 0.03) 75%);
  background-size: 60px 60px;
  background-position: 0 0, 0 30px, 30px -30px, -30px 0px;
  pointer-events: none;
  z-index: -1;
  opacity: 0.4;
  animation: backgroundShift 20s ease-in-out infinite;
}

@keyframes backgroundShift {
  0%, 100% { 
    transform: translate(0, 0);
    opacity: 0.4;
  }
  50% { 
    transform: translate(10px, 10px);
    opacity: 0.6;
  }
}

/* Hero Section */
.hero-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  position: relative;
  background: transparent;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs><pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse"><path d="M 50 0 L 0 0 0 50" fill="none" stroke="rgba(0,255,255,0.1)" stroke-width="1"/></pattern></defs><rect width="100%" height="100%" fill="url(%23grid)"/></svg>');
  pointer-events: none;
}

.hero-section::after {
  content: '';
  position: absolute;
  top: 10%;
  left: 5%;
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(138, 43, 226, 0.1));
  border-radius: 50%;
  filter: blur(60px);
  animation: floatingSphere1 15s ease-in-out infinite;
  pointer-events: none;
}

@keyframes floatingSphere1 {
  0%, 100% { 
    transform: translate(0, 0) scale(1);
    opacity: 0.6;
  }
  33% { 
    transform: translate(100px, -50px) scale(1.2);
    opacity: 0.8;
  }
  66% { 
    transform: translate(-50px, 100px) scale(0.8);
    opacity: 0.4;
  }
}

.hero-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1.5rem;
  position: relative;
  z-index: 1;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  min-height: 80vh;
}

.hero-text {
  color: #e2e8f0;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  letter-spacing: -0.025em;
}

.hero-title-accent {
  display: block;
  background: linear-gradient(135deg, #00ffff, #8a2be2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
}

.hero-description {
  font-size: 1.25rem;
  line-height: 1.6;
  margin-bottom: 2.5rem;
  opacity: 0.9;
  max-width: 500px;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

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

.cta-button.cta-secondary {
  background: rgba(15, 23, 42, 0.7) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(138, 43, 226, 0.5) !important;
  color: #8a2be2 !important;
  box-shadow: 0 8px 32px rgba(138, 43, 226, 0.2);
}

.cta-button.cta-secondary:hover {
  background: rgba(138, 43, 226, 0.2) !important;
  border-color: rgba(138, 43, 226, 0.7) !important;
  transform: translateY(-3px);
  box-shadow: 0 12px 40px rgba(138, 43, 226, 0.4);
  text-shadow: 0 0 15px rgba(138, 43, 226, 1);
}

.cta-ghost {
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  color: #00ffff;
  box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
}

.cta-ghost:hover {
  background: rgba(0, 255, 255, 0.1);
  border-color: rgba(0, 255, 255, 0.5);
  color: #00ffff;
  transform: translateY(-3px);
  box-shadow: 0 12px 40px rgba(0, 255, 255, 0.3);
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.8);
}

/* Hero Visual */
.hero-visual {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.hero-image-container {
  position: relative;
  width: 450px;
  height: 450px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(40px);
  opacity: 0.7;
  animation: float 6s ease-in-out infinite;
}

.hero-gradient-orb-1 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.3), rgba(75, 0, 130, 0.3));
  top: -75px;
  left: -75px;
  animation-delay: 0s;
}

.hero-gradient-orb-2 {
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, rgba(138, 43, 226, 0.35), rgba(75, 0, 130, 0.35));
  bottom: -50px;
  right: -50px;
  animation-delay: 3s;
}

.hero-image-container::before {
  content: '';
  position: absolute;
  top: 20%;
  right: -10%;
  width: 80px;
  height: 80px;
  background: linear-gradient(45deg, rgba(255, 20, 147, 0.4), rgba(0, 255, 255, 0.4));
  border-radius: 50%;
  filter: blur(20px);
  animation: floatingOrb1 8s ease-in-out infinite;
}

.hero-image-container::after {
  content: '';
  position: absolute;
  bottom: 10%;
  left: -15%;
  width: 60px;
  height: 60px;
  background: linear-gradient(45deg, rgba(30, 144, 255, 0.5), rgba(138, 43, 226, 0.5));
  border-radius: 50%;
  filter: blur(15px);
  animation: floatingOrb2 6s ease-in-out infinite reverse;
}

@keyframes floatingOrb1 {
  0%, 100% { 
    transform: translateY(0px) translateX(0px) scale(1);
    opacity: 0.6;
  }
  50% { 
    transform: translateY(-30px) translateX(20px) scale(1.3);
    opacity: 0.9;
  }
}

@keyframes floatingOrb2 {
  0%, 100% { 
    transform: translateY(0px) translateX(0px) scale(1);
    opacity: 0.5;
  }
  50% { 
    transform: translateY(25px) translateX(-15px) scale(1.2);
    opacity: 0.8;
  }
}

.hero-image-placeholder {
  position: relative;
  z-index: 2;
  width: 240px;
  height: 240px;
  background: rgba(15, 23, 42, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(30px);
  border: 3px solid rgba(0, 255, 255, 0.4);
  box-shadow: 
    0 0 50px rgba(0, 255, 255, 0.3),
    inset 0 0 30px rgba(138, 43, 226, 0.2);
  transition: all 0.4s ease;
}

.hero-image-placeholder:hover {
  transform: scale(1.05);
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 
    0 0 80px rgba(0, 255, 255, 0.5),
    inset 0 0 40px rgba(138, 43, 226, 0.3);
}

.robot-icon {
  font-size: 4rem;
}

/* Features Section */
.features-section {
  padding: 6rem 0;
  background: transparent;
  position: relative;
}

.features-section::before {
  content: '';
  position: absolute;
  top: 20%;
  right: 10%;
  width: 150px;
  height: 150px;
  background: radial-gradient(circle, rgba(0, 255, 255, 0.15) 0%, transparent 70%);
  border-radius: 50%;
  animation: pulseGlow 4s ease-in-out infinite;
}

.features-section::after {
  content: '';
  position: absolute;
  bottom: 30%;
  left: 5%;
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, rgba(138, 43, 226, 0.2) 0%, transparent 70%);
  border-radius: 50%;
  animation: pulseGlow 3s ease-in-out infinite reverse;
}

@keyframes pulseGlow {
  0%, 100% { 
    transform: scale(1);
    opacity: 0.6;
  }
  50% { 
    transform: scale(1.4);
    opacity: 0.9;
  }
}

.features-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.features-header {
  text-align: center;
  margin-bottom: 4rem;
}

.features-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 1rem;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}

.features-description {
  font-size: 1.125rem;
  color: #94a3b8;
  max-width: 600px;
  margin: 0 auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: all 0.4s ease;
  border: 1px solid rgba(0, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.feature-card::before {
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

.feature-card:hover {
  transform: translateY(-12px);
  box-shadow: 0 20px 40px rgba(0, 255, 255, 0.2);
  border-color: rgba(0, 255, 255, 0.4);
}

.feature-card:hover::before {
  opacity: 1;
}

.feature-content {
  text-align: center;
}

.feature-icon {
  margin-bottom: 1.5rem;
  font-size: 3rem;
}

.feature-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 1rem;
  position: relative;
  z-index: 1;
}

.feature-description {
  color: #94a3b8;
  margin-bottom: 1.5rem;
  line-height: 1.6;
  position: relative;
  z-index: 1;
}

.feature-benefits {
  list-style: none;
  padding: 0;
  text-align: left;
}

.feature-benefits li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  color: #cbd5e1;
  font-size: 0.875rem;
  position: relative;
  z-index: 1;
}

.benefit-check {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  background: linear-gradient(135deg, #00ffff, #8a2be2);
  color: #0a0a0f;
  border-radius: 50%;
  font-size: 12px;
  font-weight: bold;
  flex-shrink: 0;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

/* Stats Section */
.stats-section {
  padding: 4rem 0;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(0, 255, 255, 0.2);
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
  color: white;
  position: relative;
}

.stats-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.stat-item {
  text-align: center;
  padding: 2rem 1rem;
}

.stat-value {
  font-size: 3rem;
  font-weight: 800;
  background: linear-gradient(135deg, #00ffff, #8a2be2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
}

.stat-label {
  font-size: 1rem;
  color: #cbd5e1;
  font-weight: 500;
}

/* CTA Section */
.cta-section {
  padding: 6rem 0;
  background: transparent;
  position: relative;
}

.cta-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.cta-content {
  text-align: center;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 1rem;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}

.cta-description {
  font-size: 1.125rem;
  color: #94a3b8;
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

.cta-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

/* Animations */
@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

.animate-fade-in-up {
  animation: fadeInUp 0.8s ease-out forwards;
}

.animate-fade-in-right {
  animation: fadeInRight 0.8s ease-out forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Responsive Design */
@media (max-width: 1024px) {
  .hero-content {
    grid-template-columns: 1fr;
    gap: 3rem;
    text-align: center;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-image-container {
    width: 300px;
    height: 300px;
  }
  
  .features-grid {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-description {
    font-size: 1rem;
  }
  
  .hero-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .hero-actions :deep(.btn) {
    width: 100%;
    max-width: 300px;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .stat-value {
    font-size: 2rem;
  }
  
  .features-title,
  .cta-title {
    font-size: 2rem;
  }
}

@media (max-width: 640px) {
  .hero-container,
  .features-container,
  .stats-container,
  .cta-container {
    padding: 0 1rem;
  }
  
  .hero-section {
    padding: 2rem 0;
  }
  
  .features-section,
  .cta-section {
    padding: 4rem 0;
  }
  
  .stats-section {
    padding: 3rem 0;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .hero-image-container {
    width: 250px;
    height: 250px;
  }
  
  .hero-gradient-orb-1 {
    width: 200px;
    height: 200px;
  }
  
  .hero-gradient-orb-2 {
    width: 150px;
    height: 150px;
  }
}
</style>
