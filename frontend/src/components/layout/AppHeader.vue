<template>
  <header class="app-header">
    <div class="header-container">
      <!-- Logo and Brand -->
      <div class="header-brand">
        <router-link to="/" class="brand-link">
          <div class="brand-logo">
            <svg class="logo-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
          </div>
          <span class="brand-text">Система ИИ-Интервью</span>
        </router-link>
      </div>

      <!-- Desktop Navigation -->
      <nav class="desktop-nav" :class="{ 'nav-hidden': isMobileMenuOpen }">
        <BaseButton
          v-for="item in navigationItems"
          :key="item.id"
          tag="router-link"
          :to="item.route"
          :variant="isActiveRoute(item.route) ? 'primary' : 'ghost'"
          size="small"
          :icon="item.icon"
          @click="closeSearch"
          class="nav-button"
        >
          <span class="nav-text">{{ item.label }}</span>
        </BaseButton>
      </nav>
    </div>

    <!-- Mobile Navigation Menu -->
    <transition name="mobile-menu">
      <nav v-if="isMobileMenuOpen" class="mobile-nav" role="navigation">
        <div class="mobile-nav-content">
          <router-link
            v-for="item in navigationItems"
            :key="item.id"
            :to="item.route"
            class="mobile-nav-link"
            :class="{ 'mobile-nav-link-active': isActiveRoute(item.route) }"
            @click="closeMobileMenu"
          >
            <component :is="item.icon" class="mobile-nav-icon" />
            <span class="mobile-nav-text">{{ item.label }}</span>
          </router-link>
        </div>
      </nav>
    </transition>

    <!-- Mobile Menu Backdrop -->
    <div
      v-if="isMobileMenuOpen"
      class="mobile-backdrop"
      @click="closeMobileMenu"
      aria-hidden="true"
    ></div>
  </header>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { BaseButton } from '@/components/base'

// Props
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

// Emits
const emit = defineEmits(['search', 'logout'])

// Reactive state
const route = useRoute()
const searchQuery = ref('')
const searchInput = ref()
const userDropdown = ref()
const isMobileMenuOpen = ref(false)
const isUserMenuOpen = ref(false)

// Navigation items with simple icons
const navigationItems = [
  { 
    id: 'home', 
    label: 'Главная', 
    route: '/', 
    icon: { 
      template: '<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"/></svg>' 
    }
  },
  { 
    id: 'hr', 
    label: 'HR Панель', 
    route: '/hr', 
    icon: { 
      template: '<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V8a2 2 0 012-2h2zm4-3a1 1 0 00-1 1v1h2V4a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>' 
    }
  },
  { 
    id: 'vacancies', 
    label: 'Вакансии', 
    route: '/vacancies', 
    icon: { 
      template: '<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd"/></svg>' 
    }
  },
  { 
    id: 'resumes', 
    label: 'Резюме', 
    route: '/resumes', 
    icon: { 
      template: '<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/></svg>' 
    }
  },
  { 
    id: 'scenarios', 
    label: 'Сценарии', 
    route: '/scenarios', 
    icon: { 
      template: '<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/></svg>' 
    }
  },
  { 
    id: 'interview', 
    label: 'Интервью', 
    route: '/interview', 
    icon: { 
      template: '<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd"/></svg>' 
    }
  },
  { 
    id: 'model-status', 
    label: 'Статус модели', 
    route: '/model-status', 
    icon: { 
      template: '<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>' 
    }
  },
]


// Methods
const isActiveRoute = (routePath) => {
  if (!route?.path) return false
  return route.path === routePath || route.path.startsWith(routePath + '/')
}

const getRoleLabel = (role) => {
  const roleLabels = {
    admin: 'Администратор',
    hr: 'HR-менеджер',
    interviewer: 'Интервьюер',
    candidate: 'Кандидат'
  }
  return roleLabels[role || ''] || 'Пользователь'
}

const toggleSearch = async () => {
  searchQuery.value = searchQuery.value ? '' : ' '
  if (searchQuery.value) {
    await nextTick()
    searchInput.value?.focus()
  }
}

