import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || ''

export const useAvatarSettingsStore = defineStore('avatarSettings', {
  state: () => ({
    // Основные настройки
    selectedVoice: '66d3f6a704d077b1432fb7d3', // Nadia (по умолчанию)
    selectedAvatar: '68af59a86eeedd0042ca7e27', // Default Avatar (по умолчанию)
    
    // Настройки генерации видео
    resolution: 720,  // 1:1 format (720x720)
    speechRate: 1.5, // Обновлено на 1.5x
    isSkipRs: true, // Обновлено на быстро (стандартное качество)
    isCaptionEnabled: false,
    captionLanguage: 'ru-RU',
    
    // Настройки фона
    backgroundId: null,
    backgroundColor: 'rgb(55, 24, 212)', // Обновлено на темно-синий
    customDimensions: { width: 1920, height: 1080 },
    
    // Доступные опции (загружаются с A2E API)
    availableVoices: [],
    availableAvatars: [],
    availableBackgrounds: [],
    
    // Состояние загрузки
    loading: {
      voices: false,
      avatars: false,
      backgrounds: false,
      testGeneration: false
    },
    
    // Ошибки
    error: null,
    
    // Тестовые данные
    testVideoUrl: null,
    testVideoStatus: null
  }),

  getters: {
    // Получить выбранный голос
    currentVoice: (state) => {
      return state.availableVoices.find(v => v.id === state.selectedVoice) || null
    },
    
    // Получить выбранный аватар
    currentAvatar: (state) => {
      return state.availableAvatars.find(a => a.id === state.selectedAvatar) || null
    },
    
    // Получить выбранный фон
    currentBackground: (state) => {
      return state.availableBackgrounds.find(b => b.id === state.backgroundId) || null
    },
    
    // Проверить, загружены ли все данные
    isDataLoaded: (state) => {
      return state.availableVoices.length > 0 && 
             state.availableAvatars.length > 0 && 
             state.availableBackgrounds.length > 0
    }
  },

  actions: {
    // Загрузить доступные голоса
    async fetchAvailableVoices() {
      try {
        this.loading.voices = true
        this.error = null
        
        const response = await axios.get(`${API_BASE_URL}/api/v1/avatar/voices`)
        this.availableVoices = response.data.voices || []
        
        console.log('Available voices loaded:', this.availableVoices)
        return this.availableVoices
      } catch (error) {
        this.error = `Failed to fetch voices: ${error.response?.data?.detail || error.message}`
        console.error('Error fetching voices:', error)
        throw error
      } finally {
        this.loading.voices = false
      }
    },

    // Загрузить доступные аватары
    async fetchAvailableAvatars() {
      try {
        this.loading.avatars = true
        this.error = null
        
        const response = await axios.get(`${API_BASE_URL}/api/v1/avatar/characters`)
        this.availableAvatars = response.data.characters || []
        
        console.log('Available avatars loaded:', this.availableAvatars)
        return this.availableAvatars
      } catch (error) {
        this.error = `Failed to fetch avatars: ${error.response?.data?.detail || error.message}`
        console.error('Error fetching avatars:', error)
        throw error
      } finally {
        this.loading.avatars = false
      }
    },

    // Загрузить доступные фоны
    async fetchAvailableBackgrounds() {
      try {
        this.loading.backgrounds = true
        this.error = null
        
        // Пока используем заглушку, так как A2E API для фонов может не быть
        this.availableBackgrounds = [
          { id: 'default', name: 'По умолчанию', url: null, color: '#f5f5f5' },
          { id: 'professional', name: 'Профессиональный', url: null, color: '#ffffff' },
          { id: 'modern', name: 'Современный', url: null, color: '#f8f9fa' }
        ]
        
        console.log('Available backgrounds loaded:', this.availableBackgrounds)
        return this.availableBackgrounds
      } catch (error) {
        this.error = `Failed to fetch backgrounds: ${error.response?.data?.detail || error.message}`
        console.error('Error fetching backgrounds:', error)
        throw error
      } finally {
        this.loading.backgrounds = false
      }
    },

    // Загрузить все доступные опции
    async fetchAllOptions() {
      try {
        await Promise.all([
          this.fetchAvailableVoices(),
          this.fetchAvailableAvatars(),
          this.fetchAvailableBackgrounds()
        ])
      } catch (error) {
        console.error('Error fetching all options:', error)
        throw error
      }
    },

    // Тест генерации видео с текущими настройками
    async testVideoGeneration() {
      try {
        this.loading.testGeneration = true
        this.error = null
        this.testVideoUrl = null
        this.testVideoStatus = null
        
        const testText = 'Добро пожаловать на интервью!'
        
        console.log('Testing video generation with settings:', {
          voice: this.selectedVoice,
          avatar: this.selectedAvatar,
          resolution: this.resolution,
          speechRate: this.speechRate,
          isSkipRs: this.isSkipRs,
          text: testText
        })
        
        const response = await axios.post(`${API_BASE_URL}/api/v1/avatar/fallback/generate-video`, {
          text: testText,
          session_id: 'test-session',
          voice_id: this.selectedVoice,
          avatar_id: this.selectedAvatar,
          resolution: this.resolution
        })
        
        if (response.data.success && response.data.video_url) {
          this.testVideoUrl = response.data.video_url
          this.testVideoStatus = 'success'
          console.log('Test video generated successfully:', this.testVideoUrl)
        } else {
          throw new Error('Video generation failed')
        }
        
        return response.data
      } catch (error) {
        this.error = `Test generation failed: ${error.response?.data?.detail || error.message}`
        this.testVideoStatus = 'error'
        console.error('Error in test generation:', error)
        throw error
      } finally {
        this.loading.testGeneration = false
      }
    },

    // Обновить настройки
    updateSettings(settings) {
      Object.assign(this, settings)
      console.log('Avatar settings updated:', settings)
    },

    // Сбросить настройки к значениям по умолчанию
    resetToDefaults() {
      this.selectedVoice = '66d3f6a704d077b1432fb7d3'
      this.selectedAvatar = '68af59a86eeedd0042ca7e27'
      this.resolution = 720  // 1:1 format (720x720)
      this.speechRate = 1.5
      this.isSkipRs = true
      this.isCaptionEnabled = false
      this.captionLanguage = 'ru-RU'
      this.backgroundId = null
      this.backgroundColor = 'rgb(55, 24, 212)'
      this.customDimensions = { width: 1920, height: 1080 }
      
      console.log('Avatar settings reset to defaults')
    },

    // Сохранить настройки (пока в localStorage, потом можно в БД)
    saveSettings() {
      try {
        const settings = {
          selectedVoice: this.selectedVoice,
          selectedAvatar: this.selectedAvatar,
          resolution: this.resolution,
          speechRate: this.speechRate,
          isSkipRs: this.isSkipRs,
          isCaptionEnabled: this.isCaptionEnabled,
          captionLanguage: this.captionLanguage,
          backgroundId: this.backgroundId,
          backgroundColor: this.backgroundColor,
          customDimensions: this.customDimensions
        }
        
        localStorage.setItem('avatarSettings', JSON.stringify(settings))
        console.log('Avatar settings saved to localStorage')
        return true
      } catch (error) {
        console.error('Error saving settings:', error)
        return false
      }
    },

    // Загрузить сохраненные настройки
    loadSettings() {
      try {
        const saved = localStorage.getItem('avatarSettings')
        if (saved) {
          const settings = JSON.parse(saved)
          this.updateSettings(settings)
          console.log('Avatar settings loaded from localStorage')
          return true
        }
        return false
      } catch (error) {
        console.error('Error loading settings:', error)
        return false
      }
    }
  }
})
