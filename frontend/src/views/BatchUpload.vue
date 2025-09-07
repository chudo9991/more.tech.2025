<template>
  <div class="batch-upload">
    <!-- Header -->
    <PageHeader
      title="Пакетная загрузка резюме"
      subtitle="Загружайте и обрабатывайте несколько резюме одновременно"
    >
      <template #actions>
        <ExportButtons 
          :batch-id="currentBatchId" 
          @export-completed="handleExportCompleted" 
        />
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
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Форма загрузки -->
        <div>
          <BaseCard>
            <template #header>
              <h3 class="text-lg font-semibold text-white">Загрузка файлов</h3>
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
                  placeholder="Выберите вакансию (необязательно)"
                  clearable
                />
              </div>

              <!-- Максимум потоков -->
              <div>
                <label class="block text-sm font-medium text-slate-300 mb-2">
                  Максимум потоков
                </label>
                <BaseInput
                  v-model="form.max_concurrent"
                  type="number"
                  :min="1"
                  :max="10"
                  placeholder="3"
                />
                <p class="mt-2 text-sm text-slate-400">
                  Количество одновременно обрабатываемых файлов
                </p>
              </div>

              <!-- Загрузка файлов -->
              <div>
                <label class="block text-sm font-medium text-slate-300 mb-2">
                  Файлы
                </label>
                <div class="upload-area" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleDrop">
                  <input
                    ref="fileInput"
                    type="file"
                    accept=".pdf,.docx,.rtf,.txt"
                    @change="handleFileSelect"
                    multiple
                    class="hidden"
                  />
                  <div v-if="fileList.length === 0" class="upload-placeholder">
                    <svg class="w-12 h-12 text-cyan-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <p class="text-slate-300 mb-2">
                      Перетащите файлы сюда или <span class="text-cyan-400 cursor-pointer">нажмите для выбора</span>
                    </p>
                    <p class="text-sm text-slate-400">
                      Поддерживаемые форматы: PDF, DOCX, RTF, TXT. Максимум 50 файлов, 10MB каждый.
                    </p>
                  </div>
                  <div v-else class="files-selected">
                    <div class="mb-4">
                      <p class="text-slate-300 font-medium">Выбрано файлов: {{ fileList.length }}</p>
                    </div>
                    <div class="max-h-40 overflow-y-auto space-y-2">
                      <div
                        v-for="(file, index) in fileList"
                        :key="index"
                        class="flex items-center justify-between p-2 bg-slate-800/50 rounded-lg"
                      >
                        <div class="flex items-center gap-2">
                          <svg class="w-4 h-4 text-cyan-400" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd" />
                          </svg>
                          <span class="text-sm text-slate-300 truncate">{{ file.name }}</span>
                        </div>
                        <BaseButton
                          variant="secondary"
                          size="sm"
                          @click.stop="removeFile(index)"
                        >
                          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </BaseButton>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Кнопки действий -->
              <div class="flex gap-3">
                <BaseButton
                  variant="primary"
                  @click="startBatchUpload"
                  :loading="uploading"
                  :disabled="fileList.length === 0"
                  icon="mdi mdi-play"
                >
                  Начать обработку
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

        <!-- Статус обработки -->
        <div class="space-y-6">
          <BaseCard>
            <template #header>
              <h3 class="text-lg font-semibold text-white">Статус обработки</h3>
            </template>

            <div v-if="batchStatus" class="space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <p class="text-sm text-slate-400">ID пакета</p>
                  <p class="text-slate-300 font-mono">{{ batchStatus.batch_id }}</p>
                </div>
                <div>
                  <p class="text-sm text-slate-400">Статус</p>
                  <span :class="getStatusClass(batchStatus.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                    {{ getStatusText(batchStatus.status) }}
                  </span>
                </div>
                <div>
                  <p class="text-sm text-slate-400">Всего файлов</p>
                  <p class="text-slate-300 font-medium">{{ batchStatus.total_files }}</p>
                </div>
                <div>
                  <p class="text-sm text-slate-400">Успешно</p>
                  <p class="text-green-400 font-medium">{{ batchStatus.successful }}</p>
                </div>
                <div>
                  <p class="text-sm text-slate-400">Ошибок</p>
                  <p :class="batchStatus.failed > 0 ? 'text-red-400' : 'text-slate-300'" class="font-medium">
                    {{ batchStatus.failed }}
                  </p>
                </div>
                <div v-if="batchStatus.processing_time_seconds">
                  <p class="text-sm text-slate-400">Время обработки</p>
                  <p class="text-slate-300 font-medium">{{ formatTime(batchStatus.processing_time_seconds) }}</p>
                </div>
              </div>

              <!-- Результаты -->
              <div v-if="batchStatus.results && batchStatus.results.length > 0" class="mt-6">
                <h4 class="text-sm font-medium text-slate-300 mb-3">Результаты обработки:</h4>
                <div class="max-h-60 overflow-y-auto space-y-2">
                  <div
                    v-for="result in batchStatus.results"
                    :key="result.filename"
                    class="p-3 bg-slate-800/50 rounded-lg border border-slate-700"
                  >
                    <div class="flex items-center justify-between mb-2">
                      <p class="text-sm font-medium text-slate-300 truncate">{{ result.filename }}</p>
                      <span :class="result.status === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'" 
                            class="px-2 py-1 text-xs font-medium rounded-full">
                        {{ result.status === 'success' ? 'Успех' : 'Ошибка' }}
                      </span>
                    </div>
                    <div class="flex gap-4 text-xs text-slate-400">
                      <span>Блоков: {{ result.sections_found || 0 }}</span>
                      <span>Навыков: {{ result.skills_found || 0 }}</span>
                    </div>
                    <div v-if="result.error" class="mt-2 text-xs text-red-400">
                      {{ result.error }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="text-center py-12">
              <svg class="w-16 h-16 text-slate-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <p class="text-slate-400">Нет активной обработки</p>
            </div>
          </BaseCard>

          <!-- Статистика -->
          <BaseCard>
            <template #header>
              <h3 class="text-lg font-semibold text-white">Статистика пакетной обработки</h3>
            </template>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-slate-400">Всего пакетов</p>
                <p class="text-slate-300 font-medium">{{ batchStats.total_batches }}</p>
              </div>
              <div>
                <p class="text-sm text-slate-400">Успешных</p>
                <p class="text-green-400 font-medium">{{ batchStats.successful_batches }}</p>
              </div>
              <div>
                <p class="text-sm text-slate-400">Ошибок</p>
                <p class="text-red-400 font-medium">{{ batchStats.failed_batches }}</p>
              </div>
              <div>
                <p class="text-sm text-slate-400">Файлов обработано</p>
                <p class="text-slate-300 font-medium">{{ batchStats.total_files_processed }}</p>
              </div>
            </div>
          </BaseCard>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted, computed } from 'vue'
