<template>
  <div class="streaming-avatar-player">
    <!-- Avatar Video Container -->
    <div class="avatar-video-container">
      <div v-if="!isConnected" class="avatar-placeholder">
        <div class="avatar-placeholder-content">
          <div class="avatar-icon">🤖</div>
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
          <div class="avatar-icon">👩‍💼</div>
          <h3>HR Аватар Светлана</h3>
          <p>D-ID Streaming подключен</p>
          <div class="avatar-status">
            <span class="status-indicator"></span>
            Готова к интервью
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// Props
const props = defineProps({
  sessionId: {
    type: String,
    required: true
  }
})

// Send text to D-ID avatar
const sendTextToAvatar = async (text) => {
  try {
    console.log('Sending text to D-ID avatar:', text)
    
    const response = await fetch(`${apiBaseUrl}/api/v1/avatar/streaming/speak`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        avatar_id: avatarId,
        text: text
      })
    })
    
    if (response.ok) {
      const result = await response.json()
      console.log('Text sent to avatar:', result)
      emit('avatar-speak', { text, result })
    } else {
      console.error('Failed to send text to avatar:', response.status)
    }
  } catch (error) {
    console.error('Error sending text to avatar:', error)
  }
}

// Expose methods to parent
const setVideoUrl = (url) => {
  if (url) {
    streamUrl.value = url
    isConnected.value = true
    console.log('Video URL set:', url)
  }
}

defineExpose({
  setVideoUrl,
  sendTextToAvatar
})

// Emits
const emit = defineEmits(['avatar-connected', 'avatar-disconnected', 'avatar-question', 'avatar-speak'])

// Reactive data
const streamUrl = ref(null)
const videoElement = ref(null)
const isConnected = ref(false)
const connecting = ref(false)

// Avatar configuration
const avatarId = 'did_hr_avatar' // D-ID HR Avatar
const apiBaseUrl = import.meta.env.VITE_API_URL || ''

// Methods
const connectToAvatar = async () => {
  try {
    connecting.value = true
    console.log('Connecting to D-ID streaming avatar...')
    
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
      
      if (result.success) {
        // D-ID streaming session created successfully
        console.log('Connected to D-ID streaming avatar:', result.token)
        
        // For D-ID, we don't get a direct stream_url, so we use placeholder mode
        // but store the session info for later use
        isConnected.value = true
        streamUrl.value = null // D-ID doesn't provide direct stream URL
        
        // Store session info for later use
        window.didSessionInfo = {
          token: result.token,
          stream_id: result.stream_id,
          session_id: result.session_id,
          avatar_id: avatarId
        }
        
        emit('avatar-connected', { 
          avatarId, 
          sessionId: props.sessionId,
          didToken: result.token,
          didStreamId: result.stream_id
        })
        
        // Send initial greeting
        setTimeout(() => {
          sendTextToAvatar("Привет! Меня зовут Светлана, я HR специалист. Готова провести с вами интервью.")
        }, 1000)
        
      } else if (result.error === 'streaming_unavailable') {
        // D-ID streaming is unavailable - show placeholder
        console.log('D-ID streaming unavailable, using placeholder mode')
        isConnected.value = true
        streamUrl.value = null
        emit('avatar-connected', { avatarId: 'placeholder', sessionId: props.sessionId })
      } else {
        // Other error - show placeholder
        console.log('D-ID streaming error, using placeholder mode:', result.message)
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

.avatar-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 10px;
  font-size: 0.9rem;
}

.status-indicator {
  width: 8px;
  height: 8px;
  background-color: #4CAF50;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(76, 175, 80, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0);
  }
}
</style>
