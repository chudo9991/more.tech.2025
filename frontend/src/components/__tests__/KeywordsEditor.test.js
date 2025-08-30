import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { ElMessage } from 'element-plus'
import KeywordsEditor from '../KeywordsEditor.vue'

// Mock Element Plus
vi.mock('element-plus', () => ({
  ElMessage: {
    warning: vi.fn(),
    error: vi.fn()
  }
}))

describe('KeywordsEditor', () => {
  let wrapper

  const defaultProps = {
    visible: true,
    keywords: ['разработка', 'веб-приложения'],
    sectionType: 'responsibilities',
    sectionTitle: 'Обязанности'
  }

  beforeEach(() => {
    vi.clearAllMocks()
    wrapper = mount(KeywordsEditor, {
      props: defaultProps,
      global: {
        stubs: {
          'el-dialog': true,
          'el-input': true,
          'el-button': true,
          'el-icon': true,
          'el-tag': true,
          'el-empty': true,
          'el-alert': true
        }
      }
    })
  })

  describe('Props and Initial State', () => {
    it('renders with correct props', () => {
      expect(wrapper.props('keywords')).toEqual(['разработка', 'веб-приложения'])
      expect(wrapper.props('sectionType')).toBe('responsibilities')
      expect(wrapper.props('sectionTitle')).toBe('Обязанности')
    })

    it('initializes local keywords from props', () => {
      expect(wrapper.vm.localKeywords).toEqual(['разработка', 'веб-приложения'])
    })

    it('shows dialog when visible prop is true', () => {
      expect(wrapper.vm.dialogVisible).toBe(true)
    })
  })

  describe('Add Keywords', () => {
    it('adds new keyword when valid', async () => {
      wrapper.vm.newKeyword = 'новое_ключевое_слово'
      
      await wrapper.vm.addKeyword()

      expect(wrapper.vm.localKeywords).toContain('новое_ключевое_слово')
      expect(wrapper.vm.newKeyword).toBe('')
    })

    it('shows warning when keyword is empty', async () => {
      wrapper.vm.newKeyword = ''
      
      await wrapper.vm.addKeyword()

      expect(ElMessage.warning).toHaveBeenCalledWith('Введите ключевое слово')
      expect(wrapper.vm.localKeywords).toHaveLength(2)
    })

    it('shows warning when keyword already exists', async () => {
      wrapper.vm.newKeyword = 'разработка'
      
      await wrapper.vm.addKeyword()

      expect(ElMessage.warning).toHaveBeenCalledWith('Это ключевое слово уже существует')
      expect(wrapper.vm.localKeywords).toHaveLength(2)
    })

    it('shows warning when keyword is too long', async () => {
      wrapper.vm.newKeyword = 'a'.repeat(51)
      
      await wrapper.vm.addKeyword()

      expect(ElMessage.warning).toHaveBeenCalledWith('Ключевое слово слишком длинное (максимум 50 символов)')
      expect(wrapper.vm.localKeywords).toHaveLength(2)
    })

    it('trims whitespace from keyword', async () => {
      wrapper.vm.newKeyword = '  новое_слово  '
      
      await wrapper.vm.addKeyword()

      expect(wrapper.vm.localKeywords).toContain('новое_слово')
    })
  })

  describe('Remove Keywords', () => {
    it('removes keyword at specified index', async () => {
      await wrapper.vm.removeKeyword(0)

      expect(wrapper.vm.localKeywords).toHaveLength(1)
      expect(wrapper.vm.localKeywords).not.toContain('разработка')
      expect(wrapper.vm.localKeywords).toContain('веб-приложения')
    })

    it('validates keywords after removal', async () => {
      const validateSpy = vi.spyOn(wrapper.vm, 'validateKeywords')
      
      await wrapper.vm.removeKeyword(0)

      expect(validateSpy).toHaveBeenCalled()
    })
  })

  describe('Clear All Keywords', () => {
    it('clears all keywords', async () => {
      await wrapper.vm.clearAllKeywords()

      expect(wrapper.vm.localKeywords).toHaveLength(0)
    })

    it('validates keywords after clearing', async () => {
      const validateSpy = vi.spyOn(wrapper.vm, 'validateKeywords')
      
      await wrapper.vm.clearAllKeywords()

      expect(validateSpy).toHaveBeenCalled()
    })
  })

  describe('Sort Keywords', () => {
    it('sorts keywords alphabetically', async () => {
      wrapper.vm.localKeywords = ['зима', 'лето', 'весна', 'осень']
      
      await wrapper.vm.sortKeywords()

      expect(wrapper.vm.localKeywords).toEqual(['весна', 'зима', 'лето', 'осень'])
    })
  })

  describe('Validation', () => {
    it('validates empty keywords list', async () => {
      wrapper.vm.localKeywords = []
      
      await wrapper.vm.validateKeywords()

      expect(wrapper.vm.validationErrors).toContain('Должно быть хотя бы одно ключевое слово')
    })

    it('validates too many keywords', async () => {
      wrapper.vm.localKeywords = Array.from({ length: 21 }, (_, i) => `keyword${i}`)
      
      await wrapper.vm.validateKeywords()

      expect(wrapper.vm.validationErrors).toContain('Слишком много ключевых слов (максимум 20)')
    })

    it('validates duplicate keywords', async () => {
      wrapper.vm.localKeywords = ['разработка', 'разработка', 'веб-приложения']
      
      await wrapper.vm.validateKeywords()

      expect(wrapper.vm.validationErrors).toContain('Обнаружены дублирующиеся ключевые слова')
    })

    it('validates empty keywords', async () => {
      wrapper.vm.localKeywords = ['разработка', '', 'веб-приложения']
      
      await wrapper.vm.validateKeywords()

      expect(wrapper.vm.validationErrors).toContain('Обнаружены пустые ключевые слова')
    })

    it('clears validation errors when valid', async () => {
      wrapper.vm.localKeywords = ['разработка', 'веб-приложения']
      
      await wrapper.vm.validateKeywords()

      expect(wrapper.vm.validationErrors).toHaveLength(0)
    })
  })

  describe('Save Keywords', () => {
    it('emits save event with keywords when valid', async () => {
      wrapper.vm.localKeywords = ['новое', 'ключевое', 'слово']
      
      await wrapper.vm.handleSave()

      expect(wrapper.emitted('save')).toBeTruthy()
      expect(wrapper.emitted('save')[0][0]).toEqual(['новое', 'ключевое', 'слово'])
    })

    it('shows error when validation fails', async () => {
      wrapper.vm.localKeywords = []
      wrapper.vm.validationErrors = ['Ошибка валидации']
      
      await wrapper.vm.handleSave()

      expect(ElMessage.error).toHaveBeenCalledWith('Исправьте ошибки перед сохранением')
      expect(wrapper.emitted('save')).toBeFalsy()
    })

    it('sets saving state during save operation', async () => {
      wrapper.vm.localKeywords = ['test']
      
      const savePromise = wrapper.vm.handleSave()
      
      expect(wrapper.vm.isSaving).toBe(true)
      
      await savePromise
      
      expect(wrapper.vm.isSaving).toBe(false)
    })
  })

  describe('Close Dialog', () => {
    it('emits cancel and update:visible events', async () => {
      await wrapper.vm.handleClose()

      expect(wrapper.emitted('cancel')).toBeTruthy()
      expect(wrapper.emitted('update:visible')).toBeTruthy()
      expect(wrapper.emitted('update:visible')[0][0]).toBe(false)
    })
  })

  describe('Computed Properties', () => {
    it('computes isValid correctly', async () => {
      // Valid state
      wrapper.vm.localKeywords = ['разработка']
      wrapper.vm.validationErrors = []
      expect(wrapper.vm.isValid).toBe(true)

      // Invalid state - no keywords
      wrapper.vm.localKeywords = []
      expect(wrapper.vm.isValid).toBe(false)

      // Invalid state - validation errors
      wrapper.vm.localKeywords = ['разработка']
      wrapper.vm.validationErrors = ['Ошибка']
      expect(wrapper.vm.isValid).toBe(false)
    })

    it('computes dialogVisible correctly', async () => {
      expect(wrapper.vm.dialogVisible).toBe(true)

      await wrapper.setProps({ visible: false })
      expect(wrapper.vm.dialogVisible).toBe(false)
    })
  })

  describe('Watchers', () => {
    it('updates local keywords when props change', async () => {
      await wrapper.setProps({ keywords: ['новые', 'ключевые', 'слова'] })

      expect(wrapper.vm.localKeywords).toEqual(['новые', 'ключевые', 'слова'])
    })

    it('validates keywords when props change', async () => {
      const validateSpy = vi.spyOn(wrapper.vm, 'validateKeywords')
      
      await wrapper.setProps({ keywords: ['новые', 'слова'] })

      expect(validateSpy).toHaveBeenCalled()
    })

    it('resets state when dialog opens', async () => {
      await wrapper.setProps({ visible: false })
      wrapper.vm.newKeyword = 'test'
      wrapper.vm.localKeywords = ['test']
      
      await wrapper.setProps({ visible: true })

      expect(wrapper.vm.newKeyword).toBe('')
      expect(wrapper.vm.localKeywords).toEqual(['разработка', 'веб-приложения'])
    })
  })

  describe('Template Rendering', () => {
    it('shows keywords count in title', () => {
      const title = wrapper.find('.keywords-list h4')
      expect(title.text()).toContain('Ключевые слова (2)')
    })

    it('shows empty state when no keywords', async () => {
      await wrapper.setProps({ keywords: [] })
      
      expect(wrapper.find('.empty-keywords').exists()).toBe(true)
    })

    it('shows validation errors', async () => {
      wrapper.vm.validationErrors = ['Ошибка 1', 'Ошибка 2']
      await wrapper.vm.$nextTick()
      
      const alerts = wrapper.findAll('.validation-errors .el-alert')
      expect(alerts).toHaveLength(2)
    })

    it('disables save button when invalid', async () => {
      wrapper.vm.localKeywords = []
      wrapper.vm.validationErrors = ['Ошибка']
      await wrapper.vm.$nextTick()
      
      const saveButton = wrapper.find('.dialog-footer button[type="primary"]')
      expect(saveButton.attributes('disabled')).toBeDefined()
    })
  })

  describe('Keyboard Events', () => {
    it('adds keyword on Enter key', async () => {
      const addSpy = vi.spyOn(wrapper.vm, 'addKeyword')
      wrapper.vm.newKeyword = 'новое_слово'
      
      // Simulate Enter key press
      await wrapper.vm.$nextTick()
      const input = wrapper.find('.add-keyword-section .el-input')
      await input.trigger('keyup.enter')

      expect(addSpy).toHaveBeenCalled()
    })
  })
})
