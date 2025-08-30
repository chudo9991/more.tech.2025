import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { ElMessage, ElMessageBox } from 'element-plus'
import KeywordsSection from '../KeywordsSection.vue'

// Mock Element Plus components
vi.mock('element-plus', () => ({
  ElMessage: {
    success: vi.fn(),
    error: vi.fn(),
    warning: vi.fn()
  },
  ElMessageBox: {
    confirm: vi.fn()
  }
}))

// Mock HR Store
const mockHRStore = {
  extractSectionKeywords: vi.fn(),
  getSectionKeywords: vi.fn(),
  updateSectionKeywords: vi.fn(),
  deleteSectionKeywords: vi.fn()
}

vi.mock('@/stores/hr', () => ({
  useHRStore: () => mockHRStore
}))

describe('KeywordsSection', () => {
  let wrapper

  const defaultProps = {
    vacancyId: 'test-vacancy-123',
    sectionType: 'responsibilities',
    sectionTitle: 'Обязанности',
    sectionText: 'Разработка веб-приложений, работа с базой данных'
  }

  beforeEach(() => {
    vi.clearAllMocks()
    wrapper = mount(KeywordsSection, {
      props: defaultProps,
      global: {
        stubs: {
          'el-button': true,
          'el-icon': true,
          'el-progress': true,
          'el-tag': true,
          'el-empty': true,
          'el-skeleton': true,
          'KeywordsEditor': true
        }
      }
    })
  })

  describe('Props and Initial State', () => {
    it('renders with correct props', () => {
      expect(wrapper.find('.keywords-title').text()).toBe('Обязанности')
      expect(wrapper.props('vacancyId')).toBe('test-vacancy-123')
      expect(wrapper.props('sectionType')).toBe('responsibilities')
    })

    it('shows extract button when text is available', () => {
      expect(wrapper.find('.keywords-header button').exists()).toBe(true)
    })

    it('disables extract button when no text', async () => {
      await wrapper.setProps({ sectionText: '' })
      const button = wrapper.find('.keywords-header button')
      expect(button.attributes('disabled')).toBeDefined()
    })
  })

  describe('Keywords Display', () => {
    it('shows empty state when no keywords', () => {
      expect(wrapper.find('.keywords-empty').exists()).toBe(true)
    })

    it('shows keywords when available', async () => {
      await wrapper.setData({
        keywords: ['разработка', 'веб-приложения', 'база данных'],
        confidenceScore: 0.85
      })
      
      expect(wrapper.find('.keywords-content').exists()).toBe(true)
      expect(wrapper.find('.confidence-indicator').exists()).toBe(true)
    })

    it('displays confidence score correctly', async () => {
      await wrapper.setData({
        keywords: ['test'],
        confidenceScore: 0.75
      })
      
      const confidenceValue = wrapper.find('.confidence-value')
      expect(confidenceValue.text()).toBe('75%')
    })
  })

  describe('Extract Keywords', () => {
    it('calls extractSectionKeywords when extract button is clicked', async () => {
      mockHRStore.extractSectionKeywords.mockResolvedValue({
        success: true,
        keywords: ['разработка', 'веб-приложения'],
        confidence_score: 0.8
      })

      await wrapper.find('.keywords-header button').trigger('click')

      expect(mockHRStore.extractSectionKeywords).toHaveBeenCalledWith(
        'test-vacancy-123',
        'responsibilities',
        true
      )
    })

    it('shows success message on successful extraction', async () => {
      mockHRStore.extractSectionKeywords.mockResolvedValue({
        success: true,
        keywords: ['разработка', 'веб-приложения'],
        confidence_score: 0.8
      })

      await wrapper.find('.keywords-header button').trigger('click')

      expect(ElMessage.success).toHaveBeenCalledWith('Извлечено 2 ключевых слов')
    })

    it('shows error message on extraction failure', async () => {
      mockHRStore.extractSectionKeywords.mockResolvedValue({
        success: false,
        error: 'Ошибка извлечения'
      })

      await wrapper.find('.keywords-header button').trigger('click')

      expect(ElMessage.error).toHaveBeenCalledWith('Ошибка извлечения')
    })

    it('handles extraction error', async () => {
      mockHRStore.extractSectionKeywords.mockRejectedValue(new Error('Network error'))

      await wrapper.find('.keywords-header button').trigger('click')

      expect(ElMessage.error).toHaveBeenCalledWith('Ошибка при извлечении ключевых слов')
    })
  })

  describe('Keywords Management', () => {
    beforeEach(async () => {
      await wrapper.setData({
        keywords: ['разработка', 'веб-приложения', 'база данных'],
        confidenceScore: 0.85
      })
    })

    it('removes keyword when close button is clicked', async () => {
      const tags = wrapper.findAll('.keyword-tag')
      await tags[0].trigger('close')

      expect(wrapper.vm.keywords).toHaveLength(2)
      expect(wrapper.vm.keywords).not.toContain('разработка')
    })

    it('opens editor when edit button is clicked', async () => {
      await wrapper.find('.keywords-actions button[type="primary"]').trigger('click')
      
      expect(wrapper.vm.editorVisible).toBe(true)
    })

    it('calls re-extract when refresh button is clicked', async () => {
      mockHRStore.extractSectionKeywords.mockResolvedValue({
        success: true,
        keywords: ['новые', 'ключевые', 'слова'],
        confidence_score: 0.9
      })

      await wrapper.find('.keywords-actions button[type="warning"]').trigger('click')

      expect(mockHRStore.extractSectionKeywords).toHaveBeenCalled()
    })
  })

  describe('Clear Keywords', () => {
    beforeEach(async () => {
      await wrapper.setData({
        keywords: ['разработка', 'веб-приложения'],
        confidenceScore: 0.85
      })
    })

    it('shows confirmation dialog when clear button is clicked', async () => {
      ElMessageBox.confirm.mockResolvedValue('confirm')

      await wrapper.find('.keywords-actions button[type="danger"]').trigger('click')

      expect(ElMessageBox.confirm).toHaveBeenCalledWith(
        'Вы уверены, что хотите очистить все ключевые слова?',
        'Подтверждение',
        expect.any(Object)
      )
    })

    it('clears keywords when confirmed', async () => {
      ElMessageBox.confirm.mockResolvedValue('confirm')
      mockHRStore.deleteSectionKeywords.mockResolvedValue({ success: true })

      await wrapper.find('.keywords-actions button[type="danger"]').trigger('click')

      expect(mockHRStore.deleteSectionKeywords).toHaveBeenCalledWith(
        'test-vacancy-123',
        'responsibilities'
      )
      expect(ElMessage.success).toHaveBeenCalledWith('Ключевые слова очищены')
    })

    it('does not clear keywords when cancelled', async () => {
      ElMessageBox.confirm.mockRejectedValue('cancel')

      await wrapper.find('.keywords-actions button[type="danger"]').trigger('click')

      expect(mockHRStore.deleteSectionKeywords).not.toHaveBeenCalled()
      expect(wrapper.vm.keywords).toHaveLength(2)
    })
  })

  describe('Events', () => {
    it('emits keywords-updated when keywords are extracted', async () => {
      mockHRStore.extractSectionKeywords.mockResolvedValue({
        success: true,
        keywords: ['разработка', 'веб-приложения'],
        confidence_score: 0.8
      })

      await wrapper.find('.keywords-header button').trigger('click')

      expect(wrapper.emitted('keywords-updated')).toBeTruthy()
      expect(wrapper.emitted('keywords-updated')[0][0]).toEqual({
        sectionType: 'responsibilities',
        keywords: ['разработка', 'веб-приложения'],
        confidenceScore: 0.8
      })
    })

    it('emits keywords-updated when keywords are removed', async () => {
      await wrapper.setData({
        keywords: ['разработка', 'веб-приложения'],
        confidenceScore: 0.85
      })

      const tags = wrapper.findAll('.keyword-tag')
      await tags[0].trigger('close')

      expect(wrapper.emitted('keywords-updated')).toBeTruthy()
    })
  })

  describe('Loading States', () => {
    it('shows loading state during extraction', async () => {
      mockHRStore.extractSectionKeywords.mockImplementation(() => 
        new Promise(resolve => setTimeout(resolve, 100))
      )

      const button = wrapper.find('.keywords-header button')
      await button.trigger('click')

      expect(wrapper.vm.isExtracting).toBe(true)
    })

    it('hides loading state after extraction', async () => {
      mockHRStore.extractSectionKeywords.mockResolvedValue({
        success: true,
        keywords: ['test'],
        confidence_score: 0.8
      })

      await wrapper.find('.keywords-header button').trigger('click')

      expect(wrapper.vm.isExtracting).toBe(false)
    })
  })

  describe('Computed Properties', () => {
    it('computes hasText correctly', async () => {
      expect(wrapper.vm.hasText).toBe(true)

      await wrapper.setProps({ sectionText: '' })
      expect(wrapper.vm.hasText).toBe(false)

      await wrapper.setProps({ sectionText: '   ' })
      expect(wrapper.vm.hasText).toBe(false)
    })

    it('computes confidence percentage correctly', async () => {
      await wrapper.setData({ confidenceScore: 0.75 })
      expect(wrapper.vm.confidencePercentage).toBe(75)

      await wrapper.setData({ confidenceScore: 0.123 })
      expect(wrapper.vm.confidencePercentage).toBe(12)
    })

    it('computes confidence color correctly', async () => {
      await wrapper.setData({ confidenceScore: 0.9 })
      expect(wrapper.vm.confidenceColor).toBe('#67C23A') // Green

      await wrapper.setData({ confidenceScore: 0.7 })
      expect(wrapper.vm.confidenceColor).toBe('#E6A23C') // Orange

      await wrapper.setData({ confidenceScore: 0.5 })
      expect(wrapper.vm.confidenceColor).toBe('#F56C6C') // Red

      await wrapper.setData({ confidenceScore: 0.3 })
      expect(wrapper.vm.confidenceColor).toBe('#909399') // Gray
    })
  })
})
