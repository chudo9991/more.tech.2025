<template>
  <div class="session-detail">
    <div v-loading="loading">
      <!-- Session Overview -->
      <el-card class="overview-card">
        <template #header>
          <div class="card-header">
            <span>Session Overview</span>
            <div class="header-actions">
              <el-button size="small" @click="exportSession">
                <el-icon><Download /></el-icon>
                Export
              </el-button>
              <el-button size="small" type="primary" @click="refreshData">
                <el-icon><Refresh /></el-icon>
                Refresh
              </el-button>
            </div>
          </div>
        </template>
        
        <el-row :gutter="20" v-if="sessionData">
          <el-col :span="8">
            <div class="info-item">
              <label>Session ID:</label>
              <span>{{ sessionData.session_id }}</span>
            </div>
            <div class="info-item">
              <label>Status:</label>
              <el-tag :type="getStatusType(sessionData.status)">
                {{ getStatusLabel(sessionData.status) }}
              </el-tag>
            </div>
            <div class="info-item">
              <label>Progress:</label>
              <span>{{ sessionData.answered_questions }}/{{ sessionData.total_questions }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label>Completion Rate:</label>
              <span>{{ (sessionData.completion_rate * 100).toFixed(1) }}%</span>
            </div>
            <div class="info-item">
              <label>Total Score:</label>
              <span>{{ (sessionData.total_score * 100).toFixed(1) }}%</span>
            </div>
            <div class="info-item">
              <label>Pass Rate:</label>
              <span>{{ (sessionData.pass_rate * 100).toFixed(1) }}%</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label>Started:</label>
              <span>{{ formatDate(sessionData.started_at) }}</span>
            </div>
            <div class="info-item">
              <label>Completed:</label>
              <span>{{ formatDate(sessionData.completed_at) || 'In Progress' }}</span>
            </div>
            <div class="info-item">
              <label>Duration:</label>
              <span>{{ sessionData.duration || 'N/A' }}</span>
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- Questions and Answers -->
      <el-card class="questions-card">
        <template #header>
          <span>Questions & Answers</span>
        </template>
        
        <div v-if="sessionData && sessionData.questions.length > 0">
          <div 
            v-for="(question, index) in sessionData.questions" 
            :key="question.question_id"
            class="question-item"
          >
            <div class="question-header">
              <h3>Question {{ index + 1 }}</h3>
              <div class="question-score">
                <span class="score-label">Score:</span>
                <span class="score-value">{{ (question.avg_score * 100).toFixed(1) }}%</span>
              </div>
            </div>
            
            <div class="question-content">
              <div class="question-text">
                <strong>Question:</strong> {{ question.question_text }}
              </div>
              
              <div class="answer-section">
                <div class="answer-text">
                  <strong>Answer:</strong> {{ question.answer_text }}
                </div>
                
                <div class="answer-metrics">
                  <el-row :gutter="20">
                    <el-col :span="6">
                      <div class="metric">
                        <label>Confidence:</label>
                        <span>{{ (question.transcription_confidence * 100).toFixed(1) }}%</span>
                      </div>
                    </el-col>
                    <el-col :span="6">
                      <div class="metric">
                        <label>Pre-answer Pause:</label>
                        <span>{{ question.pre_answer_pause_s.toFixed(1) }}s</span>
                      </div>
                    </el-col>
                    <el-col :span="6">
                      <div class="metric">
                        <label>Speech Rate:</label>
                        <span>{{ question.speech_rate_wpm.toFixed(0) }} WPM</span>
                      </div>
                    </el-col>
                    <el-col :span="6">
                      <div class="metric">
                        <label>Audio:</label>
                        <el-button 
                          size="small" 
                          type="primary" 
                          @click="playAudio(question.audio_url)"
                          :disabled="!question.audio_url"
                        >
                          <el-icon><VideoPlay /></el-icon>
                          Play
                        </el-button>
                      </div>
                    </el-col>
                  </el-row>
                </div>
                
                <!-- Criteria Scores -->
                <div class="criteria-scores" v-if="question.scores.length > 0">
                  <h4>Criteria Scores:</h4>
                  <el-row :gutter="20">
                    <el-col 
                      :span="8" 
                      v-for="score in question.scores" 
                      :key="score.criterion_id"
                    >
                      <div class="criterion-score">
                        <div class="criterion-header">
                          <span class="criterion-name">{{ score.criterion_id }}</span>
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

      <!-- Summary -->
      <el-card class="summary-card" v-if="sessionData && sessionData.questions.length > 0">
        <template #header>
          <span>Performance Summary</span>
        </template>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <h4>Top Performing Questions:</h4>
            <ul class="summary-list">
              <li 
                v-for="question in sessionData.top_performing_questions" 
                :key="question.question_text"
              >
                {{ question.question_text }} ({{ question.avg_score }})
              </li>
            </ul>
          </el-col>
          <el-col :span="12">
            <h4>Areas for Improvement:</h4>
            <ul class="summary-list">
              <li 
                v-for="area in sessionData.areas_for_improvement" 
                :key="area"
              >
                {{ area }}
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

// Methods
const loadSessionData = async () => {
  try {
    loading.value = true
    const response = await hrStore.fetchSessionResults(props.sessionId)
    sessionData.value = response
  } catch (error) {
    ElMessage.error('Failed to load session data')
    console.error('Error loading session data:', error)
  } finally {
    loading.value = false
  }
}

const refreshData = async () => {
  await loadSessionData()
  ElMessage.success('Data refreshed')
}

const exportSession = async () => {
  try {
    const response = await hrStore.exportSession(props.sessionId, 'csv')
    downloadFile(response.content, response.filename)
    ElMessage.success('Session exported successfully')
  } catch (error) {
    ElMessage.error('Failed to export session')
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
    const audio = new Audio(audioUrl)
    audio.play().catch(error => {
      console.error('Error playing audio:', error)
      ElMessage.error('Failed to play audio')
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
    created: 'Created',
    in_progress: 'In Progress',
    completed: 'Completed',
    failed: 'Failed'
  }
  return labels[status] || status
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString()
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
