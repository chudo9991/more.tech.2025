<template>
  <div class="candidate-interview">
    <!-- Header -->
    <PageHeader
      title="AI Интервью"
      :subtitle="getHeaderSubtitle()"
    >
      <template #actions>
        <div v-if="sessionData && scenarioData" class="flex items-center gap-4">
          <div class="text-right">
            <div class="text-xs text-neutral-400 mb-1">Прогресс</div>
            <div class="flex items-center gap-2">
              <span class="text-sm font-medium text-white">
                {{ sessionData.currentStep }}/{{ scenarioData.total_nodes || 0 }}
              </span>
              <div class="w-24 bg-neutral-700 rounded-full h-2">
                <div 
                  class="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full transition-all duration-300"
                  :style="{ width: `${progressPercentage}%` }"
                  role="progressbar"
                  :aria-valuenow="sessionData.currentStep"
                  :aria-valuemax="scenarioData.total_nodes || 0"
                ></div>
              </div>
            </div>
          </div>
        </div>
        <BaseButton
          v-if="interviewStarted"
          variant="danger"
          @click="endInterview"
          :disabled="!interviewStarted"
        >
          Завершить Интервью
        </BaseButton>
      </template>
    </PageHeader>
    
    <!-- Main Content -->
    <div class="panel-content">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Avatar Section -->
        <div class="lg:col-span-2">
          <BaseCard class="h-full">
            <template #header>
              <div class="flex items-center justify-between">
                <h2 class="text-lg font-semibold text-neutral-900 dark:text-white">
                  AI Интервьюер
                </h2>
                <div class="flex items-center gap-2">
                  <div 
                    :class="[
                      'w-2 h-2 rounded-full',
                      isConnected ? 'bg-success-500' : 'bg-error-500'
                    ]"
                    :aria-label="isConnected ? 'Avatar connected' : 'Avatar disconnected'"
                  ></div>
                  <span class="text-sm text-neutral-600 dark:text-neutral-400">
                    {{ isConnected ? 'Подключен' : 'Отключен' }}
                  </span>
                </div>
              </div>
            </template>
            
            <div class="aspect-video bg-neutral-100 dark:bg-neutral-800 rounded-lg overflow-hidden">
              <StreamingAvatarPlayer 
                ref="avatarPlayerRef"
                :session-id="sessionId"
                @avatar-connected="handleAvatarConnected"
                @avatar-disconnected="handleAvatarDisconnected"
                @avatar-question="handleAvatarQuestion"
                @avatar-speak="handleAvatarSpeak"
                class="w-full h-full"
              />
            </div>
            
            <!-- Avatar Status -->
            <div class="mt-4 p-3 bg-neutral-50 dark:bg-neutral-800 rounded-lg">
              <div class="flex items-center justify-between text-sm">
                <span class="text-neutral-600 dark:text-neutral-400">Статус:</span>
                <span 
                  :class="[
                    'font-medium',
                    isVideoPlaying ? 'text-primary-600 dark:text-primary-400' : 'text-neutral-900 dark:text-white'
                  ]"
                >
                  {{ isVideoPlaying ? 'Говорит...' : 'Слушает' }}
                </span>
              </div>
            </div>
          </BaseCard>
        </div>
        
        <!-- Control Panel -->
        <div class="space-y-6">
          
          <!-- Interview Setup -->
          <BaseCard v-if="!interviewStarted">
            <template #header>
              <h2 class="text-lg font-semibold text-neutral-900 dark:text-white">
                Настройка Интервью
              </h2>
            </template>
            
            <div class="space-y-4">
              <!-- Code Input -->
              <div>
                <label for="interview-code" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                  Код Интервью
                </label>
                <BaseInput
                  id="interview-code"
                  v-model="interviewCode"
                  placeholder="Введите 6-значный код"
                  maxlength="6"
                  :error="codeError"
                  @keyup.enter="validateCode"
                  aria-describedby="code-help"
                />
                <p id="code-help" class="mt-1 mb-2 text-xs text-neutral-500 dark:text-neutral-400">
                  Введите 6-значный код, предоставленный HR
                </p>
              </div>
              
              <!-- Action Buttons -->
              <div class="flex flex-col sm:flex-row gap-3">
                <BaseButton
                  variant="primary"
                  @click="validateCode"
                  :loading="validatingCode"
                  :disabled="!interviewCode || interviewCode.length !== 6"
                  class="flex-1"
                >
                  Проверить Код
                </BaseButton>
                <BaseButton
                  variant="secondary"
                  @click="startInterview"
                  :disabled="!resumeLinked"
                  class="flex-1"
                >
                  Начать Интервью
                </BaseButton>
              </div>
            </div>
          </BaseCard>
          
          <!-- Resume Info -->
          <BaseCard v-if="resumeLinked && linkedResume" variant="secondary">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-success-100 dark:bg-success-900/20 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-success-600 dark:text-success-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-neutral-900 dark:text-white">
                  Резюме Привязано
                </p>
                <p class="text-sm text-neutral-500 dark:text-neutral-400 truncate">
                  {{ linkedResume.original_filename }}
                </p>
              </div>
            </div>
          </BaseCard>
          
          <!-- Interview Transcript -->
          <BaseCard v-if="interviewStarted">
            <template #header>
              <div class="flex items-center justify-between">
                <div>
                  <h2 class="text-lg font-semibold text-neutral-900 dark:text-white">
                    Транскрипция Интервью
                  </h2>
                  <div v-if="chatMessages.length > 0" class="text-xs text-neutral-500 dark:text-neutral-400 mt-1">
                    {{ chatMessages.length }} {{ chatMessages.length === 1 ? 'сообщение' : chatMessages.length < 5 ? 'сообщения' : 'сообщений' }}
                  </div>
                </div>
                <div class="flex items-center gap-3">
                  <BaseButton
                    v-if="chatMessages.length > 0"
                    variant="secondary"
                    size="sm"
                    @click="exportTranscript"
                    class="text-xs"
                  >
                    <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"/>
                    </svg>
                    Экспорт
                  </BaseButton>
                  <div class="flex items-center gap-2 text-xs text-neutral-500 dark:text-neutral-400">
                    <div class="w-2 h-2 bg-success-500 rounded-full animate-pulse"></div>
                    <span>В реальном времени</span>
                  </div>
                </div>
              </div>
            </template>
            
            <div 
              ref="chatContainer"
              class="h-80 overflow-y-auto p-4 bg-gradient-to-b from-neutral-50 to-neutral-100 dark:from-neutral-800 dark:to-neutral-900 rounded-lg border border-neutral-200 dark:border-neutral-700"
              role="log"
              aria-live="polite"
              aria-label="Interview transcript"
            >
              <div class="space-y-4">
                <div 
                  v-for="message in chatMessages" 
                  :key="message.id"
                  class="transcript-message"
                >
                  <!-- Avatar Message -->
                  <div v-if="message.type === 'avatar'" class="flex items-start gap-3 mb-4">
                    <div class="flex-shrink-0">
                      <div class="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center">
                        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                      </div>
                    </div>
                    <div class="flex-1 min-w-0">
                      <div class="flex items-center gap-2 mb-1">
                        <span class="text-sm font-semibold text-primary-600 dark:text-primary-400">
                          AI Интервьюер
                        </span>
                        <span class="text-xs text-neutral-500 dark:text-neutral-400">
                          {{ formatTime(message.timestamp) }}
                        </span>
                        <div v-if="message.is_contextual" class="px-2 py-0.5 bg-warning-100 dark:bg-warning-900/20 text-warning-700 dark:text-warning-300 text-xs rounded-full">
                          Контекстный вопрос
                        </div>
                      </div>
                      <div class="bg-white dark:bg-neutral-700 rounded-lg p-3 shadow-sm border border-neutral-200 dark:border-neutral-600">
                        <p class="text-sm text-neutral-900 dark:text-white leading-relaxed">
                          {{ message.text }}
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- User Message -->
                  <div v-else class="flex items-start gap-3 mb-4">
                    <div class="flex-shrink-0">
                      <div class="w-8 h-8 bg-gradient-to-br from-success-500 to-success-600 rounded-full flex items-center justify-center">
                        <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"/>
                        </svg>
                      </div>
                    </div>
                    <div class="flex-1 min-w-0">
                      <div class="flex items-center gap-2 mb-1">
                        <span class="text-sm font-semibold text-success-600 dark:text-success-400">
                          Кандидат
                        </span>
                        <span class="text-xs text-neutral-500 dark:text-neutral-400">
                          {{ formatTime(message.timestamp) }}
                        </span>
                        <div v-if="message.text.includes('🎤')" class="px-2 py-0.5 bg-info-100 dark:bg-info-900/20 text-info-700 dark:text-info-300 text-xs rounded-full">
                          Голосовой ответ
                        </div>
                      </div>
                      <div class="bg-success-50 dark:bg-success-900/10 rounded-lg p-3 border border-success-200 dark:border-success-800">
                        <p class="text-sm text-neutral-900 dark:text-white leading-relaxed">
                          {{ message.text }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Empty state -->
              <div v-if="chatMessages.length === 0" class="text-center py-12">
                <div class="text-neutral-400 dark:text-neutral-500">
                  <div class="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-primary-100 to-primary-200 dark:from-primary-900/20 dark:to-primary-800/20 rounded-full flex items-center justify-center">
                    <svg class="w-8 h-8 text-primary-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd" />
                    </svg>
                  </div>
                  <h3 class="text-sm font-medium text-neutral-600 dark:text-neutral-300 mb-1">
                    Транскрипция интервью
                  </h3>
                  <p class="text-xs text-neutral-500 dark:text-neutral-400">
                    Здесь будет отображаться весь диалог между вами и AI интервьюером
                  </p>
                </div>
              </div>
              
              <!-- AI Speaking indicator -->
              <div v-if="isVideoPlaying" class="flex items-start gap-3 mb-4">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center">
                    <svg class="w-4 h-4 text-white animate-pulse" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 mb-1">
                    <span class="text-sm font-semibold text-primary-600 dark:text-primary-400">
                      AI Интервьюер
                    </span>
                    <span class="text-xs text-neutral-500 dark:text-neutral-400">
                      сейчас
                    </span>
                  </div>
                  <div class="bg-white dark:bg-neutral-700 rounded-lg p-3 shadow-sm border border-neutral-200 dark:border-neutral-600">
                    <div class="flex items-center gap-1">
                      <div class="w-2 h-2 bg-primary-500 rounded-full animate-bounce"></div>
                      <div class="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                      <div class="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                      <span class="text-xs text-neutral-500 dark:text-neutral-400 ml-2">говорит...</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- User Recording indicator -->
              <div v-if="isRecording" class="flex items-start gap-3 mb-4">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-gradient-to-br from-error-500 to-error-600 rounded-full flex items-center justify-center">
                    <svg class="w-4 h-4 text-white animate-pulse" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 mb-1">
                    <span class="text-sm font-semibold text-error-600 dark:text-error-400">
                      Кандидат
                    </span>
                    <span class="text-xs text-neutral-500 dark:text-neutral-400">
                      записывает ответ
                    </span>
                    <div class="px-2 py-0.5 bg-error-100 dark:bg-error-900/20 text-error-700 dark:text-error-300 text-xs rounded-full animate-pulse">
                      REC {{ recordingDuration }}s
                    </div>
                  </div>
                  <div class="bg-error-50 dark:bg-error-900/10 rounded-lg p-3 border border-error-200 dark:border-error-800">
                    <div class="flex items-center gap-2">
                      <div class="flex gap-1">
                        <div class="w-1 h-4 bg-error-500 rounded-full animate-pulse"></div>
                        <div class="w-1 h-3 bg-error-400 rounded-full animate-pulse" style="animation-delay: 0.1s"></div>
                        <div class="w-1 h-5 bg-error-500 rounded-full animate-pulse" style="animation-delay: 0.2s"></div>
                        <div class="w-1 h-2 bg-error-400 rounded-full animate-pulse" style="animation-delay: 0.3s"></div>
                        <div class="w-1 h-4 bg-error-500 rounded-full animate-pulse" style="animation-delay: 0.4s"></div>
                      </div>
                      <span class="text-xs text-error-600 dark:text-error-400">
                        Идет запись голосового ответа...
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </BaseCard>
          
          <!-- Voice Controls -->
          <BaseCard v-if="interviewStarted">
            <template #header>
              <h2 class="text-lg font-semibold text-neutral-900 dark:text-white">
                Голосовой Ответ
              </h2>
            </template>
            
            <div class="space-y-4">
              <!-- Microphone Status -->
              <div class="flex items-center justify-between p-3 bg-neutral-50 dark:bg-neutral-800 rounded-lg">
                <div class="flex items-center gap-2">
                  <div 
                    :class="[
                      'w-2 h-2 rounded-full',
                      availableMicrophones.length > 0 ? 'bg-success-500' : 'bg-warning-500'
                    ]"
                  ></div>
                  <span class="text-sm text-neutral-600 dark:text-neutral-400">
                    {{ availableMicrophones.length > 0 ? 'Микрофон Готов' : 'Микрофон Недоступен' }}
                  </span>
                </div>
                
                <BaseButton
                  v-if="availableMicrophones.length === 0"
                  variant="warning"
                  size="sm"
                  @click="requestMicrophonePermission"
                  :disabled="!resumeLinked || isVideoPlaying || isWaitingForVideo"
                >
                  Запросить Доступ
                </BaseButton>
              </div>
              
              <!-- Microphone Selection -->
              <div v-if="availableMicrophones.length > 1">
                <label for="microphone-select" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                  Выберите Микрофон
                </label>
                <BaseSelect
                  id="microphone-select"
                  v-model="selectedMicrophone"
                  :items="microphoneOptions"
                  placeholder="Выберите микрофон"
                />
              </div>
              
              <!-- Recording Controls -->
              <div class="space-y-3">
                <div class="flex gap-3">
                  <BaseButton
                    variant="primary"
                    @click="startRecording"
                    :disabled="isRecording || !resumeLinked || isVideoPlaying || isWaitingForVideo || availableMicrophones.length === 0"
                    class="flex-1"
                    :aria-label="isRecording ? 'Recording in progress' : 'Start recording your answer'"
                  >
                    <svg v-if="!isRecording" class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clip-rule="evenodd" />
                    </svg>
                    <div v-else class="w-4 h-4 mr-2 bg-current rounded-full animate-pulse"></div>
                    {{ isRecording ? 'Запись...' : 'Записать Ответ' }}
                  </BaseButton>
                  
                  <BaseButton
                    variant="danger"
                    @click="stopRecording"
                    :disabled="!isRecording"
                    aria-label="Stop recording"
                  >
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z" clip-rule="evenodd" />
                    </svg>
                  </BaseButton>
                </div>
                
                <!-- Recording Progress -->
                <div v-if="isRecording" class="space-y-2">
                  <div class="flex items-center justify-between text-sm">
                    <span class="text-neutral-600 dark:text-neutral-400">Запись</span>
                    <span class="font-mono text-neutral-900 dark:text-white">{{ recordingDuration }}s</span>
                  </div>
                  <div class="w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
                    <div 
                      class="bg-primary-500 h-2 rounded-full transition-all duration-300"
                      :style="{ width: `${recordingProgress}%` }"
                      role="progressbar"
                      :aria-valuenow="recordingProgress"
                      aria-valuemax="100"
                      :aria-label="`Recording progress: ${recordingDuration} seconds`"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </BaseCard>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, onBeforeUnmount } from 'vue'
