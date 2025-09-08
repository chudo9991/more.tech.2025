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

<script>
export default {
  name: 'BaseModal',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: ''
    },
    width: {
      type: [String, Number],
      default: ''
    },
    maxWidth: {
      type: [String, Number],
      default: ''
    },
    height: {
      type: [String, Number],
      default: ''
    },
    maxHeight: {
      type: [String, Number],
      default: ''
    },
    fullscreen: {
      type: Boolean,
      default: false
    },
    persistent: {
      type: Boolean,
      default: false
    },
    noClickAnimation: {
      type: Boolean,
      default: false
    },
    scrollable: {
      type: Boolean,
      default: false
    },
    showCloseButton: {
      type: Boolean,
      default: true
    },
    closeAriaLabel: {
      type: String,
      default: 'Close modal'
    },
    zIndex: {
      type: Number,
      default: 1050
    }
  },
  emits: ['update:modelValue', 'after-enter', 'after-leave', 'close'],
  data() {
    return {
      previousActiveElement: null,
      focusableElements: []
    }
  },
  computed: {
    titleId() {
      return `modal-title-${Math.random().toString(36).substring(2, 11)}`
    },
    contentId() {
      return `modal-content-${Math.random().toString(36).substring(2, 11)}`
    },
    overlayClasses() {
      const base = 'fixed inset-0 flex items-center justify-center p-4 transition-all duration-300'
      const background = 'bg-black/50 backdrop-blur-sm'
      const zIndexClass = `z-[${this.zIndex}]`
      
      return `${base} ${background} ${zIndexClass}`
    },
    sizeClasses() {
      if (this.fullscreen) {
        return 'w-full h-full max-w-none max-h-none'
      }
      
      const widthClass = this.width 
        ? typeof this.width === 'number' 
          ? `w-[${this.width}px]` 
          : `w-[${this.width}]`
        : 'w-full'
        
      const maxWidthClass = this.maxWidth
        ? typeof this.maxWidth === 'number'
          ? `max-w-[${this.maxWidth}px]`
          : `max-w-[${this.maxWidth}]`
        : 'max-w-lg'
        
      const heightClass = this.height
        ? typeof this.height === 'number'
          ? `h-[${this.height}px]`
          : `h-[${this.height}]`
        : ''
        
      const maxHeightClass = this.maxHeight
        ? typeof this.maxHeight === 'number'
          ? `max-h-[${this.maxHeight}px]`
          : `max-h-[${this.maxHeight}]`
        : 'max-h-[90vh]'
      
      return [widthClass, maxWidthClass, heightClass, maxHeightClass].filter(Boolean).join(' ')
    },
    modalClasses() {
      const base = 'relative transform transition-all duration-300'
      const glassmorphism = 'bg-slate-900/70 backdrop-blur-xl border border-cyan-500/30'
      const shadow = 'shadow-2xl shadow-cyan-500/20'
      const layout = this.scrollable ? 'flex flex-col' : ''
      const fullscreenRadius = this.fullscreen ? 'rounded-none' : 'rounded-xl'
      
      return [base, glassmorphism, shadow, this.sizeClasses, layout, fullscreenRadius].filter(Boolean).join(' ')
    },
    headerClasses() {
      const base = 'flex items-center justify-between px-6 py-4'
      const border = this.scrollable ? 'border-b border-cyan-500/20' : ''
      const shrink = this.scrollable ? 'flex-shrink-0' : ''
      
      return [base, border, shrink].filter(Boolean).join(' ')
    },
    titleClasses() {
      return 'text-lg font-semibold text-slate-100'
    },
    closeButtonClasses() {
      return [
        'ml-4 p-2 rounded-lg transition-colors',
        'text-slate-400 hover:text-cyan-400 hover:bg-slate-800/50',
        'focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:ring-offset-2 focus:ring-offset-slate-900'
      ].join(' ')
    },
    contentClasses() {
      const base = 'px-6 py-4 text-slate-200'
      const scroll = this.scrollable ? 'flex-1 overflow-y-auto' : ''
      
      return [base, scroll].filter(Boolean).join(' ')
    },
    footerClasses() {
      const base = 'px-6 py-4'
      const border = this.scrollable ? 'border-t border-cyan-500/20' : ''
      const shrink = this.scrollable ? 'flex-shrink-0' : ''
      
      return [base, border, shrink].filter(Boolean).join(' ')
    }
  },
  methods: {
    getFocusableElements() {
      if (!this.$refs.modalRef) return []
      
      const focusableSelectors = [
        'button:not([disabled])',
        'input:not([disabled])',
        'textarea:not([disabled])',
        'select:not([disabled])',
        'a[href]',
        '[tabindex]:not([tabindex="-1"])'
      ].join(', ')
      
      return Array.from(this.$refs.modalRef.querySelectorAll(focusableSelectors))
    },
    trapFocus(event) {
      if (event.key !== 'Tab') return
      
      const focusableEls = this.getFocusableElements()
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
    },
    handleClose() {
      if (!this.persistent) {
        this.$emit('update:modelValue', false)
        this.$emit('close')
      }
    },
    handleBackdropClick() {
      if (!this.persistent && !this.noClickAnimation) {
        this.handleClose()
      } else if (!this.persistent && this.noClickAnimation) {
        // Add a subtle shake animation for feedback
        if (this.$refs.modalRef) {
          this.$refs.modalRef.classList.add('animate-pulse')
          setTimeout(() => {
            this.$refs.modalRef?.classList.remove('animate-pulse')
          }, 200)
        }
      }
    },
    handleEscapeKey() {
      this.handleClose()
    },
    handleAfterEnter() {
      // Store the previously focused element
      this.previousActiveElement = document.activeElement
      
      // Focus the modal or first focusable element
      setTimeout(() => {
        const focusableEls = this.getFocusableElements()
        if (focusableEls.length > 0) {
          focusableEls[0].focus()
        } else {
          this.$refs.modalRef?.focus()
        }
      }, 0)
      
      // Add focus trap
      document.addEventListener('keydown', this.trapFocus)
      
      this.$emit('after-enter')
    },
    handleAfterLeave() {
      // Remove focus trap
      document.removeEventListener('keydown', this.trapFocus)
      
      // Restore focus to previously focused element
      if (this.previousActiveElement) {
        this.previousActiveElement.focus()
        this.previousActiveElement = null
      }
      
      this.$emit('after-leave')
    },
    lockBodyScroll() {
      document.body.style.overflow = 'hidden'
    },
    unlockBodyScroll() {
      document.body.style.overflow = ''
    }
  },
  watch: {
    modelValue: {
      handler(isVisible) {
        if (isVisible) {
          this.lockBodyScroll()
        } else {
          this.unlockBodyScroll()
        }
      },
      immediate: true
    }
  },
  beforeUnmount() {
    this.unlockBodyScroll()
    document.removeEventListener('keydown', this.trapFocus)
  }
}
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

/* Enhanced glassmorphism with neon effects */
.relative {
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.4),
    0 0 0 1px rgba(0, 255, 255, 0.2),
    0 0 40px rgba(0, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

/* Enhanced neon glow effect on focus */
.relative:focus-within {
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.4),
    0 0 0 1px rgba(0, 255, 255, 0.4),
    0 0 60px rgba(0, 255, 255, 0.3),
    0 0 100px rgba(138, 43, 226, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

/* Scrollbar styling for dark theme */
:deep(*::-webkit-scrollbar) {
  width: 8px;
}

:deep(*::-webkit-scrollbar-track) {
  background: rgba(15, 23, 42, 0.3);
  border-radius: 4px;
}

:deep(*::-webkit-scrollbar-thumb) {
  background: rgba(0, 255, 255, 0.3);
  border-radius: 4px;
}

:deep(*::-webkit-scrollbar-thumb:hover) {
  background: rgba(0, 255, 255, 0.5);
}

/* Animation for pulse effect */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.02);
  }
}

.animate-pulse {
  animation: pulse 0.2s ease-in-out;
}
</style>