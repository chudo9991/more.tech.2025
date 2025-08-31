<template>
  <div class="vacancy-form">
    <el-container>
      <el-header>
        <div class="header-content">
          <div class="header-left">
            <h1>{{ isEdit ? 'Редактирование вакансии' : 'Создание вакансии' }}</h1>
          </div>
          <div class="header-actions">
            <el-button @click="goBack" size="large">
              <el-icon><ArrowLeft /></el-icon>
              Назад
            </el-button>
            <el-button 
              v-if="isEdit && route?.params?.id"
              type="success" 
              @click="generateScenario" 
              :loading="generatingScenario"
              size="large"
            >
              <el-icon><Star /></el-icon>
              Сгенерировать сценарий
            </el-button>
            <el-button 
              type="primary" 
              @click="saveVacancy" 
              :loading="saving"
              size="large"
            >
              <el-icon><Check /></el-icon>
              {{ isEdit ? 'Сохранить' : 'Создать' }}
            </el-button>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-width="200px"
          class="vacancy-form-content"
          @submit.prevent="saveVacancy"
        >
          <!-- Основная информация -->
          <el-card class="form-section">
            <template #header>
              <div class="section-header">
                <el-icon><Document /></el-icon>
                <span>Основная информация</span>
              </div>
            </template>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="Название вакансии" prop="title">
                  <el-input 
                    v-model="form.title" 
                    placeholder="Введите название вакансии"
                    maxlength="255"
                    show-word-limit
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="Статус" prop="status">
                  <el-select v-model="form.status" placeholder="Выберите статус" style="width: 100%">
                    <el-option label="Активная" value="active" />
                    <el-option label="Закрытая" value="closed" />
                    <el-option label="Черновик" value="draft" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="Регион" prop="region">
                  <el-input v-model="form.region" placeholder="Регион" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="Город" prop="city">
                  <el-input v-model="form.city" placeholder="Город" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="Адрес" prop="address">
                  <el-input v-model="form.address" placeholder="Адрес" />
                </el-form-item>
              </el-col>
            </el-row>
          </el-card>

          <!-- Условия труда -->
          <el-card class="form-section">
            <template #header>
              <div class="section-header">
                <el-icon><Briefcase /></el-icon>
                <span>Условия труда</span>
              </div>
            </template>
            
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="Тип занятости" prop="employment_type">
                  <el-select v-model="form.employment_type" placeholder="Выберите тип" style="width: 100%">
                    <el-option label="Полная" value="full" />
                    <el-option label="Частичная" value="part" />
                    <el-option label="Удаленная" value="remote" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="Тип договора" prop="contract_type">
                  <el-select v-model="form.contract_type" placeholder="Выберите тип" style="width: 100%">
                    <el-option label="Трудовой" value="employment" />
                    <el-option label="ГПХ" value="contract" />
                    <el-option label="Стажировка" value="internship" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="Командировки" prop="business_trips">
                  <el-switch v-model="form.business_trips" />
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item label="График работы" prop="work_schedule">
              <el-input
                v-model="form.work_schedule"
                type="textarea"
                :rows="3"
                placeholder="Опишите график работы"
              />
            </el-form-item>
          </el-card>

          <!-- Финансовые условия -->
          <el-card class="form-section">
            <template #header>
              <div class="section-header">
                <el-icon><Money /></el-icon>
                <span>Финансовые условия</span>
              </div>
            </template>
            
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="Оклад мин. (руб/мес)" prop="salary_min">
                  <el-input-number
                    v-model="form.salary_min"
                    :min="0"
                    :precision="0"
                    style="width: 100%"
                    placeholder="Минимальный оклад"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="Оклад макс. (руб/мес)" prop="salary_max">
                  <el-input-number
                    v-model="form.salary_max"
                    :min="0"
                    :precision="0"
                    style="width: 100%"
                    placeholder="Максимальный оклад"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="Общий доход (руб/мес)" prop="total_income">
                  <el-input-number
                    v-model="form.total_income"
                    :min="0"
                    :precision="0"
                    style="width: 100%"
                    placeholder="Общий доход"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="Годовая премия (%)" prop="annual_bonus_percent">
                  <el-input-number
                    v-model="form.annual_bonus_percent"
                    :min="0"
                    :max="100"
                    :precision="1"
                    style="width: 100%"
                    placeholder="Процент премии"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item label="Описание премирования" prop="bonus_description">
              <el-input
                v-model="form.bonus_description"
                type="textarea"
                :rows="3"
                placeholder="Опишите систему премирования"
              />
            </el-form-item>
          </el-card>

          <!-- Требования к кандидату -->
          <el-card class="form-section">
            <template #header>
              <div class="section-header">
                <el-icon><User /></el-icon>
                <span>Требования к кандидату</span>
              </div>
            </template>
            
            <el-form-item label="Обязанности" prop="responsibilities">
              <el-input
                v-model="form.responsibilities"
                type="textarea"
                :rows="5"
                placeholder="Опишите обязанности кандидата"
                maxlength="2000"
                show-word-limit
              />
              <!-- Keywords Section for Responsibilities -->
              <KeywordsSection
                v-if="isEdit && hasVacancyId"
                :vacancy-id="vacancyId"
                section-type="responsibilities"
                section-title="Обязанности"
                :section-text="form.responsibilities"
                @keywords-updated="handleKeywordsUpdated"
              />
            </el-form-item>
            
            <el-form-item label="Требования" prop="requirements">
              <el-input
                v-model="form.requirements"
                type="textarea"
                :rows="5"
                placeholder="Опишите требования к кандидату"
                maxlength="2000"
                show-word-limit
              />
              <!-- Keywords Section for Requirements -->
              <KeywordsSection
                v-if="isEdit && hasVacancyId"
                :vacancy-id="vacancyId"
                section-type="requirements"
                section-title="Требования"
                :section-text="form.requirements"
                @keywords-updated="handleKeywordsUpdated"
              />
            </el-form-item>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="Уровень образования" prop="education_level">
                  <el-select v-model="form.education_level" placeholder="Выберите уровень" style="width: 100%">
                    <el-option label="Среднее" value="secondary" />
                    <el-option label="Среднее специальное" value="vocational" />
                    <el-option label="Высшее" value="higher" />
                    <el-option label="Магистратура" value="masters" />
                    <el-option label="Аспирантура" value="phd" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="Опыт работы" prop="experience_required">
                  <el-select v-model="form.experience_required" placeholder="Выберите опыт" style="width: 100%">
                    <el-option label="Без опыта" value="no_experience" />
                    <el-option label="От 1 года" value="1_year" />
                    <el-option label="От 3 лет" value="3_years" />
                    <el-option label="От 5 лет" value="5_years" />
                    <el-option label="Более 5 лет" value="more_5_years" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item label="Специальные программы" prop="special_programs">
              <el-input
                v-model="form.special_programs"
                type="textarea"
                :rows="3"
                placeholder="Укажите требуемые программы"
              />
              <!-- Keywords Section for Special Programs -->
              <KeywordsSection
                v-if="isEdit && hasVacancyId"
                :vacancy-id="vacancyId"
                section-type="programs"
                section-title="Специальные программы"
                :section-text="form.special_programs"
                @keywords-updated="handleKeywordsUpdated"
              />
            </el-form-item>
            
            <el-form-item label="Компьютерные навыки" prop="computer_skills">
              <el-input
                v-model="form.computer_skills"
                type="textarea"
                :rows="3"
                placeholder="Опишите требуемые компьютерные навыки"
              />
              <!-- Keywords Section for Computer Skills -->
              <KeywordsSection
                v-if="isEdit && hasVacancyId"
                :vacancy-id="vacancyId"
                section-type="skills"
                section-title="Компьютерные навыки"
                :section-text="form.computer_skills"
                @keywords-updated="handleKeywordsUpdated"
              />
            </el-form-item>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="Иностранные языки" prop="foreign_languages">
                  <el-input v-model="form.foreign_languages" placeholder="Укажите языки" />
                  <!-- Keywords Section for Languages -->
                  <KeywordsSection
                    v-if="isEdit && hasVacancyId"
                    :vacancy-id="vacancyId"
                    section-type="languages"
                    section-title="Иностранные языки"
                    :section-text="form.foreign_languages"
                    @keywords-updated="handleKeywordsUpdated"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="Уровень языка" prop="language_level">
                  <el-select v-model="form.language_level" placeholder="Выберите уровень" style="width: 100%">
                    <el-option label="Базовый" value="basic" />
                    <el-option label="Средний" value="intermediate" />
                    <el-option label="Продвинутый" value="advanced" />
                    <el-option label="Свободный" value="fluent" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
          </el-card>

          <!-- Дополнительная информация -->
          <el-card class="form-section">
            <template #header>
              <div class="section-header">
                <el-icon><InfoFilled /></el-icon>
                <span>Дополнительная информация</span>
              </div>
            </template>
            
            <el-form-item label="Описание вакансии" prop="description">
              <el-input
                v-model="form.description"
                type="textarea"
                :rows="4"
                placeholder="Подробное описание вакансии"
                maxlength="1000"
                show-word-limit
              />
              <!-- Keywords Section for Description -->
              <KeywordsSection
                v-if="isEdit && hasVacancyId"
                :vacancy-id="vacancyId"
                section-type="description"
                section-title="Описание вакансии"
                :section-text="form.description"
                @keywords-updated="handleKeywordsUpdated"
              />
            </el-form-item>
            
            <el-form-item label="Дополнительная информация" prop="additional_info">
              <el-input
                v-model="form.additional_info"
                type="textarea"
                :rows="4"
                placeholder="Любая дополнительная информация"
              />
              <!-- Keywords Section for Additional Info -->
              <KeywordsSection
                v-if="isEdit && hasVacancyId"
                :vacancy-id="vacancyId"
                section-type="additional"
                section-title="Дополнительная информация"
                :section-text="form.additional_info"
                @keywords-updated="handleKeywordsUpdated"
              />
            </el-form-item>
          </el-card>
        </el-form>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  ArrowLeft, Check, Document, Briefcase, Money, User, InfoFilled, Star
} from '@element-plus/icons-vue'
import KeywordsSection from '@/components/KeywordsSection.vue'

