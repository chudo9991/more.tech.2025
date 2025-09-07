<template>
  <div class="app-layout">
    <!-- Header -->
    <AppHeader 
      :user="user"
      :show-search="showSearch"
      @search="handleSearch"
      @logout="handleLogout"
    />

    <div class="layout-content">
      <!-- Sidebar -->
      <AppSidebar 
        v-model:collapsed="sidebarCollapsed"
        v-model:mobile-open="sidebarMobileOpen"
        @navigate="handleNavigation"
      />

      <!-- Main Content -->
      <main class="main-content" :class="{ 'main-content-expanded': sidebarCollapsed }">
        <div class="content-wrapper">
          <!-- Header slot -->
          <slot name="header" />
          
          <!-- Default content -->
          <slot />
        </div>
        
        <!-- Footer -->
        <AppFooter 
          :company-info="companyInfo"
          :show-social-links="true"
          :system-status="systemStatus"
        />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
// @ts-nocheck
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from './AppHeader.vue'
import AppSidebar from './AppSidebar.vue'
import AppFooter from './AppFooter.vue'
import type { UserInfo } from '@/types/user'

interface Props {
  user?: UserInfo
  showSearch?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showSearch: true
})

const emit = defineEmits<{
  search: [query: string]
  logout: []
}>()

// Router
const router = useRouter()

// Reactive state
const sidebarCollapsed = ref(false)
const sidebarMobileOpen = ref(false)
const systemStatus = ref<'online' | 'maintenance' | 'offline'>('online')

// Company information
const companyInfo = {
  name: 'Система ИИ-Интервью',
  description: 'Современная платформа для проведения автоматизированных интервью с использованием искусственного интеллекта.',
  email: 'support@ai-interview.ru',
  phone: '+7 (495) 123-45-67',
  address: 'Москва, Россия'
}

// Methods
const handleSearch = (query: string) => {
  emit('search', query)
}

const handleLogout = () => {
  emit('logout')
}

const handleNavigation = (route: string) => {
  router.push(route)
  sidebarMobileOpen.value = false
}
</script>

<style scoped>
.app-layout {
  @apply min-h-screen bg-neutral-50;
}

.layout-content {
  @apply flex;
}

.main-content {
  @apply flex-1 flex flex-col min-h-screen;
  margin-left: 320px;
  transition: margin-left 0.3s ease-in-out;
}

.main-content-expanded {
  margin-left: 80px;
}

.content-wrapper {
  @apply flex-1 p-8;
  min-height: calc(100vh - 64px); /* Учитываем высоту header */
}

/* Responsive Design */
@media (max-width: 1024px) {
  .main-content {
    margin-left: 0;
  }
  
  .main-content-expanded {
    margin-left: 0;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .main-content {
    transition: none;
  }
}
</style>