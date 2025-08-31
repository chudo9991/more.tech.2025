<template>
  <div class="candidate-interview">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>Сессия ИИ-Интервью</h1>
          <div class="session-info" v-if="sessionData">
            <span>Сессия: {{ sessionData.session_id }}</span>
            <span>Статус: {{ getStatusLabel(sessionData.status) }}</span>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <el-row :gutter="20">
          <!-- Avatar Section -->
          <el-col :span="6">
            <el-card class="avatar-card">
              <template #header>
                <span>Аватар интервьюера</span>
              </template>
              
              <div class="avatar-container">
                <div class="rtsp-placeholder">
                  <el-icon><VideoCamera /></el-icon>
                  <span>Тут будет RTSP трансляция AI-аватара</span>
                  <small>Подключение к внешнему сервису генерации аватаров</small>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <!-- Vacancy Info Section -->
          <el-col :span="6" v-if="currentQuestion?.vacancy_context">
            <el-card class="vacancy-info-card">
              <template #header>
                <span>Информация о вакансии</span>
              </template>
              
              <div class="vacancy-info">
                <div class="vacancy-title">
                  <h4>{{ currentQuestion.vacancy_context.title }}</h4>
                  <el-tag v-if="currentQuestion.vacancy_context.vacancy_code" type="info" size="small">
                    {{ currentQuestion.vacancy_context.vacancy_code }}
                  </el-tag>
                </div>
                
                <div class="vacancy-details">
                  <div v-if="currentQuestion.vacancy_context.requirements" class="detail-item">
                    <strong>Требования:</strong>
                    <p>{{ currentQuestion.vacancy_context.requirements }}</p>
                  </div>
                  
                  <div v-if="currentQuestion.vacancy_context.experience_required" class="detail-item">
                    <strong>Опыт:</strong>
                    <p>{{ currentQuestion.vacancy_context.experience_required }}</p>
                  </div>
                  
                  <div v-if="currentQuestion.vacancy_context.education_level" class="detail-item">
                    <strong>Образование:</strong>
                    <p>{{ currentQuestion.vacancy_context.education_level }}</p>
                  </div>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <!-- Chat Section -->
          <el-col :span="currentQuestion?.vacancy_context ? 12 : 18">
            <el-card class="chat-card">
              <template #header>
                <div class="chat-controls">
                  <!-- Code Input Section -->
                  <div v-if="!interviewStarted && !resumeLinked" class="code-input-section">
                    <div class="code-input-wrapper">
                      <el-input
                        v-model="interviewCode"
                        placeholder="Введите код интервью (6 цифр)"
                        maxlength="6"
                        style="width: 200px; margin-right: 10px;"
                        @keyup.enter="validateCode"
                      >
                        <template #prefix>
                          <el-icon><Key /></el-icon>
                        </template>
                      </el-input>
                      <el-button 
                        type="primary" 
                        @click="validateCode"
                        :loading="validatingCode"
                      >
                        Подтвердить код
                      </el-button>
                    </div>
                    <div v-if="codeError" class="code-error">
                      {{ codeError }}
                    </div>
                  </div>
                  
                  <!-- Resume Info -->
                  <div v-if="resumeLinked && linkedResume" class="resume-info">
                    <el-tag type="success" size="large">
                      <el-icon><Document /></el-icon>
                      Резюме привязано: {{ linkedResume.original_filename }}
                    </el-tag>
                  </div>
                  
                  <el-button 
                    type="success" 
                    @click="startInterview"
                    :disabled="interviewStarted || !resumeLinked"
                  >
                    Начать интервью
                  </el-button>
                  <el-button 
                    type="danger" 
                    @click="endInterview"
                    :disabled="!interviewStarted"
                  >
                    Завершить интервью
                  </el-button>
                </div>
              </template>
              
              <!-- Chat Messages -->
              <div class="chat-messages" ref="chatContainer">
                <div 
                  v-for="message in chatMessages" 
                  :key="message.id"
                  :class="['message', message.type]"
                >
                  <div class="message-content">
                    <div class="message-text">{{ message.text }}</div>
                    <div class="message-time">{{ formatTime(message.timestamp) }}</div>
                  </div>
                </div>
              </div>
              
              <!-- Voice Input -->
              <div class="voice-input">
                <!-- Microphone Selection -->
                <div class="microphone-selector" v-if="availableMicrophones.length > 1">
                  <label>Микрофон:</label>
                  <el-select 
                    v-model="selectedMicrophone" 
                    placeholder="Выберите микрофон"
                    size="small"
                    style="width: 200px; margin-left: 10px;"
                  >
                    <el-option
                      v-for="mic in availableMicrophones"
                      :key="mic.deviceId"
                      :label="mic.label || `Микрофон ${mic.deviceId.slice(0, 8)}`"
                      :value="mic.deviceId"
                    />
                  </el-select>
                </div>
                
                <!-- Voice Control Buttons -->
                <div class="voice-controls" style="display: flex; gap: 10px; margin-top: 15px;">
                  <!-- Answer Button -->
                  <el-button 
                    type="primary" 
                    size="large"
                    @click="startRecording"
                    :disabled="isRecording"
                    style="flex: 1; height: 50px; font-size: 16px; font-weight: bold;"
                  >
                    {{ isRecording ? '🎤 Запись...' : '🎤 Ответ' }}
                  </el-button>
                  
                  <!-- Stop Button -->
                  <el-button 
                    type="danger" 
                    size="large"
                    @click="stopRecording"
                    :disabled="!isRecording"
                    style="flex: 1; height: 50px; font-size: 16px; font-weight: bold;"
                  >
                    🛑 Стоп
                  </el-button>
                </div>
                
                <div class="recording-status" v-if="isRecording">
                  <el-progress 
                    :percentage="recordingProgress" 
                    :show-text="false"
                    :stroke-width="4"
                  />
                  <span>{{ recordingDuration }}s</span>
                </div>
              </div>
              

            </el-card>
          </el-col>
        </el-row>
        
        <!-- Interview Progress -->
        <el-card class="progress-card" v-if="sessionData">
          <template #header>
            <span>Прогресс интервью</span>
          </template>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="progress-item">
                <label>Задано вопросов:</label>
                <span>{{ sessionData.current_step }}/{{ sessionData.total_steps }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="progress-item">
                <label>Статус:</label>
                <el-tag :type="getStatusType(sessionData.status)">
                  {{ getStatusLabel(sessionData.status) }}
                </el-tag>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, VideoCamera, Key, Document } from '@element-plus/icons-vue'