export default {
  name: 'VacancyForm',
  components: {
    ArrowLeft, Check, Document, Briefcase, Money, User, InfoFilled, Star,
    KeywordsSection
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const formRef = ref()
    const saving = ref(false)
    const generatingScenario = ref(false)
    const isEdit = ref(false)
    
    // Computed properties для безопасного доступа к route.params
    const vacancyId = computed(() => route?.params?.id || null)
    const hasVacancyId = computed(() => !!vacancyId.value)
    
    // Проверяем, что route доступен
    if (!route) {
      console.error('Route is not available')
      return {}
    }
    
    const form = reactive({
      title: '',
      status: 'active',
      region: '',
      city: '',
      address: '',
      employment_type: '',
      contract_type: '',
      work_schedule: '',
      business_trips: false,
      salary_min: null,
      salary_max: null,
      total_income: null,
      annual_bonus_percent: null,
      bonus_description: '',
      responsibilities: '',
      requirements: '',
      education_level: '',
      experience_required: '',
      special_programs: '',
      computer_skills: '',
      foreign_languages: '',
      language_level: '',
      additional_info: '',
      description: ''
    })

    const rules = {
      title: [
        { required: true, message: 'Введите название вакансии', trigger: 'blur' },
        { min: 3, max: 255, message: 'Название должно быть от 3 до 255 символов', trigger: 'blur' }
      ],
      status: [
        { required: true, message: 'Выберите статус', trigger: 'change' }
      ]
    }

    const loadVacancy = async (id) => {
      try {
        const response = await fetch(`/api/v1/vacancies/${id}`)
        if (!response.ok) throw new Error('Вакансия не найдена')
        
        const data = await response.json()
        Object.assign(form, data)
      } catch (error) {
        ElMessage.error('Ошибка загрузки вакансии: ' + error.message)
        router.push('/vacancies')
      }
    }

    const saveVacancy = async () => {
      try {
        await formRef.value.validate()
        saving.value = true
        
        const url = isEdit.value && vacancyId.value
          ? `/api/v1/vacancies/${vacancyId.value}`
          : '/api/v1/vacancies/'
        
        const method = isEdit.value ? 'PUT' : 'POST'
        
        const response = await fetch(url, {
          method,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(form)
        })
        
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.detail || 'Ошибка сохранения')
        }
        
        const data = await response.json()
        
        ElMessage.success(
          isEdit.value ? 'Вакансия успешно обновлена' : 'Вакансия успешно создана'
        )
        
        router.push(`/vacancies/${data.id}`)
      } catch (error) {
        if (error.message !== 'validation failed') {
          ElMessage.error('Ошибка сохранения вакансии: ' + error.message)
        }
      } finally {
        saving.value = false
      }
    }

    const goBack = () => {
      router.push('/vacancies')
    }

    const handleKeywordsUpdated = (data) => {
      console.log('Keywords updated:', data)
      // Можно добавить дополнительную логику обработки обновления ключевых слов
    }

    const generateScenario = async () => {
      if (!vacancyId.value) {
        ElMessage.warning('ID вакансии не найден')
        return
      }

      generatingScenario.value = true
      try {
        const response = await fetch('/api/v1/scenarios/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            vacancy_id: vacancyId.value,
            scenario_name: `Сценарий для ${form.title}`,
            description: `Автоматически сгенерированный сценарий для вакансии ${form.title}`
          })
        })

        const result = await response.json()

        if (result.success) {
          ElMessage.success('Сценарий успешно создан!')
          // Перенаправляем на страницу сценариев
          router.push('/scenarios')
        } else {
          ElMessage.error(result.error || 'Ошибка создания сценария')
        }
      } catch (error) {
        console.error('Ошибка генерации сценария:', error)
        ElMessage.error('Не удалось создать сценарий')
      } finally {
        generatingScenario.value = false
      }
    }

    onMounted(() => {
      if (vacancyId.value) {
        isEdit.value = true
        loadVacancy(vacancyId.value)
      }
    })

    return {
      formRef,
      form,
      rules,
      saving,
      generatingScenario,
      isEdit,
      vacancyId,
      hasVacancyId,
      saveVacancy,
      goBack,
      handleKeywordsUpdated,
      generateScenario
    }
  }
}
</script>

