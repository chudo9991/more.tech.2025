<template>
  <div :class="containerClasses">
    <!-- Label -->
    <label
      v-if="label"
      :for="selectId"
      :class="labelClasses"
    >
      {{ label }}
      <span v-if="required" class="text-red-400 ml-1" aria-label="required">*</span>
    </label>

    <!-- Select container -->
    <div :class="selectContainerClasses">
      <!-- Prepend icon -->
      <div
        v-if="prependIcon"
        class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none z-10"
      >
        <i :class="prependIconClasses" />
      </div>

      <!-- Select field -->
      <select
        :id="selectId"
        ref="selectRef"
        :class="selectClasses"
        :value="modelValue"
        :disabled="disabled"
        :required="required || !!placeholder"
        :aria-describedby="ariaDescribedby"
        :aria-invalid="hasError"
        @change="handleChange"
        @focus="handleFocus"
        @blur="handleBlur"
      >
        <option
          v-if="placeholder"
          value=""
          disabled
          hidden
          :selected="!modelValue || modelValue === ''"
        >
          {{ placeholder }}
        </option>
        
        <option
          v-if="clearable && modelValue"
          value=""
        >
          Очистить выбор
        </option>
        
        <option
          v-for="item in selectOptions"
          :key="getItemValue(item)"
          :value="getItemValue(item)"
          :disabled="item.disabled"
        >
          {{ getItemTitle(item) }}
        </option>
      </select>

      <!-- Dropdown arrow -->
      <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none z-20">
        <i class="mdi mdi-chevron-down text-cyan-400 text-lg" />
      </div>
    </div>

    <!-- Hint text -->
    <p
      v-if="hint && !hasError"
      :id="`${selectId}-hint`"
      :class="hintClasses"
    >
      {{ hint }}
    </p>

    <!-- Error message -->
    <p
      v-if="hasError"
      :id="`${selectId}-error`"
      :class="errorClasses"
      role="alert"
    >
      {{ errorMessage }}
    </p>

    <!-- Success message -->
    <p
      v-if="success && !hasError"
      :id="`${selectId}-success`"
      :class="successClasses"
    >
      {{ success }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

export interface SelectOption {
  label: string
  value: any
  description?: string
  disabled?: boolean
}

export interface BaseSelectProps {
  modelValue?: any
  options?: SelectOption[]
  items?: SelectOption[] // Alias for options
  label?: string
  placeholder?: string
  hint?: string
  error?: string | string[]
  success?: string
  required?: boolean
  disabled?: boolean
  clearable?: boolean
  prependIcon?: string
  size?: 'sm' | 'md' | 'lg'
  variant?: 'outlined' | 'filled' | 'underlined'
}

const props = withDefaults(defineProps<BaseSelectProps>(), {
  size: 'md',
  variant: 'outlined',
  clearable: false
})

const emit = defineEmits<{
  'update:modelValue': [value: any]
  focus: [event: FocusEvent]
  blur: [event: FocusEvent]
  change: [event: Event]
}>()

// Refs
const selectRef = ref<HTMLSelectElement>()

// Generate unique ID for select
const selectId = computed(() => `select-${Math.random().toString(36).substring(2, 11)}`)

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
  if (props.hint && !hasError.value) ids.push(`${selectId.value}-hint`)
  if (hasError.value) ids.push(`${selectId.value}-error`)
  if (props.success && !hasError.value) ids.push(`${selectId.value}-success`)
  return ids.length > 0 ? ids.join(' ') : undefined
})

// Get options (support both options and items props)
const selectOptions = computed(() => props.options || props.items || [])

// Item helpers
const getItemTitle = (item: SelectOption) => item.label
const getItemValue = (item: SelectOption) => item.value

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

// Select container classes
const selectContainerClasses = 'relative'

// Size classes
const sizeClasses = computed(() => {
  const sizes: Record<typeof props.size, string> = {
    sm: 'h-10 px-3 py-2 text-sm',
    md: 'h-12 px-4 py-3 text-base',
    lg: 'h-14 px-4 py-4 text-lg'
  }
  return sizes[props.size]
})

// Padding adjustments for icons
const paddingClasses = computed(() => {
  let leftPadding = ''
  // Правый отступ для стрелки с учетом новых размеров
  const rightPadding = props.size === 'sm' ? 'pr-10' : props.size === 'lg' ? 'pr-12' : 'pr-11'
  
  if (props.prependIcon) {
    leftPadding = props.size === 'sm' ? 'pl-10' : props.size === 'lg' ? 'pl-12' : 'pl-11'
  }
  
  return `${leftPadding} ${rightPadding}`.trim()
})

// Variant classes - обновлено для glassmorphism темы
const variantClasses = computed(() => {
  const base = 'w-full appearance-none transition-all duration-200 focus:outline-none cursor-pointer backdrop-blur-sm'
  
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

// Combined select classes
const selectClasses = computed(() => {
  const baseClasses = [
    sizeClasses.value,
    paddingClasses.value,
    variantClasses.value,
    borderRadiusClasses.value,
    disabledClasses.value,
    'text-slate-100'
  ]
  
  // Добавляем стили для плейсхолдера
  if (!props.modelValue || props.modelValue === '') {
    baseClasses.push('text-slate-400')
  }
  
  return baseClasses.filter(Boolean).join(' ')
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

// Helper text classes - темная тема
const hintClasses = 'mt-2 text-sm text-slate-400'
const errorClasses = 'mt-2 text-sm text-red-400'
const successClasses = 'mt-2 text-sm text-green-400'

// Event handlers
const handleChange = (event: Event) => {
  const target = event.target as HTMLSelectElement
  emit('update:modelValue', target.value)
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
  focus: () => selectRef.value?.focus(),
  blur: () => selectRef.value?.blur()
})
</script>
<style scoped>
/* Основные стили для селекта */
select {
  position: relative;
  z-index: 1;
  line-height: 1.2;
  font-size: inherit;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
  display: flex;
  align-items: center;
}

/* Стили для плейсхолдера */
select:invalid {
  color: rgb(148 163 184 / 0.8) !important;
}

select option:disabled {
  color: rgb(148 163 184 / 0.8) !important;
  font-style: italic;
}

select option:first-child:disabled {
  display: none;
}

/* Стили для опций */
select option {
  background: rgb(15 23 42 / 0.95);
  color: rgb(226 232 240);
  padding: 8px 12px;
}

select option:not(:disabled) {
  color: rgb(226 232 240);
}

/* Стили для стрелки */
.mdi-chevron-down {
  transition: transform 0.2s ease;
  font-size: 1.25rem;
}

/* Анимация стрелки при фокусе */
select:focus ~ div .mdi-chevron-down {
  transform: rotate(180deg);
  color: rgb(0 255 255);
}

/* Улучшенная видимость в темной теме */
select:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 255, 255, 0.3);
}
</style>