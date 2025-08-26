import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const useHRStore = defineStore('hr', {
  state: () => ({
    sessions: [],
    vacancies: [],
    statistics: {},
    loading: false,
    error: null
  }),

  getters: {
    completedSessions: (state) => state.sessions.filter(s => s.status === 'completed'),
    inProgressSessions: (state) => state.sessions.filter(s => s.status === 'in_progress'),
    totalSessions: (state) => state.sessions.length
  },

  actions: {
    async fetchSessions(params = {}) {
      try {
        this.loading = true
        this.error = null
        
        const response = await axios.get(`${API_BASE_URL}/api/v1/hr/sessions`, {
          params: {
            skip: params.skip || 0,
            limit: params.limit || 25,
            status: params.status,
            vacancy_id: params.vacancy_id
          }
        })
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch sessions'
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchSessionDetail(sessionId) {
      try {
        this.loading = true
        this.error = null
        
        const response = await axios.get(`${API_BASE_URL}/api/v1/hr/sessions/${sessionId}`)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch session detail'
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchSessionResults(sessionId) {
      try {
        this.loading = true
        this.error = null
        
        const response = await axios.get(`${API_BASE_URL}/api/v1/sessions/${sessionId}/results`)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch session results'
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchVacancies() {
      try {
        this.loading = true
        this.error = null
        
        const response = await axios.get(`${API_BASE_URL}/api/v1/hr/vacancies`)
        this.vacancies = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch vacancies'
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchStatistics() {
      try {
        this.loading = true
        this.error = null
        
        // Mock statistics for now - in real app this would come from API
        const stats = {
          total_sessions: this.sessions.length,
          completed_sessions: this.completedSessions.length,
          in_progress_sessions: this.inProgressSessions.length,
          avg_score: 0.75,
          sessions_change: '+5%',
          completed_change: '+2%',
          progress_change: '+3%',
          score_change: '+1.2%'
        }
        
        this.statistics = stats
        return stats
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch statistics'
        throw error
      } finally {
        this.loading = false
      }
    },

    async reviewSession(sessionId, reviewData) {
      try {
        this.loading = true
        this.error = null
        
        const response = await axios.post(`${API_BASE_URL}/api/v1/hr/sessions/${sessionId}/review`, reviewData)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to review session'
        throw error
      } finally {
        this.loading = false
      }
    },

    async reviewAnswer(qaId, reviewData) {
      try {
        this.loading = true
        this.error = null
        
        const response = await axios.post(`${API_BASE_URL}/api/v1/hr/qa/${qaId}/review`, reviewData)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to review answer'
        throw error
      } finally {
        this.loading = false
      }
    },

    async exportSession(sessionId, format = 'json') {
      try {
        this.loading = true
        this.error = null
        
        const response = await axios.get(`${API_BASE_URL}/api/v1/hr/sessions/${sessionId}/export`, {
          params: { format }
        })
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to export session'
        throw error
      } finally {
        this.loading = false
      }
    },

    async exportVacancy(vacancyId, format = 'json') {
      try {
        this.loading = true
        this.error = null
        
        const response = await axios.get(`${API_BASE_URL}/api/v1/hr/vacancies/${vacancyId}/export`, {
          params: { format }
        })
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to export vacancy'
        throw error
      } finally {
        this.loading = false
      }
    },

    async exportAllSessions(format = 'json') {
      try {
        this.loading = true
        this.error = null
        
        // For now, export the first vacancy - in real app this would be a bulk export
        if (this.vacancies.length > 0) {
          return await this.exportVacancy(this.vacancies[0].id, format)
        } else {
          throw new Error('No vacancies available for export')
        }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to export all sessions'
        throw error
      } finally {
        this.loading = false
      }
    },

    clearError() {
      this.error = null
    },

    async refreshData() {
      try {
        await Promise.all([
          this.fetchSessions(),
          this.fetchVacancies(),
          this.fetchStatistics()
        ])
      } catch (error) {
        console.error('Error refreshing data:', error)
        throw error
      }
    }
  }
})