<style scoped>
.vacancy-form {
  min-height: 100vh;
  background-color: #f5f7fa;
}

:deep(.el-header) {
  background-color: #409eff;
  color: white;
  height: 80px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.header-left {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
}

.header-left h1 {
  margin: 0;
  color: #303133;
  font-size: 28px;
  font-weight: 600;
  line-height: 1.2;
}

.header-subtitle {
  margin: 8px 0 0 0;
  color: #909399;
  font-size: 14px;
}



.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.vacancy-form-content {
  max-width: 1200px;
  margin: 0 auto;
}

.form-section {
  margin-bottom: 24px;
  border: none;
  border-radius: 8px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #303133;
}

.section-header .el-icon {
  font-size: 18px;
  color: #409eff;
}

:deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
  background-color: #fafafa;
}

:deep(.el-card__body) {
  padding: 24px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
}

:deep(.el-input-number) {
  width: 100%;
}

:deep(.el-textarea__inner) {
  font-family: inherit;
}

:deep(.el-switch) {
  margin-top: 8px;
}

/* Keywords section styling */
:deep(.keywords-section) {
  margin-top: 12px;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  background-color: #fafafa;
}

:deep(.keywords-header) {
  padding: 12px 16px;
  border-bottom: 1px solid #e4e7ed;
  background-color: #f5f7fa;
}

:deep(.keywords-content) {
  padding: 16px;
}

:deep(.keywords-empty) {
  padding: 20px;
  text-align: center;
}

:deep(.keywords-loading) {
  padding: 16px;
}
</style>
