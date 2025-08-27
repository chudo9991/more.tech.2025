<template>
  <div class="home">
    <div class="hero">
      <h1>Система ИИ-Интервью</h1>
      <p>Интеллектуальная система проведения интервью</p>
      <div class="features">
        <div class="feature">
          <h3>🎤 Распознавание речи</h3>
          <p>Автоматическое преобразование речи в текст</p>
        </div>
        <div class="feature">
          <h3>🤖 ИИ-Оценка</h3>
          <p>Оценка ответов с помощью искусственного интеллекта</p>
        </div>
        <div class="feature">
          <h3>📊 Аналитика</h3>
          <p>Детальная аналитика и отчеты</p>
        </div>
      </div>
      <div class="cta-buttons">
        <router-link to="/interview" class="cta-button primary">
          🎭 Начать интервью с AI-аватаром
        </router-link>
        <router-link to="/hr" class="cta-button secondary">
          Открыть HR панель
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.hero {
  text-align: center;
  max-width: 800px;
  padding: 2rem;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.hero p {
  font-size: 1.2rem;
  margin-bottom: 3rem;
  opacity: 0.9;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.feature {
  background: rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  border-radius: 10px;
  backdrop-filter: blur(10px);
}

.feature h3 {
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.feature p {
  font-size: 0.9rem;
  opacity: 0.8;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-button {
  display: inline-block;
  color: white;
  padding: 1rem 2rem;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.cta-button.primary {
  background: linear-gradient(135deg, #ff6b6b, #ee5a24);
  border-color: #ff6b6b;
}

.cta-button.secondary {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.cta-button.primary:hover {
  background: linear-gradient(135deg, #ff5252, #d63031);
}

.cta-button.secondary:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>
