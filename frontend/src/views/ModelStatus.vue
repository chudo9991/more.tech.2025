<template>
  <div class="model-status">
    <!-- Header -->
    <PageHeader
      title="Статус Системы"
      subtitle="Мониторинг AI моделей и сервисов в реальном времени"
    >
      <template #actions>
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-2">
            <div 
              :class="[
                'w-3 h-3 rounded-full',
                overallStatus === 'healthy' ? 'bg-success-500' : 
                overallStatus === 'degraded' ? 'bg-warning-500' : 'bg-error-500'
              ]"
            ></div>
            <span class="text-sm font-medium text-white">
              {{ getOverallStatusLabel() }}
            </span>
          </div>
          
          <BaseButton
            variant="secondary"
            @click="refreshAllStatus"
            :loading="loading"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Обновить Все
          </BaseButton>
        </div>
      </template>
    </PageHeader>

    <!-- Main Content -->
    <div class="panel-content">
      <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      <!-- System Overview Cards -->
      <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <BaseMetricCard
          title="Время работы"
          :value="formatUptime(systemMetrics.uptime)"
          icon="mdi mdi-clock-outline"
          :variant="systemMetrics.uptime > 86400 ? 'success' : 'warning'"
        />
        
        <BaseMetricCard
          title="Активные модели"
          :value="`${activeModelsCount}/${totalModelsCount}`"
          icon="mdi mdi-cpu-64-bit"
          :variant="activeModelsCount === totalModelsCount ? 'success' : 'warning'"
        />
        
        <BaseMetricCard
          title="Время отклика"
          :value="`${systemMetrics.avgResponseTime}ms`"
          icon="mdi mdi-flash"
          :variant="systemMetrics.avgResponseTime < 1000 ? 'success' : 'warning'"
        />
        
        <BaseMetricCard
          title="Частота ошибок"
          :value="`${systemMetrics.errorRate}%`"
          icon="mdi mdi-alert"
          :variant="systemMetrics.errorRate < 5 ? 'success' : 'error'"
        />
      </section>

      <!-- Service Status Grid -->
      <section class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        
        <!-- Whisper Model Status -->
        <ServiceStatusCard
          title="Модель Whisper STT"
          :status="whisperStatus?.model_loaded ? 'healthy' : 'down'"
          :last-updated="whisperStatus?.last_updated"
          @refresh="fetchWhisperStatus"
          :loading="loadingStates.whisper"
        >
          <template #metrics>
            <div class="grid grid-cols-2 gap-4">
              <MetricItem
                label="Модель"
                :value="whisperStatus?.whisper_model || 'Неизвестно'"
              />
              <MetricItem
                label="Размер"
                :value="`${whisperStatus?.model_size_mb || 0} МБ`"
              />
              <MetricItem
                label="Статус VAD"
                :value="whisperStatus?.vad_loaded ? 'Активен' : 'Неактивен'"
                :status="whisperStatus?.vad_loaded ? 'success' : 'error'"
              />
              <MetricItem
                label="MinIO"
                :value="whisperStatus?.minio_connected ? 'Подключен' : 'Отключен'"
                :status="whisperStatus?.minio_connected ? 'success' : 'error'"
              />
            </div>
          </template>
          
          <template #actions>
            <div class="flex gap-2">
              <BaseButton
                variant="primary"
                size="sm"
                @click="reloadWhisperModel"
                :loading="loadingStates.reloadingWhisper"
              >
                Перезагрузить Модель
              </BaseButton>
              <BaseButton
                variant="danger"
                size="sm"
                @click="clearWhisperCache"
                :loading="loadingStates.clearingCache"
              >
                Очистить Кэш
              </BaseButton>
            </div>
          </template>
        </ServiceStatusCard>

        <!-- LLM Model Status -->
        <ServiceStatusCard
          title="Azure OpenAI LLM"
          :status="llmStatus?.azure_accessible ? 'healthy' : 'down'"
          :last-updated="llmStatus?.last_updated"
          @refresh="fetchLLMStatus"
          :loading="loadingStates.llm"
        >
          <template #metrics>
            <div class="grid grid-cols-2 gap-4">
              <MetricItem
                label="Развертывание"
                :value="llmStatus?.model_deployment || 'Неизвестно'"
              />
              <MetricItem
                label="Версия API"
                :value="llmStatus?.api_version || 'Неизвестно'"
              />
              <MetricItem
                label="Клиент"
                :value="llmStatus?.client_initialized ? 'Инициализирован' : 'Не готов'"
                :status="llmStatus?.client_initialized ? 'success' : 'error'"
              />
              <MetricItem
                label="Учетные данные"
                :value="llmStatus?.credentials_configured ? 'Настроены' : 'Отсутствуют'"
                :status="llmStatus?.credentials_configured ? 'success' : 'error'"
              />
            </div>
          </template>
          
          <template #actions>
            <div class="flex gap-2">
              <BaseButton
                variant="primary"
                size="sm"
                @click="testLLMConnection"
                :loading="loadingStates.testingLLM"
              >
                Тест Соединения
              </BaseButton>
            </div>
          </template>
        </ServiceStatusCard>

        <!-- Avatar Service Status -->
        <ServiceStatusCard
          title="Сервис A2E Аватар"
          :status="avatarStatus?.service_available ? 'healthy' : 'down'"
          :last-updated="avatarStatus?.last_updated"
          @refresh="fetchAvatarStatus"
          :loading="loadingStates.avatar"
        >
          <template #metrics>
            <div class="grid grid-cols-2 gap-4">
              <MetricItem
                label="Сервис"
                :value="avatarStatus?.service_available ? 'Доступен' : 'Недоступен'"
                :status="avatarStatus?.service_available ? 'success' : 'error'"
              />
              <MetricItem
                label="Стриминг"
                :value="avatarStatus?.streaming_enabled ? 'Включен' : 'Отключен'"
                :status="avatarStatus?.streaming_enabled ? 'success' : 'warning'"
              />
              <MetricItem
                label="Активные сессии"
                :value="avatarStatus?.active_sessions || 0"
              />
              <MetricItem
                label="Длина очереди"
                :value="avatarStatus?.queue_length || 0"
              />
            </div>
          </template>
          
          <template #actions>
            <div class="flex gap-2">
              <BaseButton
                variant="primary"
                size="sm"
                @click="testAvatarConnection"
                :loading="loadingStates.testingAvatar"
              >
                Тест Сервиса
              </BaseButton>
            </div>
          </template>
        </ServiceStatusCard>

        <!-- Database Status -->
        <ServiceStatusCard
          title="Подключение к БД"
          :status="databaseStatus?.connected ? 'healthy' : 'down'"
          :last-updated="databaseStatus?.last_updated"
          @refresh="fetchDatabaseStatus"
          :loading="loadingStates.database"
        >
          <template #metrics>
            <div class="grid grid-cols-2 gap-4">
              <MetricItem
                label="Соединение"
                :value="databaseStatus?.connected ? 'Подключено' : 'Отключено'"
                :status="databaseStatus?.connected ? 'success' : 'error'"
              />
              <MetricItem
                label="Размер пула"
                :value="`${databaseStatus?.active_connections || 0}/${databaseStatus?.max_connections || 0}`"
              />
              <MetricItem
                label="Время отклика"
                :value="`${databaseStatus?.response_time || 0}мс`"
                :status="(databaseStatus?.response_time || 0) < 100 ? 'success' : 'warning'"
              />
              <MetricItem
                label="Последний запрос"
                :value="formatRelativeTime(databaseStatus?.last_query_time)"
              />
            </div>
          </template>
          
          <template #actions>
            <div class="flex gap-2">
              <BaseButton
                variant="primary"
                size="sm"
                @click="testDatabaseConnection"
                :loading="loadingStates.testingDatabase"
              >
                Тест Запроса
              </BaseButton>
            </div>
          </template>
        </ServiceStatusCard>
      </section>

      <!-- Performance Metrics -->
      <section class="mb-8">
        <BaseCard>
          <template #header>
            <div class="flex items-center justify-between">
              <h2 class="text-lg font-semibold text-neutral-900 dark:text-white">
                Метрики Производительности
              </h2>
              <div class="flex items-center gap-2">
                <span class="text-sm text-neutral-500 dark:text-neutral-400">
                  Последние 24 часа
                </span>
                <BaseButton
                  variant="secondary"
                  size="sm"
                  @click="refreshMetrics"
                  :loading="loadingStates.metrics"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </BaseButton>
              </div>
            </div>
          </template>
          
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Response Time Chart -->
            <div>
              <h3 class="text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-4">
                Тренды Времени Отклика
              </h3>
              <div class="h-64 bg-neutral-100 dark:bg-neutral-800 rounded-lg flex items-center justify-center">
                <div class="text-center text-neutral-500 dark:text-neutral-400">
                  <svg class="w-12 h-12 mx-auto mb-2" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
                  </svg>
                  <p class="text-sm">Chart visualization would go here</p>
                </div>
              </div>
            </div>
            
            <!-- Error Rate Chart -->
            <div>
              <h3 class="text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-4">
                Тренды Частоты Ошибок
              </h3>
              <div class="h-64 bg-neutral-100 dark:bg-neutral-800 rounded-lg flex items-center justify-center">
                <div class="text-center text-neutral-500 dark:text-neutral-400">
                  <svg class="w-12 h-12 mx-auto mb-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  <p class="text-sm">Chart visualization would go here</p>
                </div>
              </div>
            </div>
          </div>
        </BaseCard>
      </section>

      <!-- Recent Alerts -->
      <section v-if="alerts.length > 0">
        <BaseCard>
          <template #header>
            <div class="flex items-center justify-between">
              <h2 class="text-lg font-semibold text-neutral-900 dark:text-white">
                Недавние Уведомления
              </h2>
              <BaseButton
                variant="secondary"
                size="sm"
                @click="clearAlerts"
              >
                Очистить Все
              </BaseButton>
            </div>
          </template>
          
          <div class="space-y-4">
            <AlertItem
              v-for="alert in alerts"
              :key="alert.id"
              :alert="alert"
              @dismiss="dismissAlert"
            />
          </div>
        </BaseCard>
      </section>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseMetricCard from '@/components/base/BaseMetricCard.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import SystemMetricCard from '@/components/SystemMetricCard.vue'
