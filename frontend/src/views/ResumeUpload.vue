<template>
  <div class="resume-upload">
    <!-- Header -->
    <PageHeader
      title="Пакетная загрузка резюме"
      subtitle="Создавайте и управляйте вакансиями для автоматизированных интервью"
    >
      <template #actions>
        <BaseButton 
          variant="secondary" 
          icon="mdi mdi-arrow-left"
          @click="$router.push('/resumes')"
        >
          Назад к списку
        </BaseButton>
      </template>
    </PageHeader>

    <!-- Main Content -->
    <div class="panel-content">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2">
          <!-- Форма загрузки -->
          <BaseCard>
            <template #header>
              <h3 class="text-lg font-semibold text-white">Загрузить файл резюме</h3>
            </template>
          
            <div class="space-y-6">
              <!-- Выбор вакансии -->
              <div>
                <label class="block text-sm font-medium text-slate-300 mb-2">
                  Вакансия
                </label>
                <BaseSelect
                  v-model="form.vacancy_id"
                  :items="vacancyOptions"
                  placeholder="Выберите вакансию"
                  clearable
                />
                <p class="mt-2 text-sm text-slate-400">
                  Выберите вакансию для автоматической оценки релевантности резюме
                </p>
              </div>

              <!-- Загрузка файла -->
              <div>
                <label class="block text-sm font-medium text-slate-300 mb-2">
                  Файл резюме
                </label>
                <div class="upload-area" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleDrop">
                  <input
                    ref="fileInput"
                    type="file"
                    accept=".pdf,.docx,.rtf,.txt"
                    @change="handleFileSelect"
                    class="hidden"
                  />
                  <div v-if="!selectedFile" class="upload-placeholder">
                    <svg class="w-12 h-12 text-cyan-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <p class="text-slate-300 mb-2">
                      Перетащите файл сюда или <span class="text-cyan-400 cursor-pointer">нажмите для выбора</span>
                    </p>
                    <p class="text-sm text-slate-400">
                      Поддерживаемые форматы: PDF, DOCX, RTF, TXT (максимум 10MB)
                    </p>
                  </div>
                  <div v-else class="file-selected">
                    <div class="flex items-center justify-between">
                      <div class="flex items-center gap-3">
                        <svg class="w-8 h-8 text-cyan-400" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd" />
                        </svg>
                        <div>
                          <p class="text-slate-300 font-medium">{{ selectedFile.name }}</p>
                          <p class="text-sm text-slate-400">{{ formatFileSize(selectedFile.size) }}</p>
                        </div>
                      </div>
                      <BaseButton
                        variant="secondary"
                        size="sm"
                        @click.stop="removeFile"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </BaseButton>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Кнопки действий -->
              <div class="flex gap-3">
                <BaseButton
                  variant="primary"
                  @click="uploadResume"
                  :loading="uploading"
                  :disabled="!selectedFile"
                  icon="mdi mdi-upload"
                >
                  Загрузить резюме
                </BaseButton>
                
                <BaseButton 
                  variant="secondary" 
                  @click="resetForm" 
                  icon="mdi mdi-refresh"
                >
                  Сбросить
                </BaseButton>
              </div>
            </div>
          </BaseCard>
        </div>

        <div class="lg:col-span-1 space-y-6">
          <!-- Информация о процессе -->
          <BaseCard>
            <template #header>
              <h3 class="text-lg font-semibold text-white">Статус обработки</h3>
            </template>
          
            <div class="space-y-6">
              <div>
                <h4 class="text-sm font-medium text-slate-300 mb-3">Процесс обработки:</h4>
                <ol class="space-y-2 text-sm text-slate-400 list-decimal list-inside">
                  <li>Загрузка файла в хранилище</li>
                  <li>Извлечение текста из файла</li>
                  <li>Парсинг и структурирование данных</li>
                  <li>Извлечение навыков и опыта</li>
                  <li>Оценка релевантности (если выбрана вакансия)</li>
                </ol>
              </div>
              
              <div>
                <h4 class="text-sm font-medium text-slate-300 mb-3">Поддерживаемые форматы:</h4>
                <ul class="space-y-2 text-sm text-slate-400">
                  <li><span class="text-cyan-400 font-medium">PDF</span> - документы Adobe PDF</li>
                  <li><span class="text-cyan-400 font-medium">DOCX</span> - документы Microsoft Word</li>
                  <li><span class="text-cyan-400 font-medium">RTF</span> - Rich Text Format</li>
                  <li><span class="text-cyan-400 font-medium">TXT</span> - текстовые файлы</li>
                </ul>
              </div>
              
              <div>
                <h4 class="text-sm font-medium text-slate-300 mb-3">Ограничения:</h4>
                <ul class="space-y-2 text-sm text-slate-400">
                  <li>Максимальный размер файла: 10MB</li>
                  <li>Один файл за раз</li>
                  <li>Автоматическая обработка после загрузки</li>
                </ul>
              </div>
            </div>
          </BaseCard>

          <!-- Последние загрузки -->
          <BaseCard>
            <template #header>
              <h3 class="text-lg font-semibold text-white">Последние загрузки</h3>
            </template>
            
            <div v-if="recentUploads.length === 0" class="text-center py-8">
              <svg class="w-12 h-12 text-slate-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <p class="text-slate-400">Нет недавних загрузок</p>
            </div>
            
            <div v-else class="space-y-3">
              <div
                v-for="upload in recentUploads"
                :key="upload.id"
                class="p-3 rounded-lg bg-slate-800/50 border border-slate-700 hover:border-cyan-500/50 cursor-pointer transition-colors"
                @click="$router.push(`/resumes/${upload.id}`)"
              >
                <div class="flex items-center justify-between">
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-slate-300 truncate">{{ upload.original_filename }}</p>
                    <p class="text-xs text-slate-400 mt-1">{{ formatDate(upload.upload_date) }}</p>
                  </div>
                  <div class="ml-3">
                    <span :class="getStatusClass(upload.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                      {{ getStatusLabel(upload.status) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </BaseCard>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseSelect from '@/components/base/BaseSelect.vue'
