<template>
  <div class="resume-upload">
    <div class="page-header">
      <h1>Загрузка резюме</h1>
      <el-button @click="$router.push('/resumes')" icon="ArrowLeft">
        Назад к списку
      </el-button>
    </div>

    <el-row :gutter="20">
      <el-col :span="16">
        <!-- Форма загрузки -->
        <el-card>
          <template #header>
            <span>Загрузить файл резюме</span>
          </template>
          
          <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
            <!-- Выбор вакансии -->
            <el-form-item label="Вакансия" prop="vacancy_id">
              <el-select
                v-model="form.vacancy_id"
                placeholder="Выберите вакансию"
                style="width: 100%"
                clearable
              >
                <el-option
                  v-for="vacancy in vacancies"
                  :key="vacancy.id"
                  :label="vacancy.title"
                  :value="vacancy.id"
                >
                  <div class="vacancy-option">
                    <div class="vacancy-title">{{ vacancy.title }}</div>
                    <div class="vacancy-code">{{ vacancy.vacancy_code }}</div>
                  </div>
                </el-option>
              </el-select>
              <div class="form-help">
                Выберите вакансию для автоматической оценки релевантности резюме
              </div>
            </el-form-item>

            <!-- Загрузка файла -->
            <el-form-item label="Файл резюме" prop="file">
              <el-upload
                ref="uploadRef"
                class="resume-uploader"
                drag
                :auto-upload="false"
                :on-change="handleFileChange"
                :on-remove="handleFileRemove"
                :file-list="fileList"
                :limit="1"
                accept=".pdf,.docx,.rtf,.txt"
                :before-upload="beforeUpload"
              >
                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                <div class="el-upload__text">
                  Перетащите файл сюда или <em>нажмите для выбора</em>
                </div>
                <template #tip>
                  <div class="el-upload__tip">
                    Поддерживаемые форматы: PDF, DOCX, RTF, TXT (максимум 10MB)
                  </div>
                </template>
              </el-upload>
            </el-form-item>

            <!-- Информация о файле -->
            <el-form-item v-if="selectedFile" label="Информация о файле">
              <div class="file-info">
                <div class="file-details">
                  <div class="file-name">
                    <el-icon><Document /></el-icon>
                    {{ selectedFile.name }}
                  </div>
                  <div class="file-size">
                    Размер: {{ formatFileSize(selectedFile.size) }}
                  </div>
                  <div class="file-type">
                    Тип: {{ selectedFile.type || 'Неизвестно' }}
                  </div>
                </div>
              </div>
            </el-form-item>

            <!-- Кнопки действий -->
            <el-form-item>
              <el-button
                type="primary"
                @click="uploadResume"
                :loading="uploading"
                :disabled="!selectedFile"
                icon="Upload"
              >
                Загрузить резюме
              </el-button>
              
              <el-button @click="resetForm" icon="Refresh">
                Сбросить
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="8">
        <!-- Информация о процессе -->
        <el-card>
          <template #header>
            <span>Информация</span>
          </template>
          
          <div class="info-content">
            <h4>Процесс обработки:</h4>
            <ol class="process-steps">
              <li>Загрузка файла в хранилище</li>
              <li>Извлечение текста из файла</li>
              <li>Парсинг и структурирование данных</li>
              <li>Извлечение навыков и опыта</li>
              <li>Оценка релевантности (если выбрана вакансия)</li>
            </ol>
            
            <h4>Поддерживаемые форматы:</h4>
            <ul class="supported-formats">
              <li><strong>PDF</strong> - документы Adobe PDF</li>
              <li><strong>DOCX</strong> - документы Microsoft Word</li>
              <li><strong>RTF</strong> - Rich Text Format</li>
              <li><strong>TXT</strong> - текстовые файлы</li>
            </ul>
            
            <h4>Ограничения:</h4>
            <ul class="limitations">
              <li>Максимальный размер файла: 10MB</li>
              <li>Один файл за раз</li>
              <li>Автоматическая обработка после загрузки</li>
            </ul>
          </div>
        </el-card>

        <!-- Последние загрузки -->
        <el-card style="margin-top: 20px;">
          <template #header>
            <span>Последние загрузки</span>
          </template>
          
          <div v-if="recentUploads.length === 0" class="no-recent">
            Нет недавних загрузок
          </div>
          
          <div v-else class="recent-uploads">
            <div
              v-for="upload in recentUploads"
              :key="upload.id"
              class="recent-upload-item"
              @click="$router.push(`/resumes/${upload.id}`)"
            >
              <div class="upload-file-name">{{ upload.original_filename }}</div>
              <div class="upload-status">
                <el-tag :type="getStatusType(upload.status)" size="small">
                  {{ getStatusLabel(upload.status) }}
                </el-tag>
              </div>
              <div class="upload-date">{{ formatDate(upload.upload_date) }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { UploadFilled, Document, ArrowLeft } from '@element-plus/icons-vue'

export default {
  name: 'ResumeUpload',
  components: {
    UploadFilled,
    Document,
    ArrowLeft
  },
  setup() {
    const router = useRouter()
    const formRef = ref()
    const uploadRef = ref()
    
    const form = reactive({
      vacancy_id: null
    })
    
    const rules = {
      file: [
        { required: true, message: 'Выберите файл для загрузки', trigger: 'change' }
      ]
    }
    
    const fileList = ref([])
    const selectedFile = ref(null)
    const uploading = ref(false)
    const vacancies = ref([])
    const recentUploads = ref([])
    
    const loadVacancies = async () => {
      try {
        const response = await fetch('/api/v1/vacancies/')
        const data = await response.json()
        vacancies.value = data
      } catch (error) {
        console.error('Ошибка загрузки вакансий:', error)
      }
    }
    
    const loadRecentUploads = async () => {
      try {
        const response = await fetch('/api/v1/resumes/?limit=5')
        const data = await response.json()
        recentUploads.value = data.slice(0, 5)
      } catch (error) {
        console.error('Ошибка загрузки недавних загрузок:', error)
      }
    }
    
    const handleFileChange = (file) => {
      selectedFile.value = file.raw
    }
    
    const handleFileRemove = () => {
      selectedFile.value = null
    }
    
    const beforeUpload = (file) => {
      // Проверка размера файла
      const isLt10M = file.size / 1024 / 1024 < 10
      if (!isLt10M) {
        ElMessage.error('Размер файла не должен превышать 10MB!')
        return false
      }
      
      // Проверка типа файла
      const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/rtf', 'text/plain']
      const isValidType = allowedTypes.includes(file.type) || file.name.endsWith('.txt')
      
      if (!isValidType) {
        ElMessage.error('Неподдерживаемый тип файла!')
        return false
      }
      
      return false // Отключаем автоматическую загрузку
    }
    
    const uploadResume = async () => {
      if (!selectedFile.value) {
        ElMessage.error('Выберите файл для загрузки')
        return
      }
      
      uploading.value = true
      
      try {
        const formData = new FormData()
        formData.append('file', selectedFile.value)
        
        if (form.vacancy_id) {
          formData.append('vacancy_id', form.vacancy_id)
        }
        
        const response = await fetch('/api/v1/resumes/upload', {
          method: 'POST',
          body: formData
        })
        
        const data = await response.json()
        
        if (response.ok) {
          ElMessage.success('Резюме загружено успешно!')
          
          // Перенаправляем на детальную страницу
          router.push(`/resumes/${data.resume_id}`)
        } else {
          ElMessage.error(data.detail || 'Ошибка загрузки файла')
        }
      } catch (error) {
        ElMessage.error('Ошибка загрузки файла')
        console.error(error)
      } finally {
        uploading.value = false
      }
    }
    
    const resetForm = () => {
      formRef.value?.resetFields()
      uploadRef.value?.clearFiles()
      selectedFile.value = null
      fileList.value = []
    }
    
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    const getStatusType = (status) => {
      const types = {
        uploaded: 'info',
        processing: 'warning',
        analyzed: 'success',
        error: 'danger'
      }
      return types[status] || 'info'
    }
    
    const getStatusLabel = (status) => {
      const labels = {
        uploaded: 'Загружено',
        processing: 'Обрабатывается',
        analyzed: 'Проанализировано',
        error: 'Ошибка'
      }
      return labels[status] || status
    }
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    onMounted(() => {
      loadVacancies()
      loadRecentUploads()
    })
    
    return {
      formRef,
      uploadRef,
      form,
      rules,
      fileList,
      selectedFile,
      uploading,
      vacancies,
      recentUploads,
      handleFileChange,
      handleFileRemove,
      beforeUpload,
      uploadResume,
      resetForm,
      formatFileSize,
      getStatusType,
      getStatusLabel,
      formatDate
    }
  }
}
</script>

<style scoped>
.resume-upload {
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

.resume-uploader {
  width: 100%;
}

.vacancy-option {
  display: flex;
  flex-direction: column;
}

.vacancy-title {
  font-weight: bold;
}

.vacancy-code {
  font-size: 12px;
  color: #909399;
}

.form-help {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.file-info {
  border: 1px solid #DCDFE6;
  border-radius: 4px;
  padding: 15px;
  background-color: #FAFAFA;
}

.file-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.file-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
}

.file-size, .file-type {
  color: #606266;
  font-size: 14px;
}

.info-content h4 {
  margin: 15px 0 8px 0;
  color: #303133;
}

.process-steps, .supported-formats, .limitations {
  margin: 0;
  padding-left: 20px;
  color: #606266;
  line-height: 1.6;
}

.process-steps li, .supported-formats li, .limitations li {
  margin-bottom: 5px;
}

.no-recent {
  text-align: center;
  color: #909399;
  padding: 20px;
}

.recent-uploads {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.recent-upload-item {
  padding: 10px;
  border: 1px solid #DCDFE6;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.recent-upload-item:hover {
  background-color: #F5F7FA;
  border-color: #C0C4CC;
}

.upload-file-name {
  font-weight: bold;
  margin-bottom: 5px;
  color: #303133;
}

.upload-status {
  margin-bottom: 5px;
}

.upload-date {
  font-size: 12px;
  color: #909399;
}
</style>
