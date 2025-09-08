<template>
  <div class="app-layout">
    <!-- Header -->
    <AppHeader 
      :user="user"
      :show-search="showSearch"
      @search="handleSearch"
      @logout="handleLogout"
    />

    <!-- Main Content -->
    <main class="main-content">
      <div class="content-wrapper" :class="{ 'with-padding': !isHomePage }">
        <!-- Header slot -->
        <slot name="header" />
        
        <!-- Default content -->
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AppHeader from './AppHeader.vue'

const props = defineProps({
  user: {
    type: Object,
    default: () => ({})
  },
  showSearch: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['search', 'logout'])

// Router
const router = useRouter()
const route = useRoute()

// Computed
const isHomePage = computed(() => route.path === '/')

// Methods
const handleSearch = (query) => {
  emit('search', query)
}

const handleLogout = () => {
  emit('logout')
}
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #0f172a 50%, #1e293b 75%, #0f172a 100%);
  position: relative;
}



.main-content {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 4rem);
  position: relative;
  z-index: 1;
}

.content-wrapper {
  flex: 1;
  padding: 0;
  min-height: calc(100vh - 4rem);
}

.content-wrapper.with-padding {
  padding: 2rem 3rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .content-wrapper {
    padding: 0;
  }
  
  .content-wrapper.with-padding {
    padding: 1.5rem 2rem;
  }
}

@media (max-width: 480px) {
  .content-wrapper {
    padding: 0;
  }
  
  .content-wrapper.with-padding {
    padding: 1rem 1.5rem;
  }
}
</style>