<template>
  <div id="app">
    <div class="app-container">
      <!-- Header -->
      <header class="app-header">
        <div class="header-content">
          <div class="brand">
            <h1>Система ИИ-Интервью</h1>
          </div>
          <nav class="nav">
            <router-link to="/" class="nav-link">Главная</router-link>
            <router-link to="/hr" class="nav-link">HR Панель</router-link>
            <router-link to="/vacancies" class="nav-link">Вакансии</router-link>
            <router-link to="/resumes" class="nav-link">Резюме</router-link>
            <router-link to="/scenarios" class="nav-link">Сценарии</router-link>
            <router-link to="/interview" class="nav-link">Интервью</router-link>
            <router-link to="/model-status" class="nav-link">Статус модели</router-link>
          </nav>
        </div>
      </header>

      <!-- Main Content -->
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
@import './styles/component-fixes.css';

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
  width: 100vw;
  background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
  color: #e2e8f0;
}

.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.app-header {
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
  color: white;
  padding: 0 2rem;
  box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
  z-index: 100;
  position: relative;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  max-width: 1200px;
  margin: 0 auto;
}

.brand h1 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

.nav {
  display: flex;
  gap: 1rem;
}

.nav-link {
  color: #cbd5e1;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.nav-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.nav-link:hover {
  background: rgba(0, 255, 255, 0.1);
  color: #00ffff;
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 255, 255, 0.3);
}

.nav-link:hover::before {
  left: 100%;
}

.nav-link.router-link-active {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(255, 0, 255, 0.2));
  color: #00ffff;
  font-weight: 600;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
}

.main-content {
  flex: 1;
  padding: 0;
  overflow-y: auto;
  background: transparent;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    height: auto;
    padding: 1rem 0;
  }
  
  .nav {
    margin-top: 1rem;
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .brand h1 {
    font-size: 1.25rem;
  }
  
  .main-content {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .app-header {
    padding: 0 1rem;
  }
  
  .nav {
    gap: 0.5rem;
  }
  
  .nav-link {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }
}

body {
  margin: 0;
  padding: 0;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

html {
  height: 100%;
  width: 100%;
}

/* Global Modal Styles for HR Panel */
.hr-panel-modal .bg-white,
.hr-panel-modal .dark\:bg-neutral-800 {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95)) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(0, 255, 255, 0.3) !important;
  color: #e2e8f0 !important;
}

.hr-panel-modal .text-neutral-900,
.hr-panel-modal .dark\:text-neutral-100 {
  color: #e2e8f0 !important;
}

.hr-panel-modal .border-neutral-200,
.hr-panel-modal .dark\:border-neutral-700 {
  border-color: rgba(0, 255, 255, 0.2) !important;
}

.hr-panel-modal .text-neutral-400,
.hr-panel-modal .dark\:text-neutral-500 {
  color: #94a3b8 !important;
}

.hr-panel-modal .hover\:text-neutral-600:hover,
.hr-panel-modal .dark\:hover\:text-neutral-300:hover {
  color: #00ffff !important;
}

.hr-panel-modal .hover\:bg-neutral-100:hover,
.hr-panel-modal .dark\:hover\:bg-neutral-700:hover {
  background: rgba(0, 255, 255, 0.1) !important;
}

.hr-panel-modal .fixed.inset-0 {
  background: rgba(0, 0, 0, 0.8) !important;
  backdrop-filter: blur(8px) !important;
}

/* Modal content styling */
.hr-panel-modal h2 {
  color: #00ffff !important;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5) !important;
}

.hr-panel-modal input,
.hr-panel-modal select,
.hr-panel-modal textarea {
  background: rgba(15, 23, 42, 0.9) !important;
  border: 1px solid rgba(0, 255, 255, 0.4) !important;
  color: #ffffff !important;
  border-radius: 8px !important;
}

.hr-panel-modal input:focus,
.hr-panel-modal select:focus,
.hr-panel-modal textarea:focus {
  border-color: rgba(0, 255, 255, 0.8) !important;
  box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.2) !important;
}

.hr-panel-modal input::placeholder,
.hr-panel-modal textarea::placeholder {
  color: #94a3b8 !important;
}

/* Global form styling for all pages */
input, select, textarea, button {
  font-family: inherit;
}

/* Global input styling */
input:not([type="checkbox"]):not([type="radio"]),
select,
textarea {
  background: rgba(15, 23, 42, 0.8) !important;
  border: 1px solid rgba(0, 255, 255, 0.3) !important;
  color: #e2e8f0 !important;
  border-radius: 8px !important;
  transition: all 0.3s ease !important;
  padding: 0.75rem 1rem !important;
  font-size: 0.875rem !important;
  line-height: 1.5 !important;
}

