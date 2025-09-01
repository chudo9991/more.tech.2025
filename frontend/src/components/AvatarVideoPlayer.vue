<template>
  <div class="avatar-video-player">
    <!-- Статус загрузки -->
    <div v-if="loading" class="loading-container">
      <el-icon class="loading-icon"><Loading /></el-icon>
      <p>Генерация видео аватара...</p>
      <el-progress 
        :percentage="progress" 
        :status="progressStatus"
        :stroke-width="8"
      />
      <p class="loading-text">{{ loadingText }}</p>
    </div>

    <!-- Видео плеер -->
    <div v-else-if="videoUrl" class="video-container">
      <video
        ref="videoPlayer"
        :src="videoUrl"
        controls
        autoplay
        class="video-player"
        @loadeddata="onVideoLoaded"
        @error="onVideoError"
      >
        Ваш браузер не поддерживает видео.
      </video>
      
      <!-- Информация о видео -->
      <div class="video-info">
        <h4>Видео аватара</h4>
        <p><strong>Текст:</strong> {{ videoText }}</p>
        <p><strong>Голос:</strong> {{ voiceName }}</p>
        <p><strong>Персонаж:</strong> {{ avatarName }}</p>
        <p><strong>Разрешение:</strong> {{ resolution }}p</p>
      </div>

      <!-- Контролы -->
      <div class="video-controls">
        <el-button @click="replay" type="primary" :icon="Refresh">
          Повторить
        </el-button>
        <el-button @click="download" type="success" :icon="Download">
          Скачать
        </el-button>
        <el-button @click="share" type="info" :icon="Share">
          Поделиться
        </el-button>
      </div>
    </div>

    <!-- Ошибка -->
    <div v-else-if="error" class="error-container">
      <el-icon class="error-icon"><Warning /></el-icon>
      <h3>Ошибка генерации видео</h3>
      <p>{{ error }}</p>
      <el-button @click="retry" type="primary" :icon="Refresh">
        Попробовать снова
      </el-button>
    </div>

    <!-- Пустое состояние -->
    <div v-else class="empty-container">
      <el-icon class="empty-icon"><VideoCamera /></el-icon>
      <h3>Видео аватара</h3>
      <p>Здесь будет отображаться сгенерированное видео аватара</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Loading, Refresh, Download, Share, Warning, VideoCamera } from '@element-plus/icons-vue'
import axios from 'axios'

// Props
const props = defineProps({
  sessionId: {
    type: String,
    required: true
  },
  text: {
    type: String,
    default: ''
  },
  voiceId: {
    type: String,
    default: null
  },
  avatarId: {
    type: String,
    default: null
  },
  resolution: {
    type: Number,
    default: 720
  }
})

// Emits
const emit = defineEmits(['video-loaded', 'video-error', 'generation-complete'])

// Reactive data
const loading = ref(false)
const progress = ref(0)
const progressStatus = ref('')
const loadingText = ref('Подготовка к генерации...')
const videoUrl = ref('')
const error = ref('')
const videoPlayer = ref(null)

// Computed
const videoText = computed(() => props.text || 'Текст не указан')
const voiceName = computed(() => {
  // В реальном приложении здесь была бы маппинг ID -> имя
  return props.voiceId || 'По умолчанию'
})
const avatarName = computed(() => {
  // В реальном приложении здесь была бы маппинг ID -> имя
  return props.avatarId || 'По умолчанию'
})
const resolution = computed(() => props.resolution)

