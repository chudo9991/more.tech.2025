<template>
  <div class="vacancy-form">
    <!-- Header -->
    <PageHeader
      :title="isEdit ? 'Редактирование вакансии' : 'Создание вакансии'"
      :subtitle="autoSaveText"
    >
      <template #actions>
        <BaseButton
          variant="secondary"
          icon="mdi mdi-arrow-left"
          @click="goBack"
        >
          Назад
        </BaseButton>
        <BaseButton
          v-if="isEdit && hasVacancyId"
          variant="secondary"
          icon="mdi mdi-auto-fix"
          :loading="generatingScenario"
          @click="generateScenario"
        >
          Сгенерировать сценарий
        </BaseButton>
        <BaseButton
          variant="primary"
          icon="mdi mdi-content-save"
          :loading="saving"
          @click="saveVacancy"
        >
          {{ isEdit ? 'Сохранить' : 'Создать' }}
        </BaseButton>
      </template>
    </PageHeader>

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
              <i v-if="isStepCompleted(index)" class="mdi mdi mdi-check"></i>
              <i v-else-if="hasStepErrors(index)" class="mdi mdi mdi-alert"></i>
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
            <BaseCard padding="lg" variant="elevated">
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
                  <BaseInput
                    v-model="form.title"
                    placeholder="Введите название вакансии"
                    :error="getFieldError('title')"
                    @blur="validateField('title')"
                  />
                  <div class="field-hint">Краткое и понятное название должности</div>
                </div>

                <div class="form-group">
                  <label class="form-label required">Статус</label>
                  <BaseSelect
                    v-model="form.status"
                    placeholder="Выберите статус"
                    :options="statusOptions"
                    :error="getFieldError('status')"
                  />
                </div>

                <div class="form-group">
                  <label class="form-label">Код вакансии</label>
                  <BaseInput
                    v-model="form.vacancy_code"
                    placeholder="Автоматически"
                    disabled
                  />
                  <div class="field-hint">Генерируется автоматически при сохранении</div>
                </div>

                <div class="form-group">
                  <label class="form-label">Регион</label>
                  <BaseInput
                    v-model="form.region"
                    placeholder="Укажите регион"
                    icon="mdi mdi-map-marker"
                  />
                </div>

                <div class="form-group">
                  <label class="form-label">Город</label>
                  <BaseInput
                    v-model="form.city"
                    placeholder="Укажите город"
                    icon="mdi mdi-city"
                  />
                </div>

                <div class="form-group span-2">
                  <label class="form-label">Адрес</label>
                  <BaseInput
                    v-model="form.address"
                    placeholder="Полный адрес офиса"
                    icon="mdi mdi-map-marker-outline"
                  />
                </div>
              </div>
            </BaseCard>
          </div>

          <!-- Step 2: Employment Conditions -->
          <div v-show="currentStep === 1" class="form-step">
            <BaseCard padding="lg" variant="elevated">
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
                  <BaseSelect
                    v-model="form.employment_type"
                    placeholder="Выберите тип"
                    :options="employmentTypeOptions"
                  />
                </div>

                <div class="form-group">
                  <label class="form-label">Уровень опыта</label>
                  <BaseSelect
                    v-model="form.experience_level"
                    placeholder="Выберите уровень"
                    :options="experienceLevelOptions"
                  />
                </div>

                <div class="form-group">
                  <label class="form-label">Тип договора</label>
                  <BaseSelect
                    v-model="form.contract_type"
                    placeholder="Выберите тип"
                    :options="contractTypeOptions"
                  />
                </div>

                <div class="form-group">
                  <label class="form-label">Командировки</label>
                  <BaseCheckbox
                    v-model="form.business_trips"
                    label="Возможны командировки"
                  />
                </div>

                <div class="form-group span-2">
                  <label class="form-label">График работы</label>
                  <BaseInput
                    v-model="form.work_schedule"
                    type="textarea"
                    :rows="3"
                    placeholder="Опишите график работы (например: пн-пт 9:00-18:00)"
                  />
                </div>
              </div>
            </BaseCard>
          </div>

          <!-- Step 3: Salary and Benefits -->
          <div v-show="currentStep === 2" class="form-step">
            <BaseCard padding="lg" variant="elevated">
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
                  <BaseInput
                    v-model="form.salary_min"
                    type="number"
                    placeholder="0"
                    icon="mdi mdi-currency-rub"
                  />
                </div>

                <div class="form-group">
                  <label class="form-label">Зарплата до (₽/мес)</label>
                  <BaseInput
                    v-model="form.salary_max"
                    type="number"
                    placeholder="0"
                    icon="mdi mdi-currency-rub"
                  />
                </div>

                <div class="form-group">
                  <label class="form-label">Общий доход (₽/мес)</label>
                  <BaseInput
                    v-model="form.total_income"
                    type="number"
                    placeholder="0"
                    icon="mdi mdi-cash-multiple"
                  />
                </div>

                <div class="form-group">
                  <label class="form-label">Годовая премия (%)</label>
                  <BaseInput
                    v-model="form.annual_bonus_percent"
                    type="number"
                    placeholder="0"
                    icon="mdi mdi-percent"
                  />
                </div>

                <div class="form-group span-2">
                  <label class="form-label">Описание премирования</label>
                  <BaseInput
                    v-model="form.bonus_description"
                    type="textarea"
                    :rows="3"
                    placeholder="Опишите систему премирования и дополнительные льготы"
                  />
                </div>
              </div>
            </BaseCard>
          </div>

          <!-- Step 4: Job Description -->
          <div v-show="currentStep === 3" class="form-step">
            <BaseCard padding="lg" variant="elevated">
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
                  <RichTextEditor
                    v-model="form.description"
                    placeholder="Подробное описание вакансии, компании и условий работы"
                    :min-height="150"
                  />
                  <div class="field-hint">Привлекательное описание поможет найти лучших кандидатов</div>
                </div>

                <div class="form-group">
                  <label class="form-label required">Обязанности</label>
                  <RichTextEditor
                    v-model="form.responsibilities"
                    placeholder="Опишите основные обязанности и задачи"
                    :min-height="120"
                    :error="getFieldError('responsibilities')"
                  />
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
                  <RichTextEditor
                    v-model="form.requirements"
                    placeholder="Опишите требования к кандидату"
                    :min-height="120"
                    :error="getFieldError('requirements')"
                  />
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
            </BaseCard>
          </div>

          <!-- Step 5: Skills and Qualifications -->
          <div v-show="currentStep === 4" class="form-step">
            <BaseCard padding="lg" variant="elevated">
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
                  <BaseSelect
                    v-model="form.education_level"
                    placeholder="Выберите уровень"
                    :options="educationLevelOptions"
                  />
                </div>

                <div class="form-group">
                  <label class="form-label">Иностранные языки</label>
                  <BaseInput
                    v-model="form.foreign_languages"
                    placeholder="Английский, Немецкий"
                    icon="mdi mdi-translate"
                  />
                </div>

                <div class="form-group">
                  <label class="form-label">Уровень языка</label>
                  <BaseSelect
                    v-model="form.language_level"
                    placeholder="Выберите уровень"
                    :options="languageLevelOptions"
                  />
                </div>

                <div class="form-group span-2">
                  <label class="form-label">Компьютерные навыки</label>
                  <BaseInput
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
                  <BaseInput
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
                  <BaseInput
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
            </BaseCard>
          </div>

          <!-- Step Navigation -->
          <div class="step-navigation">
            <div class="nav-buttons">
              <BaseButton
                v-if="currentStep > 0"
                variant="secondary"
                icon="mdi mdi-chevron-left"
                @click="previousStep"
              >
                Назад
              </BaseButton>
              
              <div class="nav-spacer"></div>
              
              <BaseButton
                v-if="currentStep < steps.length - 1"
                variant="primary"
                icon="mdi mdi-chevron-right"
                icon-position="right"
                @click="nextStep"
                :disabled="!canProceedToNextStep"
              >
                Далее
              </BaseButton>
              
              <BaseButton
                v-else
                variant="primary"
                icon="mdi mdi-content-save"
                :loading="saving"
                @click="saveVacancy"
              >
                {{ isEdit ? 'Сохранить изменения' : 'Создать вакансию' }}
              </BaseButton>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch, onUnmounted } from 'vue'