import PageHeader from '@/components/layout/PageHeader.vue'

export default {
  name: 'ResumeUpload',
  components: {
    BaseButton,
    BaseCard,
    BaseSelect,
    PageHeader
  },
  setup() {
    const router = useRouter()
    const fileInput = ref()
    
    const form = reactive({
      vacancy_id: null
    })
    
    const selectedFile = ref(null)
    const uploading = ref(false)
    const vacancies = ref([])
    const recentUploads = ref([])
    
    // Computed
    const vacancyOptions = computed(() => 
      vacancies.value.map(vacancy => ({
        label: vacancy.title,
        value: vacancy.id,
        description: vacancy.vacancy_code
      }))
    )
    
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
    
    const triggerFileInput = () => {
      fileInput.value?.click()
    }
    
    const handleFileSelect = (event) => {
      const file = event.target.files[0]
      if (file && validateFile(file)) {
        selectedFile.value = file
      }
    }
    
    const handleDrop = (event) => {
      const file = event.dataTransfer.files[0]
      if (file && validateFile(file)) {
        selectedFile.value = file
      }
    }
    
    const removeFile = () => {
      selectedFile.value = null
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    }
    
    const validateFile = (file) => {
      // Проверка размера файла
      const isLt10M = file.size / 1024 / 1024 < 10
      if (!isLt10M) {
        alert('Размер файла не должен превышать 10MB!')
        return false
      }
      
      // Проверка типа файла
      const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/rtf', 'text/plain']
      const isValidType = allowedTypes.includes(file.type) || file.name.endsWith('.txt')
      
      if (!isValidType) {
        alert('Неподдерживаемый тип файла!')
        return false
      }
      
      return true
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
      form.vacancy_id = null
      selectedFile.value = null
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    }
    
    const getStatusClass = (status) => {
      const classes = {
        uploaded: 'bg-blue-100 text-blue-800',
        processing: 'bg-yellow-100 text-yellow-800',
        analyzed: 'bg-green-100 text-green-800',
        error: 'bg-red-100 text-red-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
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
      fileInput,
      form,
      selectedFile,
      uploading,
      vacancies,
      recentUploads,
      vacancyOptions,
      triggerFileInput,
      handleFileSelect,
      handleDrop,
      removeFile,
      uploadResume,
      resetForm,
      formatFileSize,
      getStatusClass,
      getStatusLabel,
      formatDate
    }
  }
}
</script>

<style scoped>
.resume-upload {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  position: relative;
}

.resume-upload::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 80%, rgba(0, 255, 255, 0.05) 0%, transparent 60%),
    radial-gradient(circle at 80% 20%, rgba(138, 43, 226, 0.05) 0%, transparent 60%);
  pointer-events: none;
  z-index: 1;
}

.panel-content {
  position: relative;
  z-index: 2;
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
}

.upload-area {
  border: 2px dashed rgba(0, 255, 255, 0.3);
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(10px);
  margin-bottom: 0.5rem;
}

.upload-area:hover {
  border-color: rgba(0, 255, 255, 0.5);
  background: rgba(15, 23, 42, 0.7);
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.file-selected {
  padding: 1rem;
  background: rgba(0, 255, 255, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(0, 255, 255, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
  .panel-content {
    padding: 1rem;
  }
  
  .upload-area {
    padding: 1.5rem;
  }
}
</style>