import { useHRStore } from '@/stores/hr'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseSelect from '@/components/base/BaseSelect.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import ExportButtons from '@/components/ExportButtons.vue'

export default {
  name: 'BatchUpload',
  components: {
    BaseButton,
    BaseCard,
    BaseSelect,
    BaseInput,
    PageHeader,
    ExportButtons
  },
  setup() {
    const fileInput = ref()
    const fileList = ref([])
    const uploading = ref(false)
    const batchStatus = ref(null)
    const batchStats = ref({
      total_batches: 0,
      successful_batches: 0,
      failed_batches: 0,
      total_files_processed: 0
    })
    const statusInterval = ref(null)
    const currentBatchId = ref(localStorage.getItem('currentBatchId') || null)

    const form = reactive({
      vacancy_id: '',
      max_concurrent: 3
    })

    const vacancies = ref([])
    
    // Computed
    const vacancyOptions = computed(() => 
      vacancies.value.map(vacancy => ({
        label: vacancy.title,
        value: vacancy.id,
        description: vacancy.vacancy_code
      }))
    )

    const triggerFileInput = () => {
      fileInput.value?.click()
    }
    
    const handleFileSelect = (event) => {
      const files = Array.from(event.target.files)
      files.forEach(file => {
        if (validateFile(file) && fileList.value.length < 50) {
          fileList.value.push(file)
        }
      })
    }
    
    const handleDrop = (event) => {
      const files = Array.from(event.dataTransfer.files)
      files.forEach(file => {
        if (validateFile(file) && fileList.value.length < 50) {
          fileList.value.push(file)
        }
      })
    }
    
    const removeFile = (index) => {
      fileList.value.splice(index, 1)
    }
    
    const validateFile = (file) => {
      // Проверка размера файла
      if (file.size > 10 * 1024 * 1024) {
        alert(`Файл ${file.name} слишком большой (максимум 10MB)`)
        return false
      }
      
      // Проверка формата
      const allowedTypes = ['pdf', 'docx', 'rtf', 'txt']
      const fileType = file.name.split('.').pop().toLowerCase()
      if (!allowedTypes.includes(fileType)) {
        alert(`Неподдерживаемый формат файла: ${file.name}`)
        return false
      }
      
      return true
    }

    const startBatchUpload = async () => {
      if (fileList.value.length === 0) {
        ElMessage.warning('Выберите файлы для загрузки')
        return
      }

      try {
        uploading.value = true
        
        const formData = new FormData()
        formData.append('max_concurrent', form.max_concurrent)
        if (form.vacancy_id) {
          formData.append('vacancy_id', form.vacancy_id)
        }
        
        fileList.value.forEach(file => {
          formData.append('files', file)
        })

        const response = await fetch('/api/v1/batch/upload', {
          method: 'POST',
          body: formData
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const result = await response.json()
        currentBatchId.value = result.batch_id
        localStorage.setItem('currentBatchId', result.batch_id)  // Сохраняем в localStorage
        batchStatus.value = result
        
        alert(`Пакетная обработка запущена. ID: ${result.batch_id}`)
        
        // Начать мониторинг статуса
        startStatusMonitoring()
        
      } catch (error) {
        console.error('Batch upload error:', error)
        alert(`Ошибка загрузки: ${error.message}`)
      } finally {
        uploading.value = false
      }
    }

    const startStatusMonitoring = () => {
      if (statusInterval.value) {
        clearInterval(statusInterval.value)
      }
      
      statusInterval.value = setInterval(async () => {
        if (currentBatchId.value) {
          try {
            const response = await fetch(`/api/v1/batch/status/${currentBatchId.value}`)
            if (response.ok) {
              const status = await response.json()
              batchStatus.value = status
              
              if (status.status === 'completed' || status.status === 'error') {
                clearInterval(statusInterval.value)
                statusInterval.value = null
                currentBatchId.value = null
                localStorage.removeItem('currentBatchId')  // Очищаем localStorage при завершении
              }
            }
          } catch (error) {
            console.error('Status monitoring error:', error)
          }
        }
      }, 2000) // Проверка каждые 2 секунды
    }

    const resetForm = () => {
      form.vacancy_id = ''
      form.max_concurrent = 3
      fileList.value = []
      if (fileInput.value) {
        fileInput.value.value = ''
      }
      batchStatus.value = null
      if (statusInterval.value) {
        clearInterval(statusInterval.value)
        statusInterval.value = null
      }
      currentBatchId.value = null
      localStorage.removeItem('currentBatchId')
    }
    
    const getStatusClass = (status) => {
      const classes = {
        processing: 'bg-yellow-100 text-yellow-800',
        completed: 'bg-green-100 text-green-800',
        error: 'bg-red-100 text-red-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    }

    const getStatusType = (status) => {
      switch (status) {
        case 'processing': return 'warning'
        case 'completed': return 'success'
        case 'error': return 'danger'
        default: return 'info'
      }
    }

    const getStatusText = (status) => {
      switch (status) {
        case 'processing': return 'Обработка'
        case 'completed': return 'Завершено'
        case 'error': return 'Ошибка'
        default: return status
      }
    }

    const formatTime = (seconds) => {
      if (seconds < 60) {
        return `${seconds.toFixed(1)} сек`
      } else {
        const minutes = Math.floor(seconds / 60)
        const remainingSeconds = seconds % 60
        return `${minutes} мин ${remainingSeconds.toFixed(1)} сек`
      }
    }

    const loadVacancies = async () => {
      try {
        const hrStore = useHRStore()
        await hrStore.fetchVacancies()
        vacancies.value = hrStore.vacancies || []
      } catch (error) {
        console.error('Error loading vacancies:', error)
      }
    }

    const loadBatchStats = async () => {
      try {
        const response = await fetch('/api/v1/batch/statistics')
        if (response.ok) {
          batchStats.value = await response.json()
        }
      } catch (error) {
        console.error('Error loading batch stats:', error)
      }
    }

    onMounted(() => {
      loadVacancies()
      loadBatchStats()
      
      // Восстанавливаем статус batch, если есть сохраненный ID
      if (currentBatchId.value) {
        startStatusMonitoring()
      }
    })

    onUnmounted(() => {
      if (statusInterval.value) {
        clearInterval(statusInterval.value)
      }
    })

                    const handleExportCompleted = (exportInfo) => {
                }
                
                return {
                  fileInput,
                  fileList,
                  uploading,
                  batchStatus,
                  batchStats,
                  form,
                  vacancies,
                  vacancyOptions,
                  triggerFileInput,
                  handleFileSelect,
                  handleDrop,
                  removeFile,
                  startBatchUpload,
                  resetForm,
                  getStatusClass,
                  getStatusType,
                  getStatusText,
                  formatTime,
                  handleExportCompleted
                }
  }
}
</script>

<style scoped>
.batch-upload {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  position: relative;
}

.batch-upload::before {
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

.files-selected {
  text-align: left;
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
