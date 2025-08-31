<template>
  <div class="scenario-visualizer">
    <div class="visualizer-header">
      <h3>Визуализация сценария: {{ scenarioName }}</h3>
      <div class="visualizer-stats">
        <el-tag type="info">{{ nodesCount }} узлов</el-tag>
        <el-tag type="success">{{ transitionsCount }} переходов</el-tag>
      </div>
    </div>
    
    <div class="visualizer-content">
      <div v-if="loading" class="loading-container">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>Загрузка диаграммы...</span>
      </div>
      
      <div v-else-if="error" class="error-container">
        <el-icon><Warning /></el-icon>
        <span>{{ error }}</span>
      </div>
      
      <div v-else class="image-container">
        <div v-if="scenarioImage" class="image-display">
          <img :src="scenarioImage" alt="Диаграмма сценария" class="scenario-image" />
        </div>
        <div v-else class="placeholder">
          <el-icon><Document /></el-icon>
          <span>Диаграмма будет отображаться здесь</span>
          <p>Скоро здесь появится изображение сценария</p>
        </div>
        
        <div class="legend">
          <h4>Легенда:</h4>
          <div class="legend-items">
            <div class="legend-item">
              <span class="legend-icon">🎬</span>
              <span>Начало интервью</span>
            </div>
            <div class="legend-item">
              <span class="legend-icon">🔴</span>
              <span>Обязательный вопрос</span>
            </div>
            <div class="legend-item">
              <span class="legend-icon">🟡</span>
              <span>Дополнительный вопрос</span>
            </div>
            <div class="legend-item">
              <span class="legend-icon">🏁</span>
              <span>Завершение интервью</span>
            </div>
            <div class="legend-item">
              <span class="legend-icon">💡</span>
              <span>Целевые навыки</span>
            </div>
            <div class="legend-item">
              <span class="legend-icon">⚖️</span>
              <span>Важность вопроса</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { ElIcon, ElTag } from 'element-plus'
import { Loading, Warning, Document } from '@element-plus/icons-vue'

const props = defineProps({
  scenarioId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['error'])

// Reactive data
const loading = ref(false)
const error = ref(null)
const scenarioName = ref('')
const nodesCount = ref(0)
const transitionsCount = ref(0)
const scenarioImage = ref('')

// Methods
const loadScenarioData = async () => {
  if (!props.scenarioId) return
  
  loading.value = true
  error.value = null
  
  try {
    const url = `${import.meta.env.VITE_API_URL || ''}/api/v1/scenarios/${props.scenarioId}`
    console.log('Загружаем данные сценария по URL:', url)
    
    const response = await fetch(url)
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    
    const data = await response.json()
    console.log('Получены данные сценария:', data)
    
    scenarioName.value = data.name || 'Неизвестный сценарий'
    nodesCount.value = data.nodes_count || 0
    transitionsCount.value = data.transitions_count || 0
    
    // Загружаем изображение сценария
    await loadScenarioImage()
    
  } catch (err) {
    console.error('Ошибка загрузки данных сценария:', err)
    error.value = `Не удалось загрузить данные сценария: ${err.message}`
    emit('error', error.value)
  } finally {
    loading.value = false
  }
}

const loadScenarioImage = async () => {
  if (!props.scenarioId) return
  
  try {
    const url = `${import.meta.env.VITE_API_URL || ''}/api/v1/scenarios/${props.scenarioId}/image?format=png`
    console.log('Загружаем изображение сценария по URL:', url)
    
    const response = await fetch(url)
    
    if (!response.ok) {
      console.warn('Не удалось загрузить изображение сценария:', response.status)
      return
    }
    
    const blob = await response.blob()
    const imageUrl = URL.createObjectURL(blob)
    scenarioImage.value = imageUrl
    
    console.log('Изображение сценария загружено')
    
  } catch (err) {
    console.error('Ошибка загрузки изображения сценария:', err)
  }
}

// Watchers
watch(() => props.scenarioId, (newId) => {
  if (newId) {
    loadScenarioData()
  }
})

// Lifecycle
onMounted(() => {
  if (props.scenarioId) {
    loadScenarioData()
  }
})
</script>

<style scoped>
.scenario-visualizer {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.visualizer-header {
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.visualizer-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.visualizer-stats {
  display: flex;
  gap: 8px;
}

.visualizer-content {
  padding: 20px;
  min-height: 400px;
  display: flex;
  flex-direction: column;
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  gap: 12px;
  color: #909399;
}

.loading-container .el-icon {
  font-size: 32px;
  color: #409EFF;
}

.error-container .el-icon {
  font-size: 32px;
  color: #F56C6C;
}

.image-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  background: #fafafa;
  gap: 12px;
  color: #909399;
}

.placeholder .el-icon {
  font-size: 48px;
  color: #c0c4cc;
}

.placeholder span {
  font-size: 16px;
  font-weight: 500;
}

.placeholder p {
  margin: 0;
  font-size: 14px;
  color: #c0c4cc;
}

.image-display {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  background: #fafafa;
  padding: 20px;
}

.scenario-image {
  max-width: 100%;
  max-height: 600px;
  height: auto;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.legend {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e9ecef;
}

.legend h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.legend-items {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #606266;
}

.legend-icon {
  font-size: 16px;
  width: 20px;
  text-align: center;
}

/* Responsive design */
@media (max-width: 768px) {
  .visualizer-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .visualizer-stats {
    align-self: stretch;
    justify-content: space-between;
  }
  
  .legend-items {
    grid-template-columns: 1fr;
  }
}
</style>
