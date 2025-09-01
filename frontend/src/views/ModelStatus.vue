<template>
  <div class="model-status">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>Статус моделей</h1>
          <div class="header-actions">
            <el-button type="primary" @click="refreshAllStatus" :loading="loading">
              <el-icon><Refresh /></el-icon>
              Обновить все
            </el-button>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <div class="page-description">
          <p>Мониторинг состояния моделей Whisper, LLM и A2E Avatar</p>
        </div>

        <!-- Whisper Model Status Card -->
        <el-card class="status-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>Статус модели Whisper</span>
              <el-tag :type="getWhisperStatusType()" size="large">
                {{ getWhisperStatusText() }}
              </el-tag>
            </div>
          </template>
          
          <el-row :gutter="20" v-if="whisperStatus">
            <el-col :span="12">
              <div class="info-section">
                <h3>Основная информация</h3>
                <div class="info-item">
                  <label>Модель:</label>
                  <span>{{ whisperStatus.whisper_model }}</span>
                </div>
                <div class="info-item">
                  <label>Статус загрузки:</label>
                  <el-tag :type="whisperStatus.model_loaded ? 'success' : 'danger'">
                    {{ whisperStatus.model_loaded ? 'Загружена' : 'Не загружена' }}
                  </el-tag>
                </div>
                <div class="info-item">
                  <label>Размер модели:</label>
                  <span>{{ whisperStatus.model_size_mb }} MB</span>
                </div>
                <div class="info-item">
                  <label>Путь к модели:</label>
                  <span class="path-text">{{ whisperStatus.model_path || 'Не найден' }}</span>
                </div>
              </div>
            </el-col>
            
            <el-col :span="12">
              <div class="info-section">
                <h3>Компоненты системы</h3>
                <div class="info-item">
                  <label>VAD (Voice Activity Detection):</label>
                  <el-tag :type="whisperStatus.vad_loaded ? 'success' : 'danger'">
                    {{ whisperStatus.vad_loaded ? 'Активен' : 'Неактивен' }}
                  </el-tag>
                </div>
                <div class="info-item">
                  <label>MinIO соединение:</label>
                  <el-tag :type="whisperStatus.minio_connected ? 'success' : 'danger'">
                    {{ whisperStatus.minio_connected ? 'Подключено' : 'Отключено' }}
                  </el-tag>
                </div>
                <div class="info-item">
                  <label>Кэш модели:</label>
                  <el-tag :type="whisperStatus.model_exists ? 'success' : 'warning'">
                    {{ whisperStatus.model_exists ? 'Найден' : 'Не найден' }}
                  </el-tag>
                </div>
              </div>
            </el-col>
          </el-row>
          
          <div v-else-if="whisperError" class="error-section">
            <el-alert
              :title="whisperError"
              type="error"
              :closable="false"
              show-icon
            />
          </div>
          
          <div v-else class="loading-section">
            <el-skeleton :rows="6" animated />
          </div>
        </el-card>

        <!-- LLM Model Status Card -->
        <el-card class="status-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>Статус модели LLM</span>
              <el-tag :type="getLLMStatusType()" size="large">
                {{ getLLMStatusText() }}
              </el-tag>
            </div>
          </template>
          
          <el-row :gutter="20" v-if="llmStatus">
            <el-col :span="12">
              <div class="info-section">
                <h3>Основная информация</h3>
                <div class="info-item">
                  <label>Модель:</label>
                  <span>{{ llmStatus.model_deployment }}</span>
                </div>
                <div class="info-item">
                  <label>Статус подключения:</label>
                  <el-tag :type="llmStatus.azure_accessible ? 'success' : 'danger'">
                    {{ llmStatus.azure_accessible ? 'Доступна' : 'Недоступна' }}
                  </el-tag>
                </div>
                <div class="info-item">
                  <label>API версия:</label>
                  <span>{{ llmStatus.api_version }}</span>
                </div>
                <div class="info-item">
                  <label>Endpoint:</label>
                  <span class="path-text">{{ llmStatus.azure_endpoint || 'Не настроен' }}</span>
                </div>
              </div>
            </el-col>
            
            <el-col :span="12">
              <div class="info-section">
                <h3>Состояние системы</h3>
                <div class="info-item">
                  <label>Клиент инициализирован:</label>
                  <el-tag :type="llmStatus.client_initialized ? 'success' : 'danger'">
                    {{ llmStatus.client_initialized ? 'Да' : 'Нет' }}
                  </el-tag>
                </div>
                <div class="info-item">
                  <label>Учетные данные:</label>
                  <el-tag :type="llmStatus.credentials_configured ? 'success' : 'warning'">
                    {{ llmStatus.credentials_configured ? 'Настроены' : 'Не настроены' }}
                  </el-tag>
                </div>
                <div class="info-item" v-if="llmStatus.error">
                  <label>Ошибка:</label>
                  <span class="error-text">{{ llmStatus.error }}</span>
                </div>
              </div>
            </el-col>
          </el-row>
          
          <div v-else-if="llmError" class="error-section">
            <el-alert
              :title="llmError"
              type="error"
              :closable="false"
              show-icon
            />
          </div>
          
          <div v-else class="loading-section">
            <el-skeleton :rows="6" animated />
          </div>
        </el-card>

        <!-- Avatar Status Component -->
        <AvatarStatus />

        <!-- Actions Card -->
        <el-card class="actions-card" shadow="never">
          <template #header>
            <span>Действия</span>
          </template>
          
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="action-item">
                <h4>Обновить статус</h4>
                <p>Получить актуальную информацию о состоянии моделей</p>
                <el-button type="primary" @click="refreshAllStatus" :loading="loading">
                  <el-icon><Refresh /></el-icon>
                  Обновить все
                </el-button>
              </div>
            </el-col>
            
            <el-col :span="6">
              <div class="action-item">
                <h4>Перезагрузить Whisper</h4>
                <p>Принудительно перезагрузить модель Whisper в память</p>
                <el-button type="warning" @click="reloadModel" :loading="reloading">
                  <el-icon><Refresh /></el-icon>
                  Перезагрузить
                </el-button>
              </div>
            </el-col>
            
            <el-col :span="6">
              <div class="action-item">
                <h4>Очистить кэш</h4>
                <p>Удалить кэшированную модель Whisper с диска</p>
                <el-button type="danger" @click="clearCache" :loading="clearing">
                  <el-icon><Delete /></el-icon>
                  Очистить
                </el-button>
              </div>
            </el-col>
            
            <el-col :span="6">
              <div class="action-item">
                <h4>Проверить Azure</h4>
                <p>Проверить подключение к Azure OpenAI</p>
                <el-button type="info" @click="checkAzureConnection" :loading="checkingAzure">
                  <el-icon><Refresh /></el-icon>
                  Проверить
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
import AvatarStatus from '@/components/AvatarStatus.vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