import ServiceStatusCard from '@/components/ServiceStatusCard.vue'
import MetricItem from '@/components/MetricItem.vue'
import AlertItem from '@/components/AlertItem.vue'

// Types
interface SystemMetrics {
  uptime: number
  avgResponseTime: number
  errorRate: number
  activeConnections: number
}

interface ServiceStatus {
  service_available?: boolean
  model_loaded?: boolean
  azure_accessible?: boolean
  connected?: boolean
  last_updated?: string
  [key: string]: any
}

interface Alert {
  id: string
  type: 'error' | 'warning' | 'info'
  title: string
  message: string
  timestamp: Date
  service?: string
}

// Reactive data
const loading = ref(false)
const whisperStatus = ref<ServiceStatus | null>(null)
const llmStatus = ref<ServiceStatus | null>(null)
const avatarStatus = ref<ServiceStatus | null>(null)
const databaseStatus = ref<ServiceStatus | null>(null)
const systemMetrics = ref<SystemMetrics>({
  uptime: 0,
  avgResponseTime: 0,
  errorRate: 0,
  activeConnections: 0
})

const alerts = ref<Alert[]>([])
const wsConnection = ref<WebSocket | null>(null)

const loadingStates = ref({
  whisper: false,
  llm: false,
  avatar: false,
  database: false,
  metrics: false,
  reloadingWhisper: false,
  clearingCache: false,
  testingLLM: false,
  testingAvatar: false,
  testingDatabase: false
})

