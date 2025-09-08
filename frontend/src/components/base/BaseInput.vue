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
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
          </svg>
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

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  type: {
    type: String,
    default: 'text',
    validator: (value) => ['text', 'email', 'password', 'number', 'tel', 'url', 'search', 'textarea'].includes(value)
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  hint: {
    type: String,
    default: ''
  },
  error: {
    type: [String, Array],
    default: ''
  },
  success: {
    type: String,
    default: ''
  },
  required: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  },
  clearable: {
    type: Boolean,
    default: false
  },
  prependIcon: {
    type: String,
    default: ''
  },
  appendIcon: {
    type: String,
    default: ''
  },
  maxlength: {
    type: Number,
    default: undefined
  },
  minlength: {
    type: Number,
    default: undefined
  },
  autocomplete: {
    type: String,
    default: ''
  },
  rows: {
    type: Number,
    default: 3
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  variant: {
    type: String,
    default: 'outlined',
    validator: (value) => ['outlined', 'filled', 'underlined'].includes(value)
  },
  clearAriaLabel: {
    type: String,
    default: 'Clear input'
  }
})

const emit = defineEmits([
  'update:modelValue',
  'focus',
  'blur',
  'change',
  'clear'
])

// Refs
const inputRef = ref()

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
  const sizes = {
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
  
  const variants = {
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
const handleInput = (event) => {
  const target = event.target
  const value = props.type === 'number' ? Number(target.value) : target.value
  emit('update:modelValue', value)
}

const handleFocus = (event) => {
  emit('focus', event)
}

const handleBlur = (event) => {
  emit('blur', event)
}

const handleChange = (event) => {
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
  select: () => inputRef.value?.select?.()
})
</script>