// @ts-ignore
import { useRoute, useRouter } from 'vue-router'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import BaseSelect from '@/components/base/BaseSelect.vue'
import BaseCheckbox from '@/components/base/BaseCheckbox.vue'
import RichTextEditor from '@/components/RichTextEditor.vue'
import KeywordsSection from '@/components/KeywordsSection.vue'
import PageHeader from '@/components/layout/PageHeader.vue'

// Types
interface VacancyForm {
  title: string
  status: string
  vacancy_code?: string
  region: string
  city: string
  address: string
  employment_type: string
  experience_level: string
  contract_type: string
  work_schedule: string
  business_trips: boolean
  salary_min: number | null
  salary_max: number | null
  total_income: number | null
  annual_bonus_percent: number | null
  bonus_description: string
  responsibilities: string
  requirements: string
  education_level: string
  special_programs: string
  computer_skills: string
  foreign_languages: string
  language_level: string
  additional_info: string
  description: string
}

interface FormStep {
  id: string
  title: string
  description: string
  fields: string[]
  required: string[]
}

interface ValidationErrors {
  [key: string]: string
}
const route = useRoute()
const router = useRouter()

// Reactive data
const saving = ref(false)
const generatingScenario = ref(false)
const autoSaving = ref(false)
const lastSaved = ref<Date | null>(null)
const currentStep = ref(0)
const validationErrors = ref<ValidationErrors>({})