input:not([type="checkbox"]):not([type="radio"]):focus,
select:focus,
textarea:focus {
  outline: none !important;
  border-color: rgba(0, 255, 255, 0.6) !important;
  box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.1) !important;
  background: rgba(15, 23, 42, 0.9) !important;
}

input::placeholder,
textarea::placeholder {
  color: #94a3b8 !important;
}

/* Select dropdown styling */
select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2300ffff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6,9 12,15 18,9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1rem;
  padding-right: 3rem !important;
}

select option {
  background: #1e293b !important;
  color: #e2e8f0 !important;
  padding: 0.5rem;
}

/* Label styling */
label {
  color: #e2e8f0 !important;
  font-weight: 500;
  margin-bottom: 0.5rem;
  display: block;
}

/* Disabled states */
input:disabled,
select:disabled,
textarea:disabled {
  opacity: 0.5 !important;
  cursor: not-allowed !important;
  background: rgba(15, 23, 42, 0.4) !important;
}

/* Checkbox and radio styling */
input[type="checkbox"],
input[type="radio"] {
  accent-color: #00ffff !important;
  width: 1.25rem !important;
  height: 1.25rem !important;
}

/* Table styling */
table {
  background: rgba(15, 23, 42, 0.6) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(0, 255, 255, 0.2) !important;
  border-radius: 12px !important;
  overflow: hidden !important;
}

table th {
  background: rgba(0, 255, 255, 0.1) !important;
  color: #00ffff !important;
  font-weight: 600 !important;
  border-bottom: 1px solid rgba(0, 255, 255, 0.2) !important;
}

table td {
  color: #e2e8f0 !important;
  border-bottom: 1px solid rgba(0, 255, 255, 0.1) !important;
}

table tr:hover {
  background: rgba(0, 255, 255, 0.05) !important;
}

/* Card styling improvements */
.card, .el-card, [class*="card"] {
  background: rgba(15, 23, 42, 0.6) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(0, 255, 255, 0.2) !important;
  border-radius: 16px !important;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.4),
    0 0 40px rgba(0, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
  color: #e2e8f0 !important;
  transition: all 0.3s ease !important;
}

