<template>
  <div class="keywords-section">
    <!-- Header with title and extract button -->
    <div class="keywords-header">
      <h4 class="keywords-title">{{ sectionTitle }}</h4>
      <el-button
        type="primary"
        size="small"
        :loading="isExtracting"
        @click="extractKeywords"
        :disabled="!hasText"
      >
        <el-icon><Star /></el-icon>
        Ключевые слова
      </el-button>
    </div>

    <!-- Keywords display -->
    <div v-if="keywords.length > 0" class="keywords-content">
      <!-- Confidence indicator -->
      <div class="confidence-indicator">
        <span class="confidence-label">Уверенность:</span>
        <el-progress
          :percentage="confidencePercentage"
          :color="confidenceColor"
          :stroke-width="8"
          :show-text="false"
        />
        <span class="confidence-value">{{ (confidenceScore * 100).toFixed(0) }}%</span>
      </div>

      <!-- Keywords tags -->
      <div class="keywords-tags">
        <el-tag
          v-for="keyword in keywords"
          :key="keyword"
          class="keyword-tag"
          closable
          @close="removeKeyword(keyword)"
          :title="`Нажмите для удаления: ${keyword}`"
        >
          {{ keyword }}
        </el-tag>
        <div v-if="keywords.length === 0" class="no-keywords">
          <el-icon><InfoFilled /></el-icon>
          <span>Нет ключевых слов</span>
        </div>
      </div>

      <!-- Action buttons -->
      <div class="keywords-actions">
        <el-button
          type="primary"
          size="small"
          @click="openEditor"
        >
          <el-icon><Edit /></el-icon>
          Редактировать
        </el-button>
        <el-button
          type="warning"
          size="small"
          @click="extractKeywords"
          :loading="isExtracting"
        >
          <el-icon><Refresh /></el-icon>
          Переизвлечь
        </el-button>
        <el-button
          type="danger"
          size="small"
          @click="clearKeywords"
        >
          <el-icon><Delete /></el-icon>
          Очистить
        </el-button>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else-if="!isExtracting" class="keywords-empty">
      <el-empty
        description="Ключевые слова не извлечены"
        :image-size="60"
      >
        <el-button
          type="primary"
          size="small"
          @click="extractKeywords"
          :disabled="!hasText"
        >
          Извлечь ключевые слова
        </el-button>
      </el-empty>
    </div>

    <!-- Loading state -->
    <div v-else class="keywords-loading">
      <el-skeleton :rows="3" animated />
    </div>

    <!-- Keywords Editor Modal -->
    <KeywordsEditor
      v-model:visible="editorVisible"
      :keywords="keywords"
      :section-type="sectionType"
      :section-title="sectionTitle"
      @save="saveKeywords"
      @cancel="closeEditor"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Star, Edit, Refresh, Delete, InfoFilled } from '@element-plus/icons-vue'
import KeywordsEditor from './KeywordsEditor.vue'
import { useHRStore } from '@/stores/hr'

// Props
const props = defineProps({
  vacancyId: {
    type: String,
    required: false,
    default: null
  },
  sectionType: {
    type: String,
    required: true
  },
  sectionTitle: {
    type: String,
    required: true
  },
  sectionText: {
    type: String,
    default: ''
  }
})

// Emits
const emit = defineEmits(['keywords-updated'])

// Store
const hrStore = useHRStore()

// Reactive data
const keywords = ref([])
const confidenceScore = ref(0.0)
const isExtracting = ref(false)
const editorVisible = ref(false)

// Computed
const hasText = computed(() => {
  return props.sectionText && props.sectionText.trim().length > 0
})

const confidencePercentage = computed(() => {
  return Math.round(confidenceScore.value * 100)
})

const confidenceColor = computed(() => {
  const score = confidenceScore.value
  if (score >= 0.8) return '#67C23A' // Green
  if (score >= 0.6) return '#E6A23C' // Orange
  if (score >= 0.4) return '#F56C6C' // Red
  return '#909399' // Gray
})

// Methods
const extractKeywords = async () => {
  if (!props.vacancyId) {
    ElMessage.warning('ID вакансии не найден')
    return
  }

  if (!hasText.value) {
    ElMessage.warning('Нет текста для извлечения ключевых слов')
    return
  }

  try {
    isExtracting.value = true
    
    const response = await hrStore.extractSectionKeywords(
      props.vacancyId,
      props.sectionType,
      true // force reload
    )

    if (response.success) {
      keywords.value = response.keywords
      confidenceScore.value = response.confidence_score
      ElMessage.success(`Извлечено ${response.keywords.length} ключевых слов`)
      emit('keywords-updated', {
        sectionType: props.sectionType,
        keywords: response.keywords,
        confidenceScore: response.confidence_score
      })
    } else {
      ElMessage.error(response.error || 'Ошибка при извлечении ключевых слов')
    }
  } catch (error) {
    console.error('Error extracting keywords:', error)
    ElMessage.error('Ошибка при извлечении ключевых слов')
  } finally {
    isExtracting.value = false
  }
}

const openEditor = () => {
  editorVisible.value = true
}

const closeEditor = () => {
  editorVisible.value = false
}