import { uploadAudioToMinio } from '@/utils/minio'

// Reactive data
const sessionData = ref(null)
const avatarUrl = ref('')
const avatarLoading = ref(false)
const interviewStarted = ref(false)
const isRecording = ref(false)
const recordingProgress = ref(0)
const recordingDuration = ref(0)

const chatMessages = ref([])
const chatContainer = ref(null)
const currentEmotion = ref('neutral')
const vadStatus = ref('listening') // 'listening', 'speaking', 'silence'
const availableMicrophones = ref([])
const selectedMicrophone = ref('')
const lastVadChange = ref(0) // For debouncing
const currentQuestion = ref(null)

// Interview code variables
const interviewCode = ref('')
const validatingCode = ref(false)
const codeError = ref('')
const resumeLinked = ref(false)
const linkedResume = ref(null)

// Recording state
let recordingInterval = null
let mediaRecorder = null
let audioChunks = []
let audioContext = null
let analyser = null
let microphone = null
let vadInterval = null
let silenceStart = null
const VAD_SILENCE_THRESHOLD = 2000 // 2.0 seconds of silence
const VAD_VOLUME_THRESHOLD = 0.1 // Volume threshold for speech detection
const VAD_DEBOUNCE_TIME = 250 // 500ms debounce

// Computed
const sessionId = ref(null)

