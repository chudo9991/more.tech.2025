<template>
  <footer class="app-footer">
    <div class="footer-container">
      <!-- Main Footer Content -->
      <div class="footer-content">
        <!-- Company Information -->
        <div class="footer-section">
          <div class="footer-brand">
            <div class="brand-logo">
              <svg class="logo-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
            </div>
            <div class="brand-info">
              <h3 class="brand-title">{{ companyInfo.name }}</h3>
              <p class="brand-description">{{ companyInfo.description }}</p>
            </div>
          </div>
          
          <!-- Contact Information -->
          <div class="contact-info">
            <div v-if="companyInfo.email" class="contact-item">
              <EnvelopeIcon class="contact-icon" />
              <a :href="`mailto:${companyInfo.email}`" class="contact-link">
                {{ companyInfo.email }}
              </a>
            </div>
            <div v-if="companyInfo.phone" class="contact-item">
              <PhoneIcon class="contact-icon" />
              <a :href="`tel:${companyInfo.phone}`" class="contact-link">
                {{ companyInfo.phone }}
              </a>
            </div>
            <div v-if="companyInfo.address" class="contact-item">
              <MapPinIcon class="contact-icon" />
              <span class="contact-text">{{ companyInfo.address }}</span>
            </div>
          </div>
        </div>

        <!-- Navigation Links -->
        <div class="footer-section">
          <h4 class="section-title">Навигация</h4>
          <nav class="footer-nav">
            <router-link
              v-for="link in navigationLinks"
              :key="link.id"
              :to="link.route"
              class="footer-nav-link"
            >
              {{ link.label }}
            </router-link>
          </nav>
        </div>

        <!-- Resources -->
        <div class="footer-section">
          <h4 class="section-title">Ресурсы</h4>
          <nav class="footer-nav">
            <a
              v-for="link in resourceLinks"
              :key="link.id"
              :href="link.href"
              class="footer-nav-link"
              :target="link.external ? '_blank' : '_self'"
              :rel="link.external ? 'noopener noreferrer' : undefined"
            >
              {{ link.label }}
              <ArrowTopRightOnSquareIcon 
                v-if="link.external" 
                class="external-icon" 
              />
            </a>
          </nav>
        </div>

        <!-- Support -->
        <div class="footer-section">
          <h4 class="section-title">Поддержка</h4>
          <nav class="footer-nav">
            <a
              v-for="link in supportLinks"
              :key="link.id"
              :href="link.href"
              class="footer-nav-link"
              :target="link.external ? '_blank' : '_self'"
              :rel="link.external ? 'noopener noreferrer' : undefined"
            >
              {{ link.label }}
              <ArrowTopRightOnSquareIcon 
                v-if="link.external" 
                class="external-icon" 
              />
            </a>
          </nav>
        </div>
      </div>

      <!-- Social Media Links -->
      <div v-if="showSocialLinks && socialLinks.length > 0" class="social-section">
        <h4 class="section-title">Мы в социальных сетях</h4>
        <div class="social-links">
          <a
            v-for="social in socialLinks"
            :key="social.id"
            :href="social.href"
            class="social-link"
            :aria-label="`Перейти в ${social.label}`"
            target="_blank"
            rel="noopener noreferrer"
          >
            <component :is="social.icon" class="social-icon" />
            <span class="social-label">{{ social.label }}</span>
          </a>
        </div>
      </div>

      <!-- Footer Bottom -->
      <div class="footer-bottom">
        <div class="footer-bottom-content">
          <!-- Copyright -->
          <div class="copyright">
            <p class="copyright-text">
              © {{ currentYear }} {{ companyInfo.name }}. Все права защищены.
            </p>
          </div>

          <!-- Legal Links -->
          <div class="legal-links">
            <a
              v-for="link in legalLinks"
              :key="link.id"
              :href="link.href"
              class="legal-link"
            >
              {{ link.label }}
            </a>
          </div>

          <!-- System Status -->
          <div class="system-status">
            <div class="status-indicator" :class="statusClass">
              <div class="status-dot"></div>
              <span class="status-text">{{ statusText }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
// @ts-nocheck
import { computed } from 'vue'
import {
  EnvelopeIcon,
  PhoneIcon,
  MapPinIcon,
  ArrowTopRightOnSquareIcon
} from '@heroicons/vue/24/outline'

// Social media icons (simplified for demo)
const TelegramIcon = {
  template: `
    <svg viewBox="0 0 24 24" fill="currentColor">
      <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/>
    </svg>
  `
}

const LinkedInIcon = {
  template: `
    <svg viewBox="0 0 24 24" fill="currentColor">
      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
    </svg>
  `
}

const GitHubIcon = {
  template: `
    <svg viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
    </svg>
  `
}

interface CompanyInfo {
  name: string
  description: string
  email?: string
  phone?: string
  address?: string
}

interface FooterLink {
  id: string
  label: string
  href?: string
  route?: string
  external?: boolean
}

interface SocialLink {
  id: string
  label: string
  href: string
  icon: any
}

interface Props {
  companyInfo?: CompanyInfo
  showSocialLinks?: boolean
  systemStatus?: 'online' | 'maintenance' | 'offline'
}

const props = withDefaults(defineProps<Props>(), {
  companyInfo: () => ({
    name: 'Система ИИ-Интервью',
    description: 'Современная платформа для проведения автоматизированных интервью с использованием искусственного интеллекта.',
    email: 'support@ai-interview.ru',
    phone: '+7 (495) 123-45-67',
    address: 'Москва, Россия'
  }),
  showSocialLinks: true,
  systemStatus: 'online'
})

// Current year for copyright
const currentYear = computed(() => new Date().getFullYear())

// Navigation links
const navigationLinks: FooterLink[] = [
  { id: 'home', label: 'Главная', route: '/' },
  { id: 'hr', label: 'HR Панель', route: '/hr' },
  { id: 'vacancies', label: 'Вакансии', route: '/vacancies' },
  { id: 'resumes', label: 'Резюме', route: '/resumes' },
  { id: 'interview', label: 'Интервью', route: '/interview' }
]

// Resource links
const resourceLinks: FooterLink[] = [
  { id: 'docs', label: 'Документация', href: '/docs' },
  { id: 'api', label: 'API', href: '/api-docs' },
  { id: 'blog', label: 'Блог', href: '/blog' },
  { id: 'changelog', label: 'История изменений', href: '/changelog' }
]

// Support links
const supportLinks: FooterLink[] = [
  { id: 'help', label: 'Справка', href: '/help' },
  { id: 'contact', label: 'Связаться с нами', href: '/contact' },
  { id: 'feedback', label: 'Обратная связь', href: '/feedback' },
  { id: 'status', label: 'Статус системы', href: 'https://status.ai-interview.ru', external: true }
]

// Social media links
const socialLinks: SocialLink[] = [
  { id: 'telegram', label: 'Telegram', href: 'https://t.me/ai_interview', icon: TelegramIcon },
  { id: 'linkedin', label: 'LinkedIn', href: 'https://linkedin.com/company/ai-interview', icon: LinkedInIcon },
  { id: 'github', label: 'GitHub', href: 'https://github.com/ai-interview', icon: GitHubIcon }
]

// Legal links
const legalLinks: FooterLink[] = [
  { id: 'privacy', label: 'Политика конфиденциальности', href: '/privacy' },
  { id: 'terms', label: 'Условия использования', href: '/terms' },
  { id: 'cookies', label: 'Использование cookies', href: '/cookies' }
]

// System status
const statusClass = computed(() => {
  const statusClasses = {
    online: 'status-online',
    maintenance: 'status-maintenance',
    offline: 'status-offline'
  }
  return statusClasses[props.systemStatus]
})

const statusText = computed(() => {
  const statusTexts = {
    online: 'Система работает',
    maintenance: 'Техническое обслуживание',
    offline: 'Система недоступна'
  }
  return statusTexts[props.systemStatus]
})
</script>

<style scoped>
.app-footer {
  @apply bg-neutral-50 border-t border-neutral-200 mt-auto;
}

.footer-container {
  @apply max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12;
}

/* Main Footer Content */
.footer-content {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-8;
}

.footer-section {
  @apply space-y-4;
}

/* Company Information */
.footer-brand {
  @apply flex items-start space-x-3 mb-4;
}

.brand-logo {
  @apply flex-shrink-0;
}

.logo-icon {
  @apply w-8 h-8 text-primary-600;
}

.brand-info {
  @apply flex-1;
}

.brand-title {
  @apply text-lg font-semibold text-neutral-900 mb-2;
}

.brand-description {
  @apply text-sm text-neutral-600 leading-relaxed;
}

/* Contact Information */
.contact-info {
  @apply space-y-3;
}

.contact-item {
  @apply flex items-center space-x-3;
}

.contact-icon {
  @apply w-4 h-4 text-neutral-500 flex-shrink-0;
}

.contact-link {
  @apply text-sm text-neutral-600 hover:text-primary-600 transition-colors;
  text-decoration: none;
}

.contact-text {
  @apply text-sm text-neutral-600;
}

/* Section Titles */
.section-title {
  @apply text-sm font-semibold text-neutral-900 uppercase tracking-wider mb-4;
}

/* Footer Navigation */
.footer-nav {
  @apply space-y-3;
}

.footer-nav-link {
  @apply flex items-center text-sm text-neutral-600 hover:text-primary-600 transition-colors;
  text-decoration: none;
}

.external-icon {
  @apply w-3 h-3 ml-1 opacity-60;
}

/* Social Media */
.social-section {
  @apply border-t border-neutral-200 pt-8 mb-8;
}

.social-links {
  @apply flex flex-wrap gap-4;
}

.social-link {
  @apply flex items-center space-x-2 px-3 py-2 rounded-lg;
  @apply text-neutral-600 hover:text-primary-600 hover:bg-primary-50;
  @apply transition-all duration-200;
  text-decoration: none;
}

.social-icon {
  @apply w-5 h-5;
}

.social-label {
  @apply text-sm font-medium;
}

/* Footer Bottom */
.footer-bottom {
  @apply border-t border-neutral-200 pt-8;
}

.footer-bottom-content {
  @apply flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0;
}

/* Copyright */
.copyright-text {
  @apply text-sm text-neutral-500;
}

/* Legal Links */
.legal-links {
  @apply flex flex-wrap gap-6;
}

.legal-link {
  @apply text-sm text-neutral-500 hover:text-neutral-700 transition-colors;
  text-decoration: none;
}

/* System Status */
.system-status {
  @apply flex items-center;
}

.status-indicator {
  @apply flex items-center space-x-2;
}

.status-dot {
  @apply w-2 h-2 rounded-full;
}

.status-text {
  @apply text-sm font-medium;
}

.status-online .status-dot {
  @apply bg-green-500;
}

.status-online .status-text {
  @apply text-green-700;
}

.status-maintenance .status-dot {
  @apply bg-yellow-500;
}

.status-maintenance .status-text {
  @apply text-yellow-700;
}

.status-offline .status-dot {
  @apply bg-red-500;
}

.status-offline .status-text {
  @apply text-red-700;
}

/* Responsive Design */
@media (max-width: 640px) {
  .footer-content {
    @apply grid-cols-1 gap-6;
  }
  
  .footer-brand {
    @apply flex-col items-start space-x-0 space-y-3;
  }
  
  .social-links {
    @apply grid grid-cols-2 gap-2;
  }
  
  .footer-bottom-content {
    @apply text-center;
  }
  
  .legal-links {
    @apply justify-center;
  }
}

@media (max-width: 768px) {
  .footer-content {
    @apply grid-cols-2;
  }
}

/* Accessibility */
.footer-nav-link:focus,
.social-link:focus,
.legal-link:focus,
.contact-link:focus {
  @apply outline-none ring-2 ring-primary-500 ring-offset-2 rounded;
}

/* High contrast mode */
@media (prefers-contrast: high) {
  .app-footer {
    @apply border-t-2;
  }
  
  .footer-nav-link:hover,
  .social-link:hover,
  .legal-link:hover,
  .contact-link:hover {
    @apply underline;
  }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  .footer-nav-link,
  .social-link,
  .legal-link,
  .contact-link {
    @apply transition-none;
  }
}
</style>