const whisperStatus = ref(null)
const whisperError = ref(null)
const llmStatus = ref(null)
const llmError = ref(null)
const loading = ref(false)
const reloading = ref(false)
const clearing = ref(false)
const checkingAzure = ref(false)

const fetchWhisperStatus = async () => {
  try {
    whisperError.value = null
    
    const response = await axios.get(`${API_BASE_URL}/api/v1/stt/model-status`)
    whisperStatus.value = response.data
  } catch (err) {
    whisperError.value = err.response?.data?.detail || 'Ошибка при получении статуса модели Whisper'
    console.error('Error fetching Whisper model status:', err)
  }
}

const fetchLLMStatus = async () => {
  try {
    llmError.value = null
    
    const response = await axios.get(`${API_BASE_URL}/api/v1/llm/model-status`)
    llmStatus.value = response.data
  } catch (err) {
    llmError.value = err.response?.data?.detail || 'Ошибка при получении статуса модели LLM'
    console.error('Error fetching LLM model status:', err)
  }
}

const fetchAllStatus = async () => {
  try {
    loading.value = true
    await Promise.all([
      fetchWhisperStatus(),
      fetchLLMStatus()
    ])
  } finally {
    loading.value = false
  }
}

const refreshAllStatus = () => {
  fetchAllStatus()
}

const checkAzureConnection = async () => {
  try {
    checkingAzure.value = true
    await fetchLLMStatus()
    ElMessage.success('Статус Azure обновлен')
  } catch (err) {
    ElMessage.error('Ошибка при проверке Azure подключения')
  } finally {
    checkingAzure.value = false
  }
}

const reloadModel = async () => {
  try {
    reloading.value = true
    
    const response = await axios.post(`${API_BASE_URL}/api/v1/stt/reload-model`)
    
    ElMessage.success('Модель Whisper успешно перезагружена')
    await fetchWhisperStatus()
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || 'Ошибка при перезагрузке модели Whisper')
    console.error('Error reloading Whisper model:', err)
  } finally {
    reloading.value = false
  }
}

const clearCache = async () => {
  try {
    await ElMessageBox.confirm(
      'Вы уверены, что хотите очистить кэш модели Whisper? Это приведет к повторной загрузке модели при следующем использовании.',
      'Подтверждение',
      {
        confirmButtonText: 'Очистить',
        cancelButtonText: 'Отмена',
        type: 'warning',
      }
    )
    
    clearing.value = true
    
    const response = await axios.post(`${API_BASE_URL}/api/v1/stt/clear-cache`)
    
    ElMessage.success('Кэш модели Whisper очищен')
    await fetchWhisperStatus()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error(err.response?.data?.detail || 'Ошибка при очистке кэша')
      console.error('Error clearing cache:', err)
    }
  } finally {
    clearing.value = false
  }
}

const getWhisperStatusType = () => {
  if (!whisperStatus.value) return 'info'
  if (whisperStatus.value.model_loaded && whisperStatus.value.model_exists) return 'success'
  if (whisperStatus.value.model_exists) return 'warning'
  return 'danger'
}

const getWhisperStatusText = () => {
  if (!whisperStatus.value) return 'Загрузка...'
  if (whisperStatus.value.model_loaded && whisperStatus.value.model_exists) return 'Готова'
  if (whisperStatus.value.model_exists) return 'Кэширована'
  return 'Не найдена'
}

const getLLMStatusType = () => {
  if (!llmStatus.value) return 'info'
  if (llmStatus.value.azure_accessible) return 'success'
  if (llmStatus.value.credentials_configured) return 'warning'
  return 'danger'
}

const getLLMStatusText = () => {
  if (!llmStatus.value) return 'Загрузка...'
  if (llmStatus.value.azure_accessible) return 'Доступна'
  if (llmStatus.value.credentials_configured) return 'Настроена'
  return 'Недоступна'
}

onMounted(() => {
  fetchAllStatus()
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

.error-text {
  color: #f56c6c;
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