// Computed properties
const vacancyId = computed(() => route?.params?.id as string || null)
const hasVacancyId = computed(() => !!vacancyId.value)
const isEdit = computed(() => !!vacancyId.value)

// Form data
const form = reactive<VacancyForm>({
  title: '',
  status: '',
  vacancy_code: '',
  region: '',
  city: '',
  address: '',
  employment_type: '',
  experience_level: '',
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
const steps: FormStep[] = [
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
    fields: ['employment_type', 'experience_level', 'contract_type', 'work_schedule', 'business_trips'],
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

// Options for selects
const statusOptions = [
  { value: 'draft', label: 'Черновик' },
  { value: 'active', label: 'Активная' },
  { value: 'paused', label: 'Приостановлена' },
  { value: 'closed', label: 'Закрыта' }
]

const employmentTypeOptions = [
  { value: 'full_time', label: 'Полная занятость' },
  { value: 'part_time', label: 'Частичная занятость' },
  { value: 'contract', label: 'Контракт' },
  { value: 'internship', label: 'Стажировка' }
]

const experienceLevelOptions = [
  { value: 'entry', label: 'Без опыта' },
  { value: 'junior', label: 'Junior (1-3 года)' },
  { value: 'middle', label: 'Middle (3-5 лет)' },
  { value: 'senior', label: 'Senior (5+ лет)' },
  { value: 'lead', label: 'Lead/Principal' }
]

const contractTypeOptions = [
  { value: 'employment', label: 'Трудовой договор' },
  { value: 'contract', label: 'ГПХ' },
  { value: 'internship', label: 'Стажировка' }
]

const educationLevelOptions = [
  { value: 'secondary', label: 'Среднее' },
  { value: 'vocational', label: 'Среднее специальное' },
  { value: 'higher', label: 'Высшее' },
  { value: 'masters', label: 'Магистратура' },
  { value: 'phd', label: 'Аспирантура' }
]

const languageLevelOptions = [
  { value: 'basic', label: 'Базовый (A1-A2)' },
  { value: 'intermediate', label: 'Средний (B1-B2)' },
  { value: 'advanced', label: 'Продвинутый (C1)' },
  { value: 'fluent', label: 'Свободный (C2)' }
]

// Auto-save functionality
let autoSaveTimeout: NodeJS.Timeout | null = null
const autoSaveDelay = 2000 // 2 seconds

// Computed properties
const formProgress = computed(() => {
  const totalFields = Object.keys(form).length
  const filledFields = Object.values(form).filter(value => 
    value !== '' && value !== null && value !== false
  ).length
  return Math.round((filledFields / totalFields) * 100)
})

const autoSaveIcon = computed(() => {
  if (autoSaving.value) return 'mdi mdi mdi-loading animate-spin'
  if (lastSaved.value) return 'mdi mdi mdi-check-circle text-success-500'
  return 'mdi mdi mdi-content-save-outline'
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
    const value = form[field as keyof VacancyForm]
    return value !== '' && value !== null
  })
})

// Validation methods
const validateField = (fieldName: string) => {
  const value = form[fieldName as keyof VacancyForm]
  
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

const getFieldError = (fieldName: string) => {
  return validationErrors.value[fieldName] || ''
}

const isStepCompleted = (stepIndex: number) => {
  const step = steps[stepIndex]
  // Шаг считается завершенным только если заполнены ВСЕ обязательные поля
  // И хотя бы одно необязательное поле (если есть необязательные поля)
  const requiredFilled = step.required.every(field => {
    const value = form[field as keyof VacancyForm]
    return value !== '' && value !== null && value !== false
  })
  
  // Если нет обязательных полей, проверяем заполненность хотя бы половины полей
  if (step.required.length === 0) {
    const filledFields = step.fields.filter(field => {
      const value = form[field as keyof VacancyForm]
      return value !== '' && value !== null && value !== false
    }).length
    return filledFields >= Math.ceil(step.fields.length / 2)
  }
  
  return requiredFilled
}

const hasStepErrors = (stepIndex: number) => {
  const step = steps[stepIndex]
  return step.fields.some(field => validationErrors.value[field])
}

const getStepProgress = (stepIndex: number) => {
  const step = steps[stepIndex]
  const totalFields = step.fields.length
  const filledFields = step.fields.filter(field => {
    const value = form[field as keyof VacancyForm]
    return value !== '' && value !== null && value !== false
  }).length
  return Math.round((filledFields / totalFields) * 100)
}

// Navigation methods
const goToStep = (stepIndex: number) => {
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

// CRUD operations
const loadVacancy = async (id: string) => {
  try {
    const response = await fetch(`/api/v1/vacancies/${id}`)
    if (!response.ok) throw new Error('Вакансия не найдена')
    
    const data = await response.json()
    Object.assign(form, data)
  } catch (error) {
    console.error('Error loading vacancy:', error)
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
    
    // Success message and redirect
    router.push(`/vacancies/${data.id}`)
  } catch (error) {
    console.error('Error saving vacancy:', error)
  } finally {
    saving.value = false
  }
}

const goBack = () => {
  router.push('/vacancies')
}

const handleKeywordsUpdated = (data: any) => {
  console.log('Keywords updated:', data)
}

const generateScenario = async () => {
  if (!vacancyId.value) {
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
      router.push('/scenarios')
    }
  } catch (error) {
    console.error('Error generating scenario:', error)
  } finally {
    generatingScenario.value = false
  }
}

// Watchers for auto-save
watch(form, () => {
  triggerAutoSave()
}, { deep: true })

// Lifecycle
onMounted(async () => {
  if (vacancyId.value) {
    await loadVacancy(vacancyId.value)
  }
})

onUnmounted(() => {
  if (autoSaveTimeout) {
    clearTimeout(autoSaveTimeout)
  }
})
</script>

<style scoped>
/* Vacancy Form Styles */
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
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 80%, rgba(0, 255, 255, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 80% 20%, rgba(0, 255, 255, 0.1) 0%, transparent 50%);
  pointer-events: none;
  z-index: 1;
}

.vacancy-form > * {
  position: relative;
  z-index: 2;
}

/* Header */
.form-header {
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
  padding: 2rem;
  position: sticky;
  top: 0;
  z-index: 20;
}

.header-content {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-info {
  flex: 1;
}

.form-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #00ffff;
  margin: 0 0 0.5rem 0;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
}

.form-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.auto-save-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #94a3b8;
  transition: all 0.3s ease;
}

