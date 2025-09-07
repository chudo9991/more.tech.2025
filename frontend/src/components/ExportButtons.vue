<template>
  <div class="export-buttons" ref="dropdownRef">
    <BaseButton 
      variant="primary" 
      @click="toggleDropdown"
      class="export-trigger"
    >
      <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
        <polyline points="7,10 12,15 17,10"/>
        <line x1="12" y1="15" x2="12" y2="3"/>
      </svg>
      Экспорт
      <svg class="arrow-icon" :class="{ 'rotated': isDropdownOpen }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="6,9 12,15 18,9"/>
      </svg>
    </BaseButton>
    
    <div v-if="isDropdownOpen" class="dropdown-menu">
      <button 
        v-if="resumeId"
        @click="handleExport('resume-json')"
        class="dropdown-item"
      >
        <svg class="item-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
        </svg>
        Резюме (JSON)
      </button>
      
      <button 
        v-if="resumeId"
        @click="handleExport('resume-csv')"
        class="dropdown-item"
      >
        <svg class="item-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
        </svg>
        Резюме (CSV)
      </button>
      
      <button 
        v-if="vacancyId"
        @click="handleExport('vacancy-json')"
        class="dropdown-item"
      >
        <svg class="item-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M10,4H4C2.89,4 2,4.89 2,6V18A2,2 0 0,0 4,20H20A2,2 0 0,0 22,18V8C22,6.89 21.1,6 20,6H12L10,4Z"/>
        </svg>
        Вакансия (JSON)
      </button>
      
      <button 
        v-if="vacancyId"
        @click="handleExport('vacancy-csv')"
        class="dropdown-item"
      >
        <svg class="item-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M10,4H4C2.89,4 2,4.89 2,6V18A2,2 0 0,0 4,20H20A2,2 0 0,0 22,18V8C22,6.89 21.1,6 20,6H12L10,4Z"/>
        </svg>
        Вакансия (CSV)
      </button>
      
      <button 
        @click="handleExport('statistics-json')"
        class="dropdown-item"
      >
        <svg class="item-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 3v18h18"/>
          <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/>
        </svg>
        Статистика (JSON)
      </button>
      
      <button 
        @click="handleExport('statistics-csv')"
        class="dropdown-item"
      >
        <svg class="item-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 3v18h18"/>
          <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/>
        </svg>
        Статистика (CSV)
      </button>
      
      <button 
        v-if="batchId"
        @click="handleExport('batch-json')"
        class="dropdown-item"
      >
        <svg class="item-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
          <path d="M16,10V18H8V10H16M14,12H10V16H14V12Z"/>
        </svg>
        Batch результаты (JSON)
      </button>
      
      <button 
        v-if="batchId"
        @click="handleExport('batch-csv')"
        class="dropdown-item"
      >
        <svg class="item-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
          <path d="M16,10V18H8V10H16M14,12H10V16H14V12Z"/>
        </svg>
        Batch результаты (CSV)
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import BaseButton from './base/BaseButton.vue'

export default {
  name: 'ExportButtons',
  components: {
    BaseButton
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
    const isDropdownOpen = ref(false)
    const dropdownRef = ref(null)

    const toggleDropdown = () => {
      isDropdownOpen.value = !isDropdownOpen.value
    }

    const closeDropdown = () => {
      isDropdownOpen.value = false
    }

    const handleClickOutside = (event) => {
      if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
        closeDropdown()
      }
    }

    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
    })

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })

    const handleExport = async (command) => {
      closeDropdown()
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
        
        // Show success message (you can replace with your notification system)
        console.log('Экспорт завершен успешно')
        emit('export-completed', { command, filename })
        
      } catch (error) {
        console.error('Export error:', error)
        // Show error message (you can replace with your notification system)
        console.error(`Ошибка экспорта: ${error.message}`)
      }
    }
    
    return {
      isDropdownOpen,
      dropdownRef,
      toggleDropdown,
      handleExport
    }
  }
}
</script>

<style scoped>
.export-buttons {
  position: relative;
  display: inline-block;
}

.export-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon {
  width: 16px;
  height: 16px;
}

.arrow-icon {
  width: 14px;
  height: 14px;
  transition: transform 0.2s ease;
}

.arrow-icon.rotated {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(30, 30, 30, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 8px;
  margin-top: 4px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  min-width: 200px;
}

.dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: none;
  border: none;
  color: #e5e7eb;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s ease;
  text-align: left;
}

.dropdown-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  transform: translateX(2px);
}

.item-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}
</style>