// Computed properties
const overallStatus = computed(() => {
  const services = [whisperStatus.value, llmStatus.value, avatarStatus.value, databaseStatus.value]
  const healthyServices = services.filter(service => 
    service?.model_loaded || service?.azure_accessible || service?.service_available || service?.connected
  ).length
  
  if (healthyServices === services.length) return 'healthy'
  if (healthyServices > 0) return 'degraded'
  return 'down'
})

const activeModelsCount = computed(() => {
  let count = 0
  if (whisperStatus.value?.model_loaded) count++
  if (llmStatus.value?.azure_accessible) count++
  if (avatarStatus.value?.service_available) count++
  if (databaseStatus.value?.connected) count++
  return count
})

const totalModelsCount = computed(() => 4)

// WebSocket connection for real-time updates
const connectWebSocket = (): void => {
  try {
    const wsUrl = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/api/v1/ws/status`
    wsConnection.value = new WebSocket(wsUrl)
    
    wsConnection.value.onopen = () => {
      console.log('WebSocket connected for real-time status updates')
    }
    
    wsConnection.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        handleRealtimeUpdate(data)
      } catch (error) {
        console.error('Error parsing WebSocket message:', error)
      }
    }
    
    wsConnection.value.onclose = () => {
      console.log('WebSocket disconnected, attempting to reconnect...')
      setTimeout(connectWebSocket, 5000) // Reconnect after 5 seconds
    }
    
    wsConnection.value.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
  } catch (error) {
    console.error('Failed to connect WebSocket:', error)
  }
}

const handleRealtimeUpdate = (data: any): void => {
  switch (data.type) {
    case 'whisper_status':
      whisperStatus.value = { ...whisperStatus.value, ...data.status }
      break
    case 'llm_status':
      llmStatus.value = { ...llmStatus.value, ...data.status }
      break
    case 'avatar_status':
      avatarStatus.value = { ...avatarStatus.value, ...data.status }
      break
    case 'database_status':
      databaseStatus.value = { ...databaseStatus.value, ...data.status }
      break
    case 'system_metrics':
      systemMetrics.value = { ...systemMetrics.value, ...data.metrics }
      break
    case 'alert':
      addAlert(data.alert)
      break
  }
}

// API methods
const fetchWhisperStatus = async (): Promise<void> => {
  loadingStates.value.whisper = true
  try {
    const response = await fetch('/api/v1/stt/model-status')
    if (response.ok) {
      const data = await response.json()
      whisperStatus.value = { ...data, last_updated: new Date().toISOString() }
    }
  } catch (error) {
    console.error('Error fetching Whisper status:', error)
    addAlert({
      id: `whisper-error-${Date.now()}`,
      type: 'error',
      title: 'Whisper Status Error',
      message: 'Failed to fetch Whisper model status',
      timestamp: new Date(),
      service: 'whisper'
    })
  } finally {
    loadingStates.value.whisper = false
  }
}

const fetchLLMStatus = async (): Promise<void> => {
  loadingStates.value.llm = true
  try {
    const response = await fetch('/api/v1/llm/model-status')
    if (response.ok) {
      const data = await response.json()
      llmStatus.value = { ...data, last_updated: new Date().toISOString() }
    }
  } catch (error) {
    console.error('Error fetching LLM status:', error)
    addAlert({
      id: `llm-error-${Date.now()}`,
      type: 'error',
      title: 'LLM Status Error',
      message: 'Failed to fetch LLM model status',
      timestamp: new Date(),
      service: 'llm'
    })
  } finally {
    loadingStates.value.llm = false
  }
}

const fetchAvatarStatus = async (): Promise<void> => {
  loadingStates.value.avatar = true
  try {
    const response = await fetch('/api/v1/avatar/status')
    if (response.ok) {
      const data = await response.json()
      avatarStatus.value = { ...data, last_updated: new Date().toISOString() }
    }
  } catch (error) {
    console.error('Error fetching Avatar status:', error)
    addAlert({
      id: `avatar-error-${Date.now()}`,
      type: 'error',
      title: 'Avatar Status Error',
      message: 'Failed to fetch Avatar service status',
      timestamp: new Date(),
      service: 'avatar'
    })
  } finally {
    loadingStates.value.avatar = false
  }
}

const fetchDatabaseStatus = async (): Promise<void> => {
  loadingStates.value.database = true
  try {
    const response = await fetch('/api/v1/database/status')
    if (response.ok) {
      const data = await response.json()
      databaseStatus.value = { ...data, last_updated: new Date().toISOString() }
    }
  } catch (error) {
    console.error('Error fetching Database status:', error)
    addAlert({
      id: `database-error-${Date.now()}`,
      type: 'error',
      title: 'Database Status Error',
      message: 'Failed to fetch database status',
      timestamp: new Date(),
      service: 'database'
    })
  } finally {
    loadingStates.value.database = false
  }
}

const fetchSystemMetrics = async (): Promise<void> => {
  try {
    const response = await fetch('/api/v1/system/metrics')
    if (response.ok) {
      const data = await response.json()
      systemMetrics.value = data
    }
  } catch (error) {
    console.error('Error fetching system metrics:', error)
  }
}

const refreshAllStatus = async (): Promise<void> => {
  loading.value = true
  try {
    await Promise.all([
      fetchWhisperStatus(),
      fetchLLMStatus(),
      fetchAvatarStatus(),
      fetchDatabaseStatus(),
      fetchSystemMetrics()
    ])
  } finally {
    loading.value = false
  }
}

const refreshMetrics = async (): Promise<void> => {
  loadingStates.value.metrics = true
  try {
    await fetchSystemMetrics()
  } finally {
    loadingStates.value.metrics = false
  }
}

// Action methods
const reloadWhisperModel = async (): Promise<void> => {
  loadingStates.value.reloadingWhisper = true
  try {
    const response = await fetch('/api/v1/stt/reload-model', { method: 'POST' })
    if (response.ok) {
      addAlert({
        id: `whisper-reload-${Date.now()}`,
        type: 'info',
        title: 'Model Reloaded',
        message: 'Whisper model has been successfully reloaded',
        timestamp: new Date(),
        service: 'whisper'
      })
      await fetchWhisperStatus()
    }
  } catch (error) {
    console.error('Error reloading Whisper model:', error)
  } finally {
    loadingStates.value.reloadingWhisper = false
  }
}

const clearWhisperCache = async (): Promise<void> => {
  if (!confirm('Are you sure you want to clear the Whisper model cache?')) {
    return
  }
  
  loadingStates.value.clearingCache = true
  try {
    const response = await fetch('/api/v1/stt/clear-cache', { method: 'POST' })
    if (response.ok) {
      addAlert({
        id: `whisper-cache-${Date.now()}`,
        type: 'info',
        title: 'Cache Cleared',
        message: 'Whisper model cache has been cleared',
        timestamp: new Date(),
        service: 'whisper'
      })
      await fetchWhisperStatus()
    }
  } catch (error) {
    console.error('Error clearing Whisper cache:', error)
  } finally {
    loadingStates.value.clearingCache = false
  }
}

const testLLMConnection = async (): Promise<void> => {
  loadingStates.value.testingLLM = true
  try {
    const response = await fetch('/api/v1/llm/test-connection', { method: 'POST' })
    if (response.ok) {
      addAlert({
        id: `llm-test-${Date.now()}`,
        type: 'info',
        title: 'Connection Test',
        message: 'LLM connection test completed successfully',
        timestamp: new Date(),
        service: 'llm'
      })
    }
  } catch (error) {
    console.error('Error testing LLM connection:', error)
  } finally {
    loadingStates.value.testingLLM = false
  }
}

const testAvatarConnection = async (): Promise<void> => {
  loadingStates.value.testingAvatar = true
  try {
    const response = await fetch('/api/v1/avatar/test-connection', { method: 'POST' })
    if (response.ok) {
      addAlert({
        id: `avatar-test-${Date.now()}`,
        type: 'info',
        title: 'Service Test',
        message: 'Avatar service test completed successfully',
        timestamp: new Date(),
        service: 'avatar'
      })
    }
  } catch (error) {
    console.error('Error testing Avatar connection:', error)
  } finally {
    loadingStates.value.testingAvatar = false
  }
}

const testDatabaseConnection = async (): Promise<void> => {
  loadingStates.value.testingDatabase = true
  try {
    const response = await fetch('/api/v1/database/test-query', { method: 'POST' })
    if (response.ok) {
      addAlert({
        id: `database-test-${Date.now()}`,
        type: 'info',
        title: 'Query Test',
        message: 'Database query test completed successfully',
        timestamp: new Date(),
        service: 'database'
      })
    }
  } catch (error) {
    console.error('Error testing Database connection:', error)
  } finally {
    loadingStates.value.testingDatabase = false
  }
}

// Alert management
const addAlert = (alert: Alert): void => {
  alerts.value.unshift(alert)
  // Keep only the last 10 alerts
  if (alerts.value.length > 10) {
    alerts.value = alerts.value.slice(0, 10)
  }
}

const dismissAlert = (alertId: string): void => {
  const index = alerts.value.findIndex(alert => alert.id === alertId)
  if (index > -1) {
    alerts.value.splice(index, 1)
  }
}

const clearAlerts = (): void => {
  alerts.value = []
}

// Utility methods
const getOverallStatusLabel = (): string => {
  switch (overallStatus.value) {
    case 'healthy': return 'Все Системы Работают'
    case 'degraded': return 'Обнаружены Проблемы'
    case 'down': return 'Проблемы Системы'
    default: return 'Неизвестный Статус'
  }
}

const formatUptime = (seconds: number): string => {
  const days = Math.floor(seconds / 86400)
  const hours = Math.floor((seconds % 86400) / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  
  if (days > 0) return `${days}d ${hours}h`
  if (hours > 0) return `${hours}h ${minutes}m`
  return `${minutes}m`
}

const formatRelativeTime = (timestamp?: string): string => {
  if (!timestamp) return 'Никогда'
  
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  
  if (diffMins < 1) return 'Только что'
  if (diffMins < 60) return `${diffMins}м назад`
  
  const diffHours = Math.floor(diffMins / 60)
  if (diffHours < 24) return `${diffHours}ч назад`
  
  const diffDays = Math.floor(diffHours / 24)
  return `${diffDays}д назад`
}

// Lifecycle
onMounted(() => {
  refreshAllStatus()
  connectWebSocket()
  
  // Set up periodic refresh every 30 seconds
  const interval = setInterval(refreshAllStatus, 30000)
  
  onBeforeUnmount(() => {
    clearInterval(interval)
    if (wsConnection.value) {
      wsConnection.value.close()
    }
  })
})
</script>

<style scoped>
/* Model Status Styles */
.model-status {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #0f172a 50%, #1e293b 75%, #0f172a 100%);
  position: relative;
  overflow-x: hidden;
}

.model-status::before {
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

.model-status::after {
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
.status-header {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.6));
  backdrop-filter: blur(30px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 0 0 20px 20px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.4),
    0 0 40px rgba(0, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 100;
}

.status-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #00ffff;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.status-subtitle {
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #94a3b8;
}

.status-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #e2e8f0;
}

/* Smooth transitions for all elements */
.model-status * {
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, backdrop-filter;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* Focus styles for accessibility */
.model-status button:focus-visible,
.model-status input:focus-visible,
.model-status select:focus-visible {
  @apply outline-none ring-2 ring-primary-500 ring-offset-2 ring-offset-white dark:ring-offset-neutral-900;
}

/* Custom animations for status indicators */
@keyframes pulse-success {
  0%, 100% {
    @apply bg-success-500;
  }
  50% {
    @apply bg-success-400;
  }
}

@keyframes pulse-warning {
  0%, 100% {
    @apply bg-warning-500;
  }
  50% {
    @apply bg-warning-400;
  }
}

@keyframes pulse-error {
  0%, 100% {
    @apply bg-error-500;
  }
  50% {
    @apply bg-error-400;
  }
}

.status-indicator-success {
  animation: pulse-success 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.status-indicator-warning {
  animation: pulse-warning 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.status-indicator-error {
  animation: pulse-error 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>