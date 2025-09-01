<template>
  <div class="avatar-settings">
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <el-icon><Setting /></el-icon>
          <span>Настройки аватара</span>
        </div>
      </template>

      <el-form 
        ref="settingsForm" 
        :model="settings" 
        :rules="rules"
        label-width="120px"
        class="settings-form"
      >
        <!-- Выбор персонажа -->
        <el-form-item label="Персонаж" prop="avatar_id">
          <el-select 
            v-model="settings.avatar_id" 
            placeholder="Выберите персонажа"
            @change="onAvatarChange"
            style="width: 100%"
          >
            <el-option
              v-for="character in characters"
              :key="character.id"
              :label="character.name"
              :value="character.id"
            >
              <div class="character-option">
                <img 
                  :src="character.preview_url" 
                  :alt="character.name"
                  class="character-preview"
                />
                <div class="character-info">
                  <div class="character-name">{{ character.name }}</div>
                  <div class="character-type">{{ character.type }}</div>
                </div>
              </div>
            </el-option>
          </el-select>
        </el-form-item>

        <!-- Выбор голоса -->
        <el-form-item label="Голос" prop="voice_id">
          <el-select 
            v-model="settings.voice_id" 
            placeholder="Выберите голос"
            @change="onVoiceChange"
            style="width: 100%"
          >
            <el-option
              v-for="voice in voices"
              :key="voice.id"
              :label="voice.name"
              :value="voice.id"
            >
              <div class="voice-option">
                <el-icon class="voice-icon">
                  <Microphone />
                </el-icon>
                <div class="voice-info">
                  <div class="voice-name">{{ voice.name }}</div>
                  <div class="voice-details">
                    {{ voice.gender }} • {{ voice.lang }}
                  </div>
                </div>
              </div>
            </el-option>
          </el-select>
        </el-form-item>

        <!-- Разрешение видео -->
        <el-form-item label="Разрешение" prop="resolution">
          <el-radio-group v-model="settings.resolution" @change="onResolutionChange">
            <el-radio :label="720">720p (HD)</el-radio>
            <el-radio :label="1080">1080p (Full HD)</el-radio>
          </el-radio-group>
        </el-form-item>

        <!-- Скорость речи -->
        <el-form-item label="Скорость речи" prop="speech_rate">
          <el-slider
            v-model="settings.speech_rate"
            :min="0.5"
            :max="2.0"
            :step="0.1"
            :show-tooltip="true"
            @change="onSpeechRateChange"
          />
          <div class="slider-labels">
            <span>Медленно</span>
            <span>Нормально</span>
            <span>Быстро</span>
          </div>
        </el-form-item>

        <!-- Качество -->
        <el-form-item label="Качество" prop="quality">
          <el-select v-model="settings.quality" @change="onQualityChange">
            <el-option label="Высокое" value="high" />
            <el-option label="Среднее" value="medium" />
            <el-option label="Низкое" value="low" />
          </el-select>
        </el-form-item>

        <!-- Предпросмотр -->
        <el-form-item label="Предпросмотр">
          <div class="preview-container">
            <div v-if="selectedCharacter" class="character-preview-large">
              <img 
                :src="selectedCharacter.preview_url" 
                :alt="selectedCharacter.name"
                class="preview-image"
              />
              <div class="preview-info">
                <h4>{{ selectedCharacter.name }}</h4>
                <p>{{ selectedCharacter.type }}</p>
              </div>
            </div>
            <div v-else class="preview-placeholder">
              <el-icon><User /></el-icon>
              <p>Выберите персонажа для предпросмотра</p>
            </div>
          </div>
        </el-form-item>

        <!-- Кнопки действий -->
        <el-form-item>
          <el-button 
            type="primary" 
            @click="saveSettings"
            :loading="saving"
            :icon="Check"
          >
            Сохранить настройки
          </el-button>
          <el-button @click="resetSettings" :icon="Refresh">
            Сбросить
          </el-button>
          <el-button @click="testSettings" :icon="VideoPlay">
            Тест
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Тестовое видео -->
    <el-dialog 
      v-model="testDialogVisible" 
      title="Тестовое видео"
      width="80%"
      :before-close="closeTestDialog"
    >
      <div v-if="testVideoUrl" class="test-video-container">
        <video 
          :src="testVideoUrl" 
          controls 
          autoplay
          class="test-video"
        >
          Ваш браузер не поддерживает видео.
        </video>
      </div>
      <div v-else-if="testLoading" class="test-loading">
        <el-icon class="loading-icon"><Loading /></el-icon>
        <p>Генерация тестового видео...</p>
      </div>
      <div v-else class="test-placeholder">
        <p>Нажмите "Тест" для генерации тестового видео</p>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Setting, 
  Microphone, 
  User, 
  Check, 
  Refresh, 
  VideoPlay, 
  Loading 
} from '@element-plus/icons-vue'
import axios from 'axios'

// Props
const props = defineProps({
  sessionId: {
    type: String,
    required: true
  }
})

// Emits
const emit = defineEmits(['settings-changed', 'settings-saved'])

// Reactive data
const settingsForm = ref(null)
const saving = ref(false)
const testDialogVisible = ref(false)
const testVideoUrl = ref('')
const testLoading = ref(false)

const settings = ref({
  avatar_id: '68af59a86eeedd0042ca7e27',
  voice_id: '66d3f6a704d077b1432fb7d3',
  resolution: 720,
  speech_rate: 1.0,
  quality: 'high'
})

