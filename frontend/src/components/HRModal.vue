<template>
  <Teleport to="body">
    <Transition
      name="hr-modal"
      @after-enter="handleAfterEnter"
      @after-leave="handleAfterLeave"
    >
      <div
        v-if="modelValue"
        class="hr-modal-overlay"
        @click="handleBackdropClick"
        @keydown.esc="handleEscapeKey"
      >
        <!-- Modal container -->
        <div
          ref="modalRef"
          class="hr-modal-container"
          :class="sizeClasses"
          role="dialog"
          :aria-modal="true"
          :aria-labelledby="titleId"
          :aria-describedby="contentId"
          tabindex="-1"
          @click.stop
        >
          <!-- Shimmer effect -->
          <div class="hr-modal-shimmer"></div>
          
          <!-- Header -->
          <div
            v-if="title || $slots.header || showCloseButton"
            class="hr-modal-header"
          >
            <div v-if="$slots.header" class="flex-1">
              <slot name="header" />
            </div>
            <div v-else-if="title" class="flex-1">
              <h2 :id="titleId" class="hr-modal-title">
                {{ title }}
              </h2>
            </div>
            
            <!-- Close button -->
            <button
              v-if="showCloseButton"
              type="button"
              class="hr-modal-close"
              :aria-label="closeAriaLabel"
              @click="handleClose"
            >
              <i class="mdi mdi mdi-close text-xl" />
            </button>
          </div>

          <!-- Content -->
          <div
            :id="contentId"
            class="hr-modal-content"
            :class="{ 'hr-modal-content-scrollable': scrollable }"
          >
            <slot />
          </div>

          <!-- Footer -->
          <div
            v-if="$slots.footer"
            class="hr-modal-footer"
          >
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'

export interface HRModalProps {
  modelValue: boolean
  title?: string
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full'
  persistent?: boolean
  scrollable?: boolean
  showCloseButton?: boolean
  closeAriaLabel?: string
}

