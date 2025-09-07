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

<script setup lang="ts">
import { computed } from 'vue'
import BaseModal from './BaseModal.vue'
import BaseButton from './BaseButton.vue'

export interface BaseDialogProps {
  modelValue: boolean
  title?: string
  message?: string
  type?: 'info' | 'success' | 'warning' | 'error' | 'confirm'
  icon?: string
  confirmText?: string
  cancelText?: string
  showCancel?: boolean
  loading?: boolean
  width?: string | number
  maxWidth?: string | number
  height?: string | number
  maxHeight?: string | number
  fullscreen?: boolean
  persistent?: boolean
  scrollable?: boolean
  showCloseButton?: boolean
  buttonSize?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<BaseDialogProps>(), {
  type: 'info',
  confirmText: 'OK',
  cancelText: 'Cancel',
  showCancel: true,
  loading: false,
  persistent: false,
  scrollable: false,
  showCloseButton: true,
  buttonSize: 'md'
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'after-enter': []
  'after-leave': []
  'close': []
  'confirm': []
  'cancel': []
}>()

// Type-based styling
const typeConfig = computed(() => {
  const configs: Record<typeof props.type, {
    icon: string
    iconColor: string
    iconBg: string
    confirmVariant: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
  }> = {
    info: {
      icon: 'mdi mdi-information',
      iconColor: 'text-info-500',
      iconBg: 'bg-info-100 dark:bg-info-900/20',
      confirmVariant: 'primary' as const
    },
    success: {
      icon: 'mdi mdi-check-circle',
      iconColor: 'text-success-500',
      iconBg: 'bg-success-100 dark:bg-success-900/20',
      confirmVariant: 'primary' as const
    },
    warning: {
      icon: 'mdi mdi-alert',
      iconColor: 'text-warning-500',
      iconBg: 'bg-warning-100 dark:bg-warning-900/20',
      confirmVariant: 'primary' as const
    },
    error: {
      icon: 'mdi mdi-alert-circle',
      iconColor: 'text-error-500',
      iconBg: 'bg-error-100 dark:bg-error-900/20',
      confirmVariant: 'danger' as const
    },
    confirm: {
      icon: 'mdi mdi-help-circle',
      iconColor: 'text-primary-500',
      iconBg: 'bg-primary-100 dark:bg-primary-900/20',
      confirmVariant: 'primary' as const
    }
  }
  
  return configs[props.type]
})

// Computed classes
const contentClasses = computed(() => {
  const hasIcon = !!(props.icon || props.type)
  return hasIcon ? 'flex gap-4' : ''
})

const iconContainerClasses = computed(() => {
  return [
    'flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center',
    typeConfig.value.iconBg
  ].join(' ')
})

const iconClasses = computed(() => {
  return [
    props.icon,
    'text-2xl',
    typeConfig.value.iconColor
  ].join(' ')
})

const typeIconClasses = computed(() => {
  return [
    typeConfig.value.icon,
    'text-2xl',
    typeConfig.value.iconColor
  ].join(' ')
})

const messageContainerClasses = computed(() => {
  const hasIcon = !!(props.icon || props.type)
  return hasIcon ? 'flex-1 pt-2' : ''
})

const messageClasses = 'text-neutral-700 dark:text-neutral-300 leading-relaxed'

const footerClasses = 'flex justify-end gap-3'

const confirmVariant = computed(() => {
  return typeConfig.value.confirmVariant
})

// Event handlers
const handleConfirm = async () => {
  emit('confirm')
  
  // Don't auto-close if loading (let parent handle it)
  if (!props.loading) {
    emit('update:modelValue', false)
  }
}

const handleCancel = () => {
  emit('cancel')
  emit('update:modelValue', false)
}
</script>