.auto-save-status.saving {
  color: #00ffff;
}

.auto-save-status.saved {
  color: #10b981;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

/* Progress Indicator */
.progress-container {
  margin-top: 0.5rem;
  padding: 1.5rem 2rem;
  position: sticky;
  top: 80px;
  z-index: 19;
}

.progress-bar {
  width: 100%;
  height: 4px;
  background: rgba(15, 23, 42, 0.8);
  border: none;
  border-radius: 0;
  overflow: hidden;
  margin-bottom: 0.75rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #00ffff, #0ea5e9);
  transition: width 0.3s ease;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
}

.progress-text {
  font-size: 0.875rem;
  color: #00ffff;
  text-align: center;
  font-weight: 500;
}

/* Main Content */
.form-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 2.5rem;
  align-items: start;
}

/* Steps Navigation */
.steps-navigation {
  position: sticky;
  top: 180px;
}

.steps-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 12px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
}

.step-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
  background: rgba(30, 41, 59, 0.5);
}

.step-item:hover {
  background: rgba(30, 41, 59, 0.8);
  border-color: rgba(0, 255, 255, 0.3);
  transform: translateX(4px);
}

.step-item.active {
  background: rgba(0, 255, 255, 0.1);
  border-color: #00ffff;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
}

.step-item.completed {
  background: rgba(16, 185, 129, 0.1);
  border-color: #10b981;
}