// Methods
const validateCode = async () => {
  if (!interviewCode.value || interviewCode.value.length !== 6) {
    codeError.value = 'Код должен содержать 6 цифр'
    return
  }
  
  validatingCode.value = true
  codeError.value = ''
  
  try {
    const response = await fetch('/api/v1/interview-codes/validate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        code: interviewCode.value
      })
    })
    
    const result = await response.json()
    
    if (result.valid) {
      // Load resume data
      const resumeResponse = await fetch(`/api/v1/resumes/${result.resume_id}`)
      if (resumeResponse.ok) {
        linkedResume.value = await resumeResponse.json()
      }
      
      resumeLinked.value = true
      ElMessage.success('Код подтвержден! Резюме привязано к интервью.')
    } else {
      codeError.value = result.message || 'Неверный код'
    }
  } catch (error) {
    codeError.value = 'Ошибка проверки кода'
    console.error('Code validation error:', error)
  } finally {
    validatingCode.value = false
  }
}

const loadSessionData = async () => {
  try {
    // In production, this would fetch from API
    sessionData.value = {
      session_id: sessionId.value,
      status: 'in_progress',
      current_step: 0,
      total_steps: 8,
      total_score: 0.0
    }
  } catch (error) {
    ElMessage.error('Failed to load session data')
    console.error('Error loading session data:', error)
  }
}





const startInterview = async () => {
  try {
    // Create session in database with resume link
    const sessionData = {
      vacancy_id: linkedResume.value?.vacancy_id || 'SWE_BACK_001', // Use resume's vacancy or default
      phone: '+7-999-999-99-99', // Default phone
      email: 'candidate@example.com', // Default email
      resume_id: linkedResume.value?.id // Link to resume
    }
    
    const sessionResponse = await fetch('/api/v1/sessions/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(sessionData)
    })
    
    if (!sessionResponse.ok) {
      throw new Error('Failed to create session')
    }
    
    const sessionResponseData = await sessionResponse.json()
    sessionId.value = sessionResponseData.id
    console.log('Session created with ID:', sessionId.value)
    
    interviewStarted.value = true
    
    // Add welcome message
    addMessage({
      id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      type: 'avatar',
      text: 'Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?',
      timestamp: new Date()
    })
    
    // Save welcome message to database
    await saveMessageToDatabase(
      'Привет! Добро пожаловать на ИИ-интервью. Я здесь, чтобы задать вам несколько вопросов о вашем опыте и навыках. Готовы начать?',
      'avatar',
      `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    )
    
    // Get first question
    await getNextQuestion()
    
    ElMessage.success('Интервью началось')
  } catch (error) {
    ElMessage.error('Не удалось начать интервью')
    console.error('Error starting interview:', error)
  }
}

const getNextQuestion = async () => {
  try {
    if (!sessionId.value) return
    
    // Используем обновленный API endpoint с поддержкой контекстных вопросов
    const response = await fetch(`/api/v1/llm-interview/generate-question`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        session_id: sessionId.value,
        vacancy_id: linkedResume.value?.vacancy_id || 'SWE_BACK_001',
        scenario_node_id: currentQuestion.value?.node_id || null,
        previous_answers: chatMessages.value
          .filter(msg => msg.type === 'user')
          .map(msg => msg.text)
      })
    })
    
    if (response.ok) {
      const result = await response.json()
      const questionData = result.question_data
      
      // Сохраняем информацию о контекстном вопросе
      currentQuestion.value = {
        ...questionData,
        is_contextual: result.is_contextual || false,
        contextual_question_id: questionData.contextual_question_id || null
      }
      
      // Add question to chat (без визуальных отличий для пользователя)
      addMessage({
        id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        type: 'avatar',
        text: questionData.question_text,
        timestamp: new Date(),
        is_contextual: result.is_contextual || false
      })
      
      // Save question to database
      await saveMessageToDatabase(
        questionData.question_text,
        'avatar',
        `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
      )
    }
  } catch (error) {
    console.error('Error getting next question:', error)
  }
}

