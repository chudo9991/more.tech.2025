<template>
  <div class="vacancy-form">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1>{{ isEdit ? 'Редактирование вакансии' : 'Создание вакансии' }}</h1>
          <p class="header-subtitle">{{ autoSaveText }}</p>
        </div>
        <div class="header-actions">
          <BaseButton variant="secondary" @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
            Назад
          </BaseButton>
          <BaseButton 
            v-if="isEdit && hasVacancyId"
            variant="secondary"
            :loading="generatingScenario"
            @click="generateScenario"
          >
            <el-icon><Star /></el-icon>
            Сгенерировать сценарий
          </BaseButton>
          <BaseButton 
            variant="primary"
            :loading="saving"
            @click="saveVacancy"
          >
            <el-icon><Check /></el-icon>
            {{ isEdit ? 'Сохранить' : 'Создать' }}
          </BaseButton>
        </div>
      </div>
    </div>

    <!-- Progress Indicator -->
    <div class="progress-container">
      <div class="progress-bar">
        <div 
          class="progress-fill" 
          :style="{ width: `${formProgress}%` }"
        ></div>
      </div>
      <div class="progress-text">
        Заполнено {{ formProgress }}% формы
      </div>
    </div>

    <!-- Main Content -->
    <div class="form-content">
      <!-- Step Navigation -->
      <div class="steps-navigation">
        <div class="steps-container">
          <div
            v-for="(step, index) in steps"
            :key="step.id"
            class="step-item"
            :class="{ 
              'active': currentStep === index, 
              'completed': isStepCompleted(index),
              'error': hasStepErrors(index)
            }"
            @click="goToStep(index)"
          >
            <div class="step-indicator">
              <el-icon v-if="isStepCompleted(index)"><Check /></el-icon>
              <el-icon v-else-if="hasStepErrors(index)"><Warning /></el-icon>
              <span v-else>{{ index + 1 }}</span>
            </div>
            <div class="step-info">
              <div class="step-title">{{ step.title }}</div>
              <div class="step-description">{{ step.description }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Form Steps -->
      <div class="form-steps">
        <form @submit.prevent="saveVacancy" class="vacancy-form-content">
          <!-- Step 1: Basic Information -->
          <div v-show="currentStep === 0" class="form-step">
            <el-card class="step-card">
              <template #header>
                <div class="step-header">
                  <div class="step-header-info">
                    <h2 class="step-title">Основная информация</h2>
                    <p class="step-subtitle">Базовые данные о вакансии</p>
                  </div>
                  <div class="step-progress">
                    <span class="progress-fraction">{{ getStepProgress(0) }}%</span>
                  </div>
                </div>
              </template>

              <div class="form-grid">
                <div class="form-group span-2">
                  <label class="form-label required">Название вакансии</label>
                  <el-input
                    v-model="form.title"
                    placeholder="Введите название вакансии"
                    maxlength="255"
                    show-word-limit
                    :class="{ 'error': getFieldError('title') }"
                    @blur="validateField('title')"
                  />
                  <div v-if="getFieldError('title')" class="field-error">{{ getFieldError('title') }}</div>
                  <div class="field-hint">Краткое и понятное название должности</div>
                </div>

                <div class="form-group">
                  <label class="form-label required">Статус</label>
                  <el-select
                    v-model="form.status"
                    placeholder="Выберите статус"
                    style="width: 100%"
                    :class="{ 'error': getFieldError('status') }"
                  >
                    <el-option label="Черновик" value="draft" />
                    <el-option label="Активная" value="active" />
                    <el-option label="Закрытая" value="closed" />
                  </el-select>
                  <div v-if="getFieldError('status')" class="field-error">{{ getFieldError('status') }}</div>
                </div>

                <div class="form-group">
                  <label class="form-label">Код вакансии</label>
                  <el-input
                    v-model="form.vacancy_code"
                    placeholder="Автоматически"
                    disabled
                  />
                  <div class="field-hint">Генерируется автоматически при сохранении</div>
                </div>

                <div class="form-group">
                  <label class="form-label">Регион</label>
                  <el-input
                    v-model="form.region"
                    placeholder="Укажите регион"
                  />
                </div>

                <div class="form-group">
                  <label class="form-label">Город</label>
                  <el-input
                    v-model="form.city"
                    placeholder="Укажите город"
                  />
                </div>

                <div class="form-group span-2">
                  <label class="form-label">Адрес</label>
                  <el-input
                    v-model="form.address"
                    placeholder="Полный адрес офиса"
                  />
                </div>
              </div>
            </el-card>
          </div>

          <!-- Step 2: Employment Conditions -->
          <div v-show="currentStep === 1" class="form-step">
            <el-card class="step-card">
              <template #header>
                <div class="step-header">
                  <div class="step-header-info">
                    <h2 class="step-title">Условия труда</h2>
                    <p class="step-subtitle">Тип занятости и рабочие условия</p>
                  </div>
                  <div class="step-progress">
                    <span class="progress-fraction">{{ getStepProgress(1) }}%</span>
                  </div>
                </div>
              </template>

              <div class="form-grid">
                <div class="form-group">
                  <label class="form-label">Тип занятости</label>
                  <el-select
                    v-model="form.employment_type"
                    placeholder="Выберите тип"
                    style="width: 100%"
                  >
                    <el-option label="Полная занятость" value="full_time" />
                    <el-option label="Частичная занятость" value="part_time" />
                    <el-option label="Контракт" value="contract" />
                    <el-option label="Стажировка" value="internship" />
                  </el-select>
                </div>

                <div class="form-group">
                  <label class="form-label">Уровень опыта</label>
                  <el-select
                    v-model="form.experience_required"
                    placeholder="Выберите уровень"
                    style="width: 100%"
                  >
                    <el-option label="Без опыта" value="no_experience" />
                    <el-option label="От 1 года" value="1_year" />
                    <el-option label="От 3 лет" value="3_years" />
                    <el-option label="От 5 лет" value="5_years" />
                    <el-option label="Более 5 лет" value="more_5_years" />
                  </el-select>
                </div>

                <div class="form-group">
                  <label class="form-label">Тип договора</label>
                  <el-select
                    v-model="form.contract_type"
                    placeholder="Выберите тип"
                    style="width: 100%"
                  >
                    <el-option label="Трудовой договор" value="employment" />
                    <el-option label="ГПХ" value="contract" />
                    <el-option label="Стажировка" value="internship" />
                  </el-select>
                </div>

                <div class="form-group">
                  <label class="form-label">Командировки</label>
                  <el-switch
                    v-model="form.business_trips"
                    active-text="Возможны"
                    inactive-text="Нет"
                  />
                </div>

                <div class="form-group span-2">
                  <label class="form-label">График работы</label>
                  <el-input
                    v-model="form.work_schedule"
                    type="textarea"
                    :rows="3"
                    placeholder="Опишите график работы (например: пн-пт 9:00-18:00)"
                  />
                </div>
              </div>
            </el-card>
          </div>

          <!-- Step 3: Salary and Benefits -->
          <div v-show="currentStep === 2" class="form-step">
            <el-card class="step-card">
              <template #header>
                <div class="step-header">
                  <div class="step-header-info">
                    <h2 class="step-title">Зарплата и льготы</h2>
                    <p class="step-subtitle">Финансовые условия и компенсации</p>
                  </div>
                  <div class="step-progress">
                    <span class="progress-fraction">{{ getStepProgress(2) }}%</span>
                  </div>
                </div>
              </template>

              <div class="form-grid">
                <div class="form-group">
                  <label class="form-label">Зарплата от (₽/мес)</label>
                  <el-input-number
                    v-model="form.salary_min"
                    :min="0"
                    :precision="0"
                    style="width: 100%"
                    placeholder="0"
                  />
                </div>

                <div class="form-group">
                  <label class="form-label">Зарплата до (₽/мес)</label>
                  <el-input-number
                    v-model="form.salary_max"
                    :min="0"
                    :precision="0"
                    style="width: 100%"
                    placeholder="0"
                  />
                </div>

                <div class="form-group">
                  <label class="form-label">Общий доход (₽/мес)</label>
                  <el-input-number
                    v-model="form.total_income"
                    :min="0"
                    :precision="0"
                    style="width: 100%"
                    placeholder="0"
                  />
                </div>

                <div class="form-group">
                  <label class="form-label">Годовая премия (%)</label>
                  <el-input-number
                    v-model="form.annual_bonus_percent"
                    :min="0"
                    :max="100"
                    :precision="1"
                    style="width: 100%"
                    placeholder="0"
                  />
                </div>

                <div class="form-group span-2">
                  <label class="form-label">Описание премирования</label>
                  <el-input
                    v-model="form.bonus_description"
                    type="textarea"
                    :rows="3"
                    placeholder="Опишите систему премирования и дополнительные льготы"
                  />
                </div>
              </div>
            </el-card>
          </div>

          <!-- Step 4: Job Description -->
          <div v-show="currentStep === 3" class="form-step">
            <el-card class="step-card">
              <template #header>
                <div class="step-header">
                  <div class="step-header-info">
                    <h2 class="step-title">Описание работы</h2>
                    <p class="step-subtitle">Обязанности и требования к кандидату</p>
                  </div>
                  <div class="step-progress">
                    <span class="progress-fraction">{{ getStepProgress(3) }}%</span>
                  </div>
                </div>
              </template>

              <div class="form-grid single-column">
                <div class="form-group">
                  <label class="form-label">Описание вакансии</label>
                  <el-input
                    v-model="form.description"
                    type="textarea"
                    :rows="4"
                    placeholder="Подробное описание вакансии, компании и условий работы"
                    maxlength="1000"
                    show-word-limit
                  />
                  <div class="field-hint">Привлекательное описание поможет найти лучших кандидатов</div>
                </div>

                <div class="form-group">
                  <label class="form-label required">Обязанности</label>
                  <el-input
                    v-model="form.responsibilities"
                    type="textarea"
                    :rows="5"
                    placeholder="Опишите основные обязанности и задачи"
                    maxlength="2000"
                    show-word-limit
                    :class="{ 'error': getFieldError('responsibilities') }"
                    @blur="validateField('responsibilities')"
                  />
                  <div v-if="getFieldError('responsibilities')" class="field-error">{{ getFieldError('responsibilities') }}</div>
                  <KeywordsSection
                    v-if="isEdit && hasVacancyId"
                    :vacancy-id="vacancyId"
                    section-type="responsibilities"
                    section-title="Обязанности"
                    :section-text="form.responsibilities"
                    @keywords-updated="handleKeywordsUpdated"
                  />
                </div>

                <div class="form-group">
                  <label class="form-label required">Требования</label>
                  <el-input
                    v-model="form.requirements"
                    type="textarea"
                    :rows="5"
                    placeholder="Опишите требования к кандидату"
                    maxlength="2000"
                    show-word-limit
                    :class="{ 'error': getFieldError('requirements') }"
                    @blur="validateField('requirements')"
                  />
                  <div v-if="getFieldError('requirements')" class="field-error">{{ getFieldError('requirements') }}</div>
                  <KeywordsSection
                    v-if="isEdit && hasVacancyId"
                    :vacancy-id="vacancyId"
                    section-type="requirements"
                    section-title="Требования"
                    :section-text="form.requirements"
                    @keywords-updated="handleKeywordsUpdated"
                  />
                </div>
              </div>
            </el-card>
          </div>

          <!-- Step 5: Skills and Qualifications -->
          <div v-show="currentStep === 4" class="form-step">
            <el-card class="step-card">
              <template #header>
                <div class="step-header">
                  <div class="step-header-info">
                    <h2 class="step-title">Навыки и квалификация</h2>
                    <p class="step-subtitle">Профессиональные и технические требования</p>
                  </div>
                  <div class="step-progress">
                    <span class="progress-fraction">{{ getStepProgress(4) }}%</span>
                  </div>
                </div>
              </template>

              <div class="form-grid">
                <div class="form-group">
                  <label class="form-label">Уровень образования</label>
                  <el-select
                    v-model="form.education_level"
                    placeholder="Выберите уровень"
                    style="width: 100%"
                  >
                    <el-option label="Среднее" value="secondary" />
                    <el-option label="Среднее специальное" value="vocational" />
                    <el-option label="Высшее" value="higher" />
                    <el-option label="Магистратура" value="masters" />
                    <el-option label="Аспирантура" value="phd" />
                  </el-select>
                </div>

                <div class="form-group">
                  <label class="form-label">Иностранные языки</label>
                  <el-input
                    v-model="form.foreign_languages"
                    placeholder="Английский, Немецкий"
                  />
                </div>

                <div class="form-group">
                  <label class="form-label">Уровень языка</label>
                  <el-select
                    v-model="form.language_level"
                    placeholder="Выберите уровень"
                    style="width: 100%"
                  >
                    <el-option label="Базовый (A1-A2)" value="basic" />
                    <el-option label="Средний (B1-B2)" value="intermediate" />
                    <el-option label="Продвинутый (C1)" value="advanced" />
                    <el-option label="Свободный (C2)" value="fluent" />
                  </el-select>
                </div>

                <div class="form-group span-2">
                  <label class="form-label">Компьютерные навыки</label>
                  <el-input
                    v-model="form.computer_skills"
                    type="textarea"
                    :rows="3"
                    placeholder="Опишите требуемые компьютерные навыки и программы"
                  />
                  <KeywordsSection
                    v-if="isEdit && hasVacancyId"
                    :vacancy-id="vacancyId"
                    section-type="skills"
                    section-title="Компьютерные навыки"
                    :section-text="form.computer_skills"
                    @keywords-updated="handleKeywordsUpdated"
                  />
                </div>

                <div class="form-group span-2">
                  <label class="form-label">Специальные программы</label>
                  <el-input
                    v-model="form.special_programs"
                    type="textarea"
                    :rows="3"
                    placeholder="Укажите специализированные программы и инструменты"
                  />
                  <KeywordsSection
                    v-if="isEdit && hasVacancyId"
                    :vacancy-id="vacancyId"
                    section-type="programs"
                    section-title="Специальные программы"
                    :section-text="form.special_programs"
                    @keywords-updated="handleKeywordsUpdated"
                  />
                </div>

                <div class="form-group span-2">
                  <label class="form-label">Дополнительная информация</label>
                  <el-input
                    v-model="form.additional_info"
                    type="textarea"
                    :rows="4"
                    placeholder="Любая дополнительная информация о вакансии"
                  />
                  <KeywordsSection
                    v-if="isEdit && hasVacancyId"
                    :vacancy-id="vacancyId"
                    section-type="additional"
                    section-title="Дополнительная информация"
                    :section-text="form.additional_info"
                    @keywords-updated="handleKeywordsUpdated"
                  />
                </div>
              </div>
            </el-card>
          </div>

          <!-- Step Navigation -->
          <div class="step-navigation">
            <div class="nav-buttons">
              <BaseButton
                v-if="currentStep > 0"
                variant="secondary"
                @click="previousStep"
              >
                <el-icon><ArrowLeft /></el-icon>
                Назад
              </BaseButton>
              
              <div class="nav-spacer"></div>
              
              <BaseButton
                v-if="currentStep < steps.length - 1"
                variant="primary"
                @click="nextStep"
                :disabled="!canProceedToNextStep"
              >
                Далее
                <el-icon><ArrowRight /></el-icon>
              </BaseButton>
              
              <BaseButton
                v-else
                variant="primary"
                :loading="saving"
                @click="saveVacancy"
              >
                <el-icon><Check /></el-icon>
                {{ isEdit ? 'Сохранить изменения' : 'Создать вакансию' }}
              </BaseButton>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed, watch, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  ArrowLeft, ArrowRight, Check, Warning, Star
} from '@element-plus/icons-vue'
import { BaseButton } from '@/components/base'
import KeywordsSection from '@/components/KeywordsSection.vue'

