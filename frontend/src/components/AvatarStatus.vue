<template>
  <div class="avatar-status">
    <el-card class="status-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>Статус модели A2E</span>
          <el-tag :type="getStatusType()" size="large">
            {{ getStatusText() }}
          </el-tag>
        </div>
      </template>
      
      <el-row :gutter="20" v-if="avatarStatus">
        <el-col :span="12">
          <div class="info-section">
            <h3>Основная информация</h3>
            <div class="info-item">
              <label>API статус:</label>
              <el-tag :type="avatarStatus.api_accessible ? 'success' : 'danger'">
                {{ avatarStatus.api_accessible ? 'Доступен' : 'Недоступен' }}
              </el-tag>
            </div>
            <div class="info-item">
              <label>Base URL:</label>
              <span class="path-text">{{ avatarStatus.base_url || 'Не настроен' }}</span>
            </div>
            <div class="info-item">
              <label>Доступные голоса:</label>
              <span>{{ avatarStatus.available_voices || 0 }}</span>
            </div>
            <div class="info-item">
              <label>Streaming Avatar:</label>
              <el-tag :type="avatarStatus.streaming_available ? 'success' : 'warning'">
                {{ avatarStatus.streaming_available ? 'Доступен' : 'Недоступен' }}
              </el-tag>
            </div>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="info-section">
            <h3>Streaming Avatar</h3>
            <div class="info-item">
              <label>Аватар Alice:</label>
              <el-tag :type="avatarStatus.alice_available ? 'success' : 'warning'">
                {{ avatarStatus.alice_available ? 'Доступен' : 'Недоступен' }}
              </el-tag>
            </div>
            <div class="info-item">
              <label>Поддерживаемые языки:</label>
              <span>{{ avatarStatus.supported_languages?.join(', ') || 'ru-RU' }}</span>
            </div>
            <div class="info-item">
              <label>Качество видео:</label>
              <span>{{ avatarStatus.video_quality || '720p/1080p' }}</span>
            </div>
            <div class="info-item" v-if="avatarStatus.error">
              <label>Ошибка:</label>
              <span class="error-text">{{ avatarStatus.error }}</span>
            </div>
          </div>
        </el-col>
      </el-row>
      
      <div v-else-if="avatarError" class="error-section">
        <el-alert :title="avatarError" type="error" :closable="false" show-icon />
      </div>
      
      <div v-else class="loading-section">
        <el-skeleton :rows="6" animated />
      </div>
    </el-card>
    
    <!-- Action Buttons -->
    <el-card class="actions-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>Действия</span>
        </div>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="action-item">
            <h4>Обновить статус</h4>
            <p>Получить актуальную информацию о состоянии A2E API</p>
            <el-button type="primary" @click="refreshStatus" :loading="loading">
              <el-icon><Refresh /></el-icon>
              Обновить
            </el-button>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="action-item">
            <h4>Тест TTS</h4>
            <p>Протестировать генерацию речи</p>
            <el-button type="success" @click="testTTS" :loading="testingTTS">
              <el-icon><Microphone /></el-icon>
              Тест TTS
            </el-button>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="action-item">
            <h4>Тест Streaming</h4>
            <p>Протестировать Streaming Avatar</p>
            <el-button type="warning" @click="testStreaming" :loading="testingStreaming">
              <el-icon><VideoCamera /></el-icon>
              Тест Streaming
            </el-button>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="action-item">
            <h4>Настройки</h4>
            <p>Управление настройками аватара</p>
            <el-button type="info" @click="openSettings">
              <el-icon><Setting /></el-icon>
              Настройки
            </el-button>
          </div>
        </el-col>
      </el-row>
    </el-card>
    
    <!-- Avatar Settings Section -->
    <el-card class="settings-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>Настройки аватара</span>
          <el-button type="primary" size="small" @click="loadAllOptions">
            <el-icon><Refresh /></el-icon>
            Загрузить опции
          </el-button>
        </div>
      </template>
      
      <el-row :gutter="20">
        <!-- Available Voices -->
        <el-col :span="8">
          <div class="settings-section">
            <h4>Доступные голоса</h4>
            <el-select 
              v-model="avatarStore.selectedVoice" 
              placeholder="Выберите голос"
              style="width: 100%"
              :loading="avatarStore.loading.voices"
            >
              <el-option
                v-for="voice in avatarStore.availableVoices"
                :key="voice.id"
                :label="voice.name || voice.id"
                :value="voice.id"
              />
            </el-select>
            <div class="setting-info">
              <small>Выбран: {{ avatarStore.currentVoice?.name || 'Не выбран' }}</small>
            </div>
          </div>
        </el-col>
        
        <!-- Available Avatars -->
        <el-col :span="8">
          <div class="settings-section">
            <h4>Доступные аватары</h4>
            <el-select 
              v-model="avatarStore.selectedAvatar" 
              placeholder="Выберите аватар"
              style="width: 100%"
              :loading="avatarStore.loading.avatars"
            >
              <el-option
                v-for="avatar in avatarStore.availableAvatars"
                :key="avatar.id"
                :label="avatar.name || avatar.id"
                :value="avatar.id"
              />
            </el-select>
            <div class="setting-info">
              <small>Выбран: {{ avatarStore.currentAvatar?.name || 'Не выбран' }}</small>
            </div>
          </div>
        </el-col>
        
        <!-- Video Resolution -->
        <el-col :span="8">
          <div class="settings-section">
            <h4>Разрешение видео (1:1 формат)</h4>
            <el-select 
              v-model="avatarStore.resolution" 
              placeholder="Выберите разрешение"
              style="width: 100%"
            >
              <el-option label="720p" :value="720" />
              <el-option label="1080p" :value="1080" />
            </el-select>
            <div class="setting-info">
              <small>Текущее: {{ avatarStore.resolution }}p</small>
            </div>
          </div>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" style="margin-top: 20px;">
        <!-- Speech Rate -->
        <el-col :span="6">
          <div class="settings-section">
            <h4>Скорость речи</h4>
            <el-slider
              v-model="avatarStore.speechRate"
              :min="0.5"
              :max="2.0"
              :step="0.1"
              :show-tooltip="true"
              :format-tooltip="(val) => `${val}x`"
            />
            <div class="setting-info">
              <small>Текущая: {{ avatarStore.speechRate }}x</small>
            </div>
          </div>
        </el-col>
        
        <!-- Lip-sync Quality -->
        <el-col :span="6">
          <div class="settings-section">
            <h4>Качество синхронизации</h4>
            <el-switch
              v-model="avatarStore.isSkipRs"
              active-text="Быстро"
              inactive-text="Высокое качество"
              :active-value="true"
              :inactive-value="false"
            />
            <div class="setting-info">
              <small>{{ avatarStore.isSkipRs ? 'Быстро (стандартное качество)' : 'Высокое качество (медленнее)' }}</small>
            </div>
          </div>
        </el-col>
        
        <!-- Captions -->
        <el-col :span="6">
          <div class="settings-section">
            <h4>Субтитры</h4>
            <el-switch
              v-model="avatarStore.isCaptionEnabled"
              active-text="Включены"
              inactive-text="Выключены"
            />
            <div class="setting-info">
              <small>{{ avatarStore.isCaptionEnabled ? 'Субтитры включены' : 'Субтитры выключены' }}</small>
            </div>
          </div>
        </el-col>
        
        <!-- Background Color -->
        <el-col :span="6">
          <div class="settings-section">
            <h4>Цвет фона</h4>
            <el-color-picker
              v-model="avatarStore.backgroundColor"
              show-alpha
              size="large"
            />
            <div class="setting-info">
              <small>Текущий: {{ avatarStore.backgroundColor }}</small>
            </div>
          </div>
        </el-col>
      </el-row>
      
      <!-- Test Video Generation -->
      <el-row style="margin-top: 30px;">
        <el-col :span="24">
          <div class="test-section">
            <h4>Тест генерации видео</h4>
            <p>Сгенерировать тестовое видео с текущими настройками</p>
            
            <el-button 
              type="success" 
              @click="testVideoGeneration"
              :loading="avatarStore.loading.testGeneration"
              size="large"
            >
              <el-icon><VideoPlay /></el-icon>
              Сгенерировать тест
            </el-button>
            
            <!-- Test Video Result -->
            <div v-if="avatarStore.testVideoUrl" class="test-result">
              <h5>Результат теста:</h5>
              <video 
                :src="avatarStore.testVideoUrl" 
                controls 
                style="max-width: 100%; max-height: 300px;"
                class="test-video"
              >
                Ваш браузер не поддерживает видео.
              </video>
              <div class="test-info">
                <p><strong>Текст:</strong> "Добро пожаловать на интервью!"</p>
                <p><strong>Голос:</strong> {{ avatarStore.currentVoice?.name || 'Не выбран' }}</p>
                <p><strong>Аватар:</strong> {{ avatarStore.currentAvatar?.name || 'Не выбран' }}</p>
                <p><strong>Разрешение:</strong> {{ avatarStore.resolution }}x{{ avatarStore.resolution }} (1:1)</p>
                <p><strong>Скорость речи:</strong> {{ avatarStore.speechRate }}x</p>
              </div>
            </div>
            
            <!-- Test Error -->
            <div v-if="avatarStore.error" class="test-error">
              <el-alert
                :title="avatarStore.error"
                type="error"
                :closable="false"
                show-icon
              />
            </div>
          </div>
        </el-col>
      </el-row>
      
      <!-- Save Settings -->
      <el-row style="margin-top: 30px;">
        <el-col :span="24">
          <div class="save-section">
            <el-button type="primary" @click="saveSettings" size="large">
              <el-icon><Check /></el-icon>
              Сохранить настройки
            </el-button>
            <el-button @click="resetSettings" size="large" style="margin-left: 10px;">
              <el-icon><RefreshLeft /></el-icon>
              Сбросить к умолчаниям
            </el-button>
          </div>
        </el-col>
      </el-row>
    </el-card>
    
    <!-- Settings Modal -->
    <el-dialog
      v-model="settingsVisible"
      title="Настройки аватара A2E"
      width="90%"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <AvatarSettings 
        :session-id="null"
        @settings-changed="handleSettingsChanged"
        @settings-saved="handleSettingsSaved"
      />
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="settingsVisible = false">Закрыть</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { Refresh, Microphone, VideoCamera, Setting, VideoPlay, Check, RefreshLeft } from '@element-plus/icons-vue'
import AvatarSettings from './AvatarSettings.vue'
import { useAvatarSettingsStore } from '../stores/avatarSettings'

