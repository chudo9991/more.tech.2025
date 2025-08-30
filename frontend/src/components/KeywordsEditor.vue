<template>
  <el-dialog
    v-model="dialogVisible"
    :title="`Редактирование ключевых слов - ${sectionTitle}`"
    width="600px"
    :before-close="handleClose"
  >
    <div class="keywords-editor">
      <!-- Add new keyword -->
      <div class="add-keyword-section">
        <el-input
          v-model="newKeyword"
          placeholder="Введите новое ключевое слово"
          @keyup.enter="addKeyword"
          clearable
        >
          <template #append>
            <el-button @click="addKeyword" :disabled="!newKeyword.trim()">
              <el-icon><Plus /></el-icon>
            </el-button>
          </template>
        </el-input>
      </div>

      <!-- Keywords list -->
      <div class="keywords-list">
        <h4>Ключевые слова ({{ keywords.length }})</h4>
        
        <div v-if="keywords.length === 0" class="empty-keywords">
          <el-empty description="Нет ключевых слов" :image-size="60" />
        </div>
        
        <div v-else class="keywords-grid">
          <div
            v-for="(keyword, index) in keywords"
            :key="index"
            class="keyword-item"
          >
            <el-tag
              :closable="true"
              @close="removeKeyword(index)"
              class="keyword-tag"
            >
              {{ keyword }}
            </el-tag>
          </div>
        </div>
      </div>

      <!-- Bulk operations -->
      <div v-if="keywords.length > 0" class="bulk-operations">
        <el-button
          type="danger"
          size="small"
          @click="clearAllKeywords"
        >
          <el-icon><Delete /></el-icon>
          Очистить все
        </el-button>
        
        <el-button
          type="warning"
          size="small"
          @click="sortKeywords"
        >
          <el-icon><Sort /></el-icon>
          Сортировать
        </el-button>
      </div>

      <!-- Validation messages -->
      <div v-if="validationErrors.length > 0" class="validation-errors">
        <el-alert
          v-for="error in validationErrors"
          :key="error"
          :title="error"
          type="error"
          :closable="false"
          show-icon
        />
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">Отмена</el-button>
        <el-button
          type="primary"
          @click="handleSave"
          :loading="isSaving"
          :disabled="!isValid"
        >
          Сохранить
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Delete, Sort } from '@element-plus/icons-vue'

// Props
const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  keywords: {
    type: Array,
    default: () => []
  },
  sectionType: {
    type: String,
    required: true
  },
  sectionTitle: {
    type: String,
    required: true
  }
})

// Emits
const emit = defineEmits(['update:visible', 'save', 'cancel'])

// Reactive data
const newKeyword = ref('')
const localKeywords = ref([])
const isSaving = ref(false)
const validationErrors = ref([])

// Computed
const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

const isValid = computed(() => {
  return localKeywords.value.length > 0 && validationErrors.value.length === 0
})

// Methods
const addKeyword = () => {
  const keyword = newKeyword.value.trim()
  
  if (!keyword) {
    ElMessage.warning('Введите ключевое слово')
    return
  }

  if (localKeywords.value.includes(keyword)) {
    ElMessage.warning('Это ключевое слово уже существует')
    return
  }

  if (keyword.length > 50) {
    ElMessage.warning('Ключевое слово слишком длинное (максимум 50 символов)')
    return
  }

  localKeywords.value.push(keyword)
  newKeyword.value = ''
  validateKeywords()
}

const removeKeyword = (index) => {
  localKeywords.value.splice(index, 1)
  validateKeywords()
}

const clearAllKeywords = () => {
  localKeywords.value = []
  validateKeywords()
}

const sortKeywords = () => {
  localKeywords.value.sort((a, b) => a.localeCompare(b, 'ru'))
}

const validateKeywords = () => {
  validationErrors.value = []

  if (localKeywords.value.length === 0) {
    validationErrors.value.push('Должно быть хотя бы одно ключевое слово')
  }

  if (localKeywords.value.length > 20) {
    validationErrors.value.push('Слишком много ключевых слов (максимум 20)')
  }

  // Check for duplicates
  const duplicates = localKeywords.value.filter((item, index) => 
    localKeywords.value.indexOf(item) !== index
  )
  
  if (duplicates.length > 0) {
    validationErrors.value.push('Обнаружены дублирующиеся ключевые слова')
  }

  // Check for empty keywords
  const emptyKeywords = localKeywords.value.filter(keyword => !keyword.trim())
  if (emptyKeywords.length > 0) {
    validationErrors.value.push('Обнаружены пустые ключевые слова')
  }
}

const handleSave = async () => {
  if (!isValid.value) {
    ElMessage.error('Исправьте ошибки перед сохранением')
    return
  }

  try {
    isSaving.value = true
    emit('save', [...localKeywords.value])
  } catch (error) {
    console.error('Error saving keywords:', error)
    ElMessage.error('Ошибка при сохранении')
  } finally {
    isSaving.value = false
  }
}

const handleClose = () => {
  emit('cancel')
  emit('update:visible', false)
}

// Watch for changes in props
watch(() => props.keywords, (newKeywords) => {
  localKeywords.value = [...newKeywords]
  validateKeywords()
}, { immediate: true })

watch(() => props.visible, (visible) => {
  if (visible) {
    localKeywords.value = [...props.keywords]
    newKeyword.value = ''
    validateKeywords()
  }
})
</script>

<style scoped>
.keywords-editor {
  max-height: 600px;
  overflow-y: auto;
  padding: 20px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 12px;
}

.add-keyword-section {
  margin-bottom: 24px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.add-keyword-section .el-input {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
}

.add-keyword-section .el-input__inner {
  background-color: transparent;
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
}

.add-keyword-section .el-input__inner::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.keywords-list {
  margin-bottom: 20px;
}

.keywords-list h4 {
  margin: 0 0 16px 0;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  text-align: center;
  padding: 16px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 10px;
  border: 1px solid #e9ecef;
}

.empty-keywords {
  padding: 20px 0;
}

.keywords-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  max-height: 250px;
  overflow-y: auto;
  padding: 20px;
  border: 2px dashed #e4e7ed;
  border-radius: 12px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  transition: all 0.3s ease;
}

.keywords-grid:hover {
  border-color: #667eea;
  background: linear-gradient(135deg, #f0f4ff 0%, #ffffff 100%);
}

.keyword-item {
  display: flex;
  align-items: center;
}

.keyword-tag {
  margin: 0;
  font-size: 13px;
  font-weight: 500;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  border-radius: 20px;
  padding: 8px 16px;
  transition: all 0.2s ease;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(102, 126, 234, 0.2);
}

.keyword-tag:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.bulk-operations {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.validation-errors {
  margin-top: 16px;
}

.validation-errors .el-alert {
  margin-bottom: 8px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* Responsive design */
@media (max-width: 768px) {
  .keywords-grid {
    max-height: 150px;
  }

  .bulk-operations {
    flex-direction: column;
  }

  .dialog-footer {
    flex-direction: column;
  }
}
</style>
