<template>
  <span 
    :class="tagClasses"
    @click="handleClick"
  >
    <slot></slot>
    <button 
      v-if="closable" 
      @click.stop="handleClose"
      class="tag-close-btn"
      type="button"
    >
      ×
    </button>
  </span>
</template>

<script>
export default {
  name: 'BaseTag',
  props: {
    type: {
      type: String,
      default: 'default',
      validator: (value) => ['default', 'primary', 'success', 'warning', 'danger', 'info'].includes(value)
    },
    size: {
      type: String,
      default: 'medium',
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    },
    closable: {
      type: Boolean,
      default: false
    },
    round: {
      type: Boolean,
      default: false
    },
    effect: {
      type: String,
      default: 'light',
      validator: (value) => ['light', 'dark', 'plain'].includes(value)
    }
  },
  emits: ['close', 'click'],
  computed: {
    tagClasses() {
      return [
        'base-tag',
        `base-tag--${this.type}`,
        `base-tag--${this.size}`,
        `base-tag--${this.effect}`,
        {
          'base-tag--round': this.round,
          'base-tag--closable': this.closable
        }
      ]
    }
  },
  methods: {
    handleClose() {
      this.$emit('close')
    },
    handleClick() {
      this.$emit('click')
    }
  }
}
</script>

<style scoped>
.base-tag {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  font-weight: 500;
  border-radius: 0.375rem;
  border: 1px solid transparent;
  cursor: default;
  transition: all 0.2s ease;
  gap: 0.25rem;
}

/* Sizes */
.base-tag--small {
  padding: 0.125rem 0.375rem;
  font-size: 0.625rem;
}

.base-tag--medium {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}

.base-tag--large {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}

/* Round */
.base-tag--round {
  border-radius: 9999px;
}

/* Closable */
.base-tag--closable {
  padding-right: 0.25rem;
}

.tag-close-btn {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  padding: 0;
  margin-left: 0.25rem;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.tag-close-btn:hover {
  opacity: 1;
}

/* Light Effect with Neon Glow */
.base-tag--light.base-tag--default {
  background: rgba(148, 163, 184, 0.15);
  color: #94a3b8;
  border-color: rgba(148, 163, 184, 0.3);
  backdrop-filter: blur(8px);
  box-shadow: 0 2px 8px rgba(148, 163, 184, 0.1);
}

.base-tag--light.base-tag--primary {
  background: rgba(0, 255, 255, 0.15);
  color: #00ffff;
  border-color: rgba(0, 255, 255, 0.3);
  backdrop-filter: blur(8px);
  box-shadow: 0 2px 8px rgba(0, 255, 255, 0.2), 0 0 12px rgba(0, 255, 255, 0.1);
}

.base-tag--light.base-tag--success {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
  border-color: rgba(34, 197, 94, 0.3);
  backdrop-filter: blur(8px);
  box-shadow: 0 2px 8px rgba(34, 197, 94, 0.2), 0 0 12px rgba(34, 197, 94, 0.1);
}

.base-tag--light.base-tag--warning {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
  border-color: rgba(245, 158, 11, 0.3);
  backdrop-filter: blur(8px);
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.2), 0 0 12px rgba(245, 158, 11, 0.1);
}

.base-tag--light.base-tag--danger {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.3);
  backdrop-filter: blur(8px);
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2), 0 0 12px rgba(239, 68, 68, 0.1);
}

.base-tag--light.base-tag--info {
  background: rgba(138, 43, 226, 0.15);
  color: #8a2be2;
  border-color: rgba(138, 43, 226, 0.3);
  backdrop-filter: blur(8px);
  box-shadow: 0 2px 8px rgba(138, 43, 226, 0.2), 0 0 12px rgba(138, 43, 226, 0.1);
}

/* Dark Effect with Enhanced Glow */
.base-tag--dark.base-tag--default {
  background: linear-gradient(135deg, #94a3b8, #64748b);
  color: #ffffff;
  border-color: #94a3b8;
  box-shadow: 0 4px 12px rgba(148, 163, 184, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.base-tag--dark.base-tag--primary {
  background: linear-gradient(135deg, #00ffff, #00d4d4);
  color: #0f172a;
  border-color: #00ffff;
  box-shadow: 0 4px 12px rgba(0, 255, 255, 0.4), 0 0 20px rgba(0, 255, 255, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.base-tag--dark.base-tag--success {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: #ffffff;
  border-color: #22c55e;
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.4), 0 0 20px rgba(34, 197, 94, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.base-tag--dark.base-tag--warning {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: #ffffff;
  border-color: #f59e0b;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4), 0 0 20px rgba(245, 158, 11, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.base-tag--dark.base-tag--danger {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: #ffffff;
  border-color: #ef4444;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4), 0 0 20px rgba(239, 68, 68, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.base-tag--dark.base-tag--info {
  background: linear-gradient(135deg, #8a2be2, #7c3aed);
  color: #ffffff;
  border-color: #8a2be2;
  box-shadow: 0 4px 12px rgba(138, 43, 226, 0.4), 0 0 20px rgba(138, 43, 226, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

/* Plain Effect */
.base-tag--plain.base-tag--default {
  background: transparent;
  color: #94a3b8;
  border-color: #94a3b8;
}

.base-tag--plain.base-tag--primary {
  background: transparent;
  color: #00ffff;
  border-color: #00ffff;
}

.base-tag--plain.base-tag--success {
  background: transparent;
  color: #22c55e;
  border-color: #22c55e;
}

.base-tag--plain.base-tag--warning {
  background: transparent;
  color: #f59e0b;
  border-color: #f59e0b;
}

.base-tag--plain.base-tag--danger {
  background: transparent;
  color: #ef4444;
  border-color: #ef4444;
}

.base-tag--plain.base-tag--info {
  background: transparent;
  color: #8a2be2;
  border-color: #8a2be2;
}

/* Enhanced Hover Effects with Stronger Glow */
.base-tag--light:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 255, 255, 0.4), 0 0 30px rgba(0, 255, 255, 0.3);
}

.base-tag--light.base-tag--primary:hover {
  box-shadow: 0 6px 20px rgba(0, 255, 255, 0.5), 0 0 35px rgba(0, 255, 255, 0.4);
}

.base-tag--dark:hover {
  transform: translateY(-2px);
  filter: brightness(1.2);
  box-shadow: 0 6px 20px rgba(0, 255, 255, 0.4), 0 0 30px rgba(0, 255, 255, 0.3);
}

.base-tag--plain:hover {
  background: rgba(0, 255, 255, 0.15);
  box-shadow: 0 4px 12px rgba(0, 255, 255, 0.3), 0 0 20px rgba(0, 255, 255, 0.2);
  transform: translateY(-2px);
}

/* Pulse animation for primary tags */
.base-tag--primary {
  animation: subtle-pulse 2s ease-in-out infinite;
}

@keyframes subtle-pulse {
  0%, 100% {
    box-shadow: 0 4px 12px rgba(0, 255, 255, 0.4), 0 0 20px rgba(0, 255, 255, 0.3);
  }
  50% {
    box-shadow: 0 4px 12px rgba(0, 255, 255, 0.6), 0 0 25px rgba(0, 255, 255, 0.4);
  }
}
</style>