<template>
  <div class="vacancies-list">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>Управление вакансиями</h1>
          <BaseButton variant="primary" @click="createVacancy" size="large" :icon="Plus">
            Создать вакансию
          </BaseButton>
        </div>
      </el-header>
      
      <el-main>
        <!-- Статистические карточки -->
        <el-row :gutter="20" class="stats-row">
          <el-col :span="6" v-for="stat in statistics" :key="stat.title">
            <BaseMetricCard
              :title="stat.title"
              :value="stat.value"
              :icon="stat.icon"
              :variant="stat.type"
            />
          </el-col>
        </el-row>

        <!-- Фильтры и поиск -->
        <el-card class="filter-card" shadow="never">
          <el-form :model="filters" inline class="filter-form">
            <el-form-item label="Статус">
              <BaseSelect 
                v-model="filters.status" 
                :options="statusOptions"
                placeholder="Все статусы" 
                clearable 
                size="sm"
              />
            </el-form-item>
            
            <el-form-item label="Регион">
              <BaseInput 
                v-model="filters.region" 
                placeholder="Поиск по региону" 
                size="sm"
              />
            </el-form-item>
            
            <el-form-item label="Город">
              <BaseInput 
                v-model="filters.city" 
                placeholder="Поиск по городу" 
                size="sm"
              />
            </el-form-item>
            
            <el-form-item label="Тип занятости">
              <BaseSelect 
                v-model="filters.employment_type" 
                :options="employmentOptions"
                placeholder="Все типы" 
                clearable 
                size="sm"
              />
            </el-form-item>
            
            <el-form-item>
              <BaseButton variant="primary" @click="applyFilters" :loading="loading" :icon="Search"  style="margin-right: 1rem;">
                Применить
              </BaseButton>
              <BaseButton variant="ghost" @click="clearFilters" :icon="Refresh">
                Очистить
              </BaseButton>
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
                <BaseButton @click="refreshData" :loading="loading" size="small" variant="ghost" :icon="Refresh">
                  Обновить
                </BaseButton>
                <BaseButton @click="exportVacancies" size="small" variant="secondary" :icon="Download">
                  Экспорт
                </BaseButton>
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
                <div class="action-buttons">
                  <BaseButton size="small" @click.stop="viewVacancy(row)" variant="primary" :icon="View" />
                  <BaseButton size="small" @click.stop="editVacancy(row)" variant="secondary" :icon="Edit" />
                  <BaseButton size="small" @click.stop="deleteVacancy(row)" variant="danger" :icon="Delete" />
                </div>
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
import { BaseSelect, BaseInput, BaseButton, BaseMetricCard } from '@/components/base'

export default {
  name: 'VacanciesList',
  components: {
    Plus, Search, Refresh, Download, View, Edit, Delete,
    Document, User, Briefcase, Money,
    BaseButton,
    BaseSelect, BaseInput, BaseMetricCard
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

    const statusOptions = computed(() => [
      { label: 'Активные', value: 'active' },
      { label: 'Закрытые', value: 'closed' },
      { label: 'Черновики', value: 'draft' }
    ])

    const employmentOptions = computed(() => [
      { label: 'Полная', value: 'full' },
      { label: 'Частичная', value: 'part' },
      { label: 'Удаленная', value: 'remote' }
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
      statusOptions,
      employmentOptions,
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
  background: transparent;
  padding: 0;
  overflow: visible;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 1rem 0;
  margin-bottom: 1rem;
}

.header-content h1 {
  margin: 0;
  color: #00ffff;
  font-size: 2rem;
  font-weight: 700;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
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
  margin-bottom: 2rem;
  margin-top: 1rem;
  padding-top: 2rem;
  padding-bottom: 1rem;
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
  margin-bottom: 2rem;
  border: none;
  border-radius: 12px;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.2);
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
  border-radius: 12px;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.2);
  margin-bottom: 2rem;
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
  padding: 1.5rem;
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
  background: transparent;
  color: #e2e8f0;
}

:deep(.el-card__body) {
  padding: 1.5rem;
  background: transparent;
}

:deep(.el-table) {
  background: transparent !important;
  color: #e2e8f0 !important;
}

:deep(.el-table th) {
  background: rgba(0, 255, 255, 0.1) !important;
  color: #00ffff !important;
  font-weight: 600;
  border-bottom: 1px solid rgba(0, 255, 255, 0.2) !important;
}

:deep(.el-table td) {
  background: transparent !important;
  color: #e2e8f0 !important;
  border-bottom: 1px solid rgba(0, 255, 255, 0.1) !important;
}

:deep(.el-table--striped .el-table__body tr.el-table__row--striped td) {
  background: rgba(0, 255, 255, 0.05) !important;
}

:deep(.el-table__body tr:hover > td) {
  background: rgba(0, 255, 255, 0.1) !important;
}

:deep(.el-container) {
  background: transparent;
}

:deep(.el-header) {
  background: transparent;
  padding: 0;
  height: auto;
}

:deep(.el-main) {
  padding: 0;
  overflow: visible !important;
}

:deep(.el-container) {
  overflow: visible !important;
}

:deep(.stats-row .el-col) {
  padding-top: 1rem;
  padding-bottom: 1rem;
}

:deep(.stats-row) {
  overflow: visible !important;
}

:deep(.el-row) {
  overflow: visible !important;
}
</style>
.action-buttons {
  display: flex;
  gap: 0.5rem;
}