const endInterview = async () => {
  try {
    // Update session status to completed
    if (sessionId.value) {
      await fetch(`/api/v1/sessions/${sessionId.value}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          status: 'completed',
          finished_at: new Date().toISOString()
        })
      })
    }
    
    interviewStarted.value = false
    
    addMessage({
      id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      type: 'avatar',
      text: 'Спасибо за участие в интервью. Ваши ответы записаны и будут оценены. Удачи!',
      timestamp: new Date()
    })
    
    // Save end message to database
    await saveMessageToDatabase(
      'Спасибо за участие в интервью. Ваши ответы записаны и будут оценены. Удачи!',
      'avatar',
      `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    )
    
    ElMessage.success('Интервью завершено')
  } catch (error) {
    ElMessage.error('Не удалось завершить интервью')
    console.error('Error ending interview:', error)
  }
}



const startRecording = async () => {
  try {
    const constraints = {
      audio: {
        deviceId: selectedMicrophone.value ? { exact: selectedMicrophone.value } : undefined
      }
    }
    console.log('Starting recording with microphone:', selectedMicrophone.value)
    const stream = await navigator.mediaDevices.getUserMedia(constraints)
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []
    
    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data)
    }
    
    mediaRecorder.onstop = async () => {
      // Use the actual MIME type from MediaRecorder
      const mimeType = mediaRecorder.mimeType || 'audio/webm'
      const audioBlob = new Blob(audioChunks, { type: mimeType })
      console.log('VAD: Audio recorded, MIME type:', mimeType, 'Size:', audioBlob.size)
      await processAudioMessage(audioBlob)
    }
    
    // Initialize VAD
    await initializeVAD(stream)
    
    mediaRecorder.start()
    isRecording.value = true
    recordingDuration.value = 0
    recordingProgress.value = 0
    silenceStart = null
    
    // Start timer
    recordingInterval = setInterval(() => {
      recordingDuration.value++
      recordingProgress.value = Math.min((recordingDuration.value / 60) * 100, 100)
      
      if (recordingDuration.value >= 60) {
        stopRecording()
      }
    }, 1000)
    
    // Start VAD monitoring
    startVADMonitoring()
    
  } catch (error) {
    ElMessage.error('Failed to start recording')
    console.error('Error starting recording:', error)
  }
}

const stopRecording = () => {
  if (mediaRecorder && isRecording.value) {
    mediaRecorder.stop()
    mediaRecorder.stream.getTracks().forEach(track => track.stop())
    isRecording.value = false
    
    if (recordingInterval) {
      clearInterval(recordingInterval)
      recordingInterval = null
    }
    
    // Clean up VAD
    stopVADMonitoring()
  }
}