const characters = ref([])
const voices = ref([])

// Validation rules
const rules = {
  avatar_id: [
    { required: true, message: 'Выберите персонажа', trigger: 'change' }
  ],
  voice_id: [
    { required: true, message: 'Выберите голос', trigger: 'change' }
  ],
  resolution: [
    { required: true, message: 'Выберите разрешение', trigger: 'change' }
  ]
}

// Computed
const selectedCharacter = computed(() => {
  return characters.value.find(c => c.id === settings.value.avatar_id)
})

// Methods
const loadCharacters = async () => {
  try {
    const response = await axios.get('/api/v1/avatar/characters')
    characters.value = response.data.characters || []
  } catch (error) {
    console.error('Error loading characters:', error)
    ElMessage.error('Ошибка загрузки персонажей')
  }
}

const loadVoices = async () => {
  try {
    const response = await axios.get('/api/v1/avatar/voices')
    voices.value = response.data.voices || []
  } catch (error) {
    console.error('Error loading voices:', error)
    ElMessage.error('Ошибка загрузки голосов')
  }
}

const loadCurrentSettings = async () => {
  try {
    const response = await axios.get('/api/v1/avatar/settings')
    settings.value = { ...settings.value, ...response.data }
  } catch (error) {
    console.error('Error loading settings:', error)
    // Используем значения по умолчанию
  }
}

const saveSettings = async () => {
  try {
    await settingsForm.value.validate()
    
    saving.value = true
    const response = await axios.put('/api/v1/avatar/settings', settings.value)
    
    if (response.data.success) {
      ElMessage.success('Настройки сохранены')
      emit('settings-saved', settings.value)
    } else {
      throw new Error('Ошибка сохранения')
    }
  } catch (error) {
    console.error('Error saving settings:', error)
    ElMessage.error('Ошибка сохранения настроек')
  } finally {
    saving.value = false
  }
}

const resetSettings = () => {
  settings.value = {
    avatar_id: '68af59a86eeedd0042ca7e27',
    voice_id: '66d3f6a704d077b1432fb7d3',
    resolution: 720,
    speech_rate: 1.0,
    quality: 'high'
  }
  ElMessage.info('Настройки сброшены')
}

const testSettings = async () => {
  testDialogVisible.value = true
  testVideoUrl.value = ''
  testLoading.value = true
  
  try {
    const response = await axios.post('/api/v1/avatar/generate', {
      text: 'Привет! Это тестовое видео для проверки настроек аватара.',
      session_id: `${props.sessionId}-test`,
      voice_id: settings.value.voice_id,
      avatar_id: settings.value.avatar_id,
      resolution: settings.value.resolution
    })
    
    if (response.data.success && response.data.video_url) {
      testVideoUrl.value = response.data.video_url
    } else {
      throw new Error('Не удалось получить тестовое видео')
    }
  } catch (error) {
    console.error('Error generating test video:', error)
    ElMessage.error('Ошибка генерации тестового видео')
  } finally {
    testLoading.value = false
  }
}

const closeTestDialog = () => {
  testDialogVisible.value = false
  testVideoUrl.value = ''
  testLoading.value = false
}

// Event handlers
const onAvatarChange = () => {
  emit('settings-changed', settings.value)
}

const onVoiceChange = () => {
  emit('settings-changed', settings.value)
}

const onResolutionChange = () => {
  emit('settings-changed', settings.value)
}

const onSpeechRateChange = () => {
  emit('settings-changed', settings.value)
}

const onQualityChange = () => {
  emit('settings-changed', settings.value)
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    loadCharacters(),
    loadVoices(),
    loadCurrentSettings()
  ])
})

// Watchers
watch(settings, (newSettings) => {
  emit('settings-changed', newSettings)
}, { deep: true })
</script>

<style scoped>
.avatar-settings {
  max-width: 600px;
  margin: 0 auto;
}

.settings-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
}

.settings-form {
  padding: 20px 0;
}

.character-option {
  display: flex;
  align-items: center;
  gap: 12px;
}

.character-preview {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  object-fit: cover;
}

.character-info {
  flex: 1;
}

.character-name {
  font-weight: 500;
  color: #333;
}

.character-type {
  font-size: 12px;
  color: #666;
  text-transform: capitalize;
}

.voice-option {
  display: flex;
  align-items: center;
  gap: 12px;
}

.voice-icon {
  font-size: 20px;
  color: #409eff;
}

.voice-info {
  flex: 1;
}

.voice-name {
  font-weight: 500;
  color: #333;
}

.voice-details {
  font-size: 12px;
  color: #666;
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 12px;
  color: #666;
}

.preview-container {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.character-preview-large {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.preview-image {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #409eff;
}

.preview-info h4 {
  margin: 0;
  color: #333;
}

.preview-info p {
  margin: 4px 0 0 0;
  color: #666;
  font-size: 14px;
}

.preview-placeholder {
  color: #999;
}

.preview-placeholder .el-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.test-video-container {
  text-align: center;
}

.test-video {
  width: 100%;
  max-width: 600px;
  border-radius: 8px;
}

.test-loading {
  text-align: center;
  padding: 40px;
}

.loading-icon {
  font-size: 48px;
  margin-bottom: 16px;
  animation: spin 2s linear infinite;
}

.test-placeholder {
  text-align: center;
  padding: 40px;
  color: #666;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .avatar-settings {
    max-width: 100%;
  }
  
  .settings-form {
    padding: 10px 0;
  }
}
</style>
