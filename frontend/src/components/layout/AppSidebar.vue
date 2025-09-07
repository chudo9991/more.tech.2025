<template>
  <aside 
    class="app-sidebar"
    :class="{ 
      'sidebar-collapsed': collapsed,
      'sidebar-mobile-open': mobileOpen 
    }"
    :aria-expanded="!collapsed"
  >
    <!-- Sidebar Header -->
    <div class="sidebar-header">
      <div class="sidebar-brand" v-if="!collapsed">
        <router-link to="/" class="brand-link">
          <div class="brand-logo">
            <svg class="logo-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
          </div>
          <span class="brand-text">ИИ-Интервью</span>
        </router-link>
      </div>
      
      <!-- Collapse Toggle -->
      <button
        @click="toggleCollapse"
        class="collapse-toggle"
        :aria-label="collapsed ? 'Развернуть боковую панель' : 'Свернуть боковую панель'"
      >
        <ChevronLeftIcon 
          class="collapse-icon" 
          :class="{ 'collapse-icon-rotated': collapsed }" 
        />
      </button>
    </div>

    <!-- Navigation -->
    <nav class="sidebar-nav" role="navigation">
      <div class="nav-section">
        <h3 v-if="!collapsed" class="nav-section-title">Основное</h3>
        
        <template v-for="item in navigationItems" :key="item.id">
          <!-- Simple Navigation Item -->
          <router-link
            v-if="!item.children"
            :to="item.route"
            class="nav-item"
            :class="{ 
              'nav-item-active': isActiveRoute(item.route),
              'nav-item-collapsed': collapsed 
            }"
            @click="handleNavClick"
          >
            <div class="nav-item-content">
              <component :is="item.icon" class="nav-icon" />
              <span v-if="!collapsed" class="nav-text">{{ item.label }}</span>
              <span v-if="item.badge && !collapsed" class="nav-badge">{{ item.badge }}</span>
            </div>
            
            <!-- Tooltip for collapsed state -->
            <div v-if="collapsed" class="nav-tooltip">
              {{ item.label }}
              <span v-if="item.badge" class="tooltip-badge">{{ item.badge }}</span>
            </div>
          </router-link>

          <!-- Navigation Item with Children -->
          <div v-else class="nav-group">
            <button
              @click="toggleGroup(item.id)"
              class="nav-group-toggle"
              :class="{ 
                'nav-group-active': isGroupActive(item),
                'nav-item-collapsed': collapsed 
              }"
              :aria-expanded="expandedGroups.includes(item.id)"
            >
              <div class="nav-item-content">
                <component :is="item.icon" class="nav-icon" />
                <span v-if="!collapsed" class="nav-text">{{ item.label }}</span>
                <span v-if="item.badge && !collapsed" class="nav-badge">{{ item.badge }}</span>
                <ChevronDownIcon 
                  v-if="!collapsed"
                  class="group-chevron"
                  :class="{ 'group-chevron-expanded': expandedGroups.includes(item.id) }"
                />
              </div>
              
              <!-- Tooltip for collapsed state -->
              <div v-if="collapsed" class="nav-tooltip">
                {{ item.label }}
                <span v-if="item.badge" class="tooltip-badge">{{ item.badge }}</span>
              </div>
            </button>

            <!-- Submenu -->
            <transition name="submenu">
              <div 
                v-if="expandedGroups.includes(item.id) && !collapsed"
                class="nav-submenu"
              >
                <router-link
                  v-for="child in item.children"
                  :key="child.id"
                  :to="child.route"
                  class="nav-subitem"
                  :class="{ 'nav-subitem-active': isActiveRoute(child.route) }"
                  @click="handleNavClick"
                >
                  <component :is="child.icon" class="nav-subicon" />
                  <span class="nav-subtext">{{ child.label }}</span>
                  <span v-if="child.badge" class="nav-badge nav-subbadge">{{ child.badge }}</span>
                </router-link>
              </div>
            </transition>
          </div>
        </template>
      </div>

      <!-- Secondary Section -->
      <div class="nav-section nav-section-secondary">
        <h3 v-if="!collapsed" class="nav-section-title">Система</h3>
        
        <router-link
          v-for="item in secondaryItems"
          :key="item.id"
          :to="item.route"
          class="nav-item"
          :class="{ 
            'nav-item-active': isActiveRoute(item.route),
            'nav-item-collapsed': collapsed 
          }"
          @click="handleNavClick"
        >
          <div class="nav-item-content">
            <component :is="item.icon" class="nav-icon" />
            <span v-if="!collapsed" class="nav-text">{{ item.label }}</span>
            <span v-if="item.badge && !collapsed" class="nav-badge">{{ item.badge }}</span>
          </div>
          
          <!-- Tooltip for collapsed state -->
          <div v-if="collapsed" class="nav-tooltip">
            {{ item.label }}
            <span v-if="item.badge" class="tooltip-badge">{{ item.badge }}</span>
          </div>
        </router-link>
      </div>
    </nav>

    <!-- Sidebar Footer -->
    <div class="sidebar-footer" v-if="!collapsed">
      <div class="footer-content">
        <div class="footer-info">
          <span class="footer-version">v1.0.0</span>
          <span class="footer-status">
            <div class="status-indicator status-online"></div>
            Онлайн
          </span>
        </div>
      </div>
    </div>

    <!-- Mobile Backdrop -->
    <div
      v-if="mobileOpen"
      class="mobile-backdrop"
      @click="closeMobile"
      aria-hidden="true"
    ></div>
  </aside>