const processAudioMessage = async (audioBlob) => {
  try {
    // Add user message placeholder
    const messageId = `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    addMessage({
      id: messageId,
      type: 'user',
      text: '🎤 [Processing voice message...]',
      timestamp: new Date()
    })
    
    // Generate filename
    const fileName = `recording_${Date.now()}.${audioBlob.type.split('/')[1] || 'webm'}`
    
    console.log('MinIO: Starting audio upload, file:', fileName, 'size:', audioBlob.size)
    
    // Upload audio to MinIO and get transcription in one step
    const formData = new FormData()
    formData.append('audio', audioBlob, fileName)
    formData.append('session_id', sessionId.value)
    
    const sttResponse = await fetch('/api/v1/stt/transcribe-file', {
      method: 'POST',
      body: formData
    })
    
    console.log('VAD: STT response status:', sttResponse.status)
    
    if (!sttResponse.ok) {
      const errorText = await sttResponse.text()
      console.error('VAD: STT service failed:', errorText)
      throw new Error(`STT service failed: ${sttResponse.status} - ${errorText}`)
    }
    
    const sttResult = await sttResponse.json()
    console.log('VAD: STT result:', sttResult)
    const transcribedText = sttResult.text || "Could not transcribe audio"
    
    // Update the message with transcribed text
    const lastMessage = chatMessages.value[chatMessages.value.length - 1]
    lastMessage.text = transcribedText
    
    // Save to database via orchestrator with audio URL
    const audioUrl = sttResult.audio_url || null
    const transcriptionConfidence = sttResult.confidence || null
    await saveMessageToDatabase(transcribedText, 'user', messageId, audioUrl, transcriptionConfidence)
    
    // Analyze tone of voice and update avatar emotion (silently)
    const toneAnalysis = await analyzeToneAndUpdateAvatar(transcribedText)
    
    // Analyze answer and save to QA table if we have current question
    if (currentQuestion.value?.question_text) {
      await analyzeAndSaveAnswer(
        currentQuestion.value.question_text,
        transcribedText,
        audioUrl,
        currentQuestion.value.question_id || 'unknown'
      )
    }
    
    // Get avatar response
    await getAvatarResponse(transcribedText)
    
    // Если это был контекстный вопрос, отмечаем его как использованный
    if (currentQuestion.value?.is_contextual && currentQuestion.value?.contextual_question_id) {
      await markContextualQuestionAsUsed(currentQuestion.value.contextual_question_id)
    }
    
    // Get next question after a short delay
    setTimeout(async () => {
      await getNextQuestion()
    }, 2000)
    
  } catch (error) {
    ElMessage.error('Failed to process audio message')
    console.error('Error processing audio message:', error)
    
    // Update message with error
    const lastMessage = chatMessages.value[chatMessages.value.length - 1]
    lastMessage.text = '❌ Failed to process voice message'
  }
}



const analyzeAndSaveAnswer = async (questionText, answerText, audioUrl, questionId) => {
  try {
    console.log('Analyzing and saving answer:', { questionText, answerText, audioUrl, questionId })
    
    const response = await fetch('/api/v1/llm-interview/analyze-answer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        question_text: questionText,
        answer_text: answerText,
        session_id: sessionId.value,
        audio_url: audioUrl,
        question_id: questionId,
        vacancy_requirements: linkedResume.value?.vacancy_requirements || ''
      })
    })
    
    if (response.ok) {
      const result = await response.json()
      console.log('Answer analysis result:', result)
      
      if (result.qa_record) {
        console.log('QA record saved:', result.qa_record)
      }
    } else {
      console.error('Failed to analyze answer:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('Error analyzing and saving answer:', error)
  }
}

const getAvatarResponse = async (userMessage) => {
  try {
    // In production, this would call LLM service for chat
    const response = await fetch(`/api/v1/llm/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        session_id: sessionId.value,
        message: userMessage
      })
    })
    
    if (response.ok) {
      const result = await response.json()
      
      addMessage({
        id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        type: 'avatar',
        text: result.response,
        timestamp: new Date()
      })
      
      // Avatar emotion is handled internally by the avatar service
      // No need to call external update-emotion endpoint
    } else {
      // Fallback response
      addMessage({
        id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        type: 'avatar',
        text: 'Thank you for your response. Could you please elaborate on that?',
        timestamp: new Date()
      })
    }
  } catch (error) {
    ElMessage.error('Failed to get avatar response')
    console.error('Error getting avatar response:', error)
  }
}

const addMessage = (message) => {
  chatMessages.value.push(message)
  scrollToBottom()
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString()
}

const getStatusType = (status) => {
  const types = {
    created: 'info',
    in_progress: 'warning',
    completed: 'success',
    failed: 'danger'
  }
  return types[status] || 'info'
}

const getStatusLabel = (status) => {
  const labels = {
    created: 'Создана',
    in_progress: 'В процессе',
    completed: 'Завершена',
    failed: 'Ошибка'
  }
  return labels[status] || status
}

const analyzeToneAndUpdateAvatar = async (text) => {
  try {
    // Silently analyze tone for internal avatar emotion updates
    const response = await fetch(`/api/v1/llm/analyze-tone`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: text,
        session_id: sessionId.value
      })
    })
    
    if (response.ok) {
      const result = await response.json()
      const detectedEmotion = result.emotion || 'neutral'
      
      // Update internal emotion state (not visible to candidate)
      currentEmotion.value = detectedEmotion
      
      // Return the tone analysis result for saving to database
      return detectedEmotion
    }
  } catch (error) {
    console.error('Error analyzing tone:', error)
    // Fallback to neutral emotion
    currentEmotion.value = 'neutral'
    return 'neutral'
  }
}