const props = withDefaults(defineProps<HRModalProps>(), {
  size: 'md',
  persistent: false,
  scrollable: false,
  showCloseButton: true,
  closeAriaLabel: 'Закрыть модальное окно'
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'after-enter': []
  'after-leave': []
  'close': []
}>()

// Refs
const modalRef = ref<HTMLElement>()

// Generate unique IDs
const titleId = computed(() => `hr-modal-title-${Math.random().toString(36).substring(2, 11)}`)
const contentId = computed(() => `hr-modal-content-${Math.random().toString(36).substring(2, 11)}`)

// Size classes
const sizeClasses = computed(() => {
  const sizes = {
    sm: 'hr-modal-sm',
    md: 'hr-modal-md', 
    lg: 'hr-modal-lg',
    xl: 'hr-modal-xl',
    full: 'hr-modal-full'
  }
  return sizes[props.size as keyof typeof sizes]
})

// Focus management
let previousActiveElement: HTMLElement | null = null

// Get focusable elements within modal
const getFocusableElements = (): HTMLElement[] => {
  if (!modalRef.value) return []
  
  const focusableSelectors = [
    'button:not([disabled])',
    'input:not([disabled])',
    'textarea:not([disabled])',
    'select:not([disabled])',
    'a[href]',
    '[tabindex]:not([tabindex="-1"])'
  ].join(', ')
  
  return Array.from(modalRef.value.querySelectorAll(focusableSelectors))
}

// Focus trap
const trapFocus = (event: KeyboardEvent) => {
  if (event.key !== 'Tab') return
  
  const focusableEls = getFocusableElements()
  if (focusableEls.length === 0) return
  
  const firstFocusable = focusableEls[0]
  const lastFocusable = focusableEls[focusableEls.length - 1]
  
  if (event.shiftKey) {
    if (document.activeElement === firstFocusable) {
      event.preventDefault()
      lastFocusable.focus()
    }
  } else {
    if (document.activeElement === lastFocusable) {
      event.preventDefault()
      firstFocusable.focus()
    }
  }
}

// Event handlers
const handleClose = () => {
  if (!props.persistent) {
    emit('update:modelValue', false)
    emit('close')
  }
}

const handleBackdropClick = () => {
  if (!props.persistent) {
    handleClose()
  } else {
    // Add shake animation for feedback
    if (modalRef.value) {
      modalRef.value.classList.add('hr-modal-shake')
      setTimeout(() => {
        modalRef.value?.classList.remove('hr-modal-shake')
      }, 500)
    }
  }
}

const handleEscapeKey = () => {
  handleClose()
}

const handleAfterEnter = () => {
  // Store the previously focused element
  previousActiveElement = document.activeElement as HTMLElement
  
  // Focus the modal or first focusable element
  setTimeout(() => {
    const focusableEls = getFocusableElements()
    if (focusableEls.length > 0) {
      focusableEls[0].focus()
    } else {
      modalRef.value?.focus()
    }
  }, 0)
  
  // Add focus trap
  document.addEventListener('keydown', trapFocus)
  
  emit('after-enter')
}

const handleAfterLeave = () => {
  // Remove focus trap
  document.removeEventListener('keydown', trapFocus)
  
  // Restore focus to previously focused element
  if (previousActiveElement) {
    previousActiveElement.focus()
    previousActiveElement = null
  }
  
  emit('after-leave')
}

// Body scroll lock
const lockBodyScroll = () => {
  document.body.style.overflow = 'hidden'
}

const unlockBodyScroll = () => {
  document.body.style.overflow = ''
}

// Watch for modal visibility changes
watch(() => props.modelValue, (isVisible) => {
  if (isVisible) {
    lockBodyScroll()
  } else {
    unlockBodyScroll()
  }
}, { immediate: true })
</script>

<style scoped>
/* HR Modal Overlay */
.hr-modal-overlay {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(25px);
  z-index: 9999;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

/* HR Modal Container */
.hr-modal-container {
  position: relative;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.98), rgba(30, 41, 59, 0.98));
  backdrop-filter: blur(30px);
  border: 1px solid rgba(0, 255, 255, 0.4);
  border-radius: 24px;
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.7),
    0 0 60px rgba(0, 255, 255, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  color: #e2e8f0;
  overflow: hidden;
  transform: translateZ(0);
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

/* Shimmer Effect */
.hr-modal-shimmer {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.15), transparent);
  animation: modalShimmer 4s ease-in-out infinite;
  pointer-events: none;
  z-index: 1;
}

@keyframes modalShimmer {
  0% { left: -100%; }
  100% { left: 100%; }
}

/* Modal Sizes */
.hr-modal-sm {
  width: 100%;
  max-width: 400px;
  max-height: 90vh;
}

.hr-modal-md {
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
}

.hr-modal-lg {
  width: 100%;
  max-width: 700px;
  max-height: 90vh;
}

.hr-modal-xl {
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
}

.hr-modal-full {
  width: 95vw;
  height: 95vh;
  max-width: none;
  max-height: none;
}

/* Modal Header */
.hr-modal-header {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 2rem;
  background: rgba(0, 255, 255, 0.08);
  border-bottom: 1px solid rgba(0, 255, 255, 0.25);
  border-radius: 24px 24px 0 0;
}

.hr-modal-title {
  color: #00ffff;
  text-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
  font-size: 1.375rem;
  font-weight: 700;
  margin: 0;
}

/* Close Button */
.hr-modal-close {
  position: relative;
  z-index: 2;
  background: rgba(0, 255, 255, 0.15);
  border: 1px solid rgba(0, 255, 255, 0.4);
  color: #00ffff;
  border-radius: 12px;
  padding: 0.75rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hr-modal-close:hover {
  background: rgba(0, 255, 255, 0.25);
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
  transform: scale(1.1) rotate(90deg);
}

.hr-modal-close:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 255, 255, 0.5);
}

