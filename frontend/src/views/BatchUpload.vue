<template>
  <div class="batch-upload">
                    <div class="page-header">
                  <h1>Пакетная загрузка резюме</h1>
                  <div class="header-buttons">
                    <ExportButtons 
                      :batch-id="currentBatchId" 
                      @export-completed="handleExportCompleted" 
                    />
                    <el-button @click="$router.push('/resumes')" icon="ArrowLeft">
                      Назад к списку
                    </el-button>
                  </div>
                </div>

    <el-row :gutter="20">
      <!-- Форма загрузки -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>Загрузка файлов</span>
          </template>

          <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
            <el-form-item label="Вакансия" prop="vacancy_id">
              <el-select 
                v-model="form.vacancy_id" 
                placeholder="Выберите вакансию (необязательно)"
                clearable
                style="width: 100%"
              >
                <el-option
                  v-for="vacancy in vacancies"
                  :key="vacancy.id"
                  :label="vacancy.title"
                  :value="vacancy.id"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="Максимум потоков" prop="max_concurrent">
              <el-input-number
                v-model="form.max_concurrent"
                :min="1"
                :max="10"
                style="width: 100%"
              />
              <div class="form-help">
                Количество одновременно обрабатываемых файлов
              </div>
            </el-form-item>

            <el-form-item label="Файлы" prop="files">
              <el-upload
                ref="uploadRef"
                :auto-upload="false"
                :on-change="handleFileChange"
                :on-remove="handleFileRemove"
                v-model:file-list="fileList"
                multiple
                :limit="50"
                accept=".pdf,.docx,.rtf,.txt"
                drag
              >
                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                <div class="el-upload__text">
                  Перетащите файлы сюда или <em>нажмите для выбора</em>
                </div>
                <template #tip>
                  <div class="el-upload__tip">
                    Поддерживаемые форматы: PDF, DOCX, RTF, TXT. Максимум 50 файлов, 10MB каждый.
                  </div>
                </template>
              </el-upload>
            </el-form-item>

            <el-form-item>
              <el-button 
                type="primary" 
                @click="startBatchUpload"
                :loading="uploading"
                :disabled="fileList.length === 0"
              >
                Начать обработку
              </el-button>
              <el-button @click="resetForm">Сбросить</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- Статус обработки -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>Статус обработки</span>
          </template>

          <div v-if="batchStatus" class="batch-status">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="ID пакета">
                {{ batchStatus.batch_id }}
              </el-descriptions-item>
              <el-descriptions-item label="Статус">
                <el-tag :type="getStatusType(batchStatus.status)">
                  {{ getStatusText(batchStatus.status) }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="Всего файлов">
                {{ batchStatus.total_files }}
              </el-descriptions-item>
              <el-descriptions-item label="Успешно">
                <el-tag type="success">{{ batchStatus.successful }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="Ошибок">
                <el-tag type="danger" v-if="batchStatus.failed > 0">
                  {{ batchStatus.failed }}
                </el-tag>
                <span v-else>0</span>
              </el-descriptions-item>
              <el-descriptions-item label="Время обработки" v-if="batchStatus.processing_time_seconds">
                {{ formatTime(batchStatus.processing_time_seconds) }}
              </el-descriptions-item>
            </el-descriptions>

            <!-- Результаты -->
            <div v-if="batchStatus.results && batchStatus.results.length > 0" class="results-section">
              <h4>Результаты обработки:</h4>
              <el-table :data="batchStatus.results" size="small" max-height="300">
                <el-table-column prop="filename" label="Файл" width="200" />
                <el-table-column prop="status" label="Статус" width="100">
                  <template #default="{ row }">
                    <el-tag :type="row.status === 'success' ? 'success' : 'danger'" size="small">
                      {{ row.status === 'success' ? 'Успех' : 'Ошибка' }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="sections_found" label="Блоков" width="80" />
                <el-table-column prop="skills_found" label="Навыков" width="80" />
                <el-table-column prop="error" label="Ошибка" show-overflow-tooltip />
              </el-table>
            </div>
          </div>

          <div v-else class="no-status">
            <el-empty description="Нет активной обработки" />
          </div>
        </el-card>

        <!-- Статистика -->
        <el-card style="margin-top: 20px">
          <template #header>
            <span>Статистика пакетной обработки</span>
          </template>

          <el-descriptions :column="2" border>
            <el-descriptions-item label="Всего пакетов">
              {{ batchStats.total_batches }}
            </el-descriptions-item>
            <el-descriptions-item label="Успешных">
              {{ batchStats.successful_batches }}
            </el-descriptions-item>
            <el-descriptions-item label="Ошибок">
              {{ batchStats.failed_batches }}
            </el-descriptions-item>
            <el-descriptions-item label="Файлов обработано">
              {{ batchStats.total_files_processed }}
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, UploadFilled } from '@element-plus/icons-vue'
import { useHRStore } from '@/stores/hr'
import ExportButtons from '@/components/ExportButtons.vue'

export default {
  name: 'BatchUpload',
  components: {
    ArrowLeft,
    UploadFilled,
    ExportButtons
  },
  setup() {
    const formRef = ref()
    const uploadRef = ref()
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

    const rules = {
      max_concurrent: [
        { required: true, message: 'Укажите количество потоков', trigger: 'blur' },
        { type: 'number', min: 1, max: 10, message: 'От 1 до 10 потоков', trigger: 'blur' }
      ]
    }

    const vacancies = ref([])

    const handleFileChange = (file, fileList) => {
      console.log('File changed:', file.name, 'FileList length:', fileList.length)
      
      // Проверка размера файла
      if (file.size > 10 * 1024 * 1024) {
        ElMessage.error(`Файл ${file.name} слишком большой (максимум 10MB)`)
        return false
      }
      
      // Проверка формата
      const allowedTypes = ['pdf', 'docx', 'rtf', 'txt']
      const fileType = file.name.split('.').pop().toLowerCase()
      if (!allowedTypes.includes(fileType)) {
        ElMessage.error(`Неподдерживаемый формат файла: ${file.name}`)
        return false
      }
      
      // Файл прошел проверку
      return true
    }

    const handleFileRemove = (file, fileList) => {
      // Файл удален из списка
    }

    const startBatchUpload = async () => {
      console.log('Starting batch upload, fileList length:', fileList.value.length)
      console.log('FileList:', fileList.value)
      
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
          formData.append('files', file.raw)
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
        
        ElMessage.success(`Пакетная обработка запущена. ID: ${result.batch_id}`)
        
        // Начать мониторинг статуса
        startStatusMonitoring()
        
      } catch (error) {
        console.error('Batch upload error:', error)
        ElMessage.error(`Ошибка загрузки: ${error.message}`)
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
      formRef.value?.resetFields()
      fileList.value = []
      uploadRef.value?.clearFiles()
      batchStatus.value = null
      if (statusInterval.value) {
        clearInterval(statusInterval.value)
        statusInterval.value = null
      }
      currentBatchId.value = null
      localStorage.removeItem('currentBatchId')  // Очищаем localStorage
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
                  console.log('Export completed:', exportInfo)
                }
                
                return {
                  formRef,
                  uploadRef,
                  fileList,
                  uploading,
                  batchStatus,
                  batchStats,
                  form,
                  rules,
                  vacancies,
                  handleFileChange,
                  handleFileRemove,
                  startBatchUpload,
                  resetForm,
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

.form-help {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.batch-status {
  margin-top: 10px;
}

.results-section {
  margin-top: 20px;
}

.results-section h4 {
  margin-bottom: 10px;
  color: #303133;
}

.no-status {
  text-align: center;
  padding: 40px 0;
}

:deep(.el-upload-dragger) {
  width: 100%;
}

:deep(.el-upload__tip) {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}
</style>
