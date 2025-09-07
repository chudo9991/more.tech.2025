<template>
  <component
    :is="componentTag"
    :class="buttonClasses"
    :disabled="disabled || loading"
    :type="type"
    :to="to"
    :href="href"
    :target="target"
    :aria-label="ariaLabel"
    :aria-describedby="ariaDescribedby"
    @click="handleClick"
  >
    <!-- Shimmer effect for primary buttons - ТОЧНО как в оригинале -->
    <span
      v-if="variant === 'primary' && !loading"
      class="absolute inset-0 -translate-x-full bg-gradient-to-r from-transparent via-cyan-400/40 to-transparent transition-transform duration-600 ease-in-out group-hover:translate-x-full"
    ></span>

    <!-- Button content container -->
    <span class="inline-flex items-center justify-center relative z-10 gap-2">
      <!-- Loading spinner -->
      <template v-if="loading">
        <svg
          class="animate-spin"
          :class="loadingIconSize"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          />
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      </template>

      <!-- Left icon (prop) -->
      <template v-else-if="icon && iconPosition === 'left'">
        <i :class="iconClasses" />
      </template>

      <!-- Button content (slot) -->
      <template v-if="!loading">
        <slot />
      </template>

      <!-- Right icon (prop) -->
      <template v-if="!loading && icon && iconPosition === 'right'">
        <i :class="iconClasses" />
      </template>

      <!-- Icon only (when no slot content) -->
      <template v-if="!loading && iconOnly && icon">
        <i :class="iconClasses" />
      </template>
    </span>
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'

export interface BaseButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  disabled?: boolean
  icon?: string
  iconOnly?: boolean
  iconPosition?: 'left' | 'right'
  type?: 'button' | 'submit' | 'reset'
  to?: string | object
  href?: string
  target?: '_blank' | '_self' | '_parent' | '_top'
  ariaLabel?: string
  ariaDescribedby?: string
}

const props = withDefaults(defineProps<BaseButtonProps>(), {
  variant: 'primary',
  size: 'md',
  loading: false,
  disabled: false,
  iconOnly: false,
  iconPosition: 'left',
  type: 'button'
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

// Determine component tag based on props
const componentTag = computed(() => {
  if (props.to) return 'router-link'
  if (props.href) return 'a'
  return 'button'
})

// Use iconOnly prop directly
const iconOnly = computed(() => props.iconOnly)

// Base button classes - ТОЧНО как cta-button: display: inline-flex, align-items: center, justify-content: center, font-weight: 600, font-size: 1.1rem, transition: all 0.3s ease, cursor: pointer
const baseClasses = 'group inline-flex items-center justify-center font-semibold cursor-pointer focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none relative overflow-hidden transition-all duration-300'

// Size classes - ТОЧНЫЕ размеры как у cta-button: padding: 1rem 2rem (16px 32px), font-size: 1.1rem, min-width: 200px
const sizeClasses = computed(() => {
  const sizes: Record<typeof props.size, string> = {
    sm: iconOnly.value 
      ? 'h-8 w-8 text-sm' 
      : 'cta-size-sm',
    md: iconOnly.value 
      ? 'h-10 w-10 text-base' 
      : 'cta-size-md',
    lg: iconOnly.value 
      ? 'h-12 w-12 text-lg' 
      : 'cta-size-lg'
  }
  return sizes[props.size]
})

// Variant classes - используем точные CSS стили как в оригинале
const variantClasses = computed(() => {
  const variants: Record<typeof props.variant, string> = {
    primary: 'cta-primary-style',
    secondary: 'cta-secondary-style', 
    outline: 'cta-outline-style',
    ghost: 'cta-ghost-style',
    danger: 'cta-danger-style'
  }
  return variants[props.variant]
})

// Border radius classes - ТОЧНО как у cta-button (border-radius: 8px)
const borderRadiusClasses = computed(() => {
  return 'rounded-lg'
})

// Combined button classes
const buttonClasses = computed(() => {
  return [
    baseClasses,
    sizeClasses.value,
    variantClasses.value,
    borderRadiusClasses.value
  ].join(' ')
})

// Icon classes
const iconClasses = computed(() => {
  const iconSizes: Record<typeof props.size, string> = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg'
  }
  return `${props.icon} ${iconSizes[props.size]}`
})

// Loading icon size
const loadingIconSize = computed(() => {
  const sizes: Record<typeof props.size, string> = {
    sm: 'h-4 w-4',
    md: 'h-5 w-5',
    lg: 'h-6 w-6'
  }
  return sizes[props.size]
})

// Icon-only specific classes
const iconOnlyClasses = computed(() => {
  return iconOnly.value ? '' : ''
})

// Text classes for proper spacing
const textClasses = computed(() => {
  return 'truncate'
})

// Handle click events
const handleClick = (event: MouseEvent) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<style scoped>
/* ТОЧНЫЕ стили как у cta-primary с главной страницы */
.cta-primary-style {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(138, 43, 226, 0.2)) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.5) !important;
  color: #00ffff !important;
  box-shadow: 0 8px 32px rgba(0, 255, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.cta-primary-style:hover {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.35), rgba(138, 43, 226, 0.35)) !important;
  transform: translateY(-3px);
  box-shadow: 0 12px 40px rgba(0, 255, 255, 0.5);
  text-shadow: 0 0 15px rgba(0, 255, 255, 1);
}

.cta-secondary-style {
  background: rgba(15, 23, 42, 0.7) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(138, 43, 226, 0.5) !important;
  color: #8a2be2 !important;
  box-shadow: 0 8px 32px rgba(138, 43, 226, 0.2) !important;
  position: relative !important;
  overflow: hidden !important;
}

.cta-secondary-style:hover {
  background: rgba(138, 43, 226, 0.2) !important;
  border-color: rgba(138, 43, 226, 0.7) !important;
  transform: translateY(-3px);
  box-shadow: 0 12px 40px rgba(138, 43, 226, 0.4);
  text-shadow: 0 0 15px rgba(138, 43, 226, 1);
}

.cta-outline-style {
  background: transparent;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.6);
  color: #00ffff;
  box-shadow: 0 4px 16px rgba(0, 255, 255, 0.1);
}

.cta-outline-style:hover {
  background: rgba(0, 255, 255, 0.1);
  border-color: rgba(0, 255, 255, 0.8);
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 255, 255, 0.3);
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.8);
}

.cta-ghost-style {
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  color: #00ffff;
  box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
}

.cta-ghost-style:hover {
  background: rgba(0, 255, 255, 0.1);
  border-color: rgba(0, 255, 255, 0.5);
  transform: translateY(-3px);
  box-shadow: 0 12px 40px rgba(0, 255, 255, 0.3);
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.8);
}

.cta-danger-style {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(236, 72, 153, 0.2)) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(239, 68, 68, 0.5) !important;
  color: #ef4444 !important;
  box-shadow: 0 8px 32px rgba(239, 68, 68, 0.3);
}

.cta-danger-style:hover {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.35), rgba(236, 72, 153, 0.35)) !important;
  transform: translateY(-3px);
  box-shadow: 0 12px 40px rgba(239, 68, 68, 0.5);
  text-shadow: 0 0 15px rgba(239, 68, 68, 1);
}

/* ТОЧНЫЕ размеры как у cta-button */
.cta-size-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  min-width: 120px;
  height: 2.5rem; /* 40px - как у BaseSelect sm */
}

.cta-size-md {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  min-width: 160px;
  height: 3rem; /* 48px - как у BaseSelect md */
}

.cta-size-lg {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  min-width: 200px;
  height: 3.5rem; /* 56px - как у BaseSelect lg */
}
</style>