const closeSearch = () => {
  searchQuery.value = ''
}

const clearSearch = () => {
  searchQuery.value = ''
  searchInput.value?.focus()
}

const handleSearchBlur = () => {
  if (!searchQuery.value.trim()) {
    closeSearch()
  }
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
  if (isMobileMenuOpen.value) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
  document.body.style.overflow = ''
}

const toggleUserMenu = () => {
  isUserMenuOpen.value = !isUserMenuOpen.value
}

const closeUserMenu = () => {
  isUserMenuOpen.value = false
}

const handleUserMenuClick = (item) => {
  if (item.action) {
    item.action()
  }
  closeUserMenu()
}

// Handle clicks outside user dropdown
const handleClickOutside = (event) => {
  if (userDropdown.value && !userDropdown.value.contains(event.target)) {
    closeUserMenu()
  }
}

// Handle escape key
const handleEscapeKey = (event) => {
  if (event.key === 'Escape') {
    if (isUserMenuOpen.value) {
      closeUserMenu()
    } else if (isMobileMenuOpen.value) {
      closeMobileMenu()
    } else if (searchQuery.value) {
      closeSearch()
    }
  }
}

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleEscapeKey)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleEscapeKey)
  document.body.style.overflow = ''
})
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95)) !important;
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
  position: sticky;
  top: 0;
  z-index: 50;
  box-shadow: 
    0 4px 20px rgba(0, 0, 0, 0.3),
    0 0 40px rgba(0, 255, 255, 0.1);
}

.header-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 4rem;
}

/* Brand */
.header-brand {
  flex-shrink: 0;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #00ffff;
  text-decoration: none;
  transition: all 0.3s ease;
}

.brand-link:hover {
  text-shadow: 0 0 15px rgba(0, 255, 255, 0.8);
  transform: translateX(2px);
}

.brand-logo {
  flex-shrink: 0;
}

.logo-icon {
  width: 2rem;
  height: 2rem;
  color: #00ffff;
  filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.5));
}

.brand-text {
  font-size: 1.125rem;
  font-weight: 600;
  display: none;
}

@media (min-width: 640px) {
  .brand-text {
    display: block;
  }
}

/* Desktop Navigation */
.desktop-nav {
  display: none;
  align-items: center;
  gap: 0.25rem;
}

@media (min-width: 768px) {
  .desktop-nav {
    display: flex;
  }
}

.nav-hidden {
  opacity: 0;
  pointer-events: none;
}

.nav-button {
  min-width: auto;
}

.nav-text {
  display: none;
}

@media (min-width: 1024px) {
  .nav-text {
    display: block;
  }
}

/* Search */
.search-container {
  flex: 1;
  max-width: 32rem;
  margin: 0 1rem;
}

.search-input-wrapper {
  position: relative;
}

.search-input {
  width: 100%;
  padding: 0.625rem 2.5rem 0.625rem 2.5rem;
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 0.5rem;
  color: #e2e8f0;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.search-input::placeholder {
  color: #94a3b8;
}

.search-input:focus {
  outline: none;
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 0 2px rgba(0, 255, 255, 0.1);
  background: rgba(15, 23, 42, 0.9);
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1rem;
  height: 1rem;
  color: #94a3b8;
}

.search-clear {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  padding: 0.25rem;
  border-radius: 9999px;
  color: #94a3b8;
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.search-clear:hover {
  color: #e2e8f0;
  background: rgba(148, 163, 184, 0.1);
}

.clear-icon {
  width: 0.75rem;
  height: 0.75rem;
}

/* Header Actions */
.header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* User Dropdown */
.user-dropdown {
  position: relative;
}

.user-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem;
  border-radius: 0.5rem;
  color: #e2e8f0;
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.user-button:hover {
  background: rgba(148, 163, 184, 0.1);
}

.user-button:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 255, 255, 0.5);
}

.user-avatar {
  flex-shrink: 0;
}

.avatar-image {
  width: 2rem;
  height: 2rem;
  border-radius: 9999px;
  object-fit: cover;
}

