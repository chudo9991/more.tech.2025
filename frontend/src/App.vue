<template>
  <AppLayout 
    :user="user"
    :show-search="true"
    @search="handleSearch"
    @logout="handleLogout"
  >
    <router-view />
  </AppLayout>
</template>

<script setup>
import { ref } from 'vue'
import AppLayout from '@/components/layout/AppLayout.vue'

// User data (можно заменить на реальные данные из store)
const user = ref({
  name: 'Администратор',
  role: 'admin',
  avatar: null
})

// Methods
const handleSearch = (query) => {
  console.log('Search query:', query)
  // Здесь можно добавить логику поиска
}

const handleLogout = () => {
  console.log('Logout')
  // Здесь можно добавить логику выхода
}
</script>

<style>
#app {
  font-family: var(--font-family-sans);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

::-webkit-scrollbar {
  width: 0;
}

/* Убираем стили Element Plus header */
.el-header {
  background-color: transparent !important;
  color: inherit !important;
  line-height: inherit !important;
}

.el-main {
  padding: 0 !important;
}
</style>