/* Modal Content */
.hr-modal-content {
  position: relative;
  z-index: 2;
  padding: 2rem;
  line-height: 1.6;
}

.hr-modal-content-scrollable {
  flex: 1;
  overflow-y: auto;
  max-height: calc(90vh - 200px);
}

/* Modal Footer */
.hr-modal-footer {
  position: relative;
  z-index: 2;
  padding: 2rem;
  border-top: 1px solid rgba(0, 255, 255, 0.25);
  background: rgba(0, 255, 255, 0.03);
  border-radius: 0 0 24px 24px;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

/* Content Styling */
.hr-modal-content h1,
.hr-modal-content h2,
.hr-modal-content h3,
.hr-modal-content h4,
.hr-modal-content h5,
.hr-modal-content h6 {
  color: #00ffff;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.4);
  margin-bottom: 1rem;
}

.hr-modal-content p {
  color: #e2e8f0;
  margin-bottom: 1rem;
}

.hr-modal-content strong {
  color: #8a2be2;
  text-shadow: 0 0 5px rgba(138, 43, 226, 0.3);
}

/* Form Elements */
.hr-modal-content input,
.hr-modal-content textarea,
.hr-modal-content select {
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(0, 255, 255, 0.3);
  color: #e2e8f0;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  width: 100%;
  transition: all 0.3s ease;
}

.hr-modal-content input:focus,
.hr-modal-content textarea:focus,
.hr-modal-content select:focus {
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 0 2px rgba(0, 255, 255, 0.2);
  outline: none;
}

.hr-modal-content input::placeholder,
.hr-modal-content textarea::placeholder {
  color: #94a3b8;
}

.hr-modal-content label {
  color: #e2e8f0;
  font-weight: 500;
  margin-bottom: 0.5rem;
  display: block;
}

/* Scrollbar */
.hr-modal-content::-webkit-scrollbar {
  width: 8px;
}

.hr-modal-content::-webkit-scrollbar-track {
  background: rgba(15, 23, 42, 0.3);
  border-radius: 4px;
}

.hr-modal-content::-webkit-scrollbar-thumb {
  background: rgba(0, 255, 255, 0.3);
  border-radius: 4px;
}

.hr-modal-content::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 255, 255, 0.5);
}

/* Animations */
.hr-modal-enter-active,
.hr-modal-leave-active {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.hr-modal-enter-from,
.hr-modal-leave-to {
  opacity: 0;
}

.hr-modal-enter-from .hr-modal-container,
.hr-modal-leave-to .hr-modal-container {
  transform: scale(0.9) translateY(-30px);
}

/* Shake Animation */
.hr-modal-shake {
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
  20%, 40%, 60%, 80% { transform: translateX(5px); }
}

/* Responsive Design */
@media (max-width: 768px) {
  .hr-modal-overlay {
    padding: 0.5rem;
  }
  
  .hr-modal-container {
    border-radius: 16px;
  }
  
  .hr-modal-header {
    padding: 1.5rem;
    border-radius: 16px 16px 0 0;
  }
  
  .hr-modal-content {
    padding: 1.5rem;
  }
  
  .hr-modal-footer {
    padding: 1.5rem;
    border-radius: 0 0 16px 16px;
    flex-direction: column;
  }
  
  .hr-modal-title {
    font-size: 1.25rem;
  }
  
  .hr-modal-sm,
  .hr-modal-md,
  .hr-modal-lg,
  .hr-modal-xl {
    width: 100%;
    max-width: none;
    margin: 0;
  }
  
  .hr-modal-full {
    width: 100vw;
    height: 100vh;
    border-radius: 0;
  }
}

@media (max-width: 480px) {
  .hr-modal-header {
    padding: 1rem;
  }
  
  .hr-modal-content {
    padding: 1rem;
  }
  
  .hr-modal-footer {
    padding: 1rem;
  }
}
</style>