</template>

<script setup lang="ts">
// @ts-nocheck
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import {
  ChevronLeftIcon,
  ChevronDownIcon,
  HomeIcon,
  BriefcaseIcon,
  DocumentIcon,
  UsersIcon,
  ChatBubbleLeftRightIcon,
  CpuChipIcon,
  CogIcon,
  ChartBarIcon,
  FolderIcon,
  ClipboardDocumentListIcon
} from '@heroicons/vue/24/outline'

interface NavigationItem {
  id: string
  label: string
  route: string
  icon: any
  badge?: string | number
  children?: NavigationItem[]
}

interface Props {
  collapsed?: boolean
  mobileOpen?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  collapsed: false,
  mobileOpen: false
})

const emit = defineEmits<{
  'update:collapsed': [value: boolean]
  'update:mobileOpen': [value: boolean]
  'navigate': [route: string]
}>()

// Reactive state
const route = useRoute()
const expandedGroups = ref<string[]>(['hr-tools'])

// Navigation items
const navigationItems: NavigationItem[] = [
  { 
    id: 'home', 
    label: 'Главная', 
    route: '/', 
    icon: HomeIcon 
  },
  {
    id: 'hr-tools',
    label: 'HR Инструменты',
    route: '/hr',
    icon: BriefcaseIcon,
    children: [
      { id: 'hr-panel', label: 'HR Панель', route: '/hr', icon: ChartBarIcon },
      { id: 'vacancies', label: 'Вакансии', route: '/vacancies', icon: DocumentIcon },
      { id: 'resumes', label: 'Резюме', route: '/resumes', icon: UsersIcon }
    ]
  },
  {
    id: 'interview-tools',
    label: 'Интервью',
    route: '/interview',
    icon: ChatBubbleLeftRightIcon,
    children: [
      { id: 'interview', label: 'Проведение', route: '/interview', icon: ChatBubbleLeftRightIcon },
      { id: 'scenarios', label: 'Сценарии', route: '/scenarios', icon: ClipboardDocumentListIcon }
    ]
  }
]

const secondaryItems: NavigationItem[] = [
  { 
    id: 'model-status', 
    label: 'Статус модели', 
    route: '/model-status', 
    icon: CpuChipIcon,
    badge: 'OK'
  },
  { 
    id: 'settings', 
    label: 'Настройки', 
    route: '/settings', 
    icon: CogIcon 
  }
]

