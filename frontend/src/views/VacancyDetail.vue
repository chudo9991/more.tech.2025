<template>
  <div class="vacancy-detail">
    <el-container>
      <el-header>
        <div class="header-content">
          <div class="header-left">
            <h1>{{ vacancy.title || 'Загрузка...' }}</h1>
            <div class="vacancy-meta">
              <el-tag v-if="vacancy.vacancy_code" type="info" size="large">
                {{ vacancy.vacancy_code }}
              </el-tag>
              <el-tag :type="getStatusType(vacancy.status)" size="large">
                {{ getStatusLabel(vacancy.status) }}
              </el-tag>
            </div>
          </div>
          <div class="header-actions">
            <el-button @click="goBack" size="large">
              <el-icon><ArrowLeft /></el-icon>
              Назад
            </el-button>
            <el-button @click="editVacancy" type="warning" size="large">
              <el-icon><Edit /></el-icon>
              Редактировать
            </el-button>
            <el-button @click="exportVacancy" type="success" size="large">
              <el-icon><Download /></el-icon>
              Экспорт
            </el-button>
          </div>
        </div>
      </el-header>
      
      <el-main v-loading="loading">
        <div v-if="vacancy.id" class="vacancy-content">
          <!-- Основная информация -->
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <el-icon><Document /></el-icon>
                <span>Основная информация</span>
              </div>
            </template>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="info-item">
                  <label>Название:</label>
                  <span class="info-value">{{ vacancy.title }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="info-item">
                  <label>Статус:</label>
                  <el-tag :type="getStatusType(vacancy.status)">
                    {{ getStatusLabel(vacancy.status) }}
                  </el-tag>
                </div>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="8">
                <div class="info-item">
                  <label>Регион:</label>
                  <span class="info-value">{{ vacancy.region || '—' }}</span>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="info-item">
                  <label>Город:</label>
                  <span class="info-value">{{ vacancy.city || '—' }}</span>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="info-item">
                  <label>Адрес:</label>
                  <span class="info-value">{{ vacancy.address || '—' }}</span>
                </div>
              </el-col>
            </el-row>
          </el-card>

          <!-- Условия труда -->
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <el-icon><Briefcase /></el-icon>
                <span>Условия труда</span>
              </div>
            </template>
            
            <el-row :gutter="20">
              <el-col :span="8">
                <div class="info-item">
                  <label>Тип занятости:</label>
                  <span class="info-value">{{ getEmploymentTypeLabel(vacancy.employment_type) || '—' }}</span>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="info-item">
                  <label>Тип договора:</label>
                  <span class="info-value">{{ getContractTypeLabel(vacancy.contract_type) || '—' }}</span>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="info-item">
                  <label>Командировки:</label>
                  <el-tag :type="vacancy.business_trips ? 'warning' : 'success'" size="small">
                    {{ vacancy.business_trips ? 'Требуются' : 'Не требуются' }}
                  </el-tag>
                </div>
              </el-col>
            </el-row>
            
            <div v-if="vacancy.work_schedule" class="info-item">
              <label>График работы:</label>
              <div class="info-text">{{ vacancy.work_schedule }}</div>
            </div>
          </el-card>

          <!-- Финансовые условия -->
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <el-icon><Money /></el-icon>
                <span>Финансовые условия</span>
              </div>
            </template>
            
            <el-row :gutter="20">
              <el-col :span="8">
                <div class="info-item">
                  <label>Оклад мин.:</label>
                  <span class="info-value">
                    {{ vacancy.salary_min ? formatSalary(vacancy.salary_min) + ' ₽/мес' : '—' }}
                  </span>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="info-item">
                  <label>Оклад макс.:</label>
                  <span class="info-value">
                    {{ vacancy.salary_max ? formatSalary(vacancy.salary_max) + ' ₽/мес' : '—' }}
                  </span>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="info-item">
                  <label>Общий доход:</label>
                  <span class="info-value">
                    {{ vacancy.total_income ? formatSalary(vacancy.total_income) + ' ₽/мес' : '—' }}
                  </span>
                </div>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="info-item">
                  <label>Годовая премия:</label>
                  <span class="info-value">
                    {{ vacancy.annual_bonus_percent ? vacancy.annual_bonus_percent + '%' : '—' }}
                  </span>
                </div>
              </el-col>
            </el-row>
            
            <div v-if="vacancy.bonus_description" class="info-item">
              <label>Описание премирования:</label>
              <div class="info-text">{{ vacancy.bonus_description }}</div>
            </div>
          </el-card>

          <!-- Требования к кандидату -->
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <el-icon><User /></el-icon>
                <span>Требования к кандидату</span>
              </div>
            </template>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="info-item">
                  <label>Уровень образования:</label>
                  <span class="info-value">{{ getEducationLevelLabel(vacancy.education_level) || '—' }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="info-item">
                  <label>Опыт работы:</label>
                  <span class="info-value">{{ getExperienceLabel(vacancy.experience_required) || '—' }}</span>
                </div>
              </el-col>
            </el-row>
            
            <div v-if="vacancy.responsibilities" class="info-item">
              <label>Обязанности:</label>
              <div class="info-text">{{ vacancy.responsibilities }}</div>
            </div>
            
            <div v-if="vacancy.requirements" class="info-item">
              <label>Требования:</label>
              <div class="info-text">{{ vacancy.requirements }}</div>
            </div>
            
            <div v-if="vacancy.special_programs" class="info-item">
              <label>Специальные программы:</label>
              <div class="info-text">{{ vacancy.special_programs }}</div>
            </div>
            
            <div v-if="vacancy.computer_skills" class="info-item">
              <label>Компьютерные навыки:</label>
              <div class="info-text">{{ vacancy.computer_skills }}</div>
            </div>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="info-item">
                  <label>Иностранные языки:</label>
                  <span class="info-value">{{ vacancy.foreign_languages || '—' }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="info-item">
                  <label>Уровень языка:</label>
                  <span class="info-value">{{ getLanguageLevelLabel(vacancy.language_level) || '—' }}</span>
                </div>
              </el-col>
            </el-row>
          </el-card>

          <!-- Дополнительная информация -->
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <el-icon><InfoFilled /></el-icon>
                <span>Дополнительная информация</span>
              </div>
            </template>
            
            <div v-if="vacancy.description" class="info-item">
              <label>Описание вакансии:</label>
              <div class="info-text">{{ vacancy.description }}</div>
            </div>
            
            <div v-if="vacancy.additional_info" class="info-item">
              <label>Дополнительная информация:</label>
              <div class="info-text">{{ vacancy.additional_info }}</div>
            </div>
          </el-card>

          <!-- Системная информация -->
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <el-icon><Setting /></el-icon>
                <span>Системная информация</span>
              </div>
            </template>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="info-item">
                  <label>ID вакансии:</label>
                  <span class="info-value">{{ vacancy.id }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="info-item">
                  <label>Код вакансии:</label>
                  <span class="info-value">{{ vacancy.vacancy_code || '—' }}</span>
                </div>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="info-item">
                  <label>Создано:</label>
                  <span class="info-value">{{ formatDate(vacancy.created_at) }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="info-item">
                  <label>Обновлено:</label>
                  <span class="info-value">{{ formatDate(vacancy.updated_at) }}</span>
                </div>
              </el-col>
            </el-row>
          </el-card>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  ArrowLeft, Edit, Download, Document, Briefcase, Money, User, InfoFilled, Setting
} from '@element-plus/icons-vue'

export default {
  name: 'VacancyDetail',
  components: {
    ArrowLeft, Edit, Download, Document, Briefcase, Money, User, InfoFilled, Setting
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const loading = ref(false)
    const vacancy = ref({})

    const loadVacancy = async () => {
      loading.value = true
      try {
        const response = await fetch(`/api/v1/vacancies/${route.params.id}`)
        if (!response.ok) throw new Error('Вакансия не найдена')
        
        const data = await response.json()
        vacancy.value = data
      } catch (error) {
        ElMessage.error('Ошибка загрузки вакансии: ' + error.message)
        router.push('/vacancies')
      } finally {
        loading.value = false
      }
    }

    const editVacancy = () => {
      router.push(`/vacancies/${route.params.id}/edit`)
    }

    const exportVacancy = () => {
      ElMessage.info('Функция экспорта будет добавлена позже')
    }

    const goBack = () => {
      router.push('/vacancies')
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

    const getContractTypeLabel = (type) => {
      const labels = {
        'employment': 'Трудовой',
        'contract': 'ГПХ',
        'internship': 'Стажировка'
      }
      return labels[type] || type
    }

    const getEducationLevelLabel = (level) => {
      const labels = {
        'secondary': 'Среднее',
        'vocational': 'Среднее специальное',
        'higher': 'Высшее',
        'masters': 'Магистратура',
        'phd': 'Аспирантура'
      }
      return labels[level] || level
    }

    const getExperienceLabel = (experience) => {
      const labels = {
        'no_experience': 'Без опыта',
        '1_year': 'От 1 года',
        '3_years': 'От 3 лет',
        '5_years': 'От 5 лет',
        'more_5_years': 'Более 5 лет'
      }
      return labels[experience] || experience
    }

    const getLanguageLevelLabel = (level) => {
      const labels = {
        'basic': 'Базовый',
        'intermediate': 'Средний',
        'advanced': 'Продвинутый',
        'fluent': 'Свободный'
      }
      return labels[level] || level
    }

    const formatSalary = (salary) => {
      return new Intl.NumberFormat('ru-RU').format(salary)
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    onMounted(() => {
      loadVacancy()
    })

    return {
      loading,
      vacancy,
      editVacancy,
      exportVacancy,
      goBack,
      getStatusType,
      getStatusLabel,
      getEmploymentTypeLabel,
      getContractTypeLabel,
      getEducationLevelLabel,
      getExperienceLabel,
      getLanguageLevelLabel,
      formatSalary,
      formatDate
    }
  }
}
</script>

<style scoped>
.vacancy-detail {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.header-left h1 {
  margin: 0 0 12px 0;
  color: #303133;
  font-size: 28px;
  font-weight: 600;
}

.vacancy-meta {
  display: flex;
  gap: 12px;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.vacancy-content {
  max-width: 1200px;
  margin: 0 auto;
}

.info-card {
  margin-bottom: 24px;
  border: none;
  border-radius: 8px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #303133;
}

.card-header .el-icon {
  font-size: 18px;
  color: #409eff;
}

.info-item {
  margin-bottom: 16px;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-item label {
  display: block;
  font-weight: 600;
  color: #606266;
  margin-bottom: 4px;
  font-size: 14px;
}

.info-value {
  color: #303133;
  font-size: 14px;
}

.info-text {
  color: #303133;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  background-color: #fafafa;
  padding: 12px;
  border-radius: 4px;
  border-left: 3px solid #409eff;
}

:deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
  background-color: #fafafa;
}

:deep(.el-card__body) {
  padding: 20px;
}
</style>
