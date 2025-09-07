<template>
  <div class="rich-text-editor" :class="{ error: hasError }">
    <div class="editor-content">
      <textarea
        ref="editorRef"
        :value="modelValue"
        :placeholder="placeholder"
        :style="{ minHeight: `${minHeight}px` }"
        class="editor-textarea"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface RichTextEditorProps {
  modelValue: string
  placeholder?: string
  minHeight?: number
  error?: string
}

const props = withDefaults(defineProps<RichTextEditorProps>(), {
  placeholder: 'Введите текст...',
  minHeight: 120,
  error: ''
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  focus: [event: FocusEvent]
  blur: [event: FocusEvent]
}>()

const editorRef = ref<HTMLTextAreaElement>()

const hasError = computed(() => !!props.error)

// Event handlers
const handleInput = (event: Event) => {
  const target = event.target as HTMLTextAreaElement
  emit('update:modelValue', target.value)
}

const handleFocus = (event: FocusEvent) => {
  emit('focus', event)
}

const handleBlur = (event: FocusEvent) => {
  emit('blur', event)
}
</script>

<style scoped>
.rich-text-editor {
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  overflow: hidden;
  background: white;
}

.rich-text-editor.error {
  border-color: #ef4444;
}

.editor-content {
  position: relative;
}

.editor-textarea {
  width: 100%;
  border: none;
  outline: none;
  resize: vertical;
  padding: 1rem;
  font-family: inherit;
  font-size: 0.875rem;
  line-height: 1.6;
  color: #374151;
  background: transparent;
}

.editor-textarea::placeholder {
  color: #9ca3af;
}

.editor-textarea:focus {
  outline: none;
}
</style>