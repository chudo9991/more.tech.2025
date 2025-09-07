<template>
  <div class="navbar">
    <div class="nav-brand">
      <h2>Система ИИ-Интервью</h2>
    </div>
    <div class="nav-links">
      <router-link to="/" class="nav-link">Главная</router-link>
      <router-link to="/hr" class="nav-link">HR Панель</router-link>
      <router-link to="/vacancies" class="nav-link">Вакансии</router-link>
      <router-link to="/resumes" class="nav-link">Резюме</router-link>
      <router-link to="/scenarios" class="nav-link">Сценарии</router-link>
      <router-link to="/interview" class="nav-link">Интервью</router-link>
      <router-link to="/model-status" class="nav-link">Статус модели</router-link>
      <router-link to="/metrics-showcase" class="nav-link">Демо карточек</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NavBar'
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.nav-brand h2 {
  margin: 0;
  color: white;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-link {
  text-decoration: none;
  color: white;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
}
</style>
