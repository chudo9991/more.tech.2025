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

<script>
export default {
  name: 'BaseSelect',
  props: {
    modelValue: {
      type: [String, Number, Boolean],
      default: ''
    },
    options: {
      type: Array,
      default: () => []
    },
    items: {
      type: Array,
      default: () => []
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
    clearable: {
      type: Boolean,
      default: false
    },
    prependIcon: {
      type: String,
      default: ''
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
    }
  },
  emits: ['update:modelValue', 'focus', 'blur', 'change'],
  computed: {
    selectId() {
      return `select-${Math.random().toString(36).substring(2, 11)}`
    },
    hasError() {
      return !!(this.error && (Array.isArray(this.error) ? this.error.length > 0 : this.error))
    },
    errorMessage() {
      if (!this.error) return ''
      return Array.isArray(this.error) ? this.error[0] : this.error
    },
    ariaDescribedby() {
      const ids = []
      if (this.hint && !this.hasError) ids.push(`${this.selectId}-hint`)
      if (this.hasError) ids.push(`${this.selectId}-error`)
      if (this.success && !this.hasError) ids.push(`${this.selectId}-success`)
      return ids.length > 0 ? ids.join(' ') : undefined
    },
    selectOptions() {
      return this.options || this.items || []
    },
    containerClasses() {
      return 'w-full'
    },
    labelClasses() {
      const base = 'block text-sm font-medium mb-2 transition-colors'
      const colors = this.hasError
        ? 'text-red-400'
        : 'text-slate-300'
      
      return `${base} ${colors}`
    },
    selectContainerClasses() {
      return 'relative'
    },
    sizeClasses() {
      const sizes = {
        sm: 'h-10 px-3 py-2 text-sm',
        md: 'h-12 px-4 py-3 text-base',
        lg: 'h-14 px-4 py-4 text-lg'
      }
      return sizes[this.size]
    },
    paddingClasses() {
      let leftPadding = ''
      const rightPadding = this.size === 'sm' ? 'pr-10' : this.size === 'lg' ? 'pr-12' : 'pr-11'
      
      if (this.prependIcon) {
        leftPadding = this.size === 'sm' ? 'pl-10' : this.size === 'lg' ? 'pl-12' : 'pl-11'
      }
      
      return `${leftPadding} ${rightPadding}`.trim()
    },
    variantClasses() {
      const base = 'w-full appearance-none transition-all duration-200 focus:outline-none cursor-pointer backdrop-blur-sm'
      
      const variants = {
        outlined: this.hasError
          ? 'border border-red-400/60 bg-slate-900/40 focus:border-red-400 focus:ring-2 focus:ring-red-400/20 focus:bg-slate-900/60'
          : 'border border-cyan-500/30 bg-slate-900/40 hover:border-cyan-500/50 focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20 focus:bg-slate-900/60 hover:box-shadow-[0_0_20px_rgba(0,255,255,0.3)]',
        
        filled: this.hasError
          ? 'border-0 border-b-2 border-red-400/60 bg-slate-900/60 focus:border-red-400 focus:bg-slate-900/80'
          : 'border-0 border-b-2 border-cyan-500/30 bg-slate-900/60 hover:bg-slate-900/70 focus:border-cyan-400 focus:bg-slate-900/80 hover:box-shadow-[0_0_15px_rgba(0,255,255,0.2)]',
        
        underlined: this.hasError
          ? 'border-0 border-b-2 border-red-400/60 bg-transparent focus:border-red-400'
          : 'border-0 border-b-2 border-cyan-500/30 bg-transparent hover:border-cyan-500/50 focus:border-cyan-400 hover:box-shadow-[0_2px_10px_rgba(0,255,255,0.2)]'
      }
      
      return `${base} ${variants[this.variant]}`
    },
    borderRadiusClasses() {
      if (this.variant === 'underlined') return ''
      return 'rounded-lg'
    },
    disabledClasses() {
      if (!this.disabled) return ''
      return 'opacity-50 cursor-not-allowed bg-slate-900/20'
    },
    selectClasses() {
      const baseClasses = [
        this.sizeClasses,
        this.paddingClasses,
        this.variantClasses,
        this.borderRadiusClasses,
        this.disabledClasses,
        'text-slate-100'
      ]
      
      if (!this.modelValue || this.modelValue === '') {
        baseClasses.push('text-slate-400')
      }
      
      return baseClasses.filter(Boolean).join(' ')
    },
    prependIconClasses() {
      const baseIcon = this.prependIcon
      const sizeClass = this.size === 'sm' ? 'text-sm' : this.size === 'lg' ? 'text-lg' : 'text-base'
      const colorClass = this.hasError 
        ? 'text-red-400' 
        : 'text-cyan-400'
      
      return `${baseIcon} ${sizeClass} ${colorClass}`
    },
    hintClasses() {
      return 'mt-2 text-sm text-slate-400'
    },
    errorClasses() {
      return 'mt-2 text-sm text-red-400'
    },
    successClasses() {
      return 'mt-2 text-sm text-green-400'
    }
  },
  methods: {
    getItemTitle(item) {
      return item.label || item.title || item.name || item
    },
    getItemValue(item) {
      return item.value !== undefined ? item.value : item
    },
    handleChange(event) {
      const target = event.target
      this.$emit('update:modelValue', target.value)
      this.$emit('change', event)
    },
    handleFocus(event) {
      this.$emit('focus', event)
    },
    handleBlur(event) {
      this.$emit('blur', event)
    },
    focus() {
      this.$refs.selectRef?.focus()
    },
    blur() {
      this.$refs.selectRef?.blur()
    }
  }
}
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

/* Enhanced neon glow effects */
select:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 255, 255, 0.3), 0 0 20px rgba(0, 255, 255, 0.2);
}

select:hover:not(:focus) {
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.15);
}

/* Neon glow for the container */
.relative:hover select {
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
}

/* Enhanced dropdown arrow glow */
.relative:hover .mdi-chevron-down {
  text-shadow: 0 0 8px rgba(0, 255, 255, 0.6);
}
</style>