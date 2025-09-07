<template>
  <component
    :is="componentTag"
    :class="cardClasses"
    :to="to"
    :href="href"
    :target="target"
    @click="handleClick"
  >
    <!-- Loading overlay -->
    <div
      v-if="loading"
      class="absolute inset-0 bg-slate-900/90 backdrop-blur-sm flex items-center justify-center z-10 rounded-lg"
    >
      <svg
        class="animate-spin h-8 w-8 text-cyan-400"
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
    </div>

    <!-- Header section -->
    <div
      v-if="title || subtitle || actions?.length || $slots.header"
      :class="headerClasses"
    >
      <div v-if="$slots.header" class="flex-1">
        <slot name="header" />
      </div>
      <div v-else-if="title || subtitle" class="flex-1">
        <h3 v-if="title" :class="titleClasses">
          {{ title }}
        </h3>
        <p v-if="subtitle" :class="subtitleClasses">
          {{ subtitle }}
        </p>
      </div>
      
      <!-- Header actions -->
      <div v-if="actions?.length" class="flex items-center gap-2 ml-4">
        <BaseButton
          v-for="action in actions"
          :key="action.label"
          :variant="action.variant || 'ghost'"
          :size="action.size || 'sm'"
          :icon="action.icon"
          :loading="action.loading"
          :disabled="action.disabled"
          :aria-label="action.ariaLabel || action.label"
          @click="handleActionClick(action, $event)"
        >
          {{ action.showLabel !== false ? action.label : '' }}
        </BaseButton>
      </div>
    </div>

    <!-- Content section -->
    <div :class="[contentClasses, (title || subtitle || actions?.length) ? 'pt-0' : '']">
      <slot />
    </div>

    <!-- Footer section -->
    <div
      v-if="$slots.footer"
      :class="footerClasses"
    >
      <slot name="footer" />
    </div>
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import BaseButton from './BaseButton.vue'

export interface BaseCardAction {
  label: string
  icon?: string
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  disabled?: boolean
  showLabel?: boolean
  ariaLabel?: string
  onClick: (event: MouseEvent) => void | Promise<void>
}

export interface BaseCardProps {
  title?: string
  subtitle?: string
  actions?: BaseCardAction[]
  loading?: boolean
  hoverable?: boolean
  padding?: 'none' | 'sm' | 'md' | 'lg'
  variant?: 'elevated' | 'outlined' | 'flat'
  to?: string | object
  href?: string
  target?: '_blank' | '_self' | '_parent' | '_top'
}

const props = withDefaults(defineProps<BaseCardProps>(), {
  loading: false,
  hoverable: false,
  padding: 'md',
  variant: 'elevated'
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

// Determine component tag based on props
const componentTag = computed(() => {
  if (props.to) return 'router-link'
  if (props.href) return 'a'
  return 'div'
})

// Check if card is interactive
const isInteractive = computed(() => {
  return !!(props.to || props.href || props.hoverable)
})

// Base card classes
const baseClasses = 'relative overflow-hidden transition-all duration-200'

// Variant classes - обновлено для glassmorphism темы
const variantClasses = computed(() => {
  const variants: Record<typeof props.variant, string> = {
    elevated: 'bg-slate-900/60 backdrop-blur-xl border border-cyan-500/20 shadow-2xl shadow-cyan-500/10',
    outlined: 'bg-slate-900/40 backdrop-blur-lg border border-cyan-500/30',
    flat: 'bg-slate-900/30 backdrop-blur-md border border-cyan-500/10'
  }
  return variants[props.variant]
})

// Hover classes - улучшенные glassmorphism эффекты наведения
const hoverClasses = computed(() => {
  if (!isInteractive.value) return ''
  
  const hoverEffects: Record<typeof props.variant, string> = {
    elevated: 'hover:shadow-2xl hover:shadow-cyan-500/20 hover:-translate-y-1 hover:border-cyan-500/40 hover:bg-slate-900/70',
    outlined: 'hover:border-cyan-500/50 hover:shadow-xl hover:shadow-cyan-500/10 hover:bg-slate-900/50',
    flat: 'hover:bg-slate-900/40 hover:border-cyan-500/20'
  }
  return hoverEffects[props.variant]
})

// Focus classes for interactive cards
const focusClasses = computed(() => {
  if (!isInteractive.value) return ''
  return 'focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:ring-offset-2 focus:ring-offset-slate-900'
})

// Border radius classes
const borderRadiusClasses = 'rounded-lg'

// Padding classes - улучшенные отступы
const paddingClasses = computed(() => {
  // Убираем padding с самой карточки, будем применять к секциям
  return ''
})

// Padding для секций контента
const sectionPaddingClasses = computed(() => {
  const paddings: Record<typeof props.padding, string> = {
    none: '',
    sm: 'px-3 py-2',
    md: 'px-4 py-3',
    lg: 'px-5 py-4'
  }
  return paddings[props.padding]
})

// Combined card classes
const cardClasses = computed(() => {
  return [
    baseClasses,
    variantClasses.value,
    hoverClasses.value,
    focusClasses.value,
    borderRadiusClasses,
    paddingClasses.value,
    isInteractive.value ? 'cursor-pointer' : ''
  ].filter(Boolean).join(' ')
})

// Header classes
const headerClasses = computed(() => {
  const baseHeader = 'flex items-start justify-between'
  const spacing = props.padding === 'none' ? '' : 'pb-2'
  return `${baseHeader} ${spacing} ${sectionPaddingClasses.value}`
})

// Title classes - темная тема с neon эффектом
const titleClasses = 'text-lg font-semibold text-cyan-400 leading-tight drop-shadow-sm'

// Subtitle classes - темная тема
const subtitleClasses = 'text-sm text-slate-300 mt-1'

// Content classes - темная тема
const contentClasses = computed(() => {
  const basePadding = props.padding === 'none' ? '' : sectionPaddingClasses.value
  return `text-slate-200 leading-relaxed ${basePadding}`
})

// Footer classes - темная тема
const footerClasses = computed(() => {
  const spacing = props.padding === 'none' ? 'mt-4 pt-4' : 'mt-6 pt-6'
  return `${spacing} border-t border-cyan-500/20 ${sectionPaddingClasses.value}`
})

// Handle card click
const handleClick = (event: MouseEvent) => {
  if (!props.loading) {
    emit('click', event)
  }
}

// Handle action click
const handleActionClick = async (action: BaseCardAction, event: MouseEvent) => {
  event.stopPropagation() // Prevent card click when action is clicked
  
  if (!action.disabled && !action.loading) {
    await action.onClick(event)
  }
}
</script>