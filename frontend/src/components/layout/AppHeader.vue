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
        <router-link
          v-for="item in navigationItems"
          :key="item.id"
          :to="item.route"
          class="nav-link"
          :class="{ 'nav-link-active': isActiveRoute(item.route) }"
          @click="closeSearch"
        >
          <component :is="item.icon" class="nav-icon" />
          <span class="nav-text">{{ item.label }}</span>
        </router-link>
      </nav>

      <!-- Search Bar -->
      <div class="search-container" v-if="showSearch">
        <div class="search-input-wrapper">
          <SearchIcon class="search-icon" />
          <input
            ref="searchInput"
            v-model="searchQuery"
            type="text"
            placeholder="Поиск..."
            class="search-input"
            @keydown.escape="closeSearch"
            @blur="handleSearchBlur"
          />
          <button
            v-if="searchQuery"
            @click="clearSearch"
            class="search-clear"
            aria-label="Очистить поиск"
          >
            <XIcon class="clear-icon" />
          </button>
        </div>
      </div>

      <!-- Header Actions -->
      <div class="header-actions">
        <!-- Search Toggle (Mobile) -->
        <BaseButton
          v-if="!showSearch"
          variant="secondary"
          size="sm"
          icon="mdi mdi-magnify"
          icon-only
          @click="toggleSearch"
          aria-label="Открыть поиск"
        />

        <!-- User Profile Dropdown -->
        <div class="user-dropdown" ref="userDropdown">
          <button
            @click="toggleUserMenu"
            @keydown.enter="toggleUserMenu"
            @keydown.space.prevent="toggleUserMenu"
            @keydown.escape="closeUserMenu"
            class="user-button"
            :aria-expanded="isUserMenuOpen"
            aria-haspopup="true"
          >
            <div class="user-avatar">
              <img
                v-if="user?.avatar"
                :src="user.avatar"
                :alt="user.name"
                class="avatar-image"
              />
              <div v-else class="avatar-placeholder">
                <UserIcon class="avatar-icon" />
              </div>
            </div>
            <div class="user-info">
              <span class="user-name">{{ user?.name || 'Пользователь' }}</span>
              <span class="user-role">{{ getRoleLabel(user?.role) }}</span>
            </div>
            <ChevronDownIcon class="dropdown-icon" :class="{ 'dropdown-icon-open': isUserMenuOpen }" />
          </button>

          <!-- User Dropdown Menu -->
          <transition name="dropdown">
            <div
              v-if="isUserMenuOpen"
              class="user-menu"
              role="menu"
              @keydown.escape="closeUserMenu"
            >
              <a
                v-for="item in userMenuItems"
                :key="item.id"
                :href="item.href"
                @click="handleUserMenuClick(item)"
                class="user-menu-item"
                role="menuitem"
                :tabindex="isUserMenuOpen ? 0 : -1"
              >
                <component :is="item.icon" class="menu-item-icon" />
                <span>{{ item.label }}</span>
              </a>
            </div>
          </transition>
        </div>

        <!-- Mobile Menu Toggle -->
        <button
          @click="toggleMobileMenu"
          class="mobile-menu-toggle"
          :aria-expanded="isMobileMenuOpen"
          aria-label="Открыть меню"
        >
          <div class="hamburger" :class="{ 'hamburger-open': isMobileMenuOpen }">
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
          </div>
        </button>
      </div>
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

<script setup lang="ts">
// @ts-nocheck
import { ref, computed, nextTick, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import type { UserInfo } from '@/types/user'
import BaseButton from '@/components/base/BaseButton.vue'

// Icons
import {
  MagnifyingGlassIcon as SearchIcon,
  XMarkIcon as XIcon,
  UserIcon,
  ChevronDownIcon,
  HomeIcon,
  BriefcaseIcon,
  DocumentIcon,
  UsersIcon,
  ChatBubbleLeftRightIcon,
  CpuChipIcon,
  CogIcon,
  ArrowRightOnRectangleIcon
} from '@heroicons/vue/24/outline'

interface NavigationItem {
  id: string
  label: string
  route: string
  icon: any
}

interface UserMenuItem {
  id: string
  label: string
  icon: any
  href?: string
  action?: () => void
}

// Props
interface Props {
  user?: UserInfo
  showSearch?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showSearch: true
})

// Emits
const emit = defineEmits<{
  search: [query: string]
  logout: []
}>()

// Reactive state
const route = useRoute()
const searchQuery = ref('')
const searchInput = ref<HTMLInputElement>()
const userDropdown = ref<HTMLElement>()
const isMobileMenuOpen = ref(false)
const isUserMenuOpen = ref(false)

