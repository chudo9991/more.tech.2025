<template>
  <component
    :is="tag"
    :to="to"
    :href="href"
    :type="type"
    :disabled="disabled"
    :class="buttonClasses"
    @click="handleClick"
  >
    <span v-if="loading" class="button-loading">
      <svg class="loading-spinner" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none" stroke-dasharray="31.416" stroke-dashoffset="31.416">
          <animate attributeName="stroke-dasharray" dur="2s" values="0 31.416;15.708 15.708;0 31.416" repeatCount="indefinite"/>
          <animate attributeName="stroke-dashoffset" dur="2s" values="0;-15.708;-31.416" repeatCount="indefinite"/>
        </circle>
      </svg>
    </span>
    <span v-if="icon && iconPosition === 'left'" class="button-icon button-icon-left">
      <component :is="icon" />
    </span>
    <span class="button-text">
      <slot />
    </span>
    <span v-if="icon && iconPosition === 'right'" class="button-icon button-icon-right">
      <component :is="icon" />
    </span>
  </component>
</template>

<script setup>
import { computed, useSlots } from 'vue'

const props = defineProps({
  // Тип кнопки
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'ghost', 'danger'].includes(value)
  },
  
  // Размер кнопки
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  
  // HTML тег или компонент
  tag: {
    type: String,
    default: 'button'
  },
  
  // Для router-link
  to: {
    type: [String, Object],
    default: null
  },
  
  // Для обычных ссылок
  href: {
    type: String,
    default: null
  },
  
  // Тип кнопки (для form)
  type: {
    type: String,
    default: 'button'
  },
  
  // Состояние загрузки
  loading: {
    type: Boolean,
    default: false
  },
  
  // Отключена ли кнопка
  disabled: {
    type: Boolean,
    default: false
  },
  
  // Иконка
  icon: {
    type: [String, Object],
    default: null
  },
  
  // Позиция иконки
  iconPosition: {
    type: String,
    default: 'left',
    validator: (value) => ['left', 'right'].includes(value)
  },
  
  // Полная ширина
  fullWidth: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])
const slots = useSlots()

// Вычисляемые свойства
const buttonClasses = computed(() => [
  'base-button',
  `base-button--${props.variant}`,
  `base-button--${props.size}`,
  {
    'base-button--loading': props.loading,
    'base-button--disabled': props.disabled,
    'base-button--full-width': props.fullWidth,
    'base-button--icon-only': !slots.default && props.icon
  }
])

// Методы
const handleClick = (event) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<style scoped>
.base-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(20px);
  font-family: inherit;
  white-space: nowrap;
}

.base-button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.3);
}

.base-button--disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

.base-button--loading {
  cursor: wait;
}

.base-button--full-width {
  width: 100%;
}

/* Размеры */
.base-button--small {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  min-height: 2rem;
}

.base-button--medium {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  min-height: 2.5rem;
}

.base-button--large {
  padding: 1rem 2rem;
  font-size: 1.125rem;
  min-height: 3rem;
}

/* Primary кнопка - как в примере с изображения */
.base-button--primary {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(138, 43, 226, 0.2));
  border: 1px solid rgba(0, 255, 255, 0.5);
  color: #00ffff;
  box-shadow: 0 8px 32px rgba(0, 255, 255, 0.3);
}

.base-button--primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.4), transparent);
  transition: left 0.6s ease;
}

.base-button--primary:hover {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.35), rgba(138, 43, 226, 0.35));
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 255, 255, 0.5);
  text-shadow: 0 0 15px rgba(0, 255, 255, 1);
}

.base-button--primary:hover::before {
  left: 100%;
}

.base-button--primary:active {
  transform: translateY(0);
}

/* Secondary кнопка - фиолетовая как в примере */
.base-button--secondary {
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid rgba(138, 43, 226, 0.5);
  color: #8a2be2;
  box-shadow: 0 8px 32px rgba(138, 43, 226, 0.2);
}

.base-button--secondary:hover {
  background: rgba(138, 43, 226, 0.2);
  border-color: rgba(138, 43, 226, 0.7);
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(138, 43, 226, 0.4);
  text-shadow: 0 0 15px rgba(138, 43, 226, 1);
}

.base-button--secondary:active {
  transform: translateY(0);
}

/* Ghost кнопка */
.base-button--ghost {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(0, 255, 255, 0.3);
  color: #00ffff;
  box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
}

.base-button--ghost:hover {
  background: rgba(0, 255, 255, 0.1);
  border-color: rgba(0, 255, 255, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 255, 255, 0.3);
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.8);
}

.base-button--ghost:active {
  transform: translateY(0);
}

/* Danger кнопка */
.base-button--danger {
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid rgba(239, 68, 68, 0.5);
  color: #ef4444;
  box-shadow: 0 8px 32px rgba(239, 68, 68, 0.2);
}

.base-button--danger:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.7);
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(239, 68, 68, 0.4);
  text-shadow: 0 0 15px rgba(239, 68, 68, 1);
}

.base-button--danger:active {
  transform: translateY(0);
}

/* Элементы кнопки */
.button-text {
  position: relative;
  z-index: 1;
}

.button-icon {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.button-icon svg {
  width: 1em;
  height: 1em;
}

.button-loading {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-spinner {
  width: 1em;
  height: 1em;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Кнопка только с иконкой */
.base-button--icon-only {
  aspect-ratio: 1;
  padding: 0.75rem;
}

.base-button--icon-only.base-button--small {
  padding: 0.5rem;
}

.base-button--icon-only.base-button--large {
  padding: 1rem;
}

/* Адаптивность */
@media (max-width: 640px) {
  .base-button--large {
    padding: 0.875rem 1.75rem;
    font-size: 1rem;
  }
  
  .base-button--medium {
    padding: 0.625rem 1.25rem;
    font-size: 0.875rem;
  }
}

/* Поддержка уменьшенной анимации */
@media (prefers-reduced-motion: reduce) {
  .base-button {
    transition: none;
  }
  
  .base-button::before {
    transition: none;
  }
  
  .loading-spinner {
    animation: none;
  }
}
</style>