// @ts-ignore
import { useRoute } from 'vue-router'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import BaseSelect from '@/components/base/BaseSelect.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import StreamingAvatarPlayer from '@/components/StreamingAvatarPlayer.vue'
import type { InterviewSession, SessionStatus } from '@/types/session'
import type { SelectItem } from '@/types/components'

// Types
interface ChatMessage {
  id: string
  type: 'user' | 'avatar'
  text: string
  timestamp: Date
  is_contextual?: boolean
}

interface LinkedResume {
  id: string
  original_filename: string
  vacancy_id?: string
  vacancy_requirements?: string
}

interface ScenarioData {
  total_nodes: number
}

interface CurrentQuestion {
  question_text: string
  question_id?: string
  node_id?: string
  is_contextual?: boolean
  contextual_question_id?: string
}

interface MicrophoneDevice {
  deviceId: string
  label: string
}

// Reactive data
const route = useRoute()
const sessionData = ref<InterviewSession | null>(null)
const interviewStarted = ref(false)
const isRecording = ref(false)
const recordingProgress = ref(0)
const recordingDuration = ref(0)
const isConnected = ref(false)

const chatMessages = ref<ChatMessage[]>([])
const chatContainer = ref<HTMLElement | null>(null)
const availableMicrophones = ref<MicrophoneDevice[]>([])
const selectedMicrophone = ref('')
const currentQuestion = ref<CurrentQuestion | null>(null)

