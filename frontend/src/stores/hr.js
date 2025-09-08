import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || ''

export const useHRStore = defineStore('hr', {
  state: () => ({
    sessions: [],
    vacancies: [],
    statistics: {},
    loading: false,
    error: null
  }),

  getters: {
    completedSessions: state => state.sessions.filter(s => s.status === 'completed'),
    inProgressSessions: state => state.sessions.filter(s => s.status === 'in_progress'),
    totalSessions: state => state.sessions.length
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

        this.sessions = response.data
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

        const response = await axios.get(`${API_BASE_URL}/api/v1/hr/sessions/${sessionId}/results`)
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

        // Используем новый API вакансий
        const response = await axios.get(`${API_BASE_URL}/api/v1/vacancies/`)
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

        // Calculate real statistics from sessions data
        const totalSessions = this.sessions.length
        const completedSessions = this.completedSessions.length
        const inProgressSessions = this.inProgressSessions.length

        // Calculate average score from completed sessions
        let avgScore = 0
        if (completedSessions > 0) {
          const totalScore = this.sessions
            .filter(s => s.status === 'completed' && s.total_score !== null)
            .reduce((sum, s) => sum + (s.total_score || 0), 0)
          avgScore = totalScore / completedSessions
        }

        // Calculate changes (for now, we'll use simple calculations)
        // In a real app, this would compare with previous period data
        const sessionsChange = totalSessions > 0 ? '+100%' : '0%'
        const completedChange = completedSessions > 0 ? '+100%' : '0%'
        const progressChange = inProgressSessions > 0 ? '+100%' : '0%'
        const scoreChange = avgScore > 0 ? `+${(avgScore * 100).toFixed(1)}%` : '0%'

        const stats = {
          total_sessions: totalSessions,
          completed_sessions: completedSessions,
          in_progress_sessions: inProgressSessions,
          avg_score: avgScore,
          sessions_change: sessionsChange,
          completed_change: completedChange,
          progress_change: progressChange,
          score_change: scoreChange
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

        const response = await axios.post(
          `${API_BASE_URL}/api/v1/hr/sessions/${sessionId}/review`,
          reviewData
        )
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

        const response = await axios.get(
          `${API_BASE_URL}/api/v1/hr/vacancies/${vacancyId}/export`,
          {
            params: { format }
          }
        )
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

    async createSession(sessionData) {
      try {
        this.loading = true
        this.error = null

        const response = await axios.post(`${API_BASE_URL}/api/v1/sessions/`, sessionData)

        // Add the new session to local state
        this.sessions.unshift(response.data)

        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to create session'
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteSession(sessionId) {
      try {
        this.loading = true
        this.error = null

        const response = await axios.delete(`${API_BASE_URL}/api/v1/sessions/${sessionId}`)

        // Remove the session from local state
        this.sessions = this.sessions.filter(s => s.id !== sessionId)

        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to delete session'
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
        await Promise.all([this.fetchSessions(), this.fetchVacancies(), this.fetchStatistics()])
      } catch (error) {
        console.error('Error refreshing data:', error)
        throw error
      }
    },

    // Keywords management methods
    async extractSectionKeywords(vacancyId, sectionType, forceReload = false) {
      try {
        this.loading = true
        this.error = null

        const response = await axios.post(
          `${API_BASE_URL}/api/v1/vacancy-keywords/vacancies/${vacancyId}/keywords/extract/${sectionType}`,
          { force_reload: forceReload }
        )

        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to extract keywords'
        throw error
      } finally {
        this.loading = false
      }
    },

    async extractAllKeywords(vacancyId, forceReload = false) {
      try {
        this.loading = true
        this.error = null

        const response = await axios.post(
          `${API_BASE_URL}/api/v1/vacancy-keywords/vacancies/${vacancyId}/keywords/extract-all`,
          { force_reload: forceReload }
        )

        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to extract all keywords'
        throw error
      } finally {
        this.loading = false
      }
    },

    async getSectionKeywords(vacancyId, sectionType) {
      try {
        this.loading = true
        this.error = null

        const response = await axios.get(
          `${API_BASE_URL}/api/v1/vacancy-keywords/vacancies/${vacancyId}/keywords/${sectionType}`
        )

        return response.data
      } catch (error) {
        if (error.response?.status === 404) {
          return null // Keywords not found
        }
        this.error = error.response?.data?.detail || 'Failed to get keywords'
        throw error
      } finally {
        this.loading = false
      }
    },

    async getAllKeywords(vacancyId) {
      try {
        this.loading = true
        this.error = null

        const response = await axios.get(
          `${API_BASE_URL}/api/v1/vacancy-keywords/vacancies/${vacancyId}/keywords`
        )

        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to get all keywords'
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateSectionKeywords(vacancyId, sectionType, keywords, confidenceScore = null) {
      try {
        this.loading = true
        this.error = null

        const updateData = { keywords }
        if (confidenceScore !== null) {
          updateData.confidence_score = confidenceScore
        }

        const response = await axios.put(
          `${API_BASE_URL}/api/v1/vacancy-keywords/vacancies/${vacancyId}/keywords/${sectionType}`,
          updateData
        )

        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to update keywords'
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteSectionKeywords(vacancyId, sectionType) {
      try {
        this.loading = true
        this.error = null

        const response = await axios.delete(
          `${API_BASE_URL}/api/v1/vacancy-keywords/vacancies/${vacancyId}/keywords/${sectionType}`
        )

        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to delete keywords'
        throw error
      } finally {
        this.loading = false
      }
    },

    async getKeywordsStats(vacancyId) {
      try {
        this.loading = true
        this.error = null

        const response = await axios.get(
          `${API_BASE_URL}/api/v1/vacancy-keywords/vacancies/${vacancyId}/keywords-stats`
        )

        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to get keywords stats'
        throw error
      } finally {
        this.loading = false
      }
    },

    async clearKeywordsCache(vacancyId) {
      try {
        this.loading = true
        this.error = null

        const response = await axios.delete(
          `${API_BASE_URL}/api/v1/vacancy-keywords/vacancies/${vacancyId}/keywords-cache`
        )

        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to clear keywords cache'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Scenario management methods
    async generateScenario(vacancyId, scenarioData) {
      try {
        this.loading = true
        this.error = null

        const response = await axios.post(`${API_BASE_URL}/api/v1/scenarios/generate`, {
          vacancy_id: vacancyId,
          scenario_name: scenarioData.scenario_name,
          description: scenarioData.description,
          force_regenerate: scenarioData.force_regenerate || false
        })

        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to generate scenario'
        throw error
      } finally {
        this.loading = false
      }
    },

    async previewScenario(vacancyId, scenarioData) {
      try {
        this.loading = true
        this.error = null

        const response = await axios.post(`${API_BASE_URL}/api/v1/scenarios/preview`, {
          vacancy_id: vacancyId,
          scenario_name: scenarioData.scenario_name,
          description: scenarioData.description
        })

        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to preview scenario'
        throw error
      } finally {
        this.loading = false
      }
    },

    async getVacancyScenarios(vacancyId) {
      try {
        this.loading = true
        this.error = null

        const response = await axios.get(
          `${API_BASE_URL}/api/v1/scenarios/vacancies/${vacancyId}/scenarios`
        )

        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch scenarios'
        throw error
      } finally {
        this.loading = false
      }
    },

    async getVacancyDynamicCriteria(vacancyId) {
      try {
        this.loading = true
        this.error = null

        const response = await axios.get(
          `${API_BASE_URL}/api/v1/scenarios/vacancies/${vacancyId}/dynamic-criteria`
        )

        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch dynamic criteria'
        throw error
      } finally {
        this.loading = false
      }
    },

    async regenerateScenario(scenarioId) {
      try {
        this.loading = true
        this.error = null

        const response = await axios.post(
          `${API_BASE_URL}/api/v1/scenarios/${scenarioId}/regenerate`
        )

        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to regenerate scenario'
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteScenario(scenarioId) {
      try {
        this.loading = true
        this.error = null

        const response = await axios.delete(`${API_BASE_URL}/api/v1/scenarios/${scenarioId}`)

        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to delete scenario'
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
