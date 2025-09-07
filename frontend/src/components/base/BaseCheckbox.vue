<template>
  <div :class="containerClasses">
    <div :class="checkboxContainerClasses">
      <!-- Hidden native checkbox for accessibility -->
      <input
        :id="checkboxId"
        ref="checkboxRef"
        type="checkbox"
        :class="hiddenCheckboxClasses"
        :checked="isChecked"
        :disabled="disabled"
        :required="required"
        :aria-describedby="ariaDescribedby"
        :aria-invalid="hasError"
        @change="handleChange"
        @focus="handleFocus"
        @blur="handleBlur"
      />
      
      <!-- Custom checkbox -->
      <label
        :for="checkboxId"
        :class="labelClasses"
      >
        <div :class="checkboxClasses">
          <!-- Check icon -->
          <i
            v-if="isChecked"
            class="mdi mdi-check text-white"
            :class="iconSizeClasses"
          />
          
          <!-- Indeterminate icon -->
          <i
            v-else-if="indeterminate"
            class="mdi mdi-minus text-white"
            :class="iconSizeClasses"
          />
        </div>
        
        <!-- Label text -->
        <span
          v-if="label || $slots.default"
          :class="labelTextClasses"
        >
          <slot>{{ label }}</slot>
        </span>
      </label>
    </div>

    <!-- Hint text -->
    <p
      v-if="hint && !hasError"
      :id="`${checkboxId}-hint`"
      :class="hintClasses"
    >
      {{ hint }}
    </p>

    <!-- Error message -->
    <p
      v-if="hasError"
      :id="`${checkboxId}-error`"
      :class="errorClasses"
      role="alert"
    >
      {{ errorMessage }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

export interface BaseCheckboxProps {
  modelValue?: boolean | any[]
  value?: any
  label?: string
  hint?: string
  error?: string | string[]
  required?: boolean
  disabled?: boolean
  indeterminate?: boolean
  size?: 'sm' | 'md' | 'lg'
  color?: 'primary' | 'success' | 'warning' | 'error'
}

const props = withDefaults(defineProps<BaseCheckboxProps>(), {
  size: 'md',
  color: 'primary'
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean | any[]]
  focus: [event: FocusEvent]
  blur: [event: FocusEvent]
  change: [event: Event]
}>()

// Refs
const checkboxRef = ref<HTMLInputElement>()

// Generate unique ID for checkbox
const checkboxId = computed(() => `checkbox-${Math.random().toString(36).substring(2, 11)}`)

// Determine if checkbox is checked
const isChecked = computed(() => {
  if (Array.isArray(props.modelValue)) {
    return props.value !== undefined && props.modelValue.includes(props.value)
  }
  return Boolean(props.modelValue)
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
  if (props.hint && !hasError.value) ids.push(`${checkboxId.value}-hint`)
  if (hasError.value) ids.push(`${checkboxId.value}-error`)
  return ids.length > 0 ? ids.join(' ') : undefined
})

// Container classes
const containerClasses = 'w-full'

// Checkbox container classes
const checkboxContainerClasses = 'relative'

// Hidden checkbox classes (for accessibility)
const hiddenCheckboxClasses = 'sr-only'

// Label classes
const labelClasses = computed(() => {
  const base = 'flex items-start gap-3 cursor-pointer transition-colors'
  const disabled = props.disabled ? 'opacity-50 cursor-not-allowed' : 'hover:opacity-80'
  
  return `${base} ${disabled}`
})

// Size classes
const sizeClasses = computed(() => {
  const sizes: Record<typeof props.size, string> = {
    sm: 'h-4 w-4',
    md: 'h-5 w-5',
    lg: 'h-6 w-6'
  }
  return sizes[props.size]
})

// Icon size classes
const iconSizeClasses = computed(() => {
  const sizes: Record<typeof props.size, string> = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base'
  }
  return sizes[props.size]
})

// Color classes
const colorClasses = computed(() => {
  if (hasError.value) {
    return isChecked.value || props.indeterminate
      ? 'bg-error-500 border-error-500'
      : 'border-error-300 dark:border-error-600'
  }
  
  const colors: Record<typeof props.color, string> = {
    primary: isChecked.value || props.indeterminate
      ? 'bg-primary-500 border-primary-500'
      : 'border-neutral-300 dark:border-neutral-600',
    success: isChecked.value || props.indeterminate
      ? 'bg-success-500 border-success-500'
      : 'border-neutral-300 dark:border-neutral-600',
    warning: isChecked.value || props.indeterminate
      ? 'bg-warning-500 border-warning-500'
      : 'border-neutral-300 dark:border-neutral-600',
    error: isChecked.value || props.indeterminate
      ? 'bg-error-500 border-error-500'
      : 'border-neutral-300 dark:border-neutral-600'
  }
  
  return colors[props.color]
})

// Hover and focus classes
const interactionClasses = computed(() => {
  if (props.disabled) return ''
  
  const base = 'transition-all duration-200'
  const hover = hasError.value
    ? 'hover:border-error-400'
    : `hover:border-${props.color}-400`
  const focus = 'focus-within:ring-2 focus-within:ring-offset-2'
  const focusColor = hasError.value
    ? 'focus-within:ring-error-200 dark:focus-within:ring-error-800'
    : `focus-within:ring-${props.color}-200 dark:focus-within:ring-${props.color}-800`
  
  return `${base} ${hover} ${focus} ${focusColor}`
})

// Combined checkbox classes
const checkboxClasses = computed(() => {
  const base = 'flex items-center justify-center border-2 rounded-md bg-white dark:bg-neutral-800'
  
  return [
    base,
    sizeClasses.value,
    colorClasses.value,
    interactionClasses.value
  ].filter(Boolean).join(' ')
})

// Label text classes
const labelTextClasses = computed(() => {
  const base = 'text-sm leading-relaxed select-none'
  const colors = hasError.value
    ? 'text-error-700 dark:text-error-400'
    : 'text-neutral-700 dark:text-neutral-300'
  
  // Adjust top margin based on checkbox size for alignment
  const alignment = props.size === 'sm' ? 'mt-0' : props.size === 'lg' ? 'mt-0.5' : 'mt-0'
  
  return `${base} ${colors} ${alignment}`
})

// Helper text classes
const hintClasses = 'mt-2 text-sm text-neutral-600 dark:text-neutral-400'
const errorClasses = 'mt-2 text-sm text-error-600 dark:text-error-400'

// Event handlers
const handleChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  
  if (Array.isArray(props.modelValue)) {
    // Handle array of values (multiple checkboxes)
    const newValue = [...props.modelValue]
    if (target.checked) {
      if (props.value !== undefined && !newValue.includes(props.value)) {
        newValue.push(props.value)
      }
    } else {
      const index = newValue.indexOf(props.value)
      if (index > -1) {
        newValue.splice(index, 1)
      }
    }
    emit('update:modelValue', newValue)
  } else {
    // Handle boolean value (single checkbox)
    emit('update:modelValue', target.checked)
  }
  
  emit('change', event)
}

const handleFocus = (event: FocusEvent) => {
  emit('focus', event)
}

const handleBlur = (event: FocusEvent) => {
  emit('blur', event)
}

// Expose methods for parent components
defineExpose({
  focus: () => checkboxRef.value?.focus(),
  blur: () => checkboxRef.value?.blur()
})
</script>