.step-item.error {
  background: rgba(239, 68, 68, 0.1);
  border-color: #ef4444;
}

.step-indicator {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  flex-shrink: 0;
  background: rgba(30, 41, 59, 0.8);
  color: #94a3b8;
  border: 1px solid rgba(148, 163, 184, 0.3);
}

.step-item.active .step-indicator {
  background: #00ffff;
  color: #0f172a;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.4);
}

.step-item.completed .step-indicator {
  background: #10b981;
  color: white;
  border-color: #10b981;
}

.step-item.error .step-indicator {
  background: #ef4444;
  color: white;
  border-color: #ef4444;
}

.step-info {
  flex: 1;
  min-width: 0;
}

.step-title {
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 0.25rem;
}

.step-item.active .step-title {
  color: #00ffff;
}

.step-description {
  font-size: 0.875rem;
  color: #94a3b8;
}

/* Form Steps */
.form-steps {
  min-width: 0;
}

.vacancy-form-content {
  width: 100%;
}

.form-step {
  min-height: 500px;
}

/* Step Header */
.step-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.step-header-info {
  flex: 1;
}

.step-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #00ffff;
  margin: 0 0 0.5rem 0;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
}

.step-subtitle {
  color: #94a3b8;
  margin: 0;
  font-size: 0.95rem;
}

.step-progress {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(0, 255, 255, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  border: 1px solid rgba(0, 255, 255, 0.3);
}

.progress-fraction {
  font-size: 0.875rem;
  font-weight: 600;
  color: #00ffff;
}

/* Form Grid */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  align-items: start;
}

.form-grid.single-column {
  grid-template-columns: 1fr;
}

/* Form Input Overrides for Dark Theme */
:deep(.base-input) {
  background: rgba(15, 23, 42, 0.8) !important;
  border: 1px solid rgba(0, 255, 255, 0.3) !important;
  color: #e2e8f0 !important;
}

:deep(.base-input:focus) {
  border-color: rgba(0, 255, 255, 0.6) !important;
  box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.1) !important;
}

:deep(.base-input::placeholder) {
  color: #94a3b8 !important;
}

:deep(.base-select) {
  background: rgba(15, 23, 42, 0.8) !important;
  border: 1px solid rgba(0, 255, 255, 0.3) !important;
  color: #e2e8f0 !important;
}

