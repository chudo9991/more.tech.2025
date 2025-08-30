<template>
  <div class="resumes-list">
                    <div class="page-header">
                  <h1>Управление резюме</h1>
                  <div class="header-buttons">
                    <ExportButtons @export-completed="handleExportCompleted" />
                    <el-button type="primary" @click="$router.push('/resumes/upload')" icon="Plus">
                      Загрузить резюме
                    </el-button>
                    <el-button type="success" @click="$router.push('/resumes/batch-upload')" icon="Upload">
                      Пакетная загрузка
                    </el-button>
                  </div>
                </div>

    <!-- Фильтры -->
    <el-card class="filter-card">
      <div class="filters">
        <el-select v-model="filters.vacancy_id" placeholder="Вакансия" clearable style="width: 200px">
          <el-option
            v-for="vacancy in vacancies"
            :key="vacancy.id"
            :label="vacancy.title"
            :value="vacancy.id"
          />
        </el-select>
        
        <el-select v-model="filters.status" placeholder="Статус" clearable style="width: 150px">
          <el-option label="Загружено" value="uploaded" />
          <el-option label="Обрабатывается" value="processing" />
          <el-option label="Проанализировано" value="analyzed" />
          <el-option label="Ошибка" value="error" />
        </el-select>
        
        <el-button @click="loadResumes" type="primary" icon="Search">
          Применить фильтры
        </el-button>
        
        <el-button @click="clearFilters" icon="Refresh">
          Сбросить
        </el-button>
      </div>
    </el-card>

    <!-- Статистика -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ statistics.total_resumes }}</div>
            <div class="stat-label">Всего резюме</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ statistics.processed_resumes }}</div>
            <div class="stat-label">Обработано</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ statistics.average_score }}%</div>
            <div class="stat-label">Средняя оценка</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ statistics.error_resumes }}</div>
            <div class="stat-label">Ошибки</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Таблица резюме -->
    <el-card>
      <template #header>
        <div class="table-header">
          <span>Список резюме</span>
          <el-button @click="loadResumes" icon="Refresh" size="small">
            Обновить
          </el-button>
        </div>
      </template>
      
      <el-table
        :data="resumes"
        v-loading="loading"
        style="width: 100%"
        @sort-change="handleSortChange"
      >
        <!-- Debug info -->
        <template #empty>
          <div>
            <p>No Data</p>
            <p>Resumes count (in component): {{ resumes.length }}</p>
            <p>Loading: {{ loading }}</p>
            <p>Total from pagination: {{ pagination.total }}</p>
            <button @click="loadResumes">Reload Resumes</button>
          </div>
        </template>

        <el-table-column prop="original_filename" label="Файл" sortable="custom">
          <template #default="{ row }">
            <div class="file-info">
              <el-icon><Document /></el-icon>
              <span>{{ row.original_filename }}</span>
              <el-tag size="small" :type="getFileTypeTag(row.file_type)">
                {{ row.file_type.toUpperCase() }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="vacancy_title" label="Вакансия" sortable="custom">
          <template #default="{ row }">
            <span v-if="row.vacancy_title">{{ row.vacancy_title }}</span>
            <span v-else class="text-muted">Не указана</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="Статус" sortable="custom" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="total_score" label="Оценка" sortable="custom" width="100">
          <template #default="{ row }">
            <div v-if="row.total_score !== null" class="score-info">
              <el-progress
                :percentage="row.total_score"
                :color="getScoreColor(row.total_score)"
                :stroke-width="8"
                :show-text="false"
              />
              <span class="score-text">{{ row.total_score }}%</span>
            </div>
            <span v-else class="text-muted">-</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="upload_date" label="Дата загрузки" sortable="custom" width="150">
          <template #default="{ row }">
            {{ formatDate(row.upload_date) }}
          </template>
        </el-table-column>
        
        <el-table-column label="Действия" width="280" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button
                size="small"
                @click="$router.push(`/resumes/${row.id}`)"
                type="primary"
                title="Просмотр"
              >
                <el-icon><View /></el-icon>
              </el-button>
              
              <el-button
                v-if="row.status === 'uploaded'"
                size="small"
                type="warning"
                @click="processResume(row.id)"
                :loading="processingResume === row.id"
                title="Обработать"
              >
                <el-icon><VideoPlay /></el-icon>
              </el-button>
              
              <el-button
                v-if="row.status === 'analyzed' && !row.total_score"
                size="small"
                type="success"
                @click="calculateScore(row.id)"
                :loading="calculatingScore === row.id"
                title="Оценить"
              >
                <el-icon><TrendCharts /></el-icon>
              </el-button>
              
              <el-button
                size="small"
                @click="downloadResume(row.id)"
                type="info"
                title="Скачать"
              >
                <el-icon><Download /></el-icon>
              </el-button>
              
              <el-button
                size="small"
                @click="deleteResume(row.id)"
                type="danger"
                title="Удалить"
              >
                <el-icon><Delete /></el-icon>
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- Пагинация -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.limit"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted, reactive, toRaw } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document, Download, Delete, Plus, Search, Refresh, View, VideoPlay, TrendCharts } from '@element-plus/icons-vue'
import ExportButtons from '@/components/ExportButtons.vue'

export default {
  name: 'ResumesList',
  components: {
    Document,
    Download,
    Delete,
    Plus,
    Search,
    Refresh,
    View,
    VideoPlay,
    TrendCharts,
    ExportButtons
  },
  setup() {
    const resumes = ref([])
    const vacancies = ref([])
    const loading = ref(false)
    const processingResume = ref(null)
    const calculatingScore = ref(null)
    
    const statistics = reactive({
      total_resumes: 0,
      processed_resumes: 0,
      average_score: 0,
      error_resumes: 0
    })
    
    const filters = reactive({
      vacancy_id: null,
      status: null
    })
    
    const pagination = reactive({
      page: 1,
      limit: 20,
      total: 0
    })
    
    const loadResumes = async () => {
      console.log('🔍 loadResumes called')
      loading.value = true
      try {
        const params = {
          skip: (pagination.page - 1) * pagination.limit,
          limit: pagination.limit
        }
        
        // Добавляем фильтры только если они не null
        if (filters.vacancy_id) {
          params.vacancy_id = filters.vacancy_id
        }
        if (filters.status) {
          params.status = filters.status
        }
        
        console.log('📤 Request params:', toRaw(params))
        const url = `/api/v1/resumes/?${new URLSearchParams(params)}`
        console.log('🌐 Request URL:', url)
        
        const response = await fetch(url)
        console.log('📥 Response status:', response.status)
        console.log('📥 Response headers:', toRaw(Object.fromEntries(response.headers.entries())))
        
        if (!response.ok) {
          const errorText = await response.text()
          throw new Error(`HTTP error! status: ${response.status}, details: ${errorText}`)
        }
        
        const data = await response.json()
        console.log('📊 API Response (raw):', toRaw(data))
        
        // Правильная обработка ответа API
        resumes.value = data.resumes || []
        console.log('✅ Resumes after update (raw):', toRaw(resumes.value))
        console.log('✅ Resumes after update (length):', resumes.value.length)
        pagination.total = data.total || 0
        pagination.page = data.page || 1
        pagination.limit = data.size || 20
        console.log('✅ Pagination after update:', toRaw(pagination))
      } catch (error) {
        ElMessage.error(`Ошибка загрузки резюме: ${error.message}`)
        console.error('❌ Error loading resumes:', error)
      } finally {
        loading.value = false
      }
    }
    
    const loadStatistics = async () => {
      try {
        const response = await fetch('/api/v1/resumes/statistics')
        const data = await response.json()
        Object.assign(statistics, data)
      } catch (error) {
        console.error('Ошибка загрузки статистики:', error)
      }
    }
    
    const loadVacancies = async () => {
      try {
        const response = await fetch('/api/v1/vacancies/')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const data = await response.json()
        vacancies.value = data || []
      } catch (error) {
        console.error('Ошибка загрузки вакансий:', error)
        ElMessage.error('Ошибка загрузки списка вакансий')
      }
    }
    
    const processResume = async (resumeId) => {
      processingResume.value = resumeId
      try {
        const response = await fetch(`/api/v1/resumes/${resumeId}/process`, {
          method: 'POST'
        })
        const data = await response.json()
        
        if (data.success) {
          ElMessage.success('Резюме обработано успешно')
          await loadResumes()
          await loadStatistics()
        } else {
          ElMessage.error(data.error || 'Ошибка обработки')
        }
      } catch (error) {
        ElMessage.error('Ошибка обработки резюме')
        console.error(error)
      } finally {
        processingResume.value = null
      }
    }
    
    const calculateScore = async (resumeId) => {
      calculatingScore.value = resumeId
      try {
        const response = await fetch(`/api/v1/resumes/${resumeId}/calculate-score`, {
          method: 'POST'
        })
        const data = await response.json()
        
        if (data.success) {
          ElMessage.success('Оценка рассчитана успешно')
          await loadResumes()
          await loadStatistics()
        } else {
          ElMessage.error(data.error || 'Ошибка расчета оценки')
        }
      } catch (error) {
        ElMessage.error('Ошибка расчета оценки')
        console.error(error)
      } finally {
        calculatingScore.value = null
      }
    }
    
    const downloadResume = async (resumeId) => {
      try {
        const response = await fetch(`/api/v1/resumes/${resumeId}/download`)
        const data = await response.json()
        
        if (data.download_url) {
          window.open(data.download_url, '_blank')
        }
      } catch (error) {
        ElMessage.error('Ошибка скачивания файла')
        console.error(error)
      }
    }
    
    const deleteResume = async (resumeId) => {
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
        
        if (response.ok) {
          ElMessage.success('Резюме удалено')
          await loadResumes()
          await loadStatistics()
        } else {
          ElMessage.error('Ошибка удаления')
        }
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('Ошибка удаления резюме')
          console.error(error)
        }
      }
    }
    
    const clearFilters = () => {
      filters.vacancy_id = null
      filters.status = null
      loadResumes()
    }
    
    const handleSortChange = ({ prop, order }) => {
      // В реальном приложении здесь будет сортировка
      console.log('Sort:', prop, order)
    }
    
    const handleSizeChange = (size) => {
      pagination.limit = size
      pagination.page = 1
      loadResumes()
    }
    
    const handleCurrentChange = (page) => {
      pagination.page = page
      loadResumes()
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
    
    const getFileTypeTag = (fileType) => {
      if (!fileType) return 'info'
      const types = {
        pdf: 'danger',
        docx: 'primary',
        rtf: 'warning',
        txt: 'info'
      }
      return types[fileType.toLowerCase()] || 'info'
    }
    
    const getScoreColor = (score) => {
      if (score >= 80) return '#67C23A'
      if (score >= 60) return '#E6A23C'
      return '#F56C6C'
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'Не указано'
      try {
        return new Date(dateString).toLocaleDateString('ru-RU', {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        })
      } catch (error) {
        console.error('Date formatting error:', error, 'for date:', dateString)
        return 'Некорректная дата'
      }
    }
    
    const handleExportCompleted = (exportInfo) => {
      console.log('Export completed:', exportInfo)
      // Можно добавить дополнительную логику после экспорта
    }
    
    onMounted(() => {
      loadResumes()
      loadStatistics()
      loadVacancies()
    })
    
    return {
      resumes,
      vacancies,
      loading,
      processingResume,
      calculatingScore,
      statistics,
      filters,
      pagination,
      loadResumes,
      processResume,
      calculateScore,
      downloadResume,
      deleteResume,
      clearFilters,
      handleSortChange,
      handleSizeChange,
      handleCurrentChange,
      getStatusType,
      getStatusLabel,
      getFileTypeTag,
      getScoreColor,
      formatDate,
      handleExportCompleted
    }
  }
}
</script>

<style scoped>
.resumes-list {
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

.filter-card {
  margin-bottom: 20px;
}

.filters {
  display: flex;
  gap: 15px;
  align-items: center;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 10px;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.stat-label {
  color: #606266;
  font-size: 14px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.score-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.score-text {
  font-weight: bold;
  min-width: 35px;
}

.text-muted {
  color: #909399;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
