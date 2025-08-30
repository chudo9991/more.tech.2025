<template>
  <div class="model-status">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>Статус модели Whisper</h1>
          <div class="header-actions">
            <el-button type="primary" @click="refreshStatus" :loading="loading">
              <el-icon><Refresh /></el-icon>
              Обновить
            </el-button>
            <el-button type="warning" @click="reloadModel" :loading="reloading">
              <el-icon><Refresh /></el-icon>
              Перезагрузить модель
            </el-button>
            <el-button type="danger" @click="clearCache" :loading="clearing">
              <el-icon><Delete /></el-icon>
              Очистить кэш
            </el-button>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <div class="page-description">
          <p>Мониторинг состояния модели Whisper для распознавания речи</p>
        </div>

        <!-- Model Status Card -->
        <el-card class="status-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>Статус модели</span>
              <el-tag :type="getStatusType()" size="large">
                {{ getStatusText() }}
              </el-tag>
            </div>
          </template>
          
          <el-row :gutter="20" v-if="modelStatus">
            <el-col :span="12">
              <div class="info-section">
                <h3>Основная информация</h3>
                <div class="info-item">
                  <label>Модель:</label>
                  <span>{{ modelStatus.whisper_model }}</span>
                </div>
                <div class="info-item">
                  <label>Статус загрузки:</label>
                  <el-tag :type="modelStatus.model_loaded ? 'success' : 'danger'">
                    {{ modelStatus.model_loaded ? 'Загружена' : 'Не загружена' }}
                  </el-tag>
                </div>
                <div class="info-item">
                  <label>Размер модели:</label>
                  <span>{{ modelStatus.model_size_mb }} MB</span>
                </div>
                <div class="info-item">
                  <label>Путь к модели:</label>
                  <span class="path-text">{{ modelStatus.model_path || 'Не найден' }}</span>
                </div>
              </div>
            </el-col>
            
            <el-col :span="12">
              <div class="info-section">
                <h3>Компоненты системы</h3>
                <div class="info-item">
                  <label>VAD (Voice Activity Detection):</label>
                  <el-tag :type="modelStatus.vad_loaded ? 'success' : 'danger'">
                    {{ modelStatus.vad_loaded ? 'Активен' : 'Неактивен' }}
                  </el-tag>
                </div>
                <div class="info-item">
                  <label>MinIO соединение:</label>
                  <el-tag :type="modelStatus.minio_connected ? 'success' : 'danger'">
                    {{ modelStatus.minio_connected ? 'Подключено' : 'Отключено' }}
                  </el-tag>
                </div>
                <div class="info-item">
                  <label>Кэш модели:</label>
                  <el-tag :type="modelStatus.model_exists ? 'success' : 'warning'">
                    {{ modelStatus.model_exists ? 'Найден' : 'Не найден' }}
                  </el-tag>
                </div>
              </div>
            </el-col>
          </el-row>
          
          <div v-else-if="error" class="error-section">
            <el-alert
              :title="error"
              type="error"
              :closable="false"
              show-icon
            />
          </div>
          
          <div v-else class="loading-section">
            <el-skeleton :rows="6" animated />
          </div>
        </el-card>

        <!-- Actions Card -->
        <el-card class="actions-card" shadow="never">
          <template #header>
            <span>Действия</span>
          </template>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="action-item">
                <h4>Обновить статус</h4>
                <p>Получить актуальную информацию о состоянии модели</p>
                <el-button type="primary" @click="refreshStatus" :loading="loading">
                  <el-icon><Refresh /></el-icon>
                  Обновить
                </el-button>
              </div>
            </el-col>
            
            <el-col :span="8">
              <div class="action-item">
                <h4>Перезагрузить модель</h4>
                <p>Принудительно перезагрузить модель в память</p>
                <el-button type="warning" @click="reloadModel" :loading="reloading">
                  <el-icon><Refresh /></el-icon>
                  Перезагрузить
                </el-button>
              </div>
            </el-col>
            
            <el-col :span="8">
              <div class="action-item">
                <h4>Очистить кэш</h4>
                <p>Удалить кэшированную модель с диска</p>
                <el-button type="danger" @click="clearCache" :loading="clearing">
                  <el-icon><Delete /></el-icon>
                  Очистить
                </el-button>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh, Delete } from '@element-plus/icons-vue'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