.card:hover, .el-card:hover, [class*="card"]:hover {
  border-color: rgba(0, 255, 255, 0.4) !important;
  box-shadow: 
    0 12px 40px rgba(0, 0, 0, 0.5),
    0 0 60px rgba(0, 255, 255, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
  transform: translateY(-2px) !important;
}

/* Element Plus overrides */
.el-card__header {
  background: rgba(0, 255, 255, 0.1) !important;
  border-bottom: 1px solid rgba(0, 255, 255, 0.2) !important;
  color: #00ffff !important;
}

.el-card__body {
  background: transparent !important;
  color: #e2e8f0 !important;
}

.el-input__inner,
.el-textarea__inner,
.el-select .el-input__inner {
  background: rgba(15, 23, 42, 0.8) !important;
  border-color: rgba(0, 255, 255, 0.3) !important;
  color: #e2e8f0 !important;
}

.el-input__inner:focus,
.el-textarea__inner:focus,
.el-select .el-input__inner:focus {
  border-color: rgba(0, 255, 255, 0.6) !important;
}

/* Стили для плейсхолдеров в селектах */
.el-select .el-input__inner::placeholder {
  color: rgba(226, 232, 240, 0.6) !important;
  opacity: 1 !important;
}

.el-select .el-input.is-focus .el-input__inner::placeholder {
  color: rgba(0, 255, 255, 0.4) !important;
}

/* Дополнительные стили для плейсхолдеров */
.el-select .el-input__inner::-webkit-input-placeholder {
  color: rgba(226, 232, 240, 0.6) !important;
}

.el-select .el-input__inner::-moz-placeholder {
  color: rgba(226, 232, 240, 0.6) !important;
  opacity: 1 !important;
}

.el-select .el-input__inner:-ms-input-placeholder {
  color: rgba(226, 232, 240, 0.6) !important;
}

.el-select .el-input__inner:-moz-placeholder {
  color: rgba(226, 232, 240, 0.6) !important;
  opacity: 1 !important;
}

/* Стили для селекта без выбранного значения */
.el-select:not(.el-select--disabled) .el-input__inner[placeholder] {
  color: rgba(226, 232, 240, 0.6) !important;
}

/* Стили для выпадающего списка селектов */
.el-select-dropdown {
  background: rgba(15, 23, 42, 0.95) !important;
  border: 1px solid rgba(0, 255, 255, 0.3) !important;
  backdrop-filter: blur(10px) !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
  z-index: 9999 !important;
}

.el-select-dropdown .el-select-dropdown__item {
  color: #e2e8f0 !important;
  background: transparent !important;
  transition: all 0.2s ease !important;
}

.el-select-dropdown .el-select-dropdown__item:hover {
  background: rgba(0, 255, 255, 0.1) !important;
  color: #00ffff !important;
}

.el-select-dropdown .el-select-dropdown__item.selected {
  background: rgba(0, 255, 255, 0.2) !important;
  color: #00ffff !important;
  font-weight: 600 !important;
}

/* Стили для пустого селекта */
.el-select .el-input.is-disabled .el-input__inner {
  background: rgba(15, 23, 42, 0.4) !important;
  color: rgba(226, 232, 240, 0.5) !important;
}

/* Стили для иконки селекта */
.el-select .el-input__suffix .el-input__suffix-inner .el-select__caret {
  color: rgba(0, 255, 255, 0.6) !important;
}

.el-select .el-input.is-focus .el-input__suffix .el-input__suffix-inner .el-select__caret {
  color: #00ffff !important;
}

/* Стили для BaseSelect плейсхолдеров */
select option:disabled {
  color: rgba(148, 163, 184, 0.8) !important;
  font-style: italic !important;
}

select option:first-child:disabled {
  display: block !important;
  color: rgba(148, 163, 184, 0.8) !important;
}

/* Улучшенные стили для нативных селектов */
select {
  color: #e2e8f0 !important;
}

select:invalid {
  color: rgba(148, 163, 184, 0.8) !important;
}

/* Стили для выбранного плейсхолдера в нативном селекте */
select option[value=""][disabled] {
  color: rgba(148, 163, 184, 0.8) !important;
  background: rgba(15, 23, 42, 0.9) !important;
}

/* Дополнительные стили для улучшения видимости плейсхолдеров */
.el-select .el-input__inner {
  transition: all 0.3s ease !important;
}

.el-select .el-input__inner:not(:focus):not(.is-focus) {
  color: rgba(226, 232, 240, 0.9) !important;
}

/* Стили для пустого состояния селекта */
.el-select .el-input__inner[placeholder]:placeholder-shown {
  color: rgba(148, 163, 184, 0.7) !important;
}

/* Стили для Element Plus селектов в темной теме */
.el-select .el-input__inner::-webkit-input-placeholder {
  color: rgba(148, 163, 184, 0.7) !important;
  opacity: 1 !important;
}

.el-select .el-input__inner::-moz-placeholder {
  color: rgba(148, 163, 184, 0.7) !important;
  opacity: 1 !important;
}

.el-select .el-input__inner:-ms-input-placeholder {
  color: rgba(148, 163, 184, 0.7) !important;
}

.el-select .el-input__inner::placeholder {
  color: rgba(148, 163, 184, 0.7) !important;
  opacity: 1 !important;
}

.el-button {
  border-radius: 8px !important;
  font-weight: 500 !important;
  transition: all 0.3s ease !important;
}

.el-button--primary {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.8), rgba(138, 43, 226, 0.8)) !important;
  border-color: rgba(0, 255, 255, 0.6) !important;
  color: #ffffff !important;
}

.el-button--primary:hover {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.9), rgba(138, 43, 226, 0.9)) !important;
  border-color: rgba(0, 255, 255, 0.8) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 25px rgba(0, 255, 255, 0.3) !important;
}

/* Page Transition Animations */
.page-enter-active,
.page-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.98);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(1.02);
}

.page-enter-to,
.page-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}

/* Smooth scrolling for all pages */
* {
  scroll-behavior: smooth;
}

/* Enhanced glassmorphism effects for all pages */
.glassmorphism {
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 16px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.4),
    0 0 40px rgba(0, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.glassmorphism:hover {
  border-color: rgba(0, 255, 255, 0.4);
  box-shadow: 
    0 12px 40px rgba(0, 0, 0, 0.5),
    0 0 60px rgba(0, 255, 255, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}

/* Fix for specific page issues */
.resume-upload, .vacancies-list, .hr-panel, .model-status, .candidate-interview {
  min-height: 100vh !important;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #0f172a 50%, #1e293b 75%, #0f172a 100%) !important;
  color: #e2e8f0 !important;
}

/* Fix for white backgrounds */
.bg-white, .bg-gray-50, .bg-neutral-50 {
  background: rgba(15, 23, 42, 0.6) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(0, 255, 255, 0.2) !important;
  color: #e2e8f0 !important;
}

/* Fix for text colors */
.text-gray-900, .text-neutral-900, .text-black {
  color: #e2e8f0 !important;
}

.text-gray-600, .text-neutral-600 {
  color: #94a3b8 !important;
}

.text-gray-500, .text-neutral-500 {
  color: #64748b !important;
}

.text-gray-400, .text-neutral-400 {
  color: #475569 !important;
}

/* Fix for borders */
.border-gray-200, .border-neutral-200 {
  border-color: rgba(0, 255, 255, 0.2) !important;
}

.border-gray-300, .border-neutral-300 {
  border-color: rgba(0, 255, 255, 0.3) !important;
}

/* Fix for buttons */
.btn, button:not(.el-button) {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.8), rgba(138, 43, 226, 0.8)) !important;
  border: 1px solid rgba(0, 255, 255, 0.6) !important;
  color: #ffffff !important;
  border-radius: 8px !important;
  padding: 0.5rem 1rem !important;
  font-weight: 500 !important;
  transition: all 0.3s ease !important;
  cursor: pointer !important;
}