// Navigation items
const navigationItems: NavigationItem[] = [
  { id: 'home', label: 'Главная', route: '/', icon: HomeIcon },
  { id: 'hr', label: 'HR Панель', route: '/hr', icon: BriefcaseIcon },
  { id: 'vacancies', label: 'Вакансии', route: '/vacancies', icon: DocumentIcon },
  { id: 'resumes', label: 'Резюме', route: '/resumes', icon: UsersIcon },
  { id: 'interview', label: 'Интервью', route: '/interview', icon: ChatBubbleLeftRightIcon },
  { id: 'model-status', label: 'Статус модели', route: '/model-status', icon: CpuChipIcon }
]

// User menu items
const userMenuItems: UserMenuItem[] = [
  { id: 'settings', label: 'Настройки', icon: CogIcon, href: '/settings' },
  { id: 'logout', label: 'Выйти', icon: ArrowRightOnRectangleIcon, action: () => emit('logout') }
]

// Computed
const showSearchInput = computed(() => props.showSearch && searchQuery.value.length > 0)

// Methods
const isActiveRoute = (routePath: string): boolean => {
  if (!route?.path) return false
  return route.path === routePath || route.path.startsWith(routePath + '/')
}

const getRoleLabel = (role?: string): string => {
  const roleLabels: Record<string, string> = {
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

const handleUserMenuClick = (item: UserMenuItem) => {
  if (item.action) {
    item.action()
  }
  closeUserMenu()
}

// Handle clicks outside user dropdown
const handleClickOutside = (event: Event) => {
  if (userDropdown.value && !userDropdown.value.contains(event.target as Node)) {
    closeUserMenu()
  }
}

// Handle escape key
const handleEscapeKey = (event: KeyboardEvent) => {
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

// Watch search query
const handleSearch = () => {
  if (searchQuery.value.trim()) {
    emit('search', searchQuery.value.trim())
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
  @apply bg-white border-b border-neutral-300 sticky top-0 z-50;
  box-shadow: 0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04);
}

.header-container {
  @apply max-w-7xl mx-auto px-4 sm:px-6 lg:px-8;
  @apply flex items-center justify-between h-16;
}

/* Brand */
.header-brand {
  @apply flex-shrink-0;
}

.brand-link {
  @apply flex items-center space-x-3 text-neutral-800 hover:text-primary-600 transition-colors;
  text-decoration: none;
}

.brand-logo {
  @apply flex-shrink-0;
}

.logo-icon {
  @apply w-8 h-8 text-primary-600;
}

.brand-text {
  @apply text-lg font-semibold hidden sm:block;
}

/* Desktop Navigation */
.desktop-nav {
  @apply hidden md:flex items-center space-x-1;
}

.nav-hidden {
  @apply opacity-0 pointer-events-none;
}

.nav-link {
  @apply flex items-center space-x-2 px-4 py-2.5 rounded-lg text-sm font-medium;
  @apply text-neutral-700 hover:text-neutral-800 hover:bg-neutral-100;
  @apply transition-all duration-200 ease-in-out;
  text-decoration: none;
}

.nav-link-active {
  @apply text-primary-600 bg-primary-50 border border-primary-200;
}

.nav-icon {
  @apply w-4 h-4;
}

.nav-text {
  @apply hidden lg:block;
}

/* Search */
.search-container {
  @apply flex-1 max-w-lg mx-4;
}

.search-input-wrapper {
  @apply relative;
}

.search-input {
  @apply w-full pl-10 pr-10 py-2.5 border border-neutral-300 rounded-lg;
  @apply text-sm placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500;
  @apply transition-all duration-200 bg-white;
}

.search-icon {
  @apply absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-neutral-400;
}

.search-clear {
  @apply absolute right-3 top-1/2 transform -translate-y-1/2 p-1 rounded-full;
  @apply text-neutral-400 hover:text-neutral-600 hover:bg-neutral-100;
  @apply transition-colors duration-200;
}

.clear-icon {
  @apply w-3 h-3;
}

/* Header Actions */
.header-actions {
  @apply flex items-center space-x-2;
}

.action-button {
  @apply p-2.5 rounded-lg text-neutral-600 hover:text-neutral-800 hover:bg-neutral-100;
  @apply transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500;
}

.search-toggle {
  @apply md:hidden;
}

.action-icon {
  @apply w-5 h-5;
}

/* User Dropdown */
.user-dropdown {
  @apply relative;
}

.user-button {
  @apply flex items-center space-x-3 p-2.5 rounded-lg;
  @apply text-neutral-700 hover:bg-neutral-100 transition-colors duration-200;
  @apply focus:outline-none focus:ring-2 focus:ring-primary-500;
}

.user-avatar {
  @apply flex-shrink-0;
}

.avatar-image {
  @apply w-8 h-8 rounded-full object-cover;
}

.avatar-placeholder {
  @apply w-8 h-8 rounded-full bg-neutral-200 flex items-center justify-center;
}

.avatar-icon {
  @apply w-5 h-5 text-neutral-500;
}

.user-info {
  @apply hidden sm:block text-left;
}

.user-name {
  @apply block text-sm font-medium text-neutral-800;
}

.user-role {
  @apply block text-xs text-neutral-500;
}

.dropdown-icon {
  @apply w-4 h-4 text-neutral-400 transition-transform duration-200;
}

.dropdown-icon-open {
  @apply transform rotate-180;
}

/* User Menu */
.user-menu {
  @apply absolute right-0 mt-2 w-48 bg-white rounded-lg border border-neutral-300;
  @apply py-2 z-50;
  box-shadow: 0 4px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.user-menu-item {
  @apply flex items-center space-x-3 px-4 py-2.5 text-sm text-neutral-700;
  @apply hover:bg-neutral-100 transition-colors duration-200;
  @apply focus:outline-none focus:bg-neutral-100;
  text-decoration: none;
}

.menu-item-icon {
  @apply w-4 h-4 text-neutral-500;
}

/* Mobile Menu Toggle */
.mobile-menu-toggle {
  @apply md:hidden p-2.5 rounded-lg text-neutral-600 hover:text-neutral-800 hover:bg-neutral-100;
  @apply transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500;
}

.hamburger {
  @apply w-6 h-6 flex flex-col justify-center space-y-1.5;
}

.hamburger-line {
  @apply w-full h-0.5 bg-current transition-all duration-300 ease-in-out;
  transform-origin: center;
}

.hamburger-open .hamburger-line:nth-child(1) {
  transform: rotate(45deg) translate(3px, 3px);
}

.hamburger-open .hamburger-line:nth-child(2) {
  @apply opacity-0 scale-0;
}

.hamburger-open .hamburger-line:nth-child(3) {
  transform: rotate(-45deg) translate(3px, -3px);
}

/* Mobile Navigation */
.mobile-nav {
  @apply md:hidden bg-white border-t border-neutral-300;
}

.mobile-nav-content {
  @apply px-4 py-4 space-y-2;
}

.mobile-nav-link {
  @apply flex items-center space-x-3 px-4 py-3 rounded-lg text-base font-medium;
  @apply text-neutral-700 hover:text-neutral-800 hover:bg-neutral-100;
  @apply transition-colors duration-200;
  text-decoration: none;
}

.mobile-nav-link-active {
  @apply text-primary-600 bg-primary-50;
}

.mobile-nav-icon {
  @apply w-5 h-5;
}

.mobile-nav-text {
  @apply flex-1;
}

/* Mobile Backdrop */
.mobile-backdrop {
  @apply fixed inset-0 bg-black bg-opacity-25 z-40 md:hidden;
}

/* Transitions - улучшенные анимации */
.dropdown-enter-active,
.dropdown-leave-active {
  @apply transition-all duration-200 ease-out;
}

.dropdown-enter-from,
.dropdown-leave-to {
  @apply opacity-0 transform scale-95 -translate-y-2;
}

.mobile-menu-enter-active,
.mobile-menu-leave-active {
  @apply transition-all duration-300 ease-out;
}

.mobile-menu-enter-from,
.mobile-menu-leave-to {
  @apply opacity-0 transform -translate-y-4;
}

/* Плавные анимации для элементов навигации */
.nav-link,
.mobile-nav-link {
  @apply transition-all duration-200 ease-in-out;
}

.nav-link:hover,
.mobile-nav-link:hover {
  @apply transform translate-x-1;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .brand-text {
    @apply text-base;
  }
  
  .header-container {
    @apply px-3;
  }
}

/* Focus styles for accessibility */
.nav-link:focus,
.mobile-nav-link:focus {
  @apply outline-none ring-2 ring-primary-500 ring-offset-2;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .app-header {
    @apply border-b-2;
  }
  
  .nav-link-active {
    @apply border-2 border-primary-600;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .nav-link,
  .user-button,
  .mobile-nav-link,
  .hamburger-line,
  .dropdown-icon {
    @apply transition-none;
  }
}
</style>