// Interview code variables
const interviewCode = ref('')
const validatingCode = ref(false)
const codeError = ref('')
const resumeLinked = ref(false)
const linkedResume = ref<LinkedResume | null>(null)
const scenarioData = ref<ScenarioData | null>(null)

// Video state management
const isVideoPlaying = ref(false)
const isWaitingForVideo = ref(false)

// Recording state
let recordingInterval: NodeJS.Timeout | null = null
let mediaRecorder: MediaRecorder | null = null
let audioChunks: Blob[] = []
let audioContext: AudioContext | null = null
let analyser: AnalyserNode | null = null
let microphone: MediaStreamAudioSourceNode | null = null
let vadInterval: NodeJS.Timeout | null = null
let silenceStart: number | null = null

const VAD_SILENCE_THRESHOLD = 2000 // 2.0 seconds of silence
const VAD_VOLUME_THRESHOLD = 0.1 // Volume threshold for speech detection
const VAD_DEBOUNCE_TIME = 250 // 250ms debounce

// Refs
const sessionId = ref<string | null>(null)
const avatarPlayerRef = ref<InstanceType<typeof StreamingAvatarPlayer> | null>(null)

// Computed properties
const progressPercentage = computed(() => {
  if (!sessionData.value || !scenarioData.value?.total_nodes) return 0
  return Math.round((sessionData.value.currentStep / scenarioData.value.total_nodes) * 100)
})