// Computed
const collapsed = computed({
  get: () => props.collapsed,
  set: (value) => emit('update:collapsed', value)
})

const mobileOpen = computed({
  get: () => props.mobileOpen,
  set: (value) => emit('update:mobileOpen', value)
})

// Methods
const isActiveRoute = (routePath: string): boolean => {
  if (!route?.path) return false
  return route.path === routePath || route.path.startsWith(routePath + '/')
}

const isGroupActive = (group: NavigationItem): boolean => {
  if (!group.children) return false
  return group.children.some(child => isActiveRoute(child.route))
}

const toggleCollapse = () => {
  collapsed.value = !collapsed.value
}

const toggleGroup = (groupId: string) => {
  if (collapsed.value) {
    // If sidebar is collapsed, expand it first
    collapsed.value = false
  }
  
  const index = expandedGroups.value.indexOf(groupId)
  if (index > -1) {
    expandedGroups.value.splice(index, 1)
  } else {
    expandedGroups.value.push(groupId)
  }
}

const handleNavClick = () => {
  // Close mobile sidebar on navigation
  if (mobileOpen.value) {
    closeMobile()
  }
}

const closeMobile = () => {
  mobileOpen.value = false
}

// Handle window resize
const handleResize = () => {
  if (window.innerWidth >= 1024) {
    mobileOpen.value = false
  }
}

// Auto-expand groups based on current route
const autoExpandGroups = () => {
  navigationItems.forEach(item => {
    if (item.children && isGroupActive(item)) {
      if (!expandedGroups.value.includes(item.id)) {
        expandedGroups.value.push(item.id)
      }
    }
  })
}

