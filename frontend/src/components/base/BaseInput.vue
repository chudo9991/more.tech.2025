<template>
  <div :class="containerClasses">
    <!-- Label -->
    <label
      v-if="label"
      :for="inputId"
      :class="labelClasses"
    >
      {{ label }}
      <span v-if="required" class="text-red-400 ml-1" aria-label="required">*</span>
    </label>

    <!-- Input container -->
    <div :class="inputContainerClasses">
      <!-- Prepend icon -->
      <div
        v-if="prependIcon"
        class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none"
      >
        <i :class="prependIconClasses" />
      </div>

      <!-- Input field -->
      <component
        :is="inputComponent"
        :id="inputId"
        ref="inputRef"
        :class="inputClasses"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :maxlength="maxlength"
        :minlength="minlength"
        :autocomplete="autocomplete"
        :aria-describedby="ariaDescribedby"
        :aria-invalid="hasError"
        :rows="type === 'textarea' ? rows : undefined"
        @input="handleInput"
        @focus="handleFocus"
        @blur="handleBlur"
        @change="handleChange"
      />

      <!-- Append icon / Clear button -->
      <div
        v-if="appendIcon || (clearable && modelValue)"
        class="absolute inset-y-0 right-0 flex items-center pr-3"
      >
        <!-- Clear button -->
        <button
          v-if="clearable && modelValue && !disabled && !readonly"
          type="button"
          class="text-slate-400 hover:text-cyan-400 transition-colors"
          :aria-label="clearAriaLabel"
          @click="handleClear"
        >
          <i class="mdi mdi-close text-sm" />
        </button>
        
        <!-- Append icon -->
        <div
          v-else-if="appendIcon"
          class="pointer-events-none"
        >
          <i :class="appendIconClasses" />
        </div>
      </div>
    </div>

    <!-- Hint text -->
    <p
      v-if="hint && !hasError"
      :id="`${inputId}-hint`"
      :class="hintClasses"
    >
      {{ hint }}
    </p>

    <!-- Error message -->
    <p
      v-if="hasError"
      :id="`${inputId}-error`"
      :class="errorClasses"
      role="alert"
    >
      {{ errorMessage }}
    </p>

    <!-- Success message -->
    <p
      v-if="success && !hasError"
      :id="`${inputId}-success`"
      :class="successClasses"
    >
      {{ success }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

export interface BaseInputProps {
  modelValue?: string | number
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search' | 'textarea'
  label?: string
  placeholder?: string
  hint?: string
  error?: string | string[]
  success?: string
  required?: boolean
  disabled?: boolean
  readonly?: boolean
  clearable?: boolean
  prependIcon?: string
  appendIcon?: string
  maxlength?: number
  minlength?: number
  autocomplete?: string
  rows?: number
  size?: 'sm' | 'md' | 'lg'
  variant?: 'outlined' | 'filled' | 'underlined'
  clearAriaLabel?: string
}

const props = withDefaults(defineProps<BaseInputProps>(), {
  type: 'text',
  size: 'md',
  variant: 'outlined',
  rows: 3,
  clearAriaLabel: 'Clear input'
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
  focus: [event: FocusEvent]
  blur: [event: FocusEvent]
  change: [event: Event]
  clear: []
}>()

// Refs
const inputRef = ref<HTMLInputElement | HTMLTextAreaElement>()

// Generate unique ID for input
const inputId = computed(() => `input-${Math.random().toString(36).substring(2, 11)}`)

// Determine input component
const inputComponent = computed(() => {
  return props.type === 'textarea' ? 'textarea' : 'input'
})

// Error handling
const hasError = computed(() => {
  return !!(props.error && (Array.isArray(props.error) ? props.error.length > 0 : props.error))
})

const errorMessage = computed(() => {
  if (!props.error) return ''
  return Array.isArray(props.error) ? props.error[0] : props.error
})

// ARIA describedby
const ariaDescribedby = computed(() => {
  const ids = []
  if (props.hint && !hasError.value) ids.push(`${inputId.value}-hint`)
  if (hasError.value) ids.push(`${inputId.value}-error`)
  if (props.success && !hasError.value) ids.push(`${inputId.value}-success`)
  return ids.length > 0 ? ids.join(' ') : undefined
})

// Container classes
const containerClasses = 'w-full'

// Label classes - темная тема
const labelClasses = computed(() => {
  const base = 'block text-sm font-medium mb-2 transition-colors'
  const colors = hasError.value
    ? 'text-red-400'
    : 'text-slate-300'
  
  return `${base} ${colors}`
})

// Input container classes
const inputContainerClasses = 'relative'

// Size classes
const sizeClasses = computed(() => {
  const sizes: Record<typeof props.size, string> = {
    sm: props.type === 'textarea' ? 'px-3 py-2 text-sm' : 'h-10 px-3 py-2 text-sm',
    md: props.type === 'textarea' ? 'px-4 py-3 text-base' : 'h-12 px-4 py-3 text-base',
    lg: props.type === 'textarea' ? 'px-4 py-4 text-lg' : 'h-14 px-4 py-4 text-lg'
  }
  return sizes[props.size]
})

// Padding adjustments for icons
const paddingClasses = computed(() => {
  let leftPadding = ''
  let rightPadding = ''
  
  if (props.prependIcon) {
    leftPadding = props.size === 'sm' ? 'pl-10' : props.size === 'lg' ? 'pl-12' : 'pl-11'
  }
  
  if (props.appendIcon || props.clearable) {
    rightPadding = props.size === 'sm' ? 'pr-10' : props.size === 'lg' ? 'pr-12' : 'pr-11'
  }
  
  return `${leftPadding} ${rightPadding}`.trim()
})

// Variant classes - обновлено для glassmorphism темы
const variantClasses = computed(() => {
  const base = 'w-full transition-all duration-200 focus:outline-none backdrop-blur-sm'
  
  const variants: Record<typeof props.variant, string> = {
    outlined: hasError.value
      ? 'border border-red-400/60 bg-slate-900/40 focus:border-red-400 focus:ring-2 focus:ring-red-400/20 focus:bg-slate-900/60'
      : 'border border-cyan-500/30 bg-slate-900/40 hover:border-cyan-500/50 focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20 focus:bg-slate-900/60',
    
    filled: hasError.value
      ? 'border-0 border-b-2 border-red-400/60 bg-slate-900/60 focus:border-red-400 focus:bg-slate-900/80'
      : 'border-0 border-b-2 border-cyan-500/30 bg-slate-900/60 hover:bg-slate-900/70 focus:border-cyan-400 focus:bg-slate-900/80',
    
    underlined: hasError.value
      ? 'border-0 border-b-2 border-red-400/60 bg-transparent focus:border-red-400'
      : 'border-0 border-b-2 border-cyan-500/30 bg-transparent hover:border-cyan-500/50 focus:border-cyan-400'
  }
  
  return `${base} ${variants[props.variant]}`
})

// Border radius classes
const borderRadiusClasses = computed(() => {
  if (props.variant === 'underlined') return ''
  return 'rounded-lg'
})

// Disabled classes - темная тема
const disabledClasses = computed(() => {
  if (!props.disabled) return ''
  return 'opacity-50 cursor-not-allowed bg-slate-900/20'
})

// Combined input classes
const inputClasses = computed(() => {
  return [
    sizeClasses.value,
    paddingClasses.value,
    variantClasses.value,
    borderRadiusClasses.value,
    disabledClasses.value,
    'text-slate-100 placeholder-slate-400'
  ].filter(Boolean).join(' ')
})

// Icon classes - темная тема
const prependIconClasses = computed(() => {
  const baseIcon = props.prependIcon
  const sizeClass = props.size === 'sm' ? 'text-sm' : props.size === 'lg' ? 'text-lg' : 'text-base'
  const colorClass = hasError.value 
    ? 'text-red-400' 
    : 'text-cyan-400'
  
  return `${baseIcon} ${sizeClass} ${colorClass}`
})

const appendIconClasses = computed(() => {
  const baseIcon = props.appendIcon
  const sizeClass = props.size === 'sm' ? 'text-sm' : props.size === 'lg' ? 'text-lg' : 'text-base'
  const colorClass = hasError.value 
    ? 'text-red-400' 
    : 'text-cyan-400'
  
  return `${baseIcon} ${sizeClass} ${colorClass}`
})

// Helper text classes - темная тема
const hintClasses = 'mt-2 text-sm text-slate-400'
const errorClasses = 'mt-2 text-sm text-red-400'
const successClasses = 'mt-2 text-sm text-green-400'

// Event handlers
const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement | HTMLTextAreaElement
  const value = props.type === 'number' ? Number(target.value) : target.value
  emit('update:modelValue', value)
}

const handleFocus = (event: FocusEvent) => {
  emit('focus', event)
}

const handleBlur = (event: FocusEvent) => {
  emit('blur', event)
}

const handleChange = (event: Event) => {
  emit('change', event)
}

const handleClear = () => {
  emit('update:modelValue', '')
  emit('clear')
  
  // Focus the input after clearing
  setTimeout(() => {
    inputRef.value?.focus()
  }, 0)
}

// Expose methods for parent components
defineExpose({
  focus: () => inputRef.value?.focus(),
  blur: () => inputRef.value?.blur(),
  select: () => (inputRef.value as HTMLInputElement)?.select?.()
})
</script>