const microphoneOptions = computed<SelectItem[]>(() => {
  return availableMicrophones.value.map(mic => ({
    title: mic.label || `Microphone ${mic.deviceId.slice(0, 8)}`,
    value: mic.deviceId
  }))
})

// Methods
const loadScenarioData = async (resumeId: string): Promise<void> => {
  try {
    // Get resume information to find linked vacancy
    const resumeResponse = await fetch(`/api/v1/resumes/${resumeId}`)
    if (resumeResponse.ok) {
      const resume = await resumeResponse.json()
      
      // Get scenario for vacancy
      if (resume.vacancy_id) {
        const scenarioResponse = await fetch(`/api/v1/scenarios/by-vacancy/${resume.vacancy_id}`)
        if (scenarioResponse.ok) {
          const scenario = await scenarioResponse.json()
          scenarioData.value = scenario
        }
      }
    }
  } catch (error) {
    console.error('Error loading scenario data:', error)
  }
}

const validateCode = async (): Promise<void> => {
  if (!interviewCode.value || interviewCode.value.length !== 6) {
    codeError.value = 'Code must contain 6 digits'
    return
  }
  
  validatingCode.value = true
  codeError.value = ''
  
  try {
    const response = await fetch('/api/v1/interview-codes/validate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        code: interviewCode.value
      })
    })
    
    const result = await response.json()
    
    if (result.valid) {
      // Load resume data
      const resumeResponse = await fetch(`/api/v1/resumes/${result.resume_id}`)
      if (resumeResponse.ok) {
        linkedResume.value = await resumeResponse.json()
      }
      
      // Load scenario data
      await loadScenarioData(result.resume_id)
      
      resumeLinked.value = true
      console.log('Code validated successfully! Resume linked to interview.')
    } else {
      codeError.value = result.message || 'Invalid code'
    }
  } catch (error) {
    codeError.value = 'Code validation error'
    console.error('Code validation error:', error)
  } finally {
    validatingCode.value = false
  }
}

const loadSessionData = async (): Promise<void> => {
  try {
    // In production, this would fetch from API
    sessionData.value = {
      id: sessionId.value || 'temp-session',
      vacancyId: linkedResume.value?.vacancy_id || 'default',
      candidateInfo: {
        phone: '+1-000-000-0000'
      },
      status: 'in_progress' as SessionStatus,
      currentStep: 0,
      totalSteps: 8,
      responses: [],
      scores: {
        overall: 0,
        technical: 0,
        communication: 0,
        experience: 0,
        cultural: 0,
        breakdown: []
      },
      metadata: {},
      createdAt: new Date(),
      updatedAt: new Date()
    }
  } catch (error) {
    console.error('Error loading session data:', error)
  }
}

