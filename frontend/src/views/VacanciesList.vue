<template>
  <div class="vacancies-list">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>Управление вакансиями</h1>
          <el-button type="primary" @click="createVacancy" size="large">
            <el-icon><Plus /></el-icon>
            Создать вакансию
          </el-button>
        </div>
      </el-header>
      
      <el-main>
        <div class="page-description">
          <p>Создавайте и управляйте вакансиями для автоматизированных интервью</p>
        </div>
        <!-- Статистические карточки -->
        <el-row :gutter="20" class="stats-row">
          <el-col :span="6" v-for="stat in statistics" :key="stat.title">
            <el-card class="stat-card" shadow="hover">
              <div class="stat-content">
                <div class="stat-icon" :class="stat.type">
                  <el-icon><component :is="stat.icon" /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stat.value }}</div>
                  <div class="stat-title">{{ stat.title }}</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <!-- Фильтры и поиск -->
        <el-card class="filter-card" shadow="never">
          <el-form :model="filters" inline class="filter-form">
            <el-form-item label="Статус">
              <el-select v-model="filters.status" placeholder="Все статусы" clearable style="width: 150px">
                <el-option label="Активные" value="active" />
                <el-option label="Закрытые" value="closed" />
                <el-option label="Черновики" value="draft" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="Регион">
              <el-input v-model="filters.region" placeholder="Поиск по региону" style="width: 200px" />
            </el-form-item>
            
            <el-form-item label="Город">
              <el-input v-model="filters.city" placeholder="Поиск по городу" style="width: 200px" />
            </el-form-item>
            
            <el-form-item label="Тип занятости">
              <el-select v-model="filters.employment_type" placeholder="Все типы" clearable style="width: 150px">
                <el-option label="Полная" value="full" />
                <el-option label="Частичная" value="part" />
                <el-option label="Удаленная" value="remote" />
              </el-select>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="applyFilters" :loading="loading">
                <el-icon><Search /></el-icon>
                Применить
              </el-button>
              <el-button @click="clearFilters">
                <el-icon><Refresh /></el-icon>
                Очистить
              </el-button>
            </el-form-item>
          </el-form>
          
          <!-- Поиск по тексту -->
          <div class="search-section">
            <el-input
              v-model="filters.search"
              placeholder="Поиск по названию, требованиям, обязанностям..."
              clearable
              @keyup.enter="applyFilters"
              style="width: 400px"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
        </el-card>

        <!-- Таблица вакансий -->
        <el-card class="table-card" shadow="never">
          <template #header>
            <div class="table-header">
              <span>Список вакансий</span>
              <div class="table-actions">
                <el-button @click="refreshData" :loading="loading" size="small">
                  <el-icon><Refresh /></el-icon>
                  Обновить
                </el-button>
                <el-button @click="exportVacancies" size="small">
                  <el-icon><Download /></el-icon>
                  Экспорт
                </el-button>
              </div>
            </div>
          </template>
          
          <el-table
            :data="vacancies"
            v-loading="loading"
            @row-click="viewVacancy"
            class="vacancies-table"
            stripe
            hover
          >
            <el-table-column prop="vacancy_code" label="Код" width="120" fixed="left">
              <template #default="{ row }">
                <el-tag v-if="row.vacancy_code" type="info" size="small">
                  {{ row.vacancy_code }}
                </el-tag>
                <span v-else class="text-muted">—</span>
              </template>
            </el-table-column>
            
            <el-table-column prop="title" label="Название" min-width="200">
              <template #default="{ row }">
                <div class="vacancy-title">
                  <strong>{{ row.title }}</strong>
                  <div class="vacancy-meta">
                    <span v-if="row.region">{{ row.region }}</span>
                    <span v-if="row.city">, {{ row.city }}</span>
                  </div>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column prop="status" label="Статус" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)" size="small">
                  {{ getStatusLabel(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            
            <el-table-column prop="employment_type" label="Тип занятости" width="120">
              <template #default="{ row }">
                <span v-if="row.employment_type">{{ getEmploymentTypeLabel(row.employment_type) }}</span>
                <span v-else class="text-muted">—</span>
              </template>
            </el-table-column>
            
            <el-table-column prop="salary_min" label="Оклад" width="150">
              <template #default="{ row }">
                <div v-if="row.salary_min || row.salary_max" class="salary-info">
                  <span v-if="row.salary_min">{{ formatSalary(row.salary_min) }}</span>
                  <span v-if="row.salary_min && row.salary_max"> — </span>
                  <span v-if="row.salary_max">{{ formatSalary(row.salary_max) }}</span>
                  <span class="salary-currency">₽/мес</span>
                </div>
                <span v-else class="text-muted">—</span>
              </template>
            </el-table-column>
            
            <el-table-column prop="created_at" label="Создано" width="180">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            
            <el-table-column label="Действия" width="200" fixed="right">
              <template #default="{ row }">
                <el-button-group>
                  <el-button size="small" @click.stop="viewVacancy(row)" type="primary">
                    <el-icon><View /></el-icon>
                  </el-button>
                  <el-button size="small" @click.stop="editVacancy(row)" type="warning">
                    <el-icon><Edit /></el-icon>
                  </el-button>
                  <el-button size="small" @click.stop="deleteVacancy(row)" type="danger">
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
              v-model:page-size="pagination.size"
              :page-sizes="[10, 20, 50, 100]"
              :total="pagination.total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Plus, Search, Refresh, Download, View, Edit, Delete,
  Document, User, Briefcase, Money
} from '@element-plus/icons-vue'

export default {
  name: 'VacanciesList',
  components: {
    Plus, Search, Refresh, Download, View, Edit, Delete,
    Document, User, Briefcase, Money
  },
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const vacancies = ref([])
    
    const filters = reactive({
      status: '',
      region: '',
      city: '',
      employment_type: '',
      search: ''
    })
    
    const pagination = reactive({
      page: 1,
      size: 20,
      total: 0
    })
    
    const statistics = ref([
      { title: 'Всего вакансий', value: 0, icon: 'Document', type: 'primary' },
      { title: 'Активные', value: 0, icon: 'User', type: 'success' },
      { title: 'Закрытые', value: 0, icon: 'Briefcase', type: 'warning' },
      { title: 'Черновики', value: 0, icon: 'Money', type: 'info' }
    ])

    const loadVacancies = async () => {
      loading.value = true
      try {
        const params = new URLSearchParams({
          skip: (pagination.page - 1) * pagination.size,
          limit: pagination.size,
          ...filters
        })
        
        const response = await fetch(`/api/v1/vacancies/?${params}`)
        if (!response.ok) throw new Error('Ошибка загрузки вакансий')
        
        const data = await response.json()
        vacancies.value = data
        pagination.total = data.length // В реальном API здесь будет общее количество
      } catch (error) {
        ElMessage.error('Ошибка загрузки вакансий: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    const loadStatistics = async () => {
      try {
        const response = await fetch('/api/v1/vacancies/statistics')
        if (!response.ok) throw new Error('Ошибка загрузки статистики')
        
        const data = await response.json()
        statistics.value[0].value = data.total
        statistics.value[1].value = data.active
        statistics.value[2].value = data.closed
        statistics.value[3].value = data.draft
      } catch (error) {
        console.error('Ошибка загрузки статистики:', error)
      }
    }

    const createVacancy = () => {
      router.push('/vacancies/create')
    }

    const viewVacancy = (row) => {
      router.push(`/vacancies/${row.id}`)
    }

    const editVacancy = (row) => {
      router.push(`/vacancies/${row.id}/edit`)
    }

    const deleteVacancy = async (row) => {
      try {
        await ElMessageBox.confirm(
          `Удалить вакансию "${row.title}"?`,
          'Подтверждение удаления',
          { 
            type: 'warning',
            confirmButtonText: 'Удалить',
            cancelButtonText: 'Отмена'
          }
        )
        
        const response = await fetch(`/api/v1/vacancies/${row.id}`, { 
          method: 'DELETE' 
        })
        
        if (!response.ok) throw new Error('Ошибка удаления вакансии')
        
        ElMessage.success('Вакансия успешно удалена')
        loadVacancies()
        loadStatistics()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('Ошибка удаления вакансии: ' + error.message)
        }
      }
    }

    const applyFilters = () => {
      pagination.page = 1
      loadVacancies()
    }

    const clearFilters = () => {
      Object.keys(filters).forEach(key => {
        filters[key] = ''
      })
      pagination.page = 1
      loadVacancies()
    }

    const refreshData = () => {
      loadVacancies()
      loadStatistics()
    }

    const exportVacancies = () => {
      ElMessage.info('Функция экспорта будет добавлена позже')
    }

    const handleSizeChange = (size) => {
      pagination.size = size
      pagination.page = 1
      loadVacancies()
    }

    const handleCurrentChange = (page) => {
      pagination.page = page
      loadVacancies()
    }

    const getStatusType = (status) => {
      const types = {
        'active': 'success',
        'closed': 'danger',
        'draft': 'info'
      }
      return types[status] || 'info'
    }

    const getStatusLabel = (status) => {
      const labels = {
        'active': 'Активная',
        'closed': 'Закрытая',
        'draft': 'Черновик'
      }
      return labels[status] || status
    }

    const getEmploymentTypeLabel = (type) => {
      const labels = {
        'full': 'Полная',
        'part': 'Частичная',
        'remote': 'Удаленная'
      }
      return labels[type] || type
    }

    const formatSalary = (salary) => {
      return new Intl.NumberFormat('ru-RU').format(salary)
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    onMounted(() => {
      loadVacancies()
      loadStatistics()
    })

    return {
      loading,
      vacancies,
      filters,
      pagination,
      statistics,
      createVacancy,
      viewVacancy,
      editVacancy,
      deleteVacancy,
      applyFilters,
      clearFilters,
      refreshData,
      exportVacancies,
      handleSizeChange,
      handleCurrentChange,
      getStatusType,
      getStatusLabel,
      getEmploymentTypeLabel,
      formatSalary,
      formatDate
    }
  }
}
</script>

<style scoped>
.vacancies-list {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.header-content h1 {
  margin: 0;
  color: #303133;
  font-size: 28px;
  font-weight: 600;
}

.page-description {
  margin-bottom: 24px;
  text-align: center;
}

.page-description p {
  margin: 0;
  font-size: 16px;
  color: #606266;
  font-weight: 400;
}

.stats-row {
  margin-bottom: 24px;
}

.stat-card {
  border: none;
  border-radius: 8px;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stat-icon.primary { background-color: #409eff; }
.stat-icon.success { background-color: #67c23a; }
.stat-icon.warning { background-color: #e6a23c; }
.stat-icon.info { background-color: #909399; }

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  line-height: 1;
}

.stat-title {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.filter-card {
  margin-bottom: 24px;
  border: none;
  border-radius: 8px;
}

.filter-form {
  margin-bottom: 16px;
}

.search-section {
  display: flex;
  justify-content: center;
}

.table-card {
  border: none;
  border-radius: 8px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.table-actions {
  display: flex;
  gap: 8px;
}

.vacancies-table {
  margin-bottom: 16px;
}

.vacancy-title {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.vacancy-meta {
  font-size: 12px;
  color: #909399;
}

.salary-info {
  display: flex;
  align-items: center;
  gap: 4px;
}

.salary-currency {
  font-size: 12px;
  color: #909399;
}

.text-muted {
  color: #c0c4cc;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 16px;
}

:deep(.el-table) {
  border-radius: 8px;
}

:deep(.el-table th) {
  background-color: #fafafa;
  font-weight: 600;
}

:deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__body) {
  padding: 20px;
}
</style>