.avatar-placeholder {
  width: 2rem;
  height: 2rem;
  border-radius: 9999px;
  background: rgba(148, 163, 184, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-icon {
  width: 1.25rem;
  height: 1.25rem;
  color: #94a3b8;
}

.user-info {
  display: none;
  text-align: left;
}

@media (min-width: 640px) {
  .user-info {
    display: block;
  }
}

.user-name {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #e2e8f0;
}

.user-role {
  display: block;
  font-size: 0.75rem;
  color: #94a3b8;
}

.dropdown-icon {
  width: 1rem;
  height: 1rem;
  color: #94a3b8;
  transition: transform 0.2s ease;
}

.dropdown-icon-open {
  transform: rotate(180deg);
}

/* User Menu */
.user-menu {
  position: absolute;
  right: 0;
  margin-top: 0.5rem;
  width: 12rem;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 0.5rem;
  padding: 0.5rem 0;
  z-index: 50;
  box-shadow: 
    0 4px 25px rgba(0, 0, 0, 0.4),
    0 0 20px rgba(0, 255, 255, 0.1);
}

.user-menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 1rem;
  font-size: 0.875rem;
  color: #e2e8f0;
  text-decoration: none;
  transition: all 0.2s ease;
}

.user-menu-item:hover {
  background: rgba(0, 255, 255, 0.1);
  color: #00ffff;
}

.user-menu-item:focus {
  outline: none;
  background: rgba(0, 255, 255, 0.1);
}

.menu-item-icon {
  width: 1rem;
  height: 1rem;
  color: #94a3b8;
}

/* Mobile Menu Toggle */
.mobile-menu-toggle {
  display: block;
  padding: 0.625rem;
  border-radius: 0.5rem;
  color: #e2e8f0;
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

@media (min-width: 768px) {
  .mobile-menu-toggle {
    display: none;
  }
}

.mobile-menu-toggle:hover {
  background: rgba(148, 163, 184, 0.1);
}

.mobile-menu-toggle:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 255, 255, 0.5);
}

.hamburger {
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.375rem;
}

.hamburger-line {
  width: 100%;
  height: 0.125rem;
  background: currentColor;
  transition: all 0.3s ease;
  transform-origin: center;
}

.hamburger-open .hamburger-line:nth-child(1) {
  transform: rotate(45deg) translate(3px, 3px);
}

.hamburger-open .hamburger-line:nth-child(2) {
  opacity: 0;
  transform: scale(0);
}

.hamburger-open .hamburger-line:nth-child(3) {
  transform: rotate(-45deg) translate(3px, -3px);
}

/* Mobile Navigation */
.mobile-nav {
  display: block;
  background: rgba(15, 23, 42, 0.98);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(0, 255, 255, 0.2);
}

@media (min-width: 768px) {
  .mobile-nav {
    display: none;
  }
}

.mobile-nav-content {
  padding: 1rem;
  gap: 0.5rem;
  display: flex;
  flex-direction: column;
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 500;
  color: #e2e8f0;
  text-decoration: none;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.mobile-nav-link:hover {
  color: #00ffff;
  background: rgba(0, 255, 255, 0.1);
  border-color: rgba(0, 255, 255, 0.3);
}

.mobile-nav-link-active {
  color: #00ffff;
  background: rgba(0, 255, 255, 0.2);
  border-color: rgba(0, 255, 255, 0.4);
}

.mobile-nav-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.mobile-nav-text {
  flex: 1;
}

/* Mobile Backdrop */
.mobile-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.25);
  z-index: 40;
}

@media (min-width: 768px) {
  .mobile-backdrop {
    display: none;
  }
}

/* Transitions */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-0.5rem);
}

.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: all 0.3s ease;
}

.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-1rem);
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .brand-text {
    font-size: 1rem;
  }
  
  .header-container {
    padding: 0 0.75rem;
  }
}

/* Focus styles for accessibility */
.nav-link:focus,
.mobile-nav-link:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 255, 255, 0.5);
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .nav-link,
  .user-button,
  .mobile-nav-link,
  .hamburger-line,
  .dropdown-icon {
    transition: none;
  }
}
</style>