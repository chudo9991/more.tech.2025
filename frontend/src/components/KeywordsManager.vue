<template>
  <div class="keywords-manager">
    <!-- Header with actions -->
    <div class="manager-header">
      <div class="header-left">
        <h3>Управление ключевыми словами</h3>
        <p class="header-subtitle">Извлечение и управление ключевыми словами по разделам вакансии</p>
      </div>
      <div class="header-actions">
        <el-button
          type="primary"
          :loading="isExtractingAll"
          @click="extractAllKeywords"
        >
          <el-icon><Star /></el-icon>
          Извлечь все
        </el-button>
        <el-button
          type="warning"
          @click="refreshAllKeywords"
          :loading="isRefreshing"
        >
          <el-icon><Refresh /></el-icon>
          Обновить
        </el-button>
        <el-button
          type="info"
          @click="showStats"
        >
          <el-icon><DataAnalysis /></el-icon>
          Статистика
        </el-button>
        <el-button
          type="danger"
          @click="clearAllKeywords"
        >
          <el-icon><Delete /></el-icon>
          Очистить все
        </el-button>
      </div>
    </div>

    <!-- Statistics summary -->
    <div v-if="stats" class="stats-summary">
      <el-row :gutter="16">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon><Document /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.total_sections }}</div>
                <div class="stat-label">Разделов</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon><Collection /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.total_keywords }}</div>
                <div class="stat-label">Ключевых слов</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon><TrendCharts /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ (stats.average_confidence * 100).toFixed(0) }}%</div>
                <div class="stat-label">Средняя уверенность</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon><Clock /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.last_extraction_time }}с</div>
                <div class="stat-label">Время извлечения</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- Keywords sections grid -->
    <div class="keywords-grid">
      <el-row :gutter="20">
        <el-col 
          v-for="section in sections" 
          :key="section.type"
          :xs="24" 
          :sm="12" 
          :md="8" 
          :lg="6"
        >
          <KeywordsSection
            :vacancy-id="vacancyId"
            :section-type="section.type"
            :section-title="section.title"
            :section-text="section.text"
            @keywords-updated="handleSectionUpdated"
          />
        </el-col>
      </el-row>
    </div>

    <!-- Empty state -->
    <div v-if="!hasAnyKeywords && !isLoading" class="empty-state">
      <el-empty
        description="Ключевые слова не извлечены"
        :image-size="120"
      >
        <template #description>
          <p>Для начала работы с ключевыми словами нажмите "Извлечь все"</p>
        </template>
        <el-button
          type="primary"
          size="large"
          @click="extractAllKeywords"
        >
          <el-icon><Star /></el-icon>
          Извлечь ключевые слова
        </el-button>
      </el-empty>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="loading-state">
      <el-skeleton :rows="6" animated />
    </div>

    <!-- Statistics Modal -->
    <el-dialog
      v-model="statsVisible"
      title="Статистика ключевых слов"
      width="600px"
    >
      <div v-if="stats" class="stats-details">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="Всего разделов">
            {{ stats.total_sections }}
          </el-descriptions-item>
          <el-descriptions-item label="Всего ключевых слов">
            {{ stats.total_keywords }}
          </el-descriptions-item>
          <el-descriptions-item label="Средняя уверенность">
            {{ (stats.average_confidence * 100).toFixed(1) }}%
          </el-descriptions-item>
          <el-descriptions-item label="Время извлечения">
            {{ stats.last_extraction_time }}с
          </el-descriptions-item>
        </el-descriptions>

        <div class="section-stats">
          <h4>По разделам:</h4>
          <el-table :data="stats.section_stats" stripe>
            <el-table-column prop="section_type" label="Раздел" />
            <el-table-column prop="keywords_count" label="Ключевых слов" width="120" />
            <el-table-column prop="confidence_score" label="Уверенность" width="120">
              <template #default="{ row }">
                <el-progress
                  :percentage="row.confidence_score"
                  :color="getConfidenceColor(row.confidence_score)"
                  :stroke-width="8"
                  :show-text="false"
                />
                <span class="confidence-text">{{ row.confidence_score.toFixed(0) }}%</span>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Star, Refresh, DataAnalysis, Delete, Document, 
  Collection, TrendCharts, Clock 
} from '@element-plus/icons-vue'
import KeywordsSection from './KeywordsSection.vue'
import { useHRStore } from '@/stores/hr'

// Props
const props = defineProps({
  vacancyId: {
    type: String,
    required: true
  },
  vacancyData: {
    type: Object,
    default: () => ({})
  }
})

// Emits
const emit = defineEmits(['keywords-updated'])

// Store
const hrStore = useHRStore()

// Reactive data
const stats = ref(null)
const statsVisible = ref(false)
const isExtractingAll = ref(false)
const isRefreshing = ref(false)
const isLoading = ref(false)

// Computed
const sections = computed(() => [
  {
    type: 'responsibilities',
    title: 'Обязанности',
    text: props.vacancyData.responsibilities || ''
  },
  {
    type: 'requirements',
    title: 'Требования',
    text: props.vacancyData.requirements || ''
  },
  {
    type: 'programs',
    title: 'Специальные программы',
    text: props.vacancyData.special_programs || ''
  },
  {
    type: 'skills',
    title: 'Компьютерные навыки',
    text: props.vacancyData.computer_skills || ''
  },
  {
    type: 'languages',
    title: 'Иностранные языки',
    text: props.vacancyData.foreign_languages || ''
  },
  {
    type: 'description',
    title: 'Описание вакансии',
    text: props.vacancyData.description || ''
  },
  {
    type: 'additional',
    title: 'Дополнительная информация',
    text: props.vacancyData.additional_info || ''
  }
])

