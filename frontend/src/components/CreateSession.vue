<template>
  <el-dialog
    :model-value="visible"
    @update:model-value="$emit('update:visible', $event)"
    title="Создать новую сессию интервью"
    width="600px"
    :before-close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      @submit.prevent="handleSubmit"
    >
      <el-form-item label="Вакансия" prop="vacancy_id">
        <el-select
          v-model="form.vacancy_id"
          placeholder="Выберите вакансию"
          style="width: 100%"
          filterable
          @change="handleVacancyChange"
        >
          <el-option
            v-for="vacancy in vacancies"
            :key="vacancy.id"
            :label="vacancy.title"
            :value="vacancy.id"
          >
            <div class="vacancy-option">
              <div class="vacancy-title">{{ vacancy.title }}</div>
              <div class="vacancy-code" v-if="vacancy.vacancy_code">{{ vacancy.vacancy_code }}</div>
            </div>
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="Телефон кандидата" prop="phone">
        <el-input
          v-model="form.phone"
          placeholder="+7 (999) 123-45-67"
          clearable
        />
      </el-form-item>

      <el-form-item label="Email кандидата" prop="email">
        <el-input
          v-model="form.email"
          placeholder="candidate@example.com"
          clearable
        />
      </el-form-item>

      <!-- Vacancy Details Preview -->
      <el-form-item v-if="selectedVacancy" label="Детали вакансии">
        <el-card shadow="never" class="vacancy-preview">
          <div class="vacancy-preview-header">
            <h4>{{ selectedVacancy.title }}</h4>
            <el-tag v-if="selectedVacancy.vacancy_code" type="info" size="small">
              {{ selectedVacancy.vacancy_code }}
            </el-tag>
          </div>
          <div class="vacancy-preview-content">
            <div v-if="selectedVacancy.requirements" class="preview-section">
              <strong>Требования:</strong>
              <p>{{ selectedVacancy.requirements }}</p>
            </div>
            <div v-if="selectedVacancy.responsibilities" class="preview-section">
              <strong>Обязанности:</strong>
              <p>{{ selectedVacancy.responsibilities }}</p>
            </div>
            <div v-if="selectedVacancy.salary_min || selectedVacancy.salary_max" class="preview-section">
              <strong>Зарплата:</strong>
              <p>
                {{ selectedVacancy.salary_min ? `${selectedVacancy.salary_min.toLocaleString()} ₽` : '' }}
                {{ selectedVacancy.salary_min && selectedVacancy.salary_max ? ' - ' : '' }}
                {{ selectedVacancy.salary_max ? `${selectedVacancy.salary_max.toLocaleString()} ₽` : '' }}
              </p>
            </div>
          </div>
        </el-card>
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">Отмена</el-button>
        <el-button
          type="primary"
          @click="handleSubmit"
          :loading="loading"
          :disabled="!form.vacancy_id"
        >
          Создать сессию
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useHRStore } from '@/stores/hr'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:visible', 'created'])

const hrStore = useHRStore()

// Form data
const formRef = ref()
const loading = ref(false)
const form = reactive({
  vacancy_id: null,
  phone: '',
  email: ''
})

// Form validation rules
const rules = {
  vacancy_id: [
    { required: true, message: 'Пожалуйста, выберите вакансию', trigger: 'change' }
  ],
  phone: [
    { required: true, message: 'Пожалуйста, введите телефон', trigger: 'blur' },
    { pattern: /^\+?[0-9\s\-\(\)]+$/, message: 'Неверный формат телефона', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: 'Неверный формат email', trigger: 'blur' }
  ]
}

// Computed
const vacancies = computed(() => hrStore.vacancies)
const selectedVacancy = computed(() => {
  if (!form.vacancy_id) return null
  return vacancies.value.find(v => v.id === form.vacancy_id)
})

// Methods
const handleVacancyChange = () => {
  // Reset form when vacancy changes
  form.phone = ''
  form.email = ''
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    // Create session
    const sessionData = {
      vacancy_id: form.vacancy_id,
      phone: form.phone,
      email: form.email || null
    }
    
    const response = await hrStore.createSession(sessionData)
    
    ElMessage.success('Сессия успешно создана')
    emit('created', response)
    handleClose()
  } catch (error) {
    if (error.message) {
      ElMessage.error(error.message)
    } else {
      ElMessage.error('Ошибка при создании сессии')
    }
    console.error('Error creating session:', error)
  } finally {
    loading.value = false
  }
}

const handleClose = () => {
  // Reset form
  form.vacancy_id = null
  form.phone = ''
  form.email = ''
  
  if (formRef.value) {
    formRef.value.resetFields()
  }
  
  emit('update:visible', false)
}

// Load vacancies when component mounts
watch(() => props.visible, async (newVal) => {
  if (newVal && vacancies.value.length === 0) {
    try {
      await hrStore.fetchVacancies()
    } catch (error) {
      console.error('Error loading vacancies:', error)
    }
  }
})
</script>

<style scoped>
.vacancy-option {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.vacancy-option .vacancy-title {
  font-weight: 500;
  color: #303133;
}

.vacancy-option .vacancy-code {
  font-size: 12px;
  color: #909399;
}

.vacancy-preview {
  border: 1px solid #e4e7ed;
  border-radius: 4px;
}

.vacancy-preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.vacancy-preview-header h4 {
  margin: 0;
  color: #303133;
}

.vacancy-preview-content {
  font-size: 14px;
  color: #606266;
}

.preview-section {
  margin-bottom: 8px;
}

.preview-section:last-child {
  margin-bottom: 0;
}

.preview-section strong {
  color: #303133;
}

.preview-section p {
  margin: 4px 0 0 0;
  line-height: 1.4;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