const API_BASE_URL = import.meta.env.VITE_API_URL || ''

// Avatar settings store
const avatarStore = useAvatarSettingsStore()

const avatarStatus = ref(null)
const avatarError = ref(null)
const loading = ref(false)
const testingTTS = ref(false)
const testingStreaming = ref(false)
const settingsVisible = ref(false)

const fetchAvatarStatus = async () => {
  try {
    avatarError.value = null
    const response = await axios.get(`${API_BASE_URL}/api/v1/avatar/a2e-status`)
    avatarStatus.value = response.data
  } catch (err) {
    avatarError.value = err.response?.data?.detail || 'Ошибка при получении статуса A2E API'
    console.error('Error fetching avatar status:', err)
  }
}

const refreshStatus = () => {
  fetchAvatarStatus()
}

const testTTS = async () => {
  try {
    testingTTS.value = true
    const response = await axios.post(`${API_BASE_URL}/api/v1/avatar/tts`, {
      text: 'Привет! Это тест генерации речи.',
      voice_id: '66d3f6a704d077b1432fb7d3' // Anna
    })
    
    if (response.data.audio_url) {
      ElMessage.success('TTS тест успешен! Аудио сгенерировано.')
    } else {
      ElMessage.warning('TTS тест завершен, но аудио не получено.')
    }
  } catch (err) {
    ElMessage.error('Ошибка TTS теста: ' + (err.response?.data?.detail || err.message))
  } finally {
    testingTTS.value = false
  }
}