const startInterview = async (): Promise<void> => {
  try {
    // Create session in database with resume link
    const sessionDataPayload = {
      vacancy_id: linkedResume.value?.vacancy_id || 'SWE_BACK_001',
      phone: '+7-999-999-99-99',
      email: 'candidate@example.com',
      resume_id: linkedResume.value?.id
    }
    
    const sessionResponse = await fetch('/api/v1/sessions/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(sessionDataPayload)
    })
    
    if (!sessionResponse.ok) {
      throw new Error('Failed to create session')
    }
    
    const sessionResponseData = await sessionResponse.json()
    sessionId.value = sessionResponseData.id
    console.log('Session created with ID:', sessionId.value)
    
    interviewStarted.value = true
    
    // Add welcome message to chat
    const welcomeMessage = 'Hello! Welcome to the AI interview. I\'m here to ask you some questions about your experience and skills. Ready to begin?'
    
    addMessage({
      id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      type: 'avatar',
      text: welcomeMessage,
      timestamp: new Date()
    })
    
    // Save welcome message to database
    await saveMessageToDatabase(
      welcomeMessage,
      'avatar',
      `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    )
    
    // Generate video for welcome message
    console.log('Generating video for welcome message...')
    disableUserInput()
    await generateAvatarVideo(welcomeMessage)
    
    // Wait for video completion
    console.log('Waiting for welcome video to complete...')
    await waitForVideoCompletion()
    
    // Get first question
    console.log('Welcome video completed, getting first question...')
    await getNextQuestion()
    
    console.log('Interview started successfully')
  } catch (error) {
    console.error('Failed to start interview')
    console.error('Error starting interview:', error)
  }
}

const getNextQuestion = async (): Promise<void> => {
  try {
    if (!sessionId.value) return
    
    const response = await fetch(`/api/v1/llm-interview/generate-question`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        session_id: sessionId.value,
        vacancy_id: linkedResume.value?.vacancy_id || 'SWE_BACK_001',
        scenario_node_id: currentQuestion.value?.node_id || null,
        previous_answers: chatMessages.value
          .filter(msg => msg.type === 'user')
          .map(msg => msg.text)
      })
    })
    
    if (response.ok) {
      const result = await response.json()
      const questionData = result.question_data
      
      currentQuestion.value = {
        ...questionData,
        is_contextual: result.is_contextual || false,
        contextual_question_id: questionData.contextual_question_id || null
      }
      
      // Add question to chat
      addMessage({
        id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        type: 'avatar',
        text: questionData.question_text,
        timestamp: new Date(),
        is_contextual: result.is_contextual || false
      })
      
      // Save question to database
      await saveMessageToDatabase(
        questionData.question_text,
        'avatar',
        `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
      )
      
      // Generate video for question
      console.log('Generating video for question:', questionData.question_text.substring(0, 50) + '...')
      disableUserInput()
      await generateAvatarVideo(questionData.question_text)
      
      // Wait for video completion
      console.log('Waiting for question video to complete...')
      await waitForVideoCompletion()
      
      // Enable user input
      console.log('Question video completed, user can now answer')
      enableUserInput()
    }
  } catch (error) {
    console.error('Error getting next question:', error)
  }
}

const endInterview = async (): Promise<void> => {
  try {
    // Update session status to completed
    if (sessionId.value) {
      await fetch(`/api/v1/sessions/${sessionId.value}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          status: 'completed',
          finished_at: new Date().toISOString()
        })
      })
    }
    
    interviewStarted.value = false
    
    addMessage({
      id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      type: 'avatar',
      text: 'Thank you for participating in the interview. Your responses have been recorded and will be evaluated. Good luck!',
      timestamp: new Date()
    })
    
    // Save end message to database
    await saveMessageToDatabase(
      'Thank you for participating in the interview. Your responses have been recorded and will be evaluated. Good luck!',
      'avatar',
      `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    )
    
    console.log('Interview completed successfully')
  } catch (error) {
    console.error('Failed to end interview')
    console.error('Error ending interview:', error)
  }
}

const initializeVAD = async (stream: MediaStream): Promise<void> => {
  try {
    audioContext = new AudioContext()
    analyser = audioContext.createAnalyser()
    microphone = audioContext.createMediaStreamSource(stream)
    
    analyser.fftSize = 256
    microphone.connect(analyser)
  } catch (error) {
    console.error('Failed to initialize VAD:', error)
  }
}

const startVADMonitoring = (): void => {
  if (!analyser) return
  
  vadInterval = setInterval(() => {
    const bufferLength = analyser!.frequencyBinCount
    const dataArray = new Uint8Array(bufferLength)
    analyser!.getByteFrequencyData(dataArray)
    
    const average = dataArray.reduce((a, b) => a + b) / bufferLength
    const volume = average / 255
    
    if (volume > VAD_VOLUME_THRESHOLD) {
      silenceStart = null
    } else if (silenceStart === null) {
      silenceStart = Date.now()
    } else if (Date.now() - silenceStart > VAD_SILENCE_THRESHOLD) {
      console.log('VAD: Silence detected, stopping recording')
      stopRecording()
    }
  }, VAD_DEBOUNCE_TIME)
}

const stopVADMonitoring = (): void => {
  if (vadInterval) {
    clearInterval(vadInterval)
    vadInterval = null
  }
  
  if (audioContext) {
    audioContext.close()
    audioContext = null
  }
  
  analyser = null
  microphone = null
}

const startRecording = async (): Promise<void> => {
  try {
    // Check that interview has started and has session ID
    if (!sessionId.value) {
      console.warn('Interview must be started first')
      return
    }
    
    // Check MediaDevices API availability
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      throw new Error('MediaDevices API not supported in this browser')
    }
    
    const constraints = {
      audio: {
        deviceId: selectedMicrophone.value ? { exact: selectedMicrophone.value } : undefined
      }
    }
    console.log('Starting recording with microphone:', selectedMicrophone.value)
    const stream = await navigator.mediaDevices.getUserMedia(constraints)
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []
    
    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data)
    }
    
    mediaRecorder.onstop = async () => {
      // Use the actual MIME type from MediaRecorder
      const mimeType = mediaRecorder!.mimeType || 'audio/webm'
      const audioBlob = new Blob(audioChunks, { type: mimeType })
      console.log('VAD: Audio recorded, MIME type:', mimeType, 'Size:', audioBlob.size)
      await processAudioMessage(audioBlob)
    }
    
    // Initialize VAD
    await initializeVAD(stream)
    
    mediaRecorder.start()
    isRecording.value = true
    recordingDuration.value = 0
    recordingProgress.value = 0
    silenceStart = null
    
    // Start timer
    recordingInterval = setInterval(() => {
      recordingDuration.value++
      recordingProgress.value = Math.min((recordingDuration.value / 60) * 100, 100)
      
      if (recordingDuration.value >= 60) {
        stopRecording()
      }
    }, 1000)
    
    // Start VAD monitoring
    startVADMonitoring()
    
  } catch (error) {
    console.error('Failed to start recording')
    console.error('Error starting recording:', error)
  }
}

