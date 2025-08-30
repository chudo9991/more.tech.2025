<template>
  <div class="session-detail">
    <div v-loading="loading">
      <!-- Session Overview -->
      <el-card class="overview-card">
        <template #header>
          <div class="card-header">
            <span>Обзор сессии</span>
            <div class="header-actions">
              <el-button size="small" @click="exportSession">
                <el-icon><Download /></el-icon>
                Экспорт
              </el-button>
              <el-button size="small" type="primary" @click="refreshData">
                <el-icon><Refresh /></el-icon>
                Обновить
              </el-button>
            </div>
          </div>
        </template>
        
        <el-row :gutter="20" v-if="sessionData">
          <el-col :span="8">
            <div class="info-item">
              <label>ID Сессии:</label>
              <span>{{ sessionData.session_id }}</span>
            </div>
            <div class="info-item">
              <label>Вакансия:</label>
              <div class="vacancy-info">
                <span>{{ sessionData.vacancy_title || 'Не указана' }}</span>
                <el-tag v-if="sessionData.vacancy_code" type="info" size="small" style="margin-left: 8px;">
                  {{ sessionData.vacancy_code }}
                </el-tag>
              </div>
            </div>
            <div class="info-item">
              <label>Статус:</label>
              <el-tag :type="getStatusType(sessionData.status)">
                {{ getStatusLabel(sessionData.status) }}
              </el-tag>
            </div>
            <div class="info-item">
              <label>Прогресс:</label>
              <span>{{ sessionData.current_step }}/{{ sessionData.qa_records?.length || 0 }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label>Процент завершения:</label>
              <span>{{ sessionData.qa_records ? ((sessionData.qa_records.length / sessionData.current_step) * 100).toFixed(1) : 0 }}%</span>
            </div>
            <div class="info-item">
              <label>Общий балл:</label>
              <span>{{ sessionData.total_score ? (sessionData.total_score * 100).toFixed(1) : 0 }}%</span>
            </div>
            <div class="info-item">
              <label>Процент прохождения:</label>
              <span>{{ sessionData.qa_records ? ((sessionData.qa_records.filter(q => q.passed).length / sessionData.qa_records.length) * 100).toFixed(1) : 0 }}%</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label>Начато:</label>
              <span>{{ formatDate(sessionData.started_at) }}</span>
            </div>
            <div class="info-item">
              <label>Завершено:</label>
              <span>{{ formatDate(sessionData.finished_at) || 'В процессе' }}</span>
            </div>
            <div class="info-item">
              <label>Длительность:</label>
              <span>{{ sessionData.started_at && sessionData.finished_at ? formatDuration(sessionData.started_at, sessionData.finished_at) : 'Н/Д' }}</span>
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- Questions and Answers -->
      <el-card class="questions-card">
        <template #header>
          <span>Вопросы и ответы</span>
        </template>
        
        <div v-if="sessionData && sessionData.qa_records && sessionData.qa_records.length > 0">
          <div 
            v-for="(qa, index) in sessionData.qa_records" 
            :key="qa.id"
            class="question-item"
          >
            <div class="question-header">
              <h3>Вопрос {{ qa.step_no }}</h3>
              <div class="question-score">
                <span class="score-label">Балл:</span>
                <span class="score-value">{{ qa.scores && qa.scores.length > 0 ? (qa.scores.reduce((sum, s) => sum + s.score, 0) / qa.scores.length * 100).toFixed(1) : 0 }}%</span>
              </div>
            </div>
            
            <div class="question-content">
              <div class="question-text">
                <strong>Вопрос:</strong> {{ qa.question_text }}
              </div>
              
              <div class="answer-section">
                <div class="answer-text">
                  <strong>Ответ:</strong> {{ qa.answer_text }}
                </div>
                
                <div class="answer-metrics">
                  <el-row :gutter="20">
                    <el-col :span="6">
                      <div class="metric">
                        <label>Тон:</label>
                        <span>{{ qa.tone || 'Н/Д' }}</span>
                      </div>
                    </el-col>
                    <el-col :span="6">
                      <div class="metric">
                        <label>Пройдено:</label>
                        <el-tag :type="qa.passed ? 'success' : 'danger'">
                          {{ qa.passed ? 'Да' : 'Нет' }}
                        </el-tag>
                      </div>
                    </el-col>
                    <el-col :span="6">
                      <div class="metric">
                        <label>Создано:</label>
                        <span>{{ formatDate(qa.created_at) }}</span>
                      </div>
                    </el-col>
                    <el-col :span="6">
                      <div class="metric">
                        <label>Аудио:</label>
                        <el-button 
                          size="small" 
                          type="primary" 
                          @click="playAudio(qa.audio_url)"
                          :disabled="!qa.audio_url"
                        >
                          <el-icon><VideoPlay /></el-icon>
                          Воспроизвести
                        </el-button>
                      </div>
                    </el-col>
                  </el-row>
                </div>
                
                <!-- Criteria Scores -->
                <div class="criteria-scores" v-if="qa.scores && qa.scores.length > 0">
                  <h4>Criteria Scores:</h4>
                  <el-row :gutter="20">
                    <el-col 
                      :span="8" 
                      v-for="score in qa.scores" 
                      :key="score.criterion_id"
                    >
                      <div class="criterion-score">
                        <div class="criterion-header">
                          <span class="criterion-name">{{ score.criterion_name }}</span>
                          <span class="criterion-value">{{ (score.score * 100).toFixed(1) }}%</span>
                        </div>
                        <div class="criterion-evidence" v-if="score.evidence">
                          <small>{{ score.evidence }}</small>
                        </div>
                      </div>
                    </el-col>
                  </el-row>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else class="no-questions">
          <el-empty description="No questions answered yet" />
        </div>
      </el-card>

      <!-- Chat Messages -->
      <el-card class="messages-card">
        <template #header>
          <span>Сообщения чата</span>
        </template>
        
        <div v-if="messages && messages.length > 0">
          <div 
            v-for="message in messages" 
            :key="message.id"
            class="message-item"
          >
            <div class="message-header">
              <span class="message-type">{{ message.message_type === 'user' ? '👤 Кандидат' : '🤖 Аватар' }}</span>
              <span class="message-time">{{ formatDate(message.timestamp) }}</span>
            </div>
            
            <div class="message-content">
              <div class="message-text">{{ message.text }}</div>
              
              <div class="message-metrics" v-if="message.audio_url || message.transcription_confidence">
                <el-row :gutter="20">
                  <el-col :span="6" v-if="message.audio_url">
                    <div class="metric">
                      <label>Аудио:</label>
                      <el-button 
                        size="small" 
                        type="primary" 
                        @click="playAudio(message.audio_url)"
                      >
                        <el-icon><VideoPlay /></el-icon>
                        Воспроизвести
                      </el-button>
                    </div>
                  </el-col>
                  <el-col :span="6" v-if="message.transcription_confidence">
                    <div class="metric">
                      <label>Уверенность STT:</label>
                      <span>{{ (message.transcription_confidence * 100).toFixed(1) }}%</span>
                    </div>
                  </el-col>
                  <el-col :span="6" v-if="message.tone_analysis">
                    <div class="metric">
                      <label>Тон голоса:</label>
                      <span>{{ getToneLabel(message.tone_analysis) }}</span>
                    </div>
                  </el-col>
                </el-row>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else class="no-messages">
          <el-empty description="Сообщений пока нет" />
        </div>
      </el-card>

      <!-- Summary -->
      <el-card class="summary-card" v-if="sessionData && sessionData.qa_records && sessionData.qa_records.length > 0">
        <template #header>
          <span>Performance Summary</span>
        </template>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <h4>Session Overview:</h4>
            <ul class="summary-list">
              <li>Total Questions: {{ sessionData.qa_records.length }}</li>
              <li>Completed: {{ sessionData.current_step }}</li>
              <li>Passed: {{ sessionData.qa_records.filter(q => q.passed).length }}</li>
              <li>Average Score: {{ sessionData.total_score ? (sessionData.total_score * 100).toFixed(1) : 0 }}%</li>
            </ul>
          </el-col>
          <el-col :span="12">
            <h4>Criteria Performance:</h4>
            <ul class="summary-list">
              <li v-for="qa in sessionData.qa_records" :key="qa.id">
                Question {{ qa.step_no }}: {{ qa.scores && qa.scores.length > 0 ? (qa.scores.reduce((sum, s) => sum + s.score, 0) / qa.scores.length * 100).toFixed(1) : 0 }}%
              </li>
            </ul>
          </el-col>
        </el-row>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Download, Refresh, VideoPlay } from '@element-plus/icons-vue'