:deep(.base-select:focus) {
  border-color: rgba(0, 255, 255, 0.6) !important;
  box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.1) !important;
}

:deep(.base-textarea) {
  background: rgba(15, 23, 42, 0.8) !important;
  border: 1px solid rgba(0, 255, 255, 0.3) !important;
  color: #e2e8f0 !important;
  resize: vertical;
}

:deep(.base-textarea:focus) {
  border-color: rgba(0, 255, 255, 0.6) !important;
  box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.1) !important;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-group.span-2 {
  grid-column: span 2;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #e2e8f0;
}

.form-label.required::after {
  content: ' *';
  color: #00ffff;
  margin-left: 2px;
}

.field-hint {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-top: 0.25rem;
  font-style: italic;
}

/* Step Navigation */
.step-navigation {
  margin-top: 2.5rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(0, 255, 255, 0.2);
}

.nav-buttons {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-spacer {
  flex: 1;
}

/* Rich Text Editor */
:deep(.rich-text-editor) {
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  overflow: hidden;
}

:deep(.rich-text-editor.error) {
  border-color: #ef4444;
}

:deep(.rich-text-editor .editor-toolbar) {
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
  padding: 0.5rem;
}

:deep(.rich-text-editor .editor-content) {
  min-height: 120px;
  padding: 1rem;
}

/* Keywords Section */
:deep(.keywords-section) {
  margin-top: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  background: #f9fafb;
}

:deep(.keywords-header) {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e5e7eb;
  background: #f3f4f6;
  font-weight: 500;
  color: #374151;
}

:deep(.keywords-content) {
  padding: 1rem;
}

:deep(.keywords-empty) {
  padding: 1.5rem;
  text-align: center;
  color: #6b7280;
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.form-step {
  animation: fadeInUp 0.4s ease-out;
}

.step-item {
  animation: slideInRight 0.3s ease-out;
}

.step-item.active .step-indicator {
  animation: pulse 2s infinite;
}

/* Loading animations */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .form-content {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    padding: 1.5rem;
  }
  
  .steps-navigation {
    position: static;
    margin-bottom: 1.5rem;
  }
  
  .steps-container {
    flex-direction: row;
    overflow-x: auto;
    padding: 1rem 0.5rem;
    gap: 1rem;
    scrollbar-width: thin;
    scrollbar-color: rgba(0, 255, 255, 0.3) transparent;
  }
  
  .steps-container::-webkit-scrollbar {
    height: 6px;
  }
  
  .steps-container::-webkit-scrollbar-track {
    background: rgba(15, 23, 42, 0.5);
    border-radius: 3px;
  }
  
  .steps-container::-webkit-scrollbar-thumb {
    background: rgba(0, 255, 255, 0.3);
    border-radius: 3px;
  }
  
  .step-item {
    flex-shrink: 0;
    min-width: 220px;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-group.span-2 {
    grid-column: span 1;
  }
}

@media (max-width: 768px) {
  .form-header {
    padding: 1.5rem 1rem;
  }
  
  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .header-actions {
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .progress-container {
    padding: 1rem;
  }
  
  .form-content {
    padding: 1rem;
  }
  
  .steps-container {
    padding: 0.75rem;
  }
  
  .step-item {
    padding: 1rem;
    min-width: 200px;
  }
  
  .step-title {
    font-size: 1.25rem;
  }
  
  .step-indicator {
    width: 2rem;
    height: 2rem;
    font-size: 0.75rem;
  }
  
  .nav-buttons {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
  }
  
  .nav-spacer {
    display: none;
  }
}

@media (max-width: 640px) {
  .form-title {
    font-size: 1.5rem;
  }
  
  .header-actions {
    flex-direction: column;
  }
  
  .steps-container {
    flex-direction: column;
  }
  
  .step-item {
    min-width: auto;
  }
  
  .step-info {
    display: none;
  }
  
  .step-indicator {
    width: 2rem;
    height: 2rem;
  }
}
</style>

<style scoped>
/* Vacancy Form Styles */
.vacancy-form {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #0f172a 50%, #1e293b 75%, #0f172a 100%);
  position: relative;
  overflow-x: hidden;
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
    radial-gradient(circle at 80% 20%, rgba(138, 43, 226, 0.1) 0%, transparent 60%),
    radial-gradient(circle at 40% 40%, rgba(75, 0, 130, 0.08) 0%, transparent 50%);
  pointer-events: none;
  z-index: -1;
}

.vacancy-form::after {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(45deg, rgba(0, 255, 255, 0.02) 25%, transparent 25%),
    linear-gradient(-45deg, rgba(138, 43, 226, 0.02) 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, rgba(0, 255, 255, 0.02) 75%),
    linear-gradient(-45deg, transparent 75%, rgba(138, 43, 226, 0.02) 75%);
  background-size: 60px 60px;
  background-position: 0 0, 0 30px, 30px -30px, -30px 0px;
  pointer-events: none;
  z-index: -1;
  opacity: 0.3;
}

/* Header */
.form-header {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.6));
  backdrop-filter: blur(30px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 20px;
  padding: 2.5rem;
  position: relative;
  z-index: 100;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.4),
    0 0 40px rgba(0, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  margin: 2rem 2rem 0 2rem;
  overflow: hidden;
}

.form-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.1), transparent);
  animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
  0% { left: -100%; }
  100% { left: 100%; }
}