const stopRecording = (): void => {
  if (mediaRecorder && isRecording.value) {
    mediaRecorder.stop()
    mediaRecorder.stream.getTracks().forEach(track => track.stop())
    isRecording.value = false
    
    if (recordingInterval) {
      clearInterval(recordingInterval)
      recordingInterval = null
    }
    
    // Clean up VAD
    stopVADMonitoring()
  }
}

const processAudioMessage = async (audioBlob: Blob): Promise<void> => {
  try {
    // Add user message placeholder
    const messageId = `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    addMessage({
      id: messageId,
      type: 'user',
      text: '🎤 [Processing voice message...]',
      timestamp: new Date()
    })
    
    // Generate filename
    const fileName = `recording_${Date.now()}.${audioBlob.type.split('/')[1] || 'webm'}`
    
    console.log('MinIO: Starting audio upload, file:', fileName, 'size:', audioBlob.size)
    
    // Upload audio to MinIO and get transcription in one step
    const formData = new FormData()
    formData.append('audio', audioBlob, fileName)
    formData.append('session_id', sessionId.value!)
    
    const sttResponse = await fetch('/api/v1/stt/transcribe-file', {
      method: 'POST',
      body: formData
    })
    
    console.log('VAD: STT response status:', sttResponse.status)
    
    if (!sttResponse.ok) {
      const errorText = await sttResponse.text()
      console.error('VAD: STT service failed:', errorText)
      throw new Error(`STT service failed: ${sttResponse.status} - ${errorText}`)
    }
    
    const sttResult = await sttResponse.json()
    console.log('VAD: STT result:', sttResult)
    const transcribedText = sttResult.text || "Could not transcribe audio"
    
    // Update the message with transcribed text
    const lastMessage = chatMessages.value[chatMessages.value.length - 1]
    lastMessage.text = transcribedText
    
    // Save to database via orchestrator with audio URL
    const audioUrl = sttResult.audio_url || null
    const transcriptionConfidence = sttResult.confidence || null
    await saveMessageToDatabase(transcribedText, 'user', messageId, audioUrl, transcriptionConfidence)
    
    // Analyze answer and save to QA table if we have current question
    if (currentQuestion.value?.question_text) {
      await analyzeAndSaveAnswer(
        currentQuestion.value.question_text,
        transcribedText,
        audioUrl,
        currentQuestion.value.question_id || 'unknown'
      )
    }
    
    // Get avatar response
    await getAvatarResponse(transcribedText)
    
    // If this was a contextual question, mark it as used
    if (currentQuestion.value?.is_contextual && currentQuestion.value?.contextual_question_id) {
      await markContextualQuestionAsUsed(currentQuestion.value.contextual_question_id)
    }
    
    // Get next question after a short delay
    setTimeout(async () => {
      await getNextQuestion()
    }, 2000)
    
  } catch (error) {
    console.error('Failed to process audio message')
    console.error('Error processing audio message:', error)
    
    // Update message with error
    const lastMessage = chatMessages.value[chatMessages.value.length - 1]
    lastMessage.text = '❌ Failed to process voice message'
  }
}

const analyzeAndSaveAnswer = async (
  questionText: string, 
  answerText: string, 
  audioUrl: string | null, 
  questionId: string
): Promise<void> => {
  try {
    console.log('Analyzing and saving answer:', { questionText, answerText, audioUrl, questionId })
    
    const response = await fetch('/api/v1/llm-interview/analyze-answer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        question_text: questionText,
        answer_text: answerText,
        session_id: sessionId.value,
        audio_url: audioUrl,
        question_id: questionId,
        vacancy_requirements: linkedResume.value?.vacancy_requirements || ''
      })
    })
    
    if (response.ok) {
      const result = await response.json()
      console.log('Answer analysis result:', result)
      
      if (result.qa_record) {
        console.log('QA record saved:', result.qa_record)
      }
    } else {
      console.error('Failed to analyze answer:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('Error analyzing and saving answer:', error)
  }
}

const getAvatarResponse = async (userMessage: string): Promise<void> => {
  try {
    // Check if session ID is available
    if (!sessionId.value) {
      console.error('No session ID available, cannot get avatar response')
      addMessage({
        id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        type: 'avatar',
        text: 'Sorry, an error occurred. Please try again.',
        timestamp: new Date()
      })
      return
    }

    // Step 1: Get LLM response
    const llmResponse = await fetch(`/api/v1/llm/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        session_id: sessionId.value,
        message: userMessage
      })
    })
    
    if (llmResponse.ok) {
      const llmResult = await llmResponse.json()
      const avatarText = llmResult.response
      
      // Add response to chat
      addMessage({
        id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        type: 'avatar',
        text: avatarText,
        timestamp: new Date()
      })
      
      // Generate video for response
      console.log('Generating video for LLM response:', avatarText.substring(0, 50) + '...')
      disableUserInput()
      await generateAvatarVideo(avatarText)
      
      // Wait for video completion
      console.log('Waiting for response video to complete...')
      await waitForVideoCompletion()
      
      // Get next question
      console.log('Response video completed, getting next question...')
      await getNextQuestion()
      
    } else {
      // Fallback response
      addMessage({
        id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        type: 'avatar',
        text: 'Thank you for your answer. Can you tell me more about that?',
        timestamp: new Date()
      })
    }
  } catch (error) {
    console.error('Failed to get avatar response')
    console.error('Error getting avatar response:', error)
  }
}