const initializeVAD = async (stream) => {
  try {
    console.log('VAD: Initializing...')
    audioContext = new (window.AudioContext || window.webkitAudioContext)()
    analyser = audioContext.createAnalyser()
    microphone = audioContext.createMediaStreamSource(stream)
    
    analyser.fftSize = 256
    analyser.smoothingTimeConstant = 0.8
    
    microphone.connect(analyser)
    console.log('VAD: Initialized successfully')
  } catch (error) {
    console.error('VAD: Failed to initialize:', error)
  }
}

const startVADMonitoring = () => {
  if (!analyser) {
    console.log('VAD: Analyser not available')
    return
  }
  
  console.log('VAD: Starting monitoring')
  vadStatus.value = 'listening'
  
  vadInterval = setInterval(() => {
    try {
      const dataArray = new Uint8Array(analyser.frequencyBinCount)
      analyser.getByteFrequencyData(dataArray)
      
      // Calculate average volume
      const average = dataArray.reduce((a, b) => a + b) / dataArray.length
      const volume = average / 255
      
      // Only log every 50th measurement to reduce console spam
      if (Math.random() < 0.02) {
        console.log('VAD: Volume:', volume.toFixed(4), 'Threshold:', VAD_VOLUME_THRESHOLD)
      }
      
      const now = Date.now()
      
      if (volume > VAD_VOLUME_THRESHOLD) {
        // Speech detected, reset silence timer
        if (vadStatus.value !== 'speaking' && (now - lastVadChange.value) > VAD_DEBOUNCE_TIME) {
          console.log('VAD: Speech detected')
          vadStatus.value = 'speaking'
          lastVadChange.value = now
        }
        silenceStart = null
      } else {
        // Silence detected
        if (silenceStart === null) {
          silenceStart = Date.now()
          if (vadStatus.value !== 'silence' && (now - lastVadChange.value) > VAD_DEBOUNCE_TIME) {
            console.log('VAD: Silence started')
            vadStatus.value = 'silence'
            lastVadChange.value = now
          }
        } else {
          const silenceDuration = Date.now() - silenceStart
          if (silenceDuration > VAD_SILENCE_THRESHOLD) {
            // Stop recording after silence threshold
            console.log('VAD: Silence threshold reached, stopping recording')
            stopRecording()
          }
        }
      }
    } catch (error) {
      console.error('VAD: Error in monitoring:', error)
    }
  }, 100) // Check every 100ms
}

const stopVADMonitoring = () => {
  if (vadInterval) {
    clearInterval(vadInterval)
    vadInterval = null
  }
  
  if (audioContext) {
    audioContext.close()
    audioContext = null
  }
  
  analyser = null
  microphone = null
  silenceStart = null
  vadStatus.value = 'listening'
}

const saveMessageToDatabase = async (text, type, messageId, audioUrl = null, transcriptionConfidence = null, toneAnalysis = null) => {
  try {
    if (!sessionId.value) {
      console.error('No session ID available, cannot save message')
      return
    }
    
    console.log('Saving message to database:', {
      session_id: sessionId.value,
      message_id: messageId,
      text: text,
      message_type: type,
      audio_url: audioUrl,
      transcription_confidence: transcriptionConfidence,
      tone_analysis: toneAnalysis
    })
    
    const response = await fetch('/api/v1/sessions/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
              body: JSON.stringify({
          session_id: sessionId.value,
          message_id: messageId,
          text: text,
          message_type: type,
          timestamp: new Date().toISOString(),
          audio_url: audioUrl,
          transcription_confidence: transcriptionConfidence,
          tone_analysis: toneAnalysis
        })
    })
    
    if (!response.ok) {
      const errorText = await response.text()
      console.error('Failed to save message to database:', response.status, errorText)
    } else {
      console.log('Message saved successfully')
    }
  } catch (error) {
    console.error('Error saving message to database:', error)
  }
}

const getEmotionLabel = (emotion) => {
  const labels = {
    positive: '😊 Positive',
    neutral: '😐 Neutral',
    concerned: '😟 Concerned',
    excited: '🤩 Excited',
    confused: '😕 Confused',
    confident: '😎 Confident'
  }
  return labels[emotion] || '😐 Neutral'
}