const testStreaming = async () => {
  try {
    testingStreaming.value = true
    
    // Test streaming avatar endpoints
    const avatarsResponse = await axios.get(`${API_BASE_URL}/api/v1/avatar/streaming-avatars`)
    
    if (avatarsResponse.data.avatars && avatarsResponse.data.avatars.length > 0) {
      ElMessage.success('Streaming Avatar тест успешен! Аватары доступны.')
    } else {
      ElMessage.warning('Streaming Avatar тест: аватары не найдены.')
    }
  } catch (err) {
    ElMessage.error('Ошибка Streaming Avatar теста: ' + (err.response?.data?.detail || err.message))
  } finally {
    testingStreaming.value = false
  }
}

const openSettings = () => {
  settingsVisible.value = true
}

const handleSettingsChanged = (settings) => {
  console.log('Avatar settings changed:', settings)
}

const handleSettingsSaved = (settings) => {
  console.log('Avatar settings saved:', settings)
  ElMessage.success('Настройки аватара сохранены!')
  settingsVisible.value = false
}

// Load all available options from A2E API
const loadAllOptions = async () => {
  try {
    await avatarStore.fetchAllOptions()
    ElMessage.success('Опции загружены успешно!')
  } catch (error) {
    ElMessage.error('Ошибка загрузки опций: ' + error.message)
  }
}