// Methods
const generateVideo = async () => {
  if (!props.text) {
    ElMessage.warning('Текст для генерации не указан')
    return
  }

  loading.value = true
  progress.value = 0
  progressStatus.value = ''
  error.value = ''
  videoUrl.value = ''

  try {
    // Этап 1: Подготовка
    progress.value = 10
    loadingText.value = 'Подготовка к генерации...'
    await new Promise(resolve => setTimeout(resolve, 500))

    // Этап 2: Генерация TTS
    progress.value = 30
    loadingText.value = 'Генерация речи...'
    await new Promise(resolve => setTimeout(resolve, 1000))

    // Этап 3: Генерация видео
    progress.value = 60
    loadingText.value = 'Генерация видео аватара...'
    
    const response = await axios.post('/api/v1/avatar/generate', {
      text: props.text,
      session_id: props.sessionId,
      voice_id: props.voiceId,
      avatar_id: props.avatarId,
      resolution: props.resolution
    })

    if (response.data.success && response.data.video_url) {
      progress.value = 100
      progressStatus.value = 'success'
      loadingText.value = 'Готово!'
      
      await new Promise(resolve => setTimeout(resolve, 500))
      
      videoUrl.value = response.data.video_url
      loading.value = false
      
      emit('generation-complete', {
        videoUrl: response.data.video_url,
        sessionId: props.sessionId,
        text: props.text
      })
      
      ElMessage.success('Видео аватара успешно сгенерировано!')
    } else {
      throw new Error('Не удалось получить URL видео')
    }

  } catch (err) {
    console.error('Error generating video:', err)
    error.value = err.response?.data?.detail || err.message || 'Неизвестная ошибка'
    loading.value = false
    progressStatus.value = 'exception'
    
    emit('video-error', error.value)
    ElMessage.error('Ошибка при генерации видео аватара')
  }
}

const onVideoLoaded = () => {
  emit('video-loaded', {
    videoUrl: videoUrl.value,
    sessionId: props.sessionId
  })
}

const onVideoError = (event) => {
  console.error('Video error:', event)
  error.value = 'Ошибка загрузки видео'
  emit('video-error', error.value)
}

const replay = () => {
  if (videoPlayer.value) {
    videoPlayer.value.currentTime = 0
    videoPlayer.value.play()
  }
}

const download = async () => {
  if (!videoUrl.value) return
  
  try {
    const link = document.createElement('a')
    link.href = videoUrl.value
    link.download = `avatar-video-${props.sessionId}.mp4`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    ElMessage.success('Начата загрузка видео')
  } catch (err) {
    console.error('Download error:', err)
    ElMessage.error('Ошибка при загрузке видео')
  }
}

const share = () => {
  if (!videoUrl.value) return
  
  if (navigator.share) {
    navigator.share({
      title: 'Видео аватара',
      text: 'Посмотрите на это видео аватара!',
      url: videoUrl.value
    })
  } else {
    // Fallback: копирование ссылки
    navigator.clipboard.writeText(videoUrl.value)
    ElMessage.success('Ссылка на видео скопирована в буфер обмена')
  }
}

const retry = () => {
  generateVideo()
}

// Lifecycle
onMounted(() => {
  if (props.text) {
    generateVideo()
  }
})

onUnmounted(() => {
  // Cleanup
})
</script>

<style scoped>
.avatar-video-player {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  border-radius: 12px;
  overflow: hidden;
  background: #f8f9fa;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.loading-container {
  padding: 40px 20px;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.loading-icon {
  font-size: 48px;
  margin-bottom: 16px;
  animation: spin 2s linear infinite;
}

.loading-text {
  margin-top: 16px;
  font-size: 14px;
  opacity: 0.8;
}

.video-container {
  background: #000;
}

.video-player {
  width: 100%;
  height: auto;
  max-height: 500px;
  display: block;
}

.video-info {
  padding: 20px;
  background: white;
}

.video-info h4 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 18px;
}

.video-info p {
  margin: 8px 0;
  color: #666;
  font-size: 14px;
}

.video-controls {
  padding: 16px 20px;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
  display: flex;
  gap: 12px;
  justify-content: center;
}

.error-container {
  padding: 40px 20px;
  text-align: center;
  background: #fff5f5;
  color: #c53030;
}

.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.error-container h3 {
  margin: 0 0 16px 0;
  color: #c53030;
}

.empty-container {
  padding: 60px 20px;
  text-align: center;
  background: white;
  color: #666;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  color: #ddd;
}

.empty-container h3 {
  margin: 0 0 16px 0;
  color: #333;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .avatar-video-player {
    max-width: 100%;
  }
  
  .video-controls {
    flex-direction: column;
  }
  
  .video-controls .el-button {
    width: 100%;
  }
}
</style>