// Lifecycle
onMounted(async () => {
  await loadSessionData()
  await getAvailableMicrophones()
})

const getAvailableMicrophones = async () => {
  try {
    const devices = await navigator.mediaDevices.enumerateDevices()
    const audioInputs = devices.filter(device => device.kind === 'audioinput')
    availableMicrophones.value = audioInputs
    if (audioInputs.length > 0) {
      selectedMicrophone.value = audioInputs[0].deviceId
    }
    console.log('Available microphones:', audioInputs)
  } catch (error) {
    console.error('Error getting microphones:', error)
  }
}

// Метод для отметки контекстного вопроса как использованного
const markContextualQuestionAsUsed = async (questionId) => {
  try {
    const response = await fetch(`/api/v1/llm-interview/contextual-questions/${questionId}/mark-used`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        session_id: sessionId.value
      })
    })
    
    if (!response.ok) {
      console.error('Failed to mark contextual question as used:', response.status)
    }
  } catch (error) {
    console.error('Error marking contextual question as used:', error)
  }
}
</script>

<style scoped>
.candidate-interview {
  height: 100vh;
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
}

.session-info {
  display: flex;
  gap: 20px;
  font-size: 0.9rem;
  color: #606266;
}

.avatar-card {
  height: 600px;
}

.avatar-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  margin-bottom: 20px;
}

.avatar-image {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #409eff;
}

.avatar-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: #909399;
  font-size: 0.9rem;
}

.avatar-placeholder .el-icon {
  font-size: 3rem;
}

.rtsp-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 15px;
  color: #606266;
  font-size: 1rem;
  text-align: center;
  padding: 40px 20px;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  background-color: #fafafa;
  width: 100%;
  height: 100%;
  min-height: 300px;
}

.rtsp-placeholder .el-icon {
  font-size: 4rem;
  color: #409eff;
}

.rtsp-placeholder span {
  font-weight: 600;
  color: #303133;
}

.rtsp-placeholder small {
  color: #909399;
  font-size: 0.85rem;
}

.avatar-controls {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chat-card {
  height: 600px;
}

.chat-controls {
  display: flex;
  gap: 10px;
}

.chat-messages {
  height: 300px;
  overflow-y: auto;
  padding: 10px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  margin-bottom: 20px;
}

.message {
  margin-bottom: 15px;
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.message.avatar {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 10px 15px;
  border-radius: 15px;
  position: relative;
}

.message.user .message-content {
  background-color: #409eff;
  color: white;
}

.message.avatar .message-content {
  background-color: #f5f7fa;
  color: #303133;
}

.message-time {
  font-size: 0.8rem;
  opacity: 0.7;
  margin-top: 5px;
}

.voice-input {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.stop-button {
  margin-top: 5px;
  font-weight: bold;
}



.recording-status {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 200px;
}

.text-input {
  margin-top: 10px;
}

.progress-card {
  margin-top: 20px;
}

.progress-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.progress-item label {
  font-weight: 600;
  color: #606266;
}

.vacancy-info-card {
  height: 600px;
}

.vacancy-info {
  height: 100%;
  overflow-y: auto;
}

.vacancy-title {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #ebeef5;
}

.vacancy-title h4 {
  margin: 0;
  color: #303133;
  font-size: 16px;
  line-height: 1.4;
}

.vacancy-details {
  font-size: 14px;
  color: #606266;
}

.detail-item {
  margin-bottom: 12px;
}

.code-input-section {
  margin-bottom: 15px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.code-input-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
}

.code-error {
  color: #f56c6c;
  font-size: 14px;
  margin-top: 8px;
}

.resume-info {
  margin-bottom: 15px;
}

.resume-info .el-tag {
  font-size: 14px;
  padding: 8px 12px;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.detail-item strong {
  color: #303133;
  display: block;
  margin-bottom: 4px;
}

.detail-item p {
  margin: 0;
  line-height: 1.4;
  color: #606266;
}
</style>