// Placeholder methods for missing functionality
const saveMessageToDatabase = async (
  text: string, 
  type: 'user' | 'avatar', 
  messageId: string, 
  audioUrl?: string, 
  confidence?: number
): Promise<void> => {
  try {
    const response = await fetch('/api/v1/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId.value,
        message_id: messageId,
        text,
        type,
        audio_url: audioUrl,
        confidence,
        timestamp: new Date().toISOString()
      })
    })
    
    if (!response.ok) {
      console.error('Failed to save message to database')
    }
  } catch (error) {
    console.error('Error saving message:', error)
  }
}

const generateAvatarVideo = async (text: string): Promise<string | null> => {
  try {
    console.log('Generating avatar video for text:', text.substring(0, 50) + '...')
    
    const response = await fetch('/api/v1/llm-interview/avatar-speak', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId.value,
        text: text,
        avatar_id: '68af59a86eeedd0042ca7e27',
        voice_id: '66d3f6a704d077b1432fb7d3'
      })
    })
    
    if (response.ok) {
      const result = await response.json()
      if (result.success && result.mode === 'fallback_video') {
        console.log('Fallback video generated:', result.video_url)
        avatarPlayerRef.value?.setVideoUrl(result.video_url)
        return result.video_url
      }
    }
  } catch (error) {
    console.warn('Avatar video generation failed:', error)
  }
  return null
}

const enableUserInput = (): void => {
  isVideoPlaying.value = false
  isWaitingForVideo.value = false
  console.log('User input enabled')
}

const disableUserInput = (): void => {
  isVideoPlaying.value = true
  isWaitingForVideo.value = true
  console.log('User input disabled')
}

const waitForVideoCompletion = (): Promise<void> => {
  return new Promise((resolve) => {
    if (!avatarPlayerRef.value) {
      console.log('No avatar player ref, resolving immediately')
      resolve()
      return
    }
    
    console.log('Waiting for video completion...')
    
    const onVideoEnd = () => {
      console.log('Video ended, resolving promise')
      resolve()
      const videoElement = avatarPlayerRef.value?.$el?.querySelector('video')
      if (videoElement) {
        videoElement.removeEventListener('ended', onVideoEnd)
      }
    }
    
    const videoElement = avatarPlayerRef.value?.$el?.querySelector('video')
    if (videoElement) {
      videoElement.addEventListener('ended', onVideoEnd)
      console.log('Video end listener added')
    } else {
      console.log('Video element not found, resolving in 5 seconds')
    }
    
    setTimeout(() => {
      console.log('Video completion timeout, resolving')
      resolve()
    }, 5000)
  })
}

const markContextualQuestionAsUsed = async (questionId: string): Promise<void> => {
  try {
    await fetch(`/api/v1/contextual-questions/${questionId}/mark-used`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    })
  } catch (error) {
    console.error('Failed to mark contextual question as used:', error)
  }
}

const getHeaderSubtitle = (): string => {
  if (!interviewStarted.value) {
    return 'Введите код интервью для начала сессии'
  }
  
  if (linkedResume.value) {
    return `Интервью с кандидатом • ${linkedResume.value.original_filename}`
  }
  
  if (sessionData.value) {
    return `Сессия ${sessionData.value.id} • ${getStatusLabel(sessionData.value.status)}`
  }
  
  return 'Проведение AI интервью с кандидатом'
}

const exportTranscript = (): void => {
  try {
    const transcript = chatMessages.value.map(message => {
      const speaker = message.type === 'avatar' ? 'AI Интервьюер' : 'Кандидат'
      const time = formatTime(message.timestamp)
      const contextualTag = message.is_contextual ? ' [Контекстный вопрос]' : ''
      return `[${time}] ${speaker}${contextualTag}: ${message.text}`
    }).join('\n\n')
    
    const header = `Транскрипция интервью\n`
    const sessionInfo = sessionData.value ? `Сессия: ${sessionData.value.id}\n` : ''
    const resumeInfo = linkedResume.value ? `Резюме: ${linkedResume.value.original_filename}\n` : ''
    const dateInfo = `Дата: ${new Date().toLocaleString('ru-RU')}\n`
    const separator = `${'='.repeat(50)}\n\n`
    
    const fullTranscript = header + sessionInfo + resumeInfo + dateInfo + separator + transcript
    
    const blob = new Blob([fullTranscript], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `interview-transcript-${sessionId.value || 'session'}-${new Date().toISOString().split('T')[0]}.txt`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
    
    console.log('Transcript exported successfully')
  } catch (error) {
    console.error('Failed to export transcript:', error)
  }
}

const getStatusVariant = (status: SessionStatus): 'primary' | 'secondary' | 'success' | 'warning' | 'danger' => {
  const variants: Record<SessionStatus, 'primary' | 'secondary' | 'success' | 'warning' | 'danger'> = {
    created: 'secondary',
    in_progress: 'warning',
    completed: 'success',
    failed: 'danger',
    cancelled: 'secondary'
  }
  return variants[status] || 'secondary'
}

const getStatusLabel = (status: SessionStatus): string => {
  const labels: Record<SessionStatus, string> = {
    created: 'Created',
    in_progress: 'In Progress',
    completed: 'Completed',
    failed: 'Failed',
    cancelled: 'Cancelled'
  }
  return labels[status] || status
}

const formatTime = (timestamp: Date): string => {
  return new Date(timestamp).toLocaleTimeString()
}

const addMessage = (message: ChatMessage): void => {
  chatMessages.value.push(message)
  scrollToBottom()
}

const scrollToBottom = async (): Promise<void> => {
  // Use setTimeout to ensure DOM updates are complete
  await new Promise(resolve => setTimeout(resolve, 100))
  if (chatContainer.value) {
    chatContainer.value.scrollTo({
      top: chatContainer.value.scrollHeight,
      behavior: 'smooth'
    })
  }
}

// Event handlers
const handleAvatarConnected = (): void => {
  isConnected.value = true
  console.log('Avatar connected')
}

const handleAvatarDisconnected = (): void => {
  isConnected.value = false
  console.log('Avatar disconnected')
}

const handleAvatarQuestion = (): void => {
  console.log('Avatar question event')
}

const handleAvatarSpeak = (): void => {
  console.log('Avatar speak event')
}

// Microphone management
const requestMicrophonePermission = async (): Promise<void> => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    stream.getTracks().forEach(track => track.stop()) // Stop the stream immediately
    await loadAvailableMicrophones()
  } catch (error) {
    console.error('Failed to request microphone permission:', error)
    // Show user-friendly error message
  }
}