.header-content {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #00ffff;
  margin: 0 0 0.25rem 0;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.form-meta {
  color: #e2e8f0;
  margin: 0;
  font-size: 1rem;
}

.auto-save-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #94a3b8;
}

.auto-save-status.saving {
  color: #fbbf24;
}

.auto-save-status.saved {
  color: #10b981;
}

/* Progress */
.progress-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 1rem 2rem;
}

.progress-bar {
  width: 100%;
  height: 4px;
  background: rgba(15, 23, 42, 0.8);
  border: none;
  border-radius: 0;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #00ffff, #8a2be2);
  border: none;
  border-radius: 0;
  transition: width 0.3s ease;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.progress-text {
  font-size: 0.875rem;
  color: #e2e8f0;
  text-align: center;
}

/* Form Content */
.form-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem 2rem 2rem;
}

.steps-navigation {
  margin-bottom: 2rem;
}

.steps-container {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  padding: 1rem 0.5rem;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 200px;
  flex-shrink: 0;
}

.step-item:hover {
  border-color: rgba(0, 255, 255, 0.4);
  box-shadow: 0 8px 32px rgba(0, 255, 255, 0.2);
}

.step-item.active {
  background: rgba(0, 255, 255, 0.1);
  border-color: rgba(0, 255, 255, 0.5);
  box-shadow: 0 8px 32px rgba(0, 255, 255, 0.3);
}

.step-item.completed {
  background: rgba(16, 185, 129, 0.1);
  border-color: rgba(16, 185, 129, 0.5);
}

.step-item.error {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.5);
}

