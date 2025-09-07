<template>
  <Teleport to="body">
    <Transition
      name="modal"
      @after-enter="handleAfterEnter"
      @after-leave="handleAfterLeave"
    >
      <div
        v-if="modelValue"
        :class="overlayClasses"
        @click="handleBackdropClick"
        @keydown.esc="handleEscapeKey"
      >
        <!-- Modal container -->
        <div
          ref="modalRef"
          :class="modalClasses"
          role="dialog"
          :aria-modal="true"
          :aria-labelledby="titleId"
          :aria-describedby="contentId"
          tabindex="-1"
          @click.stop
        >
          <!-- Header -->
          <div
            v-if="title || $slots.header || showCloseButton"
            :class="headerClasses"
          >
            <div v-if="$slots.header" class="flex-1">
              <slot name="header" />
            </div>
            <div v-else-if="title" class="flex-1">
              <h2 :id="titleId" :class="titleClasses">
                {{ title }}
              </h2>
            </div>
            
            <!-- Close button -->
            <button
              v-if="showCloseButton"
              type="button"
              :class="closeButtonClasses"
              :aria-label="closeAriaLabel"
              @click="handleClose"
            >
              <i class="mdi mdi-close text-xl" />
            </button>
          </div>

          <!-- Content -->
          <div
            :id="contentId"
            :class="contentClasses"
          >
            <slot />
          </div>

          <!-- Footer -->
          <div
            v-if="$slots.footer"
            :class="footerClasses"
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

export interface BaseModalProps {
  modelValue: boolean
  title?: string
  width?: string | number
  maxWidth?: string | number
  height?: string | number
  maxHeight?: string | number
  fullscreen?: boolean
  persistent?: boolean
  noClickAnimation?: boolean
  scrollable?: boolean
  showCloseButton?: boolean
  closeAriaLabel?: string
  zIndex?: number
}

const props = withDefaults(defineProps<BaseModalProps>(), {
  persistent: false,
  noClickAnimation: false,
  scrollable: false,
  showCloseButton: true,
  closeAriaLabel: 'Close modal',
  zIndex: 1050
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
const titleId = computed(() => `modal-title-${Math.random().toString(36).substring(2, 11)}`)
const contentId = computed(() => `modal-content-${Math.random().toString(36).substring(2, 11)}`)

// Focus management
let previousActiveElement: HTMLElement | null = null
const focusableElements = ref<HTMLElement[]>([])

// Overlay classes
const overlayClasses = computed(() => {
  const base = 'fixed inset-0 flex items-center justify-center p-4 transition-all duration-300'
  const background = 'bg-black/50 backdrop-blur-sm'
  const zIndexClass = `z-[${props.zIndex}]`
  
  return `${base} ${background} ${zIndexClass}`
})

// Modal size classes
const sizeClasses = computed(() => {
  if (props.fullscreen) {
    return 'w-full h-full max-w-none max-h-none'
  }
  
  const widthClass = props.width 
    ? typeof props.width === 'number' 
      ? `w-[${props.width}px]` 
      : `w-[${props.width}]`
    : 'w-full'
    
  const maxWidthClass = props.maxWidth
    ? typeof props.maxWidth === 'number'
      ? `max-w-[${props.maxWidth}px]`
      : `max-w-[${props.maxWidth}]`
    : 'max-w-lg'
    
  const heightClass = props.height
    ? typeof props.height === 'number'
      ? `h-[${props.height}px]`
      : `h-[${props.height}]`
    : ''
    
  const maxHeightClass = props.maxHeight
    ? typeof props.maxHeight === 'number'
      ? `max-h-[${props.maxHeight}px]`
      : `max-h-[${props.maxHeight}]`
    : 'max-h-[90vh]'
  
  return [widthClass, maxWidthClass, heightClass, maxHeightClass].filter(Boolean).join(' ')
})

// Modal classes
const modalClasses = computed(() => {
  const base = 'relative bg-white dark:bg-neutral-800 rounded-xl shadow-2xl transform transition-all duration-300'
  const layout = props.scrollable ? 'flex flex-col' : ''
  const fullscreenRadius = props.fullscreen ? 'rounded-none' : ''
  
  return [base, sizeClasses.value, layout, fullscreenRadius].filter(Boolean).join(' ')
})

// Header classes
const headerClasses = computed(() => {
  const base = 'flex items-center justify-between px-6 py-4'
  const border = props.scrollable ? 'border-b border-neutral-200 dark:border-neutral-700' : ''
  const shrink = props.scrollable ? 'flex-shrink-0' : ''
  
  return [base, border, shrink].filter(Boolean).join(' ')
})

// Title classes
const titleClasses = 'text-lg font-semibold text-neutral-900 dark:text-neutral-100'

// Close button classes
const closeButtonClasses = computed(() => {
  return [
    'ml-4 p-2 rounded-lg transition-colors',
    'text-neutral-400 hover:text-neutral-600 hover:bg-neutral-100',
    'dark:text-neutral-500 dark:hover:text-neutral-300 dark:hover:bg-neutral-700',
    'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2'
  ].join(' ')
})

// Content classes
const contentClasses = computed(() => {
  const base = 'px-6 py-4'
  const scroll = props.scrollable ? 'flex-1 overflow-y-auto' : ''
  
  return [base, scroll].filter(Boolean).join(' ')
})

// Footer classes
const footerClasses = computed(() => {
  const base = 'px-6 py-4'
  const border = props.scrollable ? 'border-t border-neutral-200 dark:border-neutral-700' : ''
  const shrink = props.scrollable ? 'flex-shrink-0' : ''
  
  return [base, border, shrink].filter(Boolean).join(' ')
})

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

// Focus management
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
  if (!props.persistent && !props.noClickAnimation) {
    handleClose()
  } else if (!props.persistent && props.noClickAnimation) {
    // Add a subtle shake animation for feedback
    if (modalRef.value) {
      modalRef.value.classList.add('animate-pulse')
      setTimeout(() => {
        modalRef.value?.classList.remove('animate-pulse')
      }, 200)
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

// Cleanup on unmount - handled by watch
</script>

<style scoped>
/* Modal transition animations */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .relative,
.modal-leave-active .relative {
  transition: transform 0.3s ease;
}

.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.95) translateY(-20px);
}
</style>