const loadAvailableMicrophones = async (): Promise<void> => {
  try {
    const devices = await navigator.mediaDevices.enumerateDevices()
    availableMicrophones.value = devices
      .filter(device => device.kind === 'audioinput')
      .map(device => ({
        deviceId: device.deviceId,
        label: device.label || `Microphone ${device.deviceId.slice(0, 8)}`
      }))
    
    if (availableMicrophones.value.length > 0 && !selectedMicrophone.value) {
      selectedMicrophone.value = availableMicrophones.value[0].deviceId
    }
  } catch (error) {
    console.error('Failed to load microphones:', error)
  }
}

// Initialize microphones on mount
onMounted(async () => {
  await loadAvailableMicrophones()
  
  // Load session data if session ID is provided in route
  const routeSessionId = route.params.sessionId as string
  if (routeSessionId) {
    sessionId.value = routeSessionId
    await loadSessionData()
  }
})

// Watch for microphone permission changes
watch(() => navigator.mediaDevices, async () => {
  await loadAvailableMicrophones()
}, { deep: true })

// Cleanup on unmount
const cleanup = (): void => {
  if (recordingInterval) {
    clearInterval(recordingInterval)
  }
  if (vadInterval) {
    clearInterval(vadInterval)
  }
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop()
  }
  if (audioContext) {
    audioContext.close()
  }
}

onBeforeUnmount(cleanup)
</script>



<style scoped>
/* Candidate Interview Styles */
.candidate-interview {
  min-height: 100vh;
}

/* Panel Content */
.panel-content {
  padding: 2rem 0;
}

/* Aspect ratio for video container */
.aspect-video {
  aspect-ratio: 16 / 9;
}

/* Custom styles for better visual hierarchy */
.candidate-interview h1,
.candidate-interview h2 {
  font-weight: 700;
  letter-spacing: -0.025em;
}

/* Transcript message styles */
.candidate-interview .transcript-message {
  position: relative;
}

.candidate-interview .transcript-message:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 16px;
  top: 40px;
  bottom: -16px;
  width: 2px;
  background: linear-gradient(to bottom, rgba(59, 130, 246, 0.3), transparent);
  border-radius: 1px;
}

/* Improved message bubble styles */
.candidate-interview .message-bubble {
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
}

/* Smooth animations for transcript */
.transcript-message {
  animation: fadeInUp 0.4s ease-out;
  animation-fill-mode: both;
}

.transcript-message:nth-child(even) {
  animation-delay: 0.1s;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(15px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Hover effects for transcript messages */
.transcript-message:hover {
  transform: translateX(2px);
  transition: transform 0.2s ease-out;
}

/* Enhanced visual feedback */
.transcript-message .bg-white:hover,
.transcript-message .bg-success-50:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s ease-out;
}

/* Enhanced scrollbar for transcript */
.candidate-interview .overflow-y-auto::-webkit-scrollbar {
  width: 8px;
}

.candidate-interview .overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(229, 231, 235, 0.5);
  border-radius: 4px;
}

.candidate-interview .overflow-y-auto::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, rgba(59, 130, 246, 0.6), rgba(59, 130, 246, 0.4));
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.candidate-interview .overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to bottom, rgba(59, 130, 246, 0.8), rgba(59, 130, 246, 0.6));
}

/* Loading state animations */
.candidate-interview .loading-dots::after {
  content: '';
  animation: dots 1.5s steps(5, end) infinite;
}

@keyframes dots {
  0%, 20% {
    color: rgba(0,0,0,0);
    text-shadow:
      .25em 0 0 rgba(0,0,0,0),
      .5em 0 0 rgba(0,0,0,0);
  }
  40% {
    color: currentColor;
    text-shadow:
      .25em 0 0 rgba(0,0,0,0),
      .5em 0 0 rgba(0,0,0,0);
  }
  60% {
    text-shadow:
      .25em 0 0 currentColor,
      .5em 0 0 rgba(0,0,0,0);
  }
  80%, 100% {
    text-shadow:
      .25em 0 0 currentColor,
      .5em 0 0 currentColor;
  }
}
</style>