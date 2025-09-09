<template>
  <div class="resume-detail">
    <div class="page-header">
      <h1>Детали резюме</h1>
      <div class="header-buttons">
        <ExportButtons 
          :resume-id="resumeId" 
          @export-completed="handleExportCompleted" 
        />
        <el-button @click="$router.push('/resumes')" icon="ArrowLeft">
          Назад к списку
        </el-button>
      </div>
    </div>
    
    <!-- Loading state -->
    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="10" animated />
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="error-state">
      <el-result
        icon="error"
        title="Ошибка загрузки"
        :sub-title="error"
      >
        <template #extra>
          <el-button type="primary" @click="loadResume">Попробовать снова</el-button>
        </template>
      </el-result>
    </div>
    
    <!-- Resume content -->
    <div v-else-if="resume" class="resume-content">
      <!-- Основная информация -->
      <el-card class="main-info">
        <template #header>
          <span>Основная информация</span>
        </template>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID резюме">
            {{ resume.id }}
          </el-descriptions-item>
          <el-descriptions-item label="Название файла">
            {{ resume.original_filename }}
          </el-descriptions-item>
          <el-descriptions-item label="Тип файла">
            <el-tag :type="getFileTypeTag(resume.file_type).type">
              {{ resume.file_type.toUpperCase() }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="Размер файла">
            {{ formatFileSize(resume.file_size) }}
          </el-descriptions-item>
          <el-descriptions-item label="Статус">
            <el-tag :type="getStatusType(resume.status)">
              {{ getStatusLabel(resume.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="Дата загрузки">
            {{ formatDate(resume.upload_date) }}
          </el-descriptions-item>
          <el-descriptions-item label="Вакансия" v-if="resume.vacancy_title">
            {{ resume.vacancy_title }}
          </el-descriptions-item>
          <el-descriptions-item label="Общая оценка" v-if="resume.total_score !== null">
            <el-tag :type="getScoreColor(resume.total_score)" size="large">
              {{ resume.total_score.toFixed(1) }}%
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="Уверенность" v-if="resume.confidence_score !== null">
            <el-progress 
              :percentage="Math.round(resume.confidence_score)" 
              :color="getConfidenceColor(resume.confidence_score)"
            />
          </el-descriptions-item>
        </el-descriptions>
        
        <!-- Действия -->
        <div class="actions-section">
          <el-button 
            type="primary" 
            @click="processResume" 
            :loading="processing"
            :disabled="resume.status === 'analyzed'"
          >
            Обработать резюме
          </el-button>
          
          <el-button 
            type="success" 
            @click="calculateScore" 
            :loading="calculating"
            :disabled="resume.status !== 'analyzed' || !resume.vacancy_id"
          >
            Рассчитать оценку
          </el-button>
          
          <el-button 
            type="warning" 
            @click="downloadResume"
            :disabled="!resume.filename"
          >
            Скачать файл
          </el-button>
          
          <el-button 
            type="danger" 
            @click="deleteResume"
          >
            Удалить
          </el-button>
        </div>
      </el-card>
      
      <!-- Блоки анализа -->
      <el-card v-if="resume.resume_blocks && resume.resume_blocks.length > 0" class="analysis-blocks">
        <template #header>
          <span>Анализ блоков</span>
        </template>
        
        <el-collapse v-model="activeBlocks">
          <el-collapse-item 
            v-for="block in resume.resume_blocks" 
            :key="block.id"
            :title="block.block_name"
            :name="block.id"
          >
            <template #title>
              <div class="block-header">
                <span>{{ block.block_name }}</span>
                <div class="block-scores">
                  <el-tag 
                    v-if="block.relevance_score !== null" 
                    :type="getScoreColor(block.relevance_score)"
                    size="small"
                  >
                    Релевантность: {{ block.relevance_score.toFixed(1) }}%
                  </el-tag>
                  <el-tag 
                    v-if="block.confidence_score !== null" 
                    type="info" 
                    size="small"
                  >
                    Уверенность: {{ Math.round(block.confidence_score) }}%
                  </el-tag>
                </div>
              </div>
            </template>
            
            <div class="block-content">
              <div class="block-text">
                <h4>Извлеченный текст:</h4>
                <p>{{ block.extracted_text }}</p>
              </div>
              
              <div v-if="block.matched_requirements && block.matched_requirements.length > 0" class="matched-requirements">
                <h4>Соответствующие требования:</h4>
                <el-tag 
                  v-for="req in block.matched_requirements" 
                  :key="req"
                  type="success" 
                  size="small"
                  style="margin: 2px"
                >
                  {{ req }}
                </el-tag>
              </div>
              
              <div v-if="block.missing_requirements && block.missing_requirements.length > 0" class="missing-requirements">
                <h4>Отсутствующие требования:</h4>
                <el-tag 
                  v-for="req in block.missing_requirements" 
                  :key="req"
                  type="danger" 
                  size="small"
                  style="margin: 2px"
                >
                  {{ req }}
                </el-tag>
              </div>
              
              <div v-if="block.analysis_notes" class="analysis-notes">
                <h4>Заметки анализа:</h4>
                <p>{{ block.analysis_notes }}</p>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>
      </el-card>
      
      <!-- Навыки -->
      <el-card v-if="resume.resume_skills && resume.resume_skills.length > 0" class="skills-section">
        <template #header>
          <span>Навыки</span>
        </template>
        
        <el-table :data="resume.resume_skills" stripe>
          <el-table-column prop="skill_name" label="Навык" />
          <el-table-column prop="skill_category" label="Категория" />
          <el-table-column prop="experience_level" label="Уровень опыта" />
          <el-table-column prop="confidence_score" label="Уверенность">
            <template #default="{ row }">
              <el-progress 
                :percentage="Math.round(row.confidence_score)" 
                :color="getConfidenceColor(row.confidence_score)"
              />
            </template>
          </el-table-column>
          <el-table-column label="Соответствие требованиям" width="200">
            <template #default="{ row }">
              <el-button 
                type="primary" 
                size="small"
                @click="analyzeSkill(row)"
                :loading="analyzingSkills.includes(row.id)"
              >
                Анализировать
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <!-- Результаты анализа навыков -->
        <div v-if="skillsAnalysis.length > 0" class="skills-analysis">
          <h4>Анализ соответствия требованиям вакансии:</h4>
          <el-table :data="skillsAnalysis" stripe>
            <el-table-column prop="skill_name" label="Навык" />
            <el-table-column prop="relevance_score" label="Релевантность">
              <template #default="{ row }">
                <el-progress 
                  :percentage="row.relevance_score" 
                  :color="getScoreColor(row.relevance_score)"
                />
                <span>{{ row.relevance_score }}%</span>
              </template>
            </el-table-column>
            <el-table-column prop="matches_requirements" label="Соответствие">
              <template #default="{ row }">
                <el-tag :type="row.matches_requirements ? 'success' : 'danger'">
                  {{ row.matches_requirements ? 'Да' : 'Нет' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="matched_keywords" label="Соответствующие ключевые слова">
              <template #default="{ row }">
                <el-tag 
                  v-for="keyword in row.matched_keywords" 
                  :key="keyword"
                  type="info" 
                  size="small"
                  style="margin: 2px"
                >
                  {{ keyword }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
          
          <div v-if="overallMatchScore !== null" class="overall-match">
            <h4>Общая оценка соответствия: {{ overallMatchScore }}%</h4>
            <p v-if="analysisSummary">{{ analysisSummary }}</p>
          </div>
        </div>
      </el-card>
      
      <!-- Пустое состояние -->
      <el-card v-if="!resume.resume_blocks || resume.resume_blocks.length === 0" class="empty-state">
        <el-empty description="Анализ блоков не найден">
          <el-button type="primary" @click="processResume" :loading="processing">
            Обработать резюме
          </el-button>
        </el-empty>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import ExportButtons from '@/components/ExportButtons.vue'

export default {
  name: 'ResumeDetail',
  components: {
    ArrowLeft,
    ExportButtons
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    // Проверяем, что route доступен
    if (!route) {
      console.error('Route is not available')
      return {}
    }
    
    const resumeId = route?.params?.id
    
    const resume = ref(null)
    const loading = ref(true)
    const error = ref(null)
    const processing = ref(false)
    const calculating = ref(false)
    const activeBlocks = ref([])
    
    // Skills analysis
    const skillsAnalysis = ref([])
    const overallMatchScore = ref(null)
    const analysisSummary = ref('')
    const analyzingSkills = ref([])
    
    const loadResume = async () => {
      loading.value = true
      error.value = null
      
      try {
        const response = await fetch(`/api/v1/resumes/${resumeId}`)
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const data = await response.json()
        resume.value = data
        
        // Автоматически раскрыть все блоки
        if (data.resume_blocks) {
          activeBlocks.value = data.resume_blocks.map(block => block.id)
        }
        
      } catch (err) {
        error.value = err.message
        console.error('Load resume error:', err)
      } finally {
        loading.value = false
      }
    }
    
    const processResume = async () => {
      processing.value = true
      try {
        const response = await fetch(`/api/v1/resumes/${resumeId}/process`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: resume.value?.original_filename || 'resume'
          })
        })
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const data = await response.json()
        
        if (data.success) {
          ElMessage.success('Резюме обработано успешно')
          await loadResume()
        } else {
          ElMessage.error(data.error || 'Ошибка обработки')
        }
      } catch (err) {
        ElMessage.error('Ошибка обработки резюме')
        console.error('Process resume error:', err)
      } finally {
        processing.value = false
      }
    }
    
    const calculateScore = async () => {
      calculating.value = true
      try {
        const response = await fetch(`/api/v1/resumes/${resumeId}/calculate-score`, {
          method: 'POST'
        })
        
        if (!response.ok) {
          const errorText = await response.text()
          throw new Error(`HTTP ${response.status}: ${errorText}`)
        }
        
        const data = await response.json()
        
        if (data.success) {
          ElMessage.success('Оценка рассчитана успешно')
          await loadResume()
        } else {
          ElMessage.error(data.error || 'Ошибка расчета оценки')
        }
      } catch (err) {
        ElMessage.error(`Ошибка расчета оценки: ${err.message}`)
        console.error('Calculate score error:', err)
      } finally {
        calculating.value = false
      }
    }
    
    const downloadResume = async () => {
      try {
        const response = await fetch(`/api/v1/resumes/${resumeId}/download`)
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = resume.value.original_filename
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        ElMessage.success('Файл скачан успешно')
      } catch (err) {
        ElMessage.error('Ошибка скачивания файла')
        console.error('Download resume error:', err)
      }
    }
    
    const deleteResume = async () => {
      try {
        await ElMessageBox.confirm(
          'Вы уверены, что хотите удалить это резюме?',
          'Подтверждение удаления',
          {
            confirmButtonText: 'Удалить',
            cancelButtonText: 'Отмена',
            type: 'warning'
          }
        )
        
        const response = await fetch(`/api/v1/resumes/${resumeId}`, {
          method: 'DELETE'
        })
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        ElMessage.success('Резюме удалено успешно')
        router.push('/resumes')
      } catch (err) {
        if (err !== 'cancel') {
          ElMessage.error('Ошибка удаления резюме')
          console.error('Delete resume error:', err)
        }
      }
    }
    
    const handleExportCompleted = (exportInfo) => {
    }
    
    const analyzeSkill = async (skill) => {
      analyzingSkills.value.push(skill.id)
      try {
        const response = await fetch(`/api/v1/resumes/${resumeId}/analyze-skills`, {
          method: 'POST'
        })
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const result = await response.json()
        
        if (result.success) {
          skillsAnalysis.value = result.skills_analysis
          overallMatchScore.value = result.overall_match_score
          analysisSummary.value = result.summary
          ElMessage.success('Анализ навыков выполнен успешно')
        } else {
          throw new Error(result.error || 'Ошибка анализа навыков')
        }
        
      } catch (err) {
        ElMessage.error('Ошибка анализа навыков: ' + err.message)
        console.error('Analyze skills error:', err)
      } finally {
        analyzingSkills.value = analyzingSkills.value.filter(id => id !== skill.id)
      }
    }
    
    // Utility functions
    const getStatusType = (status) => {
      switch (status) {
        case 'uploaded': return 'info'
        case 'processing': return 'warning'
        case 'analyzed': return 'success'
        case 'error': return 'danger'
        default: return 'info'
      }
    }
    
    const getStatusLabel = (status) => {
      switch (status) {
        case 'uploaded': return 'Загружено'
        case 'processing': return 'Обрабатывается'
        case 'analyzed': return 'Проанализировано'
        case 'error': return 'Ошибка'
        default: return status
      }
    }
    
    const getFileTypeTag = (fileType) => {
      switch (fileType.toLowerCase()) {
        case 'pdf': return { type: 'danger' }
        case 'docx': return { type: 'primary' }
        case 'rtf': return { type: 'warning' }
        case 'txt': return { type: 'info' }
        default: return { type: 'info' }
      }
    }
    
    const getScoreColor = (score) => {
      if (score >= 80) return 'success'
      if (score >= 60) return 'warning'
      return 'danger'
    }
    
    const getConfidenceColor = (confidence) => {
      if (confidence >= 0.8) return '#67C23A'
      if (confidence >= 0.6) return '#E6A23C'
      return '#F56C6C'
    }
    
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'Не указано'
      return new Date(dateString).toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    onMounted(() => {
      loadResume()
    })
    
    return {
      resumeId,
      resume,
      loading,
      error,
      processing,
      calculating,
      activeBlocks,
      skillsAnalysis,
      overallMatchScore,
      analysisSummary,
      analyzingSkills,
      loadResume,
      processResume,
      calculateScore,
      downloadResume,
      deleteResume,
      analyzeSkill,
      handleExportCompleted,
      getStatusType,
      getStatusLabel,
      getFileTypeTag,
      getScoreColor,
      getConfidenceColor,
      formatFileSize,
      formatDate
    }
  }
}
</script>

<style scoped>
.resume-detail {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  color: #303133;
}

.header-buttons {
  display: flex;
  gap: 10px;
  align-items: center;
}

.loading-state,
.error-state {
  margin-top: 20px;
}

.resume-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.main-info {
  margin-bottom: 20px;
}

.actions-section {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.analysis-blocks,
.skills-section {
  margin-bottom: 20px;
}

.skills-analysis {
  margin-top: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.skills-analysis h4 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 16px;
  font-weight: bold;
}

.overall-match {
  margin-top: 20px;
  padding: 15px;
  background-color: #e8f5e8;
  border-radius: 8px;
  border-left: 4px solid #67C23A;
}

.overall-match h4 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 16px;
  font-weight: bold;
}

.overall-match p {
  margin: 0;
  color: #606266;
  line-height: 1.5;
}

.block-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.block-scores {
  display: flex;
  gap: 8px;
}

.block-content {
  padding: 10px 0;
}

.block-text h4,
.matched-requirements h4,
.missing-requirements h4,
.analysis-notes h4 {
  margin: 10px 0 5px 0;
  color: #303133;
  font-size: 14px;
  font-weight: bold;
}

.block-text p {
  margin: 5px 0;
  line-height: 1.5;
  color: #606266;
}

.matched-requirements,
.missing-requirements {
  margin: 10px 0;
}

.analysis-notes p {
  margin: 5px 0;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  color: #606266;
}

.empty-state {
  text-align: center;
  padding: 40px;
}

:deep(.el-collapse-item__header) {
  font-weight: bold;
}

:deep(.el-descriptions__label) {
  font-weight: bold;
}
</style>