export default {
  name: 'VacancyForm',
  components: {
    ArrowLeft, ArrowRight, Check, Warning, Star,
    BaseButton,
    KeywordsSection
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const saving = ref(false)
    const generatingScenario = ref(false)
    const autoSaving = ref(false)
    const lastSaved = ref(null)
    const currentStep = ref(0)
    const validationErrors = ref({})
    
    // Computed properties
    const vacancyId = computed(() => route?.params?.id || null)
    const hasVacancyId = computed(() => !!vacancyId.value)
    const isEdit = computed(() => !!vacancyId.value)
    
    // Form data
    const form = reactive({
      title: '',
      status: 'draft',
      vacancy_code: '',
      region: '',
      city: '',
      address: '',
      employment_type: '',
      experience_required: '',
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
      special_programs: '',
      computer_skills: '',
      foreign_languages: '',
      language_level: '',
      additional_info: '',
      description: ''
    })

    // Form steps configuration
    const steps = [
      {
        id: 'basic',
        title: 'Основная информация',
        description: 'Название, статус и местоположение',
        fields: ['title', 'status', 'vacancy_code', 'region', 'city', 'address'],
        required: ['title', 'status']
      },
      {
        id: 'employment',
        title: 'Условия труда',
        description: 'Тип занятости и график работы',
        fields: ['employment_type', 'experience_required', 'contract_type', 'work_schedule', 'business_trips'],
        required: []
      },
      {
        id: 'salary',
        title: 'Зарплата и льготы',
        description: 'Финансовые условия',
        fields: ['salary_min', 'salary_max', 'total_income', 'annual_bonus_percent', 'bonus_description'],
        required: []
      },
      {
        id: 'description',
        title: 'Описание работы',
        description: 'Обязанности и требования',
        fields: ['description', 'responsibilities', 'requirements'],
        required: ['responsibilities', 'requirements']
      },
      {
        id: 'skills',
        title: 'Навыки и квалификация',
        description: 'Образование и специальные навыки',
        fields: ['education_level', 'foreign_languages', 'language_level', 'computer_skills', 'special_programs', 'additional_info'],
        required: []
      }
    ]

    // Auto-save functionality
    let autoSaveTimeout = null
    const autoSaveDelay = 2000 // 2 seconds

    // Computed properties
    const formProgress = computed(() => {
      const totalFields = Object.keys(form).length
      const filledFields = Object.values(form).filter(value => 
        value !== '' && value !== null && value !== false
      ).length
      return Math.round((filledFields / totalFields) * 100)
    })

    const autoSaveText = computed(() => {
      if (autoSaving.value) return 'Сохранение...'
      if (lastSaved.value) {
        const now = new Date()
        const diff = Math.floor((now.getTime() - lastSaved.value.getTime()) / 1000)
        if (diff < 60) return 'Сохранено только что'
        if (diff < 3600) return `Сохранено ${Math.floor(diff / 60)} мин назад`
        return `Сохранено ${Math.floor(diff / 3600)} ч назад`
      }
      return 'Не сохранено'
    })

    const canProceedToNextStep = computed(() => {
      const step = steps[currentStep.value]
      return step.required.every(field => {
        const value = form[field]
        return value !== '' && value !== null
      })
    })

    // Validation methods
    const validateField = (fieldName) => {
      const value = form[fieldName]
      
      // Required field validation
      const currentStepData = steps[currentStep.value]
      if (currentStepData.required.includes(fieldName)) {
        if (!value || value === '') {
          validationErrors.value[fieldName] = 'Это поле обязательно для заполнения'
          return false
        }
      }
      
      // Specific field validations
      if (fieldName === 'title' && value) {
        if (typeof value === 'string' && (value.length < 3 || value.length > 255)) {
          validationErrors.value[fieldName] = 'Название должно быть от 3 до 255 символов'
          return false
        }
      }
      
      // Clear error if validation passes
      delete validationErrors.value[fieldName]
      return true
    }

    const getFieldError = (fieldName) => {
      return validationErrors.value[fieldName] || ''
    }

    const isStepCompleted = (stepIndex) => {
      const step = steps[stepIndex]
      const requiredFilled = step.required.every(field => {
        const value = form[field]
        return value !== '' && value !== null && value !== false
      })
      
      if (step.required.length === 0) {
        const filledFields = step.fields.filter(field => {
          const value = form[field]
          return value !== '' && value !== null && value !== false
        }).length
        return filledFields >= Math.ceil(step.fields.length / 2)
      }
      
      return requiredFilled
    }

    const hasStepErrors = (stepIndex) => {
      const step = steps[stepIndex]
      return step.fields.some(field => validationErrors.value[field])
    }

    const getStepProgress = (stepIndex) => {
      const step = steps[stepIndex]
      const totalFields = step.fields.length
      const filledFields = step.fields.filter(field => {
        const value = form[field]
        return value !== '' && value !== null && value !== false
      }).length
      return Math.round((filledFields / totalFields) * 100)
    }

    // Navigation methods
    const goToStep = (stepIndex) => {
      if (stepIndex >= 0 && stepIndex < steps.length) {
        currentStep.value = stepIndex
      }
    }

    const nextStep = () => {
      if (canProceedToNextStep.value && currentStep.value < steps.length - 1) {
        currentStep.value++
      }
    }

    const previousStep = () => {
      if (currentStep.value > 0) {
        currentStep.value--
      }
    }

    // Auto-save functionality
    const triggerAutoSave = () => {
      if (autoSaveTimeout) {
        clearTimeout(autoSaveTimeout)
      }
      
      autoSaveTimeout = setTimeout(async () => {
        if (isEdit.value && vacancyId.value) {
          await autoSave()
        }
      }, autoSaveDelay)
    }

    const autoSave = async () => {
      if (autoSaving.value || saving.value) return
      
      try {
        autoSaving.value = true
        
        const response = await fetch(`/api/v1/vacancies/${vacancyId.value}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(form)
        })
        
        if (response.ok) {
          lastSaved.value = new Date()
        }
      } catch (error) {
        console.error('Auto-save failed:', error)
      } finally {
        autoSaving.value = false
      }
    }

    // Watch for form changes to trigger auto-save
    watch(form, () => {
      if (isEdit.value) {
        triggerAutoSave()
      }
    }, { deep: true })

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
        // Validate all required fields
        let hasErrors = false
        steps.forEach(step => {
          step.required.forEach(field => {
            if (!validateField(field)) {
              hasErrors = true
            }
          })
        })
        
        if (hasErrors) {
          ElMessage.error('Пожалуйста, заполните все обязательные поля')
          return
        }
        
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
        ElMessage.error('Ошибка сохранения вакансии: ' + error.message)
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
        loadVacancy(vacancyId.value)
      }
    })

    onUnmounted(() => {
      if (autoSaveTimeout) {
        clearTimeout(autoSaveTimeout)
      }
    })

    return {
      // Data
      form,
      saving,
      generatingScenario,
      autoSaving,
      lastSaved,
      currentStep,
      validationErrors,
      steps,
      
      // Computed
      vacancyId,
      hasVacancyId,
      isEdit,
      formProgress,
      autoSaveText,
      canProceedToNextStep,
      
      // Methods
      validateField,
      getFieldError,
      isStepCompleted,
      hasStepErrors,
      getStepProgress,
      goToStep,
      nextStep,
      previousStep,
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
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #0f172a 50%, #1e293b 75%, #0f172a 100%);
  position: relative;
}

.vacancy-form::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 80%, rgba(0, 255, 255, 0.1) 0%, transparent 60%),
    radial-gradient(circle at 80% 20%, rgba(138, 43, 226, 0.1) 0%, transparent 60%);
  pointer-events: none;
  z-index: -1;
}

/* Header */
.page-header {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.15), rgba(138, 43, 226, 0.15));
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
  color: white;
  padding: 20px 0;
}

.el-textarea .el-input__count {
    background: transparent;
    bottom: 5px;
    color: var(--el-color-info);
    font-size: 12px;
    line-height: 14px;
    position: absolute;
    right: 10px;
}
.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left h1 {
  margin: 0;
  color: #e2e8f0;
  font-size: 28px;
  font-weight: 600;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}

.header-subtitle {
  margin: 8px 0 0 0;
  color: #94a3b8;
  font-size: 14px;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

/* Progress Bar */
.progress-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(30, 41, 59, 0.8);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #00ffff, #8a2be2);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  text-align: center;
  color: #94a3b8;
  font-size: 14px;
}

/* Form Content */
.form-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Steps Navigation */
.steps-navigation {
  margin-bottom: 30px;
}

.steps-container {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  overflow-x: auto;
  padding: 20px 0;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(100, 116, 139, 0.3);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 200px;
  backdrop-filter: blur(10px);
}

.step-item:hover {
  background: rgba(30, 41, 59, 0.8);
  border-color: rgba(0, 255, 255, 0.4);
}

.step-item.active {
  background: rgba(0, 255, 255, 0.1);
  border-color: rgba(0, 255, 255, 0.5);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
}

.step-item.completed {
  background: rgba(34, 197, 94, 0.1);
  border-color: rgba(34, 197, 94, 0.4);
}

.step-item.error {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.4);
}

.step-indicator {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(30, 41, 59, 0.8);
  border: 2px solid rgba(100, 116, 139, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #e2e8f0;
  flex-shrink: 0;
}

.step-item.active .step-indicator {
  background: rgba(0, 255, 255, 0.2);
  border-color: rgba(0, 255, 255, 0.6);
  color: #00ffff;
}

.step-item.completed .step-indicator {
  background: rgba(34, 197, 94, 0.2);
  border-color: rgba(34, 197, 94, 0.6);
  color: #22c55e;
}

.step-item.error .step-indicator {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.6);
  color: #ef4444;
}

.step-info {
  flex: 1;
}

.step-title {
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 4px;
}

.step-description {
  font-size: 12px;
  color: #94a3b8;
}

/* Form Steps */
.form-steps {
  margin-bottom: 30px;
}

.form-step {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.step-card {
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.step-header-info h2 {
  margin: 0;
  color: #e2e8f0;
  font-size: 24px;
  font-weight: 600;
}

.step-subtitle {
  margin: 4px 0 0 0;
  color: #94a3b8;
  font-size: 14px;
}

.progress-fraction {
  background: rgba(0, 255, 255, 0.2);
  color: #00ffff;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

/* Form Grid */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 20px;
}

.form-grid.single-column {
  grid-template-columns: 1fr;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group.span-2 {
  grid-column: span 2;
}

.form-label {
  font-weight: 500;
  color: #e2e8f0;
  font-size: 14px;
}

.form-label.required::after {
  content: ' *';
  color: #ef4444;
}

.field-hint {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 4px;
}

.field-error {
  font-size: 12px;
  color: #ef4444;
  margin-top: 4px;
}

/* Step Navigation */
.step-navigation {
  margin-top: 40px;
  padding: 20px 0;
  border-top: 1px solid rgba(0, 255, 255, 0.2);
}

.nav-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-spacer {
  flex: 1;
}

/* Responsive */
@media (max-width: 768px) {
  .steps-container {
    flex-direction: column;
  }
  
  .step-item {
    min-width: auto;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-group.span-2 {
    grid-column: span 1;
  }
  
  .header-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .header-actions {
    flex-wrap: wrap;
    justify-content: center;
  }
}

/* Element Plus Overrides */
:deep(.el-card__header) {
  background: rgba(0, 255, 255, 0.1);
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
  color: #00ffff;
}

:deep(.el-card__body) {
  background: transparent;
  color: #e2e8f0;
}

:deep(.el-switch.is-checked .el-switch__core) {
  background-color: #00ffff;
  border-color: #00ffff;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

:deep(.el-input-number) {
  width: 100%;
}

/* Keywords section styling */
:deep(.keywords-section) {
  margin-top: 12px;
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 8px;
  background: rgba(15, 23, 42, 0.6);
}

:deep(.keywords-header) {
  padding: 12px 16px;
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
  background: rgba(0, 255, 255, 0.1);
  color: #00ffff;
}

:deep(.keywords-content) {
  padding: 16px;
  color: #e2e8f0;
}

:deep(.keywords-empty) {
  padding: 20px;
  text-align: center;
  color: #94a3b8;
}

:deep(.keywords-loading) {
  padding: 16px;
  color: #94a3b8;
}
</style>
