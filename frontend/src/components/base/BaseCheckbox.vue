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
            class="mdi mdi-check text-slate-900"
            :class="iconSizeClasses"
          />
          
          <!-- Indeterminate icon -->
          <i
            v-else-if="indeterminate"
            class="mdi mdi-minus text-slate-900"
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

<script>
export default {
  name: 'BaseCheckbox',
  props: {
    modelValue: {
      type: [Boolean, Array],
      default: false
    },
    value: {
      type: [String, Number, Boolean],
      default: undefined
    },
    label: {
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
    required: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    },
    indeterminate: {
      type: Boolean,
      default: false
    },
    size: {
      type: String,
      default: 'md',
      validator: (value) => ['sm', 'md', 'lg'].includes(value)
    },
    color: {
      type: String,
      default: 'primary',
      validator: (value) => ['primary', 'success', 'warning', 'error'].includes(value)
    }
  },
  emits: ['update:modelValue', 'focus', 'blur', 'change'],
  computed: {
    checkboxId() {
      return `checkbox-${Math.random().toString(36).substring(2, 11)}`
    },
    isChecked() {
      if (Array.isArray(this.modelValue)) {
        return this.value !== undefined && this.modelValue.includes(this.value)
      }
      return Boolean(this.modelValue)
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
      if (this.hint && !this.hasError) ids.push(`${this.checkboxId}-hint`)
      if (this.hasError) ids.push(`${this.checkboxId}-error`)
      return ids.length > 0 ? ids.join(' ') : undefined
    },
    containerClasses() {
      return 'w-full'
    },
    checkboxContainerClasses() {
      return 'relative'
    },
    hiddenCheckboxClasses() {
      return 'sr-only'
    },
    labelClasses() {
      const base = 'flex items-start gap-3 cursor-pointer transition-colors'
      const disabled = this.disabled ? 'opacity-50 cursor-not-allowed' : 'hover:opacity-80'
      
      return `${base} ${disabled}`
    },
    sizeClasses() {
      const sizes = {
        sm: 'h-4 w-4',
        md: 'h-5 w-5',
        lg: 'h-6 w-6'
      }
      return sizes[this.size]
    },
    iconSizeClasses() {
      const sizes = {
        sm: 'text-xs',
        md: 'text-sm',
        lg: 'text-base'
      }
      return sizes[this.size]
    },
    colorClasses() {
      if (this.hasError) {
        return this.isChecked || this.indeterminate
          ? 'bg-red-500 border-red-500 shadow-red-500/50'
          : 'border-red-400/60 bg-slate-900/40'
      }
      
      const colors = {
        primary: this.isChecked || this.indeterminate
          ? 'bg-gradient-to-br from-cyan-400 to-cyan-500 border-cyan-400 shadow-cyan-400/50'
          : 'border-cyan-500/30 bg-slate-900/40',
        success: this.isChecked || this.indeterminate
          ? 'bg-gradient-to-br from-green-400 to-green-500 border-green-400 shadow-green-400/50'
          : 'border-green-500/30 bg-slate-900/40',
        warning: this.isChecked || this.indeterminate
          ? 'bg-gradient-to-br from-yellow-400 to-yellow-500 border-yellow-400 shadow-yellow-400/50'
          : 'border-yellow-500/30 bg-slate-900/40',
        error: this.isChecked || this.indeterminate
          ? 'bg-gradient-to-br from-red-400 to-red-500 border-red-400 shadow-red-400/50'
          : 'border-red-500/30 bg-slate-900/40'
      }
      
      return colors[this.color]
    },
    interactionClasses() {
      if (this.disabled) return ''
      
      const base = 'transition-all duration-200 backdrop-blur-sm'
      const hover = this.hasError
        ? 'hover:border-red-400/80 hover:bg-slate-900/60'
        : 'hover:border-cyan-500/50 hover:bg-slate-900/60'
      const focus = 'focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-offset-slate-900'
      const focusColor = this.hasError
        ? 'focus-within:ring-red-400/30'
        : 'focus-within:ring-cyan-400/30'
      
      return `${base} ${hover} ${focus} ${focusColor}`
    },
    checkboxClasses() {
      const base = 'flex items-center justify-center border-2 rounded-md'
      const glow = this.isChecked || this.indeterminate ? 'shadow-lg' : ''
      
      return [
        base,
        this.sizeClasses,
        this.colorClasses,
        this.interactionClasses,
        glow
      ].filter(Boolean).join(' ')
    },
    labelTextClasses() {
      const base = 'text-sm leading-relaxed select-none'
      const colors = this.hasError
        ? 'text-red-400'
        : 'text-slate-300'
      
      // Adjust top margin based on checkbox size for alignment
      const alignment = this.size === 'sm' ? 'mt-0' : this.size === 'lg' ? 'mt-0.5' : 'mt-0'
      
      return `${base} ${colors} ${alignment}`
    },
    hintClasses() {
      return 'mt-2 text-sm text-slate-400'
    },
    errorClasses() {
      return 'mt-2 text-sm text-red-400'
    }
  },
  methods: {
    handleChange(event) {
      const target = event.target
      
      if (Array.isArray(this.modelValue)) {
        // Handle array of values (multiple checkboxes)
        const newValue = [...this.modelValue]
        if (target.checked) {
          if (this.value !== undefined && !newValue.includes(this.value)) {
            newValue.push(this.value)
          }
        } else {
          const index = newValue.indexOf(this.value)
          if (index > -1) {
            newValue.splice(index, 1)
          }
        }
        this.$emit('update:modelValue', newValue)
      } else {
        // Handle boolean value (single checkbox)
        this.$emit('update:modelValue', target.checked)
      }
      
      this.$emit('change', event)
    },
    handleFocus(event) {
      this.$emit('focus', event)
    },
    handleBlur(event) {
      this.$emit('blur', event)
    },
    focus() {
      this.$refs.checkboxRef?.focus()
    },
    blur() {
      this.$refs.checkboxRef?.blur()
    }
  }
}
</script>

<style scoped>
/* Enhanced neon glow effects */
.shadow-cyan-400\/50 {
  box-shadow: 0 0 20px rgba(34, 211, 238, 0.5), 0 4px 12px rgba(34, 211, 238, 0.3);
}

.shadow-green-400\/50 {
  box-shadow: 0 0 20px rgba(34, 197, 94, 0.5), 0 4px 12px rgba(34, 197, 94, 0.3);
}

.shadow-yellow-400\/50 {
  box-shadow: 0 0 20px rgba(245, 158, 11, 0.5), 0 4px 12px rgba(245, 158, 11, 0.3);
}

.shadow-red-400\/50 {
  box-shadow: 0 0 20px rgba(239, 68, 68, 0.5), 0 4px 12px rgba(239, 68, 68, 0.3);
}

/* Pulse animation for checked state */
input:checked + label > div {
  animation: checkbox-pulse 2s ease-in-out infinite;
}

@keyframes checkbox-pulse {
  0%, 100% {
    box-shadow: 0 0 20px rgba(34, 211, 238, 0.5), 0 4px 12px rgba(34, 211, 238, 0.3);
  }
  50% {
    box-shadow: 0 0 25px rgba(34, 211, 238, 0.7), 0 4px 15px rgba(34, 211, 238, 0.4);
  }
}

/* Screen reader only class */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>