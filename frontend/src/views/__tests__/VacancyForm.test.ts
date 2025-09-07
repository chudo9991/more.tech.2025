import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import VacancyForm from '../VacancyForm.vue'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import BaseSelect from '@/components/base/BaseSelect.vue'
import BaseCheckbox from '@/components/base/BaseCheckbox.vue'

// Mock the router
vi.mock('vue-router', () => ({
  useRoute: () => ({
    params: { id: null }
  }),
  useRouter: () => ({
    push: vi.fn()
  })
}))

// Mock fetch
global.fetch = vi.fn()

describe('VacancyForm', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(global.fetch).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({})
    } as any)
  })

  it('renders form header with title and actions', () => {
    const wrapper = mount(VacancyForm, {
      global: {
        components: {
          BaseButton,
          BaseCard,
          BaseInput,
          BaseSelect,
          BaseCheckbox
        },
        stubs: {
          RichTextEditor: true,
          KeywordsSection: true
        }
      }
    })

    expect(wrapper.find('.form-title').text()).toBe('Создание вакансии')
  })

  it('renders progress indicator', () => {
    const wrapper = mount(VacancyForm, {
      global: {
        components: {
          BaseButton,
          BaseCard,
          BaseInput,
          BaseSelect,
          BaseCheckbox
        },
        stubs: {
          RichTextEditor: true,
          KeywordsSection: true
        }
      }
    })

    expect(wrapper.find('.progress-container').exists()).toBe(true)
    expect(wrapper.find('.progress-bar').exists()).toBe(true)
  })

  it('renders step navigation', () => {
    const wrapper = mount(VacancyForm, {
      global: {
        components: {
          BaseButton,
          BaseCard,
          BaseInput,
          BaseSelect,
          BaseCheckbox
        },
        stubs: {
          RichTextEditor: true,
          KeywordsSection: true
        }
      }
    })

    expect(wrapper.find('.steps-navigation').exists()).toBe(true)
    const stepItems = wrapper.findAll('.step-item')
    expect(stepItems.length).toBe(5) // 5 steps
  })

  it('shows first step by default', () => {
    const wrapper = mount(VacancyForm, {
      global: {
        components: {
          BaseButton,
          BaseCard,
          BaseInput,
          BaseSelect,
          BaseCheckbox
        },
        stubs: {
          RichTextEditor: true,
          KeywordsSection: true
        }
      }
    })

    expect(wrapper.vm.currentStep).toBe(0)
    const activeStep = wrapper.find('.step-item.active')
    expect(activeStep.exists()).toBe(true)
  })

  it('renders auto-save status', () => {
    const wrapper = mount(VacancyForm, {
      global: {
        components: {
          BaseButton,
          BaseCard,
          BaseInput,
          BaseSelect,
          BaseCheckbox
        },
        stubs: {
          RichTextEditor: true,
          KeywordsSection: true
        }
      }
    })

    expect(wrapper.find('.auto-save-status').exists()).toBe(true)
  })

  it('navigates between steps', async () => {
    const wrapper = mount(VacancyForm, {
      global: {
        components: {
          BaseButton,
          BaseCard,
          BaseInput,
          BaseSelect,
          BaseCheckbox
        },
        stubs: {
          RichTextEditor: true,
          KeywordsSection: true
        }
      }
    })

    // Click on second step
    const stepItems = wrapper.findAll('.step-item')
    await stepItems[1].trigger('click')
    
    expect(wrapper.vm.currentStep).toBe(1)
  })
})