const saveKeywords = async (newKeywords) => {
  try {
    const response = await hrStore.updateSectionKeywords(
      props.vacancyId,
      props.sectionType,
      newKeywords,
      confidenceScore.value
    )

    if (response) {
      keywords.value = newKeywords
      ElMessage.success('Ключевые слова обновлены')
      emit('keywords-updated', {
        sectionType: props.sectionType,
        keywords: newKeywords,
        confidenceScore: confidenceScore.value
      })
    } else {
      ElMessage.error('Ошибка при обновлении ключевых слов')
    }
  } catch (error) {
    console.error('Error updating keywords:', error)
    ElMessage.error('Ошибка при обновлении ключевых слов')
  } finally {
    closeEditor()
  }
}

const removeKeyword = (keyword) => {
  const index = keywords.value.indexOf(keyword)
  if (index > -1) {
    keywords.value.splice(index, 1)
    emit('keywords-updated', {
      sectionType: props.sectionType,
      keywords: keywords.value,
      confidenceScore: confidenceScore.value
    })
  }
}

const clearKeywords = async () => {
  try {
    await ElMessageBox.confirm(
      'Вы уверены, что хотите очистить все ключевые слова?',
      'Подтверждение',
      {
        confirmButtonText: 'Очистить',
        cancelButtonText: 'Отмена',
        type: 'warning'
      }
    )

    const response = await hrStore.deleteSectionKeywords(
      props.vacancyId,
      props.sectionType
    )

    if (response) {
      keywords.value = []
      confidenceScore.value = 0.0
      ElMessage.success('Ключевые слова очищены')
      emit('keywords-updated', {
        sectionType: props.sectionType,
        keywords: [],
        confidenceScore: 0.0
      })
    } else {
      ElMessage.error('Ошибка при очистке ключевых слов')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Error clearing keywords:', error)
      ElMessage.error('Ошибка при очистке ключевых слов')
    }
  }
}

// Load existing keywords on mount
const loadKeywords = async () => {
  if (!props.vacancyId) {
    return
  }

  try {
    const response = await hrStore.getSectionKeywords(
      props.vacancyId,
      props.sectionType
    )

    if (response) {
      keywords.value = response.keywords || []
      confidenceScore.value = response.confidence_score || 0.0
    }
  } catch (error) {
    console.error('Error loading keywords:', error)
  }
}

// Watch for changes in section text
watch(() => props.sectionText, (newText) => {
  if (newText && newText.trim().length > 0 && keywords.value.length === 0) {
    // Auto-extract keywords when text is added and no keywords exist
    // extractKeywords()
  }
}, { immediate: true })

// Load keywords on mount
loadKeywords()
</script>

<style scoped>
.keywords-section {
  margin-bottom: 20px;
  padding: 0;
  border: 1px solid #e4e7ed;
  border-radius: 12px;
  background-color: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  transition: all 0.3s ease;
}

.keywords-section:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.keywords-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin-bottom: 0;
}

.keywords-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.keywords-content {
  padding: 20px;
  background-color: #ffffff;
}

.confidence-indicator {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 10px;
  border: 1px solid #e9ecef;
}

.confidence-label {
  font-size: 12px;
  color: #606266;
  white-space: nowrap;
}

.confidence-value {
  font-size: 12px;
  font-weight: 600;
  color: #303133;
  min-width: 40px;
  text-align: right;
}

.keywords-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 16px;
  min-height: 40px;
  align-items: center;
}

.no-keywords {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
  font-size: 14px;
  font-style: italic;
  padding: 8px 12px;
  background-color: #f5f7fa;
  border-radius: 6px;
  border: 1px dashed #d9d9d9;
}

.keyword-tag {
  margin: 0;
  font-size: 13px;
  font-weight: 500;
  border-radius: 20px;
  padding: 6px 12px;
  transition: all 0.2s ease;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.keyword-tag:hover {
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

/* Animation for keywords appearing */
.keyword-tag {
  animation: fadeInUp 0.3s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Stagger animation for multiple keywords */
.keywords-tags .keyword-tag:nth-child(1) { animation-delay: 0.1s; }
.keywords-tags .keyword-tag:nth-child(2) { animation-delay: 0.2s; }
.keywords-tags .keyword-tag:nth-child(3) { animation-delay: 0.3s; }
.keywords-tags .keyword-tag:nth-child(4) { animation-delay: 0.4s; }
.keywords-tags .keyword-tag:nth-child(5) { animation-delay: 0.5s; }

.keywords-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.keywords-empty {
  padding: 40px 20px;
  text-align: center;
  background-color: #ffffff;
}

.keywords-loading {
  margin-top: 12px;
}

/* Responsive design */
@media (max-width: 768px) {
  .keywords-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    padding: 16px;
  }

  .keywords-title {
    font-size: 14px;
  }

  .keywords-content {
    padding: 16px;
  }

  .keywords-actions {
    flex-direction: column;
    gap: 8px;
  }

  .confidence-indicator {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    padding: 12px;
  }

  .keywords-tags {
    gap: 8px;
  }

  .keyword-tag {
    font-size: 12px;
    padding: 4px 10px;
  }
}

@media (max-width: 480px) {
  .keywords-section {
    margin-bottom: 16px;
    border-radius: 8px;
  }

  .keywords-header {
    padding: 12px;
  }

  .keywords-content {
    padding: 12px;
  }

  .confidence-indicator {
    padding: 10px;
  }

  .keywords-actions {
    gap: 6px;
  }
}
</style>