.btn:hover, button:not(.el-button):hover {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.9), rgba(138, 43, 226, 0.9)) !important;
  border-color: rgba(0, 255, 255, 0.8) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 25px rgba(0, 255, 255, 0.3) !important;
}

/* Fix for specific component issues */
.page-header, .panel-header, .status-header, .interview-header {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.6)) !important;
  backdrop-filter: blur(30px) !important;
  border: 1px solid rgba(0, 255, 255, 0.3) !important;
  border-radius: 20px !important;
  padding: 2rem !important;
  margin: 1rem !important;
  z-index: 10 !important;
  position: relative !important;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.4),
    0 0 40px rgba(0, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
}

/* Fix for statistics cards */
.stat-card, .stats-grid > *, .statistics > * {
  background: rgba(15, 23, 42, 0.6) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(0, 255, 255, 0.2) !important;
  border-radius: 16px !important;
  padding: 1.5rem !important;
  color: #e2e8f0 !important;
}

/* Fix for filters and forms */
.filters-card, .filter-group, .form-group {
  background: rgba(15, 23, 42, 0.6) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(0, 255, 255, 0.2) !important;
  border-radius: 12px !important;
  padding: 1rem !important;
  margin-bottom: 1rem !important;
}

/* Fix for tables */
.table-container, .data-table, .vacancies-table {
  background: rgba(15, 23, 42, 0.6) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(0, 255, 255, 0.2) !important;
  border-radius: 12px !important;
  overflow: hidden !important;
}

/* Fix for empty states */
.empty-state, .loading-container {
  background: rgba(15, 23, 42, 0.4) !important;
  backdrop-filter: blur(10px) !important;
  border: 1px solid rgba(0, 255, 255, 0.1) !important;
  border-radius: 12px !important;
  padding: 3rem !important;
  text-align: center !important;
  color: #94a3b8 !important;
}

/* Fix for progress bars */
.progress-bar, .score-bar {
  background: rgba(15, 23, 42, 0.8) !important;
  border: none !important;
  border-radius: 0 !important;
  overflow: hidden !important;
  height: 4px !important;
}

.progress-fill, .score-fill {
  background: linear-gradient(90deg, #00ffff, #8a2be2) !important;
  border: none !important;
  border-radius: 0 !important;
  transition: width 0.3s ease !important;
}

/* Fix for badges and status indicators */
.status-badge, .badge {
  padding: 0.25rem 0.75rem !important;
  border-radius: 12px !important;
  font-size: 0.75rem !important;
  font-weight: 500 !important;
  border: 1px solid !important;
}

.status-active, .badge-success {
  background: rgba(34, 197, 94, 0.2) !important;
  border-color: rgba(34, 197, 94, 0.5) !important;
  color: #22c55e !important;
}

.status-closed, .badge-danger {
  background: rgba(239, 68, 68, 0.2) !important;
  border-color: rgba(239, 68, 68, 0.5) !important;
  color: #ef4444 !important;
}

.status-draft, .badge-warning {
  background: rgba(245, 158, 11, 0.2) !important;
  border-color: rgba(245, 158, 11, 0.5) !important;
  color: #f59e0b !important;
}

.status-paused, .badge-info {
  background: rgba(59, 130, 246, 0.2) !important;
  border-color: rgba(59, 130, 246, 0.5) !important;
  color: #3b82f6 !important;
}

/* Neon glow effects */
.neon-glow {
  text-shadow: 
    0 0 5px currentColor,
    0 0 10px currentColor,
    0 0 15px currentColor,
    0 0 20px currentColor;
}

.neon-border {
  border: 1px solid;
  box-shadow: 
    0 0 5px currentColor,
    0 0 10px currentColor,
    0 0 15px currentColor,
    inset 0 0 5px currentColor;
}

/* Animated background patterns */
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

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
}

/* Loading animations */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}
</style>
