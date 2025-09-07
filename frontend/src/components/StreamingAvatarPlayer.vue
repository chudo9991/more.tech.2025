<template>
  <div class="streaming-avatar-player">
    <!-- Avatar Video Container -->
    <div class="avatar-video-container">
      <div v-if="!isConnected" class="avatar-placeholder">
        <div class="avatar-placeholder-content">
          <div class="avatar-icon">
            <IconAIAvatar :size="60" />
          </div>
          <h3>AI Аватар</h3>
          <p>Готов к интервью</p>
          <el-button 
            type="primary" 
            size="small"
            @click="connectToAvatar"
            :loading="connecting"
          >
            {{ connecting ? 'Подключение...' : 'Подключить' }}
          </el-button>
        </div>
      </div>
      
      <video 
        v-else-if="streamUrl"
        ref="videoElement"
        :src="streamUrl"
        autoplay
        controls
        preload="metadata"
        class="avatar-video"
        style="width: 100%; height: 100%; object-fit: cover; max-width: 100%; max-height: 100%;"
        @error="handleVideoError"
        @loadstart="handleVideoLoadStart"
        @canplay="handleVideoCanPlay"
        @loadedmetadata="handleVideoLoadedMetadata"
      >
        Ваш браузер не поддерживает видео.
      </video>
      
      <div v-else class="avatar-placeholder">
        <div class="avatar-placeholder-content">
          <div class="avatar-icon">🎭</div>
          <h3>AI Аватар Подключен</h3>
          <p>Готов к интервью</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import IconAIAvatar from '@/components/icons/IconAIAvatar.vue'

// Props
const props = defineProps({
  sessionId: {
    type: String,
    required: true
  }
})

// Expose methods to parent
const setVideoUrl = (url) => {
  if (url) {
    streamUrl.value = url
    isConnected.value = true
    console.log('Video URL set:', url)
  }
}

defineExpose({
  setVideoUrl
})

// Emits
const emit = defineEmits(['avatar-connected', 'avatar-disconnected', 'avatar-question', 'avatar-speak'])

// Reactive data
const streamUrl = ref(null)
const videoElement = ref(null)
const isConnected = ref(false)
const connecting = ref(false)

// Avatar configuration
const avatarId = '68af59a86eeedd0042ca7e27' // Alice (working for video)
const apiBaseUrl = import.meta.env.VITE_API_URL || ''

// Methods
const connectToAvatar = async () => {
  try {
    connecting.value = true
    console.log('Connecting to A2E streaming avatar...')
    
    // Get streaming avatar token from our avatar service
    const tokenResponse = await fetch(`${apiBaseUrl}/api/v1/avatar/streaming/get-token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        avatar_id: avatarId
      })
    })
    
    if (tokenResponse.ok) {
      const result = await tokenResponse.json()
      
          if (result.success && result.stream_url) {
      streamUrl.value = result.stream_url
      isConnected.value = true
      console.log('Connected to A2E streaming avatar:', result.stream_url)
      emit('avatar-connected', { avatarId, sessionId: props.sessionId })
    } else if (result.error === 'streaming_unavailable') {
      // A2E streaming is unavailable - show placeholder
      console.log('A2E streaming unavailable, using placeholder mode')
      isConnected.value = true
      streamUrl.value = null
      emit('avatar-connected', { avatarId: 'placeholder', sessionId: props.sessionId })
    } else {
      // Other error - show placeholder
      console.log('A2E streaming error, using placeholder mode:', result.message)
      isConnected.value = true
      streamUrl.value = null
      emit('avatar-connected', { avatarId: 'placeholder', sessionId: props.sessionId })
    }
    } else {
      // Fallback to placeholder mode
      console.log('Avatar service error, using placeholder mode')
      isConnected.value = true
      streamUrl.value = null
      emit('avatar-connected', { avatarId: 'placeholder', sessionId: props.sessionId })
    }
  } catch (error) {
    console.error('Error connecting to avatar, using placeholder mode:', error)
    // Fallback to placeholder mode
    isConnected.value = true
    streamUrl.value = null
    emit('avatar-connected', { avatarId: 'placeholder', sessionId: props.sessionId })
  } finally {
    connecting.value = false
  }
}

const handleVideoError = (error) => {
  console.error('Video error:', error)
  isConnected.value = false
  emit('avatar-disconnected', { error: error.message })
}

const handleVideoLoadStart = () => {
  console.log('Video loading started')
}

const handleVideoCanPlay = () => {
  console.log('Video can play')
  isConnected.value = true
  emit('avatar-connected', { sessionId: props.sessionId })
}

const handleVideoLoadedMetadata = () => {
  console.log('Video metadata loaded')
  if (videoElement.value) {
    console.log('Video duration:', videoElement.value.duration)
    console.log('Video dimensions:', videoElement.value.videoWidth, 'x', videoElement.value.videoHeight)
    console.log('Video ready state:', videoElement.value.readyState)
  }
}

onMounted(async () => {
  console.log('StreamingAvatarPlayer mounted, connecting to avatar...')
  await connectToAvatar()
})
</script>

<style scoped>
.streaming-avatar-player {
  width: 100%;
  height: 100%;
}

.avatar-video-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
}

.avatar-placeholder-content {
  text-align: center;
  padding: 20px;
}

.avatar-icon {
  font-size: 4rem;
  margin-bottom: 15px;
}

.avatar-placeholder-content h3 {
  margin: 0 0 10px 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.avatar-placeholder-content p {
  margin: 0 0 20px 0;
  font-size: 1rem;
  opacity: 0.9;
}

.avatar-video {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important; /* Изменено с contain на cover для формата 1:1 */
  border-radius: 8px;
  background-color: #f5f5f5;
  max-width: 100% !important;
  max-height: 100% !important;
}
</style>