import { useHRStore } from '@/stores/hr'

const props = defineProps({
  sessionId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['close'])

const hrStore = useHRStore()
const loading = ref(false)
const sessionData = ref(null)
const messages = ref([])

// Methods
const loadSessionData = async () => {
  try {
    loading.value = true
    const response = await hrStore.fetchSessionResults(props.sessionId)
    sessionData.value = response
    
    // Load messages
    await loadMessages()
  } catch (error) {
    ElMessage.error('Failed to load session data')
    console.error('Error loading session data:', error)
  } finally {
    loading.value = false
  }
}

const loadMessages = async () => {
  try {
    console.log('Loading messages for session:', props.sessionId)
    const response = await fetch(`/api/v1/sessions/messages?session_id=${props.sessionId}`)
    if (response.ok) {
      const data = await response.json()
      messages.value = data.messages || []
      console.log('Loaded messages:', messages.value.length, 'messages')
    } else {
      console.error('Failed to load messages:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('Error loading messages:', error)
  }
}

const refreshData = async () => {
  await loadSessionData()
  await loadMessages()
  ElMessage.success('Данные обновлены')
}

const exportSession = async () => {
  try {
    const response = await hrStore.exportSession(props.sessionId, 'csv')
    downloadFile(response.content, response.filename)
    ElMessage.success('Сессия успешно экспортирована')
  } catch (error) {
    ElMessage.error('Не удалось экспортировать сессию')
    console.error('Error exporting session:', error)
  }
}

const downloadFile = (content, filename) => {
  const blob = new Blob([content], { type: 'text/csv' })
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  window.URL.revokeObjectURL(url)
  document.body.removeChild(a)
}

const playAudio = (audioUrl) => {
  if (audioUrl) {
    // Extract filename from MinIO URL (format: minio://audio-files/session_id_filename)
    const urlParts = audioUrl.split('/')
    const fullFilename = urlParts[urlParts.length - 1]
    
    // Remove session_id prefix from filename and clean up the filename
    const sessionId = props.sessionId
    let filename = fullFilename.replace(`${sessionId}_`, '')
    
    // Remove the codecs part from filename if present
    if (filename.includes(';codecs=')) {
      filename = filename.split(';codecs=')[0]
    }
    
    // Create proper audio URL
    const audioEndpoint = `/api/v1/sessions/audio/${sessionId}/${filename}`
    console.log('Playing audio from:', audioEndpoint)
    console.log('Original audioUrl:', audioUrl)
    console.log('Extracted filename:', filename)
    
    const audio = new Audio(audioEndpoint)
    audio.play().catch(error => {
      console.error('Error playing audio:', error)
      if (error.name === 'NotSupportedError' || error.message.includes('404')) {
        ElMessage.warning('Аудио запись недоступна (файл не найден)')
      } else {
        ElMessage.error('Не удалось воспроизвести аудио')
      }
    })
  }
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

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString()
}

const formatDuration = (startDate, endDate) => {
  if (!startDate || !endDate) return 'N/A'
  const start = new Date(startDate)
  const end = new Date(endDate)
  const diffMs = end - start
  const diffMins = Math.floor(diffMs / 60000)
  const diffSecs = Math.floor((diffMs % 60000) / 1000)
  return `${diffMins}m ${diffSecs}s`
}

const getToneLabel = (tone) => {
  const labels = {
    positive: '😊 Позитивный',
    neutral: '😐 Нейтральный',
    concerned: '😟 Обеспокоенный',
    excited: '🤩 Восторженный',
    confused: '😕 Растерянный',
    confident: '😎 Уверенный'
  }
  return labels[tone] || tone
}

// Watchers
watch(() => props.sessionId, (newId) => {
  if (newId) {
    loadSessionData()
  }
})

// Lifecycle
onMounted(() => {
  if (props.sessionId) {
    loadSessionData()
  }
})
</script>

<style scoped>
.session-detail {
  padding: 20px;
}

.overview-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.info-item {
  margin-bottom: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-item label {
  font-weight: 600;
  color: #606266;
}

.questions-card {
  margin-bottom: 20px;
}

.question-item {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin-bottom: 20px;
  padding: 20px;
  background-color: #fafafa;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.question-header h3 {
  margin: 0;
  color: #303133;
}

.question-score {
  display: flex;
  align-items: center;
  gap: 10px;
}

.score-label {
  font-weight: 600;
  color: #606266;
}

.score-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: #409eff;
}

.question-content {
  background-color: white;
  padding: 15px;
  border-radius: 6px;
}

.question-text {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.answer-section {
  border-top: 1px solid #ebeef5;
  padding-top: 15px;
}

.answer-text {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f0f9ff;
  border-radius: 4px;
  border-left: 4px solid #409eff;
}

.answer-metrics {
  margin-bottom: 15px;
}

.metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.metric label {
  font-weight: 600;
  color: #606266;
  font-size: 0.9rem;
}

.criteria-scores {
  border-top: 1px solid #ebeef5;
  padding-top: 15px;
}

.criteria-scores h4 {
  margin-bottom: 15px;
  color: #303133;
}

.criterion-score {
  background-color: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 10px;
}

.criterion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.criterion-name {
  font-weight: 600;
  color: #303133;
}

.criterion-value {
  font-weight: bold;
  color: #409eff;
}

.criterion-evidence {
  color: #909399;
  font-style: italic;
}

.summary-card {
  margin-bottom: 20px;
}

.messages-card {
  margin-bottom: 20px;
}

.message-item {
  background-color: white;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 15px;
  border: 1px solid #ebeef5;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.message-type {
  font-weight: 600;
  color: #303133;
}

.message-time {
  font-size: 0.9rem;
  color: #909399;
}

.message-content {
  margin-bottom: 10px;
}

.message-text {
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 10px;
  line-height: 1.5;
}

.message-metrics {
  margin-top: 10px;
}

.no-messages {
  text-align: center;
  padding: 40px;
  color: #909399;
}

.summary-list {
  list-style: none;
  padding: 0;
}

.summary-list li {
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.summary-list li:last-child {
  border-bottom: none;
}

.no-questions {
  text-align: center;
  padding: 40px;
}
</style>