.step-indicator {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(15, 23, 42, 0.8);
  border: 2px solid rgba(0, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #00ffff;
  flex-shrink: 0;
}

.step-item.active .step-indicator {
  background: rgba(0, 255, 255, 0.2);
  border-color: #00ffff;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
}

.step-item.completed .step-indicator {
  background: rgba(16, 185, 129, 0.2);
  border-color: #10b981;
  color: #10b981;
}

.step-item.error .step-indicator {
  background: rgba(239, 68, 68, 0.2);
  border-color: #ef4444;
  color: #ef4444;
}

.step-info {
  flex: 1;
}

.step-title {
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 0.25rem;
}

.step-description {
  font-size: 0.875rem;
  color: #94a3b8;
}

/* Form Steps */
.form-steps {
  margin-bottom: 2rem;
}

.form-step {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.step-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #00ffff;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
}

.step-subtitle {
  color: #94a3b8;
  margin-top: 0.25rem;
}

.step-progress {
  font-size: 0.875rem;
  color: #8a2be2;
  font-weight: 600;
}

/* Form Grid */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.form-grid.single-column {
  grid-template-columns: 1fr;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group.span-2 {
  grid-column: span 2;
}

.form-label {
  font-weight: 500;
  color: #e2e8f0;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.form-label.required::after {
  content: ' *';
  color: #ef4444;
}

.field-hint {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-top: 0.25rem;
  line-height: 1.4;
}

/* Form Card Styling */
.form-steps .form-step > * {
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 16px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.4),
    0 0 40px rgba(0, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

/* Step Header Styling */
.step-header-info {
  flex: 1;
}

.step-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #00ffff;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
  margin-bottom: 0.5rem;
}

.step-subtitle {
  color: #94a3b8;
  margin: 0;
}

.step-progress {
  font-size: 0.875rem;
  color: #8a2be2;
  font-weight: 600;
  background: rgba(138, 43, 226, 0.2);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: 1px solid rgba(138, 43, 226, 0.3);
}

/* Enhanced Form Elements */
.form-group input,
.form-group select,
.form-group textarea {
  background: rgba(15, 23, 42, 0.8) !important;
  border: 1px solid rgba(0, 255, 255, 0.3) !important;
  color: #e2e8f0 !important;
  border-radius: 8px !important;
  padding: 0.75rem 1rem !important;
  transition: all 0.3s ease !important;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: rgba(0, 255, 255, 0.6) !important;
  box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.1) !important;
  background: rgba(15, 23, 42, 0.9) !important;
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: #94a3b8 !important;
}

/* Checkbox Styling */
.form-group input[type="checkbox"] {
  width: 1.25rem !important;
  height: 1.25rem !important;
  accent-color: #00ffff !important;
}

/* Number Input Styling */
.form-group input[type="number"] {
  -moz-appearance: textfield;
}

.form-group input[type="number"]::-webkit-outer-spin-button,
.form-group input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Select Dropdown Styling */
.form-group select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2300ffff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6,9 12,15 18,9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1rem;
  padding-right: 3rem !important;
}

.form-group select option {
  background: #1e293b;
  color: #e2e8f0;
  padding: 0.5rem;
}

/* Textarea Styling */
.form-group textarea {
  resize: vertical;
  min-height: 100px;
  line-height: 1.5;
}

/* Rich Text Editor Styling */
.form-group .rich-text-editor {
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 8px;
  overflow: hidden;
}

.form-group .rich-text-editor:focus-within {
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.1);
}

/* Error States */
.form-group.error input,
.form-group.error select,
.form-group.error textarea {
  border-color: rgba(239, 68, 68, 0.6) !important;
}

.form-group.error .form-label {
  color: #ef4444 !important;
}

.form-group .error-message {
  color: #ef4444;
  font-size: 0.75rem;
  margin-top: 0.25rem;
}

/* Success States */
.form-group.success input,
.form-group.success select,
.form-group.success textarea {
  border-color: rgba(16, 185, 129, 0.6) !important;
}

.form-group.success .form-label {
  color: #10b981 !important;
}

/* Disabled States */
.form-group input:disabled,
.form-group select:disabled,
.form-group textarea:disabled {
  opacity: 0.5 !important;
  cursor: not-allowed !important;
  background: rgba(15, 23, 42, 0.4) !important;
}

/* Step Navigation */
.step-navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 0;
  border-top: 1px solid rgba(0, 255, 255, 0.2);
  margin-top: 2rem;
}

.nav-buttons {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
}

.nav-spacer {
  flex: 1;
}

/* Responsive Design */
@media (max-width: 768px) {
  .form-header {
    margin: 1rem;
    padding: 1.5rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .form-content {
    padding: 0 1rem 2rem 1rem;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-group.span-2 {
    grid-column: span 1;
  }
  
  .steps-container {
    flex-direction: column;
  }
  
  .step-item {
    min-width: auto;
  }
  
  .nav-buttons {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .nav-spacer {
    display: none;
  }
}
</style>