const modelStatus = ref(null)
const error = ref(null)
const loading = ref(false)
const reloading = ref(false)
const clearing = ref(false)

const fetchStatus = async () => {
  try {
    loading.value = true
    error.value = null
    
    const response = await axios.get(`${API_BASE_URL}/api/v1/stt/model-status`)
    modelStatus.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка при получении статуса модели'
    console.error('Error fetching model status:', err)
  } finally {
    loading.value = false
  }
}

const refreshStatus = () => {
  fetchStatus()
}

const reloadModel = async () => {
  try {
    reloading.value = true
    
    const response = await axios.post(`${API_BASE_URL}/api/v1/stt/reload-model`)
    
    ElMessage.success('Модель успешно перезагружена')
    await fetchStatus()
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || 'Ошибка при перезагрузке модели')
    console.error('Error reloading model:', err)
  } finally {
    reloading.value = false
  }
}

const clearCache = async () => {
  try {
    await ElMessageBox.confirm(
      'Вы уверены, что хотите очистить кэш модели? Это приведет к повторной загрузке модели при следующем использовании.',
      'Подтверждение',
      {
        confirmButtonText: 'Очистить',
        cancelButtonText: 'Отмена',
        type: 'warning',
      }
    )
    
    clearing.value = true
    
    const response = await axios.post(`${API_BASE_URL}/api/v1/stt/clear-cache`)
    
    ElMessage.success('Кэш модели очищен')
    await fetchStatus()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error(err.response?.data?.detail || 'Ошибка при очистке кэша')
      console.error('Error clearing cache:', err)
    }
  } finally {
    clearing.value = false
  }
}

const getStatusType = () => {
  if (!modelStatus.value) return 'info'
  if (modelStatus.value.model_loaded && modelStatus.value.model_exists) return 'success'
  if (modelStatus.value.model_exists) return 'warning'
  return 'danger'
}

const getStatusText = () => {
  if (!modelStatus.value) return 'Загрузка...'
  if (modelStatus.value.model_loaded && modelStatus.value.model_exists) return 'Готова'
  if (modelStatus.value.model_exists) return 'Кэширована'
  return 'Не найдена'
}

onMounted(() => {
  fetchStatus()
})
</script>

<style scoped>
.model-status {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.header-content h1 {
  margin: 0;
  color: #303133;
  font-size: 28px;
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.page-description {
  margin-bottom: 24px;
  text-align: center;
}

.page-description p {
  margin: 0;
  font-size: 16px;
  color: #606266;
  font-weight: 400;
}

.status-card {
  margin-bottom: 24px;
  border: none;
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-section h3 {
  margin: 0 0 16px 0;
  color: #303133;
  font-size: 18px;
  font-weight: 600;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item label {
  font-weight: 500;
  color: #606266;
  min-width: 120px;
}

.info-item span {
  color: #303133;
  text-align: right;
}

.path-text {
  font-family: monospace;
  font-size: 12px;
  word-break: break-all;
}

.actions-card {
  border: none;
  border-radius: 8px;
}

.action-item {
  text-align: center;
  padding: 20px;
}

.action-item h4 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 16px;
  font-weight: 600;
}

.action-item p {
  margin: 0 0 16px 0;
  color: #606266;
  font-size: 14px;
  line-height: 1.5;
}

.error-section {
  margin: 20px 0;
}

.loading-section {
  padding: 20px 0;
}

:deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__body) {
  padding: 20px;
}
</style>
