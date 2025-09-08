<template>
  <BaseModal
    :model-value="modelValue"
    :title="title"
    :width="width"
    :max-width="maxWidth"
    :height="height"
    :max-height="maxHeight"
    :fullscreen="fullscreen"
    :persistent="persistent"
    :scrollable="scrollable"
    :show-close-button="showCloseButton"
    @update:model-value="$emit('update:modelValue', $event)"
    @after-enter="$emit('after-enter')"
    @after-leave="$emit('after-leave')"
    @close="$emit('close')"
  >
    <!-- Header slot -->
    <template v-if="$slots.header" #header>
      <slot name="header" />
    </template>

    <!-- Content -->
    <div :class="contentClasses">
      <!-- Icon -->
      <div
        v-if="icon || type"
        :class="iconContainerClasses"
      >
        <i
          v-if="icon"
          :class="iconClasses"
        />
        <i
          v-else-if="type"
          :class="typeIconClasses"
        />
      </div>

      <!-- Message -->
      <div :class="messageContainerClasses">
        <p
          v-if="message"
          :class="messageClasses"
        >
          {{ message }}
        </p>
        
        <!-- Custom content -->
        <div v-if="$slots.default">
          <slot />
        </div>
      </div>
    </div>

    <!-- Footer with action buttons -->
    <template #footer>
      <div :class="footerClasses">
        <!-- Cancel button -->
        <BaseButton
          v-if="showCancel"
          variant="secondary"
          :size="buttonSize"
          :disabled="loading"
          @click="handleCancel"
        >
          {{ cancelText }}
        </BaseButton>

        <!-- Confirm button -->
        <BaseButton
          :variant="confirmVariant"
          :size="buttonSize"
          :loading="loading"
          @click="handleConfirm"
        >
          {{ confirmText }}
        </BaseButton>
      </div>
    </template>
  </BaseModal>
</template>

<script>
import BaseModal from './BaseModal.vue'
import BaseButton from './BaseButton.vue'

export default {
  name: 'BaseDialog',
  components: {
    BaseModal,
    BaseButton
  },
  props: {
    modelValue: {
      type: Boolean,
      required: true
    },
    title: {
      type: String,
      default: ''
    },
    message: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: 'info',
      validator: (value) => ['info', 'success', 'warning', 'error', 'confirm'].includes(value)
    },
    icon: {
      type: String,
      default: ''
    },
    confirmText: {
      type: String,
      default: 'OK'
    },
    cancelText: {
      type: String,
      default: 'Cancel'
    },
    showCancel: {
      type: Boolean,
      default: true
    },
    loading: {
      type: Boolean,
      default: false
    },
    width: {
      type: [String, Number],
      default: ''
    },
    maxWidth: {
      type: [String, Number],
      default: ''
    },
    height: {
      type: [String, Number],
      default: ''
    },
    maxHeight: {
      type: [String, Number],
      default: ''
    },
    fullscreen: {
      type: Boolean,
      default: false
    },
    persistent: {
      type: Boolean,
      default: false
    },
    scrollable: {
      type: Boolean,
      default: false
    },
    showCloseButton: {
      type: Boolean,
      default: true
    },
    buttonSize: {
      type: String,
      default: 'md',
      validator: (value) => ['sm', 'md', 'lg'].includes(value)
    }
  },
  emits: ['update:modelValue', 'after-enter', 'after-leave', 'close', 'confirm', 'cancel'],
  computed: {
    typeConfig() {
      const configs = {
        info: {
          icon: 'mdi mdi-information',
          iconColor: 'text-cyan-400',
          iconBg: 'bg-cyan-500/20 border border-cyan-500/30',
          confirmVariant: 'primary'
        },
        success: {
          icon: 'mdi mdi-check-circle',
          iconColor: 'text-green-400',
          iconBg: 'bg-green-500/20 border border-green-500/30',
          confirmVariant: 'primary'
        },
        warning: {
          icon: 'mdi mdi-alert',
          iconColor: 'text-yellow-400',
          iconBg: 'bg-yellow-500/20 border border-yellow-500/30',
          confirmVariant: 'primary'
        },
        error: {
          icon: 'mdi mdi-alert-circle',
          iconColor: 'text-red-400',
          iconBg: 'bg-red-500/20 border border-red-500/30',
          confirmVariant: 'danger'
        },
        confirm: {
          icon: 'mdi mdi-help-circle',
          iconColor: 'text-purple-400',
          iconBg: 'bg-purple-500/20 border border-purple-500/30',
          confirmVariant: 'primary'
        }
      }
      
      return configs[this.type]
    },
    contentClasses() {
      const hasIcon = !!(this.icon || this.type)
      return hasIcon ? 'flex gap-4' : ''
    },
    iconContainerClasses() {
      return [
        'flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center backdrop-blur-sm',
        this.typeConfig.iconBg
      ].join(' ')
    },
    iconClasses() {
      return [
        this.icon,
        'text-2xl',
        this.typeConfig.iconColor
      ].join(' ')
    },
    typeIconClasses() {
      return [
        this.typeConfig.icon,
        'text-2xl',
        this.typeConfig.iconColor
      ].join(' ')
    },
    messageContainerClasses() {
      const hasIcon = !!(this.icon || this.type)
      return hasIcon ? 'flex-1 pt-2' : ''
    },
    messageClasses() {
      return 'text-slate-300 leading-relaxed'
    },
    footerClasses() {
      return 'flex justify-end gap-3'
    },
    confirmVariant() {
      return this.typeConfig.confirmVariant
    }
  },
  methods: {
    async handleConfirm() {
      this.$emit('confirm')
      
      // Don't auto-close if loading (let parent handle it)
      if (!this.loading) {
        this.$emit('update:modelValue', false)
      }
    },
    handleCancel() {
      this.$emit('cancel')
      this.$emit('update:modelValue', false)
    }
  }
}
</script>

<style scoped>
/* Enhanced neon glow effects for dialog icons */
.bg-cyan-500\/20 {
  box-shadow: 0 0 20px rgba(34, 211, 238, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.bg-green-500\/20 {
  box-shadow: 0 0 20px rgba(34, 197, 94, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.bg-yellow-500\/20 {
  box-shadow: 0 0 20px rgba(245, 158, 11, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.bg-red-500\/20 {
  box-shadow: 0 0 20px rgba(239, 68, 68, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.bg-purple-500\/20 {
  box-shadow: 0 0 20px rgba(138, 43, 226, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

/* Pulse animation for icons */
.flex-shrink-0 {
  animation: icon-pulse 2s ease-in-out infinite;
}

@keyframes icon-pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}
</style>