<template>
  <div class="export-buttons">
    <el-dropdown @command="handleExport" trigger="click">
      <el-button type="primary" icon="Download">
        Экспорт
        <el-icon class="el-icon--right"><arrow-down /></el-icon>
      </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item command="resume-json" v-if="resumeId">
            <el-icon><document /></el-icon>
            Резюме (JSON)
          </el-dropdown-item>
          <el-dropdown-item command="resume-csv" v-if="resumeId">
            <el-icon><document /></el-icon>
            Резюме (CSV)
          </el-dropdown-item>
          <el-dropdown-item command="vacancy-json" v-if="vacancyId">
            <el-icon><folder /></el-icon>
            Вакансия (JSON)
          </el-dropdown-item>
          <el-dropdown-item command="vacancy-csv" v-if="vacancyId">
            <el-icon><folder /></el-icon>
            Вакансия (CSV)
          </el-dropdown-item>
          <el-dropdown-item command="statistics-json">
            <el-icon><data-analysis /></el-icon>
            Статистика (JSON)
          </el-dropdown-item>
          <el-dropdown-item command="statistics-csv">
            <el-icon><data-analysis /></el-icon>
            Статистика (CSV)
          </el-dropdown-item>
          <el-dropdown-item command="batch-json" v-if="batchId">
            <el-icon><files /></el-icon>
            Batch результаты (JSON)
          </el-dropdown-item>
          <el-dropdown-item command="batch-csv" v-if="batchId">
            <el-icon><files /></el-icon>
            Batch результаты (CSV)
          </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'
import { ArrowDown, Document, Folder, DataAnalysis, Files } from '@element-plus/icons-vue'

export default {
  name: 'ExportButtons',
  components: {
    ArrowDown,
    Document,
    Folder,
    DataAnalysis,
    Files
  },
  props: {
    resumeId: {
      type: String,
      default: null
    },
    vacancyId: {
      type: String,
      default: null
    },
    batchId: {
      type: String,
      default: null
    }
  },
  emits: ['export-completed'],
  setup(props, { emit }) {
    const handleExport = async (command) => {
      try {
        let url = ''
        let filename = ''
        
        switch (command) {
          case 'resume-json':
            url = `/api/v1/export/resume/${props.resumeId}/json`
            filename = `resume_${props.resumeId}.json`
            break
          case 'resume-csv':
            url = `/api/v1/export/resume/${props.resumeId}/csv`
            filename = `resume_${props.resumeId}.csv`
            break
          case 'vacancy-json':
            url = `/api/v1/export/vacancy/${props.vacancyId}/resumes/json`
            filename = `vacancy_${props.vacancyId}_resumes.json`
            break
          case 'vacancy-csv':
            url = `/api/v1/export/vacancy/${props.vacancyId}/resumes/csv`
            filename = `vacancy_${props.vacancyId}_resumes.csv`
            break
          case 'statistics-json':
            url = `/api/v1/export/statistics/json`
            filename = `resume_statistics.json`
            break
          case 'statistics-csv':
            url = `/api/v1/export/statistics/csv`
            filename = `resume_statistics.csv`
            break
          case 'batch-json':
            url = `/api/v1/export/batch/${props.batchId}/results/json`
            filename = `batch_${props.batchId}_results.json`
            break
          case 'batch-csv':
            url = `/api/v1/export/batch/${props.batchId}/results/csv`
            filename = `batch_${props.batchId}_results.csv`
            break
          default:
            ElMessage.error('Неизвестный тип экспорта')
            return
        }
        
        const response = await fetch(url)
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        // Check if it's a CSV download
        const contentType = response.headers.get('content-type')
        if (contentType && contentType.includes('text/csv')) {
          // Handle CSV download
          const blob = await response.blob()
          const downloadUrl = window.URL.createObjectURL(blob)
          const link = document.createElement('a')
          link.href = downloadUrl
          link.download = filename
          document.body.appendChild(link)
          link.click()
          document.body.removeChild(link)
          window.URL.revokeObjectURL(downloadUrl)
        } else {
          // Handle JSON download
          const data = await response.json()
          const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
          const downloadUrl = window.URL.createObjectURL(blob)
          const link = document.createElement('a')
          link.href = downloadUrl
          link.download = filename
          document.body.appendChild(link)
          link.click()
          document.body.removeChild(link)
          window.URL.revokeObjectURL(downloadUrl)
        }
        
        ElMessage.success('Экспорт завершен успешно')
        emit('export-completed', { command, filename })
        
      } catch (error) {
        console.error('Export error:', error)
        ElMessage.error(`Ошибка экспорта: ${error.message}`)
      }
    }
    
    return {
      handleExport
    }
  }
}
</script>

<style scoped>
.export-buttons {
  display: inline-block;
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 8px;
}

:deep(.el-dropdown-menu__item .el-icon) {
  margin-right: 0;
}
</style>