const hasAnyKeywords = computed(() => {
  return stats.value && stats.value.total_keywords > 0
})

// Methods
const extractAllKeywords = async () => {
  try {
    isExtractingAll.value = true
    
    const response = await hrStore.extractAllKeywords(props.vacancyId, true)
    
    if (response.success) {
      ElMessage.success(`Извлечено ${response.sections.length} разделов с ключевыми словами`)
      await loadStats()
      emit('keywords-updated', response)
    } else {
      ElMessage.error(response.error || 'Ошибка при извлечении ключевых слов')
    }
  } catch (error) {
    console.error('Error extracting all keywords:', error)
    ElMessage.error('Ошибка при извлечении ключевых слов')
  } finally {
    isExtractingAll.value = false
  }
}

const refreshAllKeywords = async () => {
  try {
    isRefreshing.value = true
    await loadStats()
    ElMessage.success('Статистика обновлена')
  } catch (error) {
    console.error('Error refreshing keywords:', error)
    ElMessage.error('Ошибка при обновлении статистики')
  } finally {
    isRefreshing.value = false
  }
}

const clearAllKeywords = async () => {
  try {
    await ElMessageBox.confirm(
      'Вы уверены, что хотите очистить все ключевые слова? Это действие нельзя отменить.',
      'Подтверждение',
      {
        confirmButtonText: 'Очистить все',
        cancelButtonText: 'Отмена',
        type: 'warning'
      }
    )

    // Clear keywords for each section
    const clearPromises = sections.value.map(section =>
      hrStore.deleteSectionKeywords(props.vacancyId, section.type)
    )
    
    await Promise.all(clearPromises)
    
    ElMessage.success('Все ключевые слова очищены')
    await loadStats()
    emit('keywords-updated', { cleared: true })
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Error clearing all keywords:', error)
      ElMessage.error('Ошибка при очистке ключевых слов')
    }
  }
}

const showStats = () => {
  statsVisible.value = true
}

const loadStats = async () => {
  try {
    isLoading.value = true
    const response = await hrStore.getKeywordsStats(props.vacancyId)
    stats.value = response
  } catch (error) {
    console.error('Error loading keywords stats:', error)
    stats.value = null
  } finally {
    isLoading.value = false
  }
}

const handleSectionUpdated = (data) => {
  console.log('Section updated:', data)
  emit('keywords-updated', data)
  // Reload stats after update
  loadStats()
}

const getConfidenceColor = (score) => {
  if (score >= 0.8) return '#67C23A'
  if (score >= 0.6) return '#E6A23C'
  if (score >= 0.4) return '#F56C6C'
  return '#909399'
}

// Load stats on mount
onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.keywords-manager {
  padding: 24px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  min-height: 100vh;
}

.manager-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  padding: 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  border: none;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
  color: white;
}

.header-left h3 {
  margin: 0 0 8px 0;
  color: white;
  font-size: 24px;
  font-weight: 700;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-subtitle {
  margin: 0;
  color: rgba(255, 255, 255, 0.9);
  font-size: 16px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.header-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.stats-summary {
  margin-bottom: 24px;
}

.stat-card {
  border: none;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  transition: all 0.3s ease;
  overflow: hidden;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

/* Animation for stats cards */
.stat-card {
  animation: slideInUp 0.4s ease-out;
}

.stat-card:nth-child(1) { animation-delay: 0.1s; }
.stat-card:nth-child(2) { animation-delay: 0.2s; }
.stat-card:nth-child(3) { animation-delay: 0.3s; }
.stat-card:nth-child(4) { animation-delay: 0.4s; }

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  font-size: 24px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
  line-height: 1;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.stat-label {
  font-size: 13px;
  color: #606266;
  margin-top: 6px;
  font-weight: 500;
}

.keywords-grid {
  margin-bottom: 24px;
}

.empty-state {
  padding: 60px 20px;
  text-align: center;
}

.loading-state {
  padding: 20px;
}

.stats-details {
  max-height: 400px;
  overflow-y: auto;
}

.section-stats {
  margin-top: 20px;
}

.section-stats h4 {
  margin: 0 0 12px 0;
  color: #303133;
  font-size: 16px;
  font-weight: 600;
}

.confidence-text {
  margin-left: 8px;
  font-size: 12px;
  color: #606266;
}

/* Responsive design */
@media (max-width: 768px) {
  .keywords-manager {
    padding: 16px;
  }

  .manager-header {
    flex-direction: column;
    gap: 20px;
    padding: 20px;
    border-radius: 12px;
  }

  .header-left h3 {
    font-size: 20px;
  }

  .header-subtitle {
    font-size: 14px;
  }

  .header-actions {
    justify-content: center;
    flex-wrap: wrap;
    gap: 8px;
  }

  .stats-summary {
    margin-bottom: 20px;
  }

  .stat-content {
    flex-direction: column;
    text-align: center;
    gap: 8px;
  }

  .stat-icon {
    width: 48px;
    height: 48px;
    font-size: 20px;
  }

  .stat-value {
    font-size: 24px;
  }

  .stat-label {
    font-size: 12px;
  }

  .keywords-grid {
    margin-bottom: 20px;
  }
}

@media (max-width: 480px) {
  .keywords-manager {
    padding: 12px;
  }

  .manager-header {
    padding: 16px;
    gap: 16px;
  }

  .header-left h3 {
    font-size: 18px;
  }

  .header-subtitle {
    font-size: 13px;
  }

  .header-actions {
    gap: 6px;
  }

  .stat-icon {
    width: 40px;
    height: 40px;
    font-size: 18px;
  }

  .stat-value {
    font-size: 20px;
  }
}
</style>