// Lifecycle
onMounted(() => {
  autoExpandGroups()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.app-sidebar {
  @apply fixed left-0 top-0 h-full bg-white border-r border-neutral-300 z-40;
  @apply transition-all duration-300 ease-in-out;
  width: 320px;
  transform: translateX(-100%);
  box-shadow: 2px 0 15px -3px rgba(0, 0, 0, 0.07), 10px 0 20px -2px rgba(0, 0, 0, 0.04);
}

.app-sidebar:not(.sidebar-collapsed) {
  transform: translateX(0);
}

.sidebar-collapsed {
  width: 80px;
  transform: translateX(0);
}

.sidebar-mobile-open {
  transform: translateX(0);
}

/* Sidebar Header */
.sidebar-header {
  @apply flex items-center justify-between px-6 py-4 border-b border-neutral-300;
  height: 64px;
}

.sidebar-brand {
  @apply flex-1;
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
  @apply text-lg font-semibold;
}

.collapse-toggle {
  @apply p-2 rounded-lg text-neutral-500 hover:text-neutral-700 hover:bg-neutral-100;
  @apply transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500;
}

.collapse-icon {
  @apply w-5 h-5 transition-transform duration-300;
}

.collapse-icon-rotated {
  @apply transform rotate-180;
}

/* Navigation */
.sidebar-nav {
  @apply flex-1 overflow-y-hidden py-8;
  scrollbar-width: none;
}

.sidebar-nav::-webkit-scrollbar {
  width: 6px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}

.nav-section {
  @apply px-8 mb-10;
}

.nav-section-secondary {
  @apply border-t border-neutral-300 pt-6 mt-auto;
}

.nav-section-title {
  @apply text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-4 px-2;
}

/* Navigation Items */
.nav-item,
.nav-group-toggle {
  @apply relative flex items-center w-full px-4 py-4 mb-3 rounded-lg;
  @apply text-neutral-700 hover:text-neutral-800 hover:bg-neutral-100;
  @apply transition-all duration-200 ease-in-out;
  @apply focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2;
  text-decoration: none;
}

.nav-item-active,
.nav-group-active {
  @apply text-primary-700 bg-primary-50 border border-primary-200;
}

.nav-item-collapsed {
  @apply justify-center px-2;
}

.nav-item-content {
  @apply flex items-center flex-1 min-w-0;
}

.nav-icon {
  @apply w-5 h-5 flex-shrink-0;
}

.nav-text {
  @apply ml-3 text-sm font-medium truncate;
}

.nav-badge {
  @apply ml-auto px-2 py-0.5 text-xs font-medium bg-neutral-100 text-neutral-600 rounded-full;
}

.nav-item-active .nav-badge {
  @apply bg-primary-100 text-primary-700;
}

/* Group Navigation */
.nav-group {
  @apply mb-1;
}

.group-chevron {
  @apply w-4 h-4 ml-auto transition-transform duration-200;
}

.group-chevron-expanded {
  @apply transform rotate-180;
}

/* Submenu */
.nav-submenu {
  @apply ml-8 mt-2 space-y-1;
}

.nav-subitem {
  @apply flex items-center px-3 py-2.5 rounded-lg text-sm;
  @apply text-neutral-600 hover:text-neutral-800 hover:bg-neutral-100;
  @apply transition-colors duration-200;
  @apply focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2;
  text-decoration: none;
}

.nav-subitem-active {
  @apply text-primary-700 bg-primary-50;
}

.nav-subicon {
  @apply w-4 h-4 flex-shrink-0;
}

.nav-subtext {
  @apply ml-3 font-medium;
}

.nav-subbadge {
  @apply text-xs px-1.5 py-0.5;
}

/* Tooltips */
.nav-tooltip {
  @apply absolute left-full ml-2 px-3 py-2 bg-neutral-900 text-white text-sm rounded-lg;
  @apply opacity-0 invisible transition-all duration-200 pointer-events-none z-50;
  @apply whitespace-nowrap;
}

.nav-item:hover .nav-tooltip,
.nav-group-toggle:hover .nav-tooltip {
  @apply opacity-100 visible;
}

.tooltip-badge {
  @apply ml-2 px-1.5 py-0.5 text-xs bg-neutral-700 rounded-full;
}

/* Sidebar Footer */
.sidebar-footer {
  @apply border-t border-neutral-300 p-6;
}

.footer-content {
  @apply space-y-2;
}

.footer-info {
  @apply flex items-center justify-between text-xs text-neutral-500;
}

.footer-version {
  @apply font-medium;
}

.footer-status {
  @apply flex items-center space-x-1;
}

.status-indicator {
  @apply w-2 h-2 rounded-full;
}

.status-online {
  @apply bg-green-500;
}

/* Mobile Backdrop */
.mobile-backdrop {
  @apply fixed inset-0 bg-black bg-opacity-25 z-30 lg:hidden;
}

/* Transitions - улучшенные анимации */
.submenu-enter-active,
.submenu-leave-active {
  @apply transition-all duration-300 ease-out;
}

.submenu-enter-from,
.submenu-leave-to {
  @apply opacity-0 transform -translate-y-2;
  max-height: 0;
}

.submenu-enter-to,
.submenu-leave-from {
  max-height: 200px;
}

/* Плавные анимации для элементов навигации */
.nav-item:hover,
.nav-group-toggle:hover {
  @apply transform translate-x-1;
}

.nav-subitem:hover {
  @apply transform translate-x-2;
}

/* Responsive Design */
@media (min-width: 1024px) {
  .app-sidebar {
    @apply relative transform-none;
    position: sticky;
    top: 0;
    height: 100vh;
  }
  
  .mobile-backdrop {
    @apply hidden;
  }
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  .app-sidebar,
  .collapse-icon,
  .group-chevron,
  .nav-item,
  .nav-group-toggle,
  .nav-subitem {
    @apply transition-none;
  }
}

/* High contrast mode */
@media (prefers-contrast: high) {
  .nav-item-active,
  .nav-group-active {
    @apply border-2 border-primary-600;
  }
}

/* Focus management */
.nav-item:focus-visible,
.nav-group-toggle:focus-visible,
.nav-subitem:focus-visible {
  @apply ring-2 ring-primary-500 ring-offset-2;
}
</style>