// Test video generation with current settings
const testVideoGeneration = async () => {
  try {
    await avatarStore.testVideoGeneration()
    ElMessage.success('Тестовое видео сгенерировано успешно!')
  } catch (error) {
    ElMessage.error('Ошибка генерации тестового видео: ' + error.message)
  }
}

// Save current settings
const saveSettings = () => {
  if (avatarStore.saveSettings()) {
    ElMessage.success('Настройки сохранены!')
  } else {
    ElMessage.error('Ошибка сохранения настроек')
  }
}

// Reset settings to defaults
const resetSettings = () => {
  avatarStore.resetToDefaults()
  ElMessage.success('Настройки сброшены к умолчаниям!')
}

const getStatusType = () => {
  if (!avatarStatus.value) return 'info'
  if (avatarStatus.value.api_accessible && avatarStatus.value.streaming_available) return 'success'
  if (avatarStatus.value.api_accessible) return 'warning'
  return 'danger'
}

const getStatusText = () => {
  if (!avatarStatus.value) return 'Загрузка...'
  if (avatarStatus.value.api_accessible && avatarStatus.value.streaming_available) return 'Полностью доступен'
  if (avatarStatus.value.api_accessible) return 'Частично доступен'
  return 'Недоступен'
}

onMounted(async () => {
  await fetchAvatarStatus()
  
  // Load saved settings and available options
  avatarStore.loadSettings()
  try {
    await avatarStore.fetchAllOptions()
  } catch (error) {
    console.warn('Failed to load avatar options:', error)
  }
})
</script>

<style scoped>
.avatar-status {
  margin-bottom: 20px;
}

.status-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-section h3 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  font-size: 14px;
}

.info-item label {
  color: #606266;
  font-weight: 500;
}

.info-item span {
  color: #303133;
}

.path-text {
  font-family: monospace;
  background-color: #f5f7fa;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
}

.error-text {
  color: #f56c6c;
  font-size: 12px;
}

.error-section {
  margin: 20px 0;
}

.loading-section {
  margin: 20px 0;
}

.actions-card {
  margin-top: 20px;
}

.action-item {
  text-align: center;
  padding: 15px;
}

.action-item h4 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 14px;
}

.action-item p {
  margin: 0 0 15px 0;
  color: #606266;
  font-size: 12px;
  line-height: 1.4;
}

.action-item .el-button {
  width: 100%;
}

/* Settings Card Styles */
.settings-card {
  margin-top: 20px;
}

.settings-section {
  margin-bottom: 20px;
}

.settings-section h4 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 14px;
  font-weight: 600;
}

.setting-info {
  margin-top: 8px;
  color: #909399;
}

.setting-info small {
  font-size: 12px;
}

/* Test Section Styles */
.test-section {
  text-align: center;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.test-section h4 {
  margin: 0 0 10px 0;
  color: #303133;
}

.test-section p {
  margin: 0 0 20px 0;
  color: #606266;
}

.test-result {
  margin-top: 20px;
  text-align: left;
}

.test-result h5 {
  margin: 0 0 15px 0;
  color: #303133;
}

.test-video {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.test-info {
  margin-top: 15px;
  padding: 15px;
  background-color: #f0f9ff;
  border-radius: 6px;
}

.test-info p {
  margin: 5px 0;
  font-size: 13px;
}

.test-error {
  margin-top: 20px;
}

/* Save Section Styles */
.save-section {
  text-align: center;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}
</style>
