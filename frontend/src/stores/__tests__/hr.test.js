import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useHRStore } from '../hr'

// Mock axios
const mockAxios = {
  get: vi.fn(),
  post: vi.fn(),
  put: vi.fn(),
  delete: vi.fn()
}

vi.mock('axios', () => ({
  default: mockAxios
}))

// Mock environment variables
vi.mock('import.meta.env', () => ({
      VITE_API_URL: 'http://localhost:8000'
}))

describe('HR Store - Keywords Management', () => {
  let store

  beforeEach(() => {
    setActivePinia(createPinia())
    store = useHRStore()
    vi.clearAllMocks()
  })

  describe('extractSectionKeywords', () => {
    it('successfully extracts keywords for a section', async () => {
      const mockResponse = {
        data: {
          success: true,
          keywords: ['разработка', 'веб-приложения'],
          confidence_score: 0.85
        }
      }
      mockAxios.post.mockResolvedValue(mockResponse)

      const result = await store.extractSectionKeywords('vacancy-123', 'responsibilities', true)

      expect(mockAxios.post).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/vacancy-keywords/vacancies/vacancy-123/keywords/extract/responsibilities',
        { force_reload: true }
      )
      expect(result).toEqual(mockResponse.data)
      expect(store.loading).toBe(false)
      expect(store.error).toBe(null)
    })

    it('handles extraction error', async () => {
      const error = new Error('Network error')
      mockAxios.post.mockRejectedValue(error)

      await expect(store.extractSectionKeywords('vacancy-123', 'responsibilities'))
        .rejects.toThrow('Network error')

      expect(store.error).toBe('Failed to extract keywords')
      expect(store.loading).toBe(false)
    })

    it('handles API error response', async () => {
      const errorResponse = {
        response: {
          data: { detail: 'Invalid section type' }
        }
      }
      mockAxios.post.mockRejectedValue(errorResponse)

      await expect(store.extractSectionKeywords('vacancy-123', 'invalid'))
        .rejects.toEqual(errorResponse)

      expect(store.error).toBe('Invalid section type')
    })
  })

  describe('extractAllKeywords', () => {
    it('successfully extracts keywords for all sections', async () => {
      const mockResponse = {
        data: {
          success: true,
          sections: [
            { section_type: 'responsibilities', keywords: ['разработка'] },
            { section_type: 'requirements', keywords: ['опыт'] }
          ],
          total_extraction_time: 2.5
        }
      }
      mockAxios.post.mockResolvedValue(mockResponse)

      const result = await store.extractAllKeywords('vacancy-123', false)

      expect(mockAxios.post).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/vacancy-keywords/vacancies/vacancy-123/keywords/extract-all',
        { force_reload: false }
      )
      expect(result).toEqual(mockResponse.data)
    })

    it('handles extraction error', async () => {
      mockAxios.post.mockRejectedValue(new Error('Service unavailable'))

      await expect(store.extractAllKeywords('vacancy-123'))
        .rejects.toThrow('Service unavailable')

      expect(store.error).toBe('Failed to extract all keywords')
    })
  })

  describe('getSectionKeywords', () => {
    it('successfully retrieves keywords for a section', async () => {
      const mockResponse = {
        data: {
          id: 'kw-123',
          keywords: ['разработка', 'веб-приложения'],
          confidence_score: 0.85
        }
      }
      mockAxios.get.mockResolvedValue(mockResponse)

      const result = await store.getSectionKeywords('vacancy-123', 'responsibilities')

      expect(mockAxios.get).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/vacancy-keywords/vacancies/vacancy-123/keywords/responsibilities'
      )
      expect(result).toEqual(mockResponse.data)
    })

    it('returns null when keywords not found (404)', async () => {
      const errorResponse = {
        response: { status: 404 }
      }
      mockAxios.get.mockRejectedValue(errorResponse)

      const result = await store.getSectionKeywords('vacancy-123', 'responsibilities')

      expect(result).toBe(null)
      expect(store.error).toBe(null)
    })

    it('handles other errors', async () => {
      mockAxios.get.mockRejectedValue(new Error('Server error'))

      await expect(store.getSectionKeywords('vacancy-123', 'responsibilities'))
        .rejects.toThrow('Server error')

      expect(store.error).toBe('Failed to get keywords')
    })
  })

  describe('getAllKeywords', () => {
    it('successfully retrieves all keywords', async () => {
      const mockResponse = {
        data: {
          vacancy_id: 'vacancy-123',
          sections: [
            { section_type: 'responsibilities', keywords: ['разработка'] },
            { section_type: 'requirements', keywords: ['опыт'] }
          ]
        }
      }
      mockAxios.get.mockResolvedValue(mockResponse)

      const result = await store.getAllKeywords('vacancy-123')

      expect(mockAxios.get).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/vacancy-keywords/vacancies/vacancy-123/keywords'
      )
      expect(result).toEqual(mockResponse.data)
    })

    it('handles retrieval error', async () => {
      mockAxios.get.mockRejectedValue(new Error('Database error'))

      await expect(store.getAllKeywords('vacancy-123'))
        .rejects.toThrow('Database error')

      expect(store.error).toBe('Failed to get all keywords')
    })
  })

  describe('updateSectionKeywords', () => {
    it('successfully updates keywords', async () => {
      const mockResponse = {
        data: {
          success: true,
          updated_keywords: ['разработка', 'веб-приложения', 'новое_слово']
        }
      }
      mockAxios.put.mockResolvedValue(mockResponse)

      const keywords = ['разработка', 'веб-приложения', 'новое_слово']
      const result = await store.updateSectionKeywords('vacancy-123', 'responsibilities', keywords, 0.9)

      expect(mockAxios.put).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/vacancy-keywords/vacancies/vacancy-123/keywords/responsibilities',
        { keywords, confidence_score: 0.9 }
      )
      expect(result).toEqual(mockResponse.data)
    })

    it('updates keywords without confidence score', async () => {
      const mockResponse = { data: { success: true } }
      mockAxios.put.mockResolvedValue(mockResponse)

      const keywords = ['разработка', 'веб-приложения']
      await store.updateSectionKeywords('vacancy-123', 'responsibilities', keywords)

      expect(mockAxios.put).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/vacancy-keywords/vacancies/vacancy-123/keywords/responsibilities',
        { keywords }
      )
    })

    it('handles update error', async () => {
      mockAxios.put.mockRejectedValue(new Error('Validation error'))

      await expect(store.updateSectionKeywords('vacancy-123', 'responsibilities', []))
        .rejects.toThrow('Validation error')

      expect(store.error).toBe('Failed to update keywords')
    })
  })

  describe('deleteSectionKeywords', () => {
    it('successfully deletes keywords', async () => {
      const mockResponse = {
        data: {
          success: true,
          message: 'Keywords deleted successfully'
        }
      }
      mockAxios.delete.mockResolvedValue(mockResponse)

      const result = await store.deleteSectionKeywords('vacancy-123', 'responsibilities')

      expect(mockAxios.delete).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/vacancy-keywords/vacancies/vacancy-123/keywords/responsibilities'
      )
      expect(result).toEqual(mockResponse.data)
    })

    it('handles deletion error', async () => {
      mockAxios.delete.mockRejectedValue(new Error('Permission denied'))

      await expect(store.deleteSectionKeywords('vacancy-123', 'responsibilities'))
        .rejects.toThrow('Permission denied')

      expect(store.error).toBe('Failed to delete keywords')
    })
  })

  describe('getKeywordsStats', () => {
    it('successfully retrieves keywords statistics', async () => {
      const mockResponse = {
        data: {
          total_sections: 7,
          total_keywords: 25,
          average_confidence: 0.78,
          last_extraction_time: 3.2,
          section_stats: [
            { section_type: 'responsibilities', keywords_count: 5, confidence_score: 0.85 }
          ]
        }
      }
      mockAxios.get.mockResolvedValue(mockResponse)

      const result = await store.getKeywordsStats('vacancy-123')

      expect(mockAxios.get).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/vacancy-keywords/vacancies/vacancy-123/keywords-stats'
      )
      expect(result).toEqual(mockResponse.data)
    })

    it('handles stats retrieval error', async () => {
      mockAxios.get.mockRejectedValue(new Error('Analytics service unavailable'))

      await expect(store.getKeywordsStats('vacancy-123'))
        .rejects.toThrow('Analytics service unavailable')

      expect(store.error).toBe('Failed to get keywords stats')
    })
  })

  describe('clearKeywordsCache', () => {
    it('successfully clears keywords cache', async () => {
      const mockResponse = {
        data: {
          success: true,
          message: 'Cache cleared successfully',
          cleared_entries: 15
        }
      }
      mockAxios.delete.mockResolvedValue(mockResponse)

      const result = await store.clearKeywordsCache('vacancy-123')

      expect(mockAxios.delete).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/vacancy-keywords/vacancies/vacancy-123/keywords-cache'
      )
      expect(result).toEqual(mockResponse.data)
    })

    it('handles cache clearing error', async () => {
      mockAxios.delete.mockRejectedValue(new Error('Cache service error'))

      await expect(store.clearKeywordsCache('vacancy-123'))
        .rejects.toThrow('Cache service error')

      expect(store.error).toBe('Failed to clear keywords cache')
    })
  })

  describe('Loading and Error States', () => {
    it('sets loading state during API calls', async () => {
      mockAxios.get.mockImplementation(() => 
        new Promise(resolve => setTimeout(() => resolve({ data: {} }), 100))
      )

      const promise = store.getSectionKeywords('vacancy-123', 'responsibilities')
      
      expect(store.loading).toBe(true)
      
      await promise
      
      expect(store.loading).toBe(false)
    })

    it('clears error state on successful calls', async () => {
      store.error = 'Previous error'
      mockAxios.get.mockResolvedValue({ data: {} })

      await store.getSectionKeywords('vacancy-123', 'responsibilities')

      expect(store.error).toBe(null)
    })

    it('sets error state on failed calls', async () => {
      mockAxios.get.mockRejectedValue(new Error('Test error'))

      try {
        await store.getSectionKeywords('vacancy-123', 'responsibilities')
      } catch (error) {
        // Expected to throw
      }

      expect(store.error).toBe('Failed to get keywords')
    })
  })

  describe('Error Message Handling', () => {
    it('uses API error detail when available', async () => {
      const errorResponse = {
        response: {
          data: { detail: 'Custom API error message' }
        }
      }
      mockAxios.get.mockRejectedValue(errorResponse)

      try {
        await store.getSectionKeywords('vacancy-123', 'responsibilities')
      } catch (error) {
        // Expected to throw
      }

      expect(store.error).toBe('Custom API error message')
    })

    it('uses default error message when no detail available', async () => {
      mockAxios.get.mockRejectedValue(new Error('Network error'))

      try {
        await store.getSectionKeywords('vacancy-123', 'responsibilities')
      } catch (error) {
        // Expected to throw
      }

      expect(store.error).toBe('Failed to get keywords')
    })
  })
})
