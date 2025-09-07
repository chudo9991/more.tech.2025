import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import HRPanel from '../HRPanel.vue'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import BaseSelect from '@/components/base/BaseSelect.vue'
import BaseModal from '@/components/base/BaseModal.vue'

// Mock the HR store
vi.mock('@/stores/hr', () => ({
  useHRStore: () => ({
    sessions: [],
    vacancies: [],
    fetchSessions: vi.fn().mockResolvedValue({ total: 0 }),
    fetchVacancies: vi.fn().mockResolvedValue([]),
    fetchStatistics: vi.fn().mockResolvedValue({
      total_sessions: 0,
      completed_sessions: 0,
      in_progress_sessions: 0,
      avg_score: 0
    }),
    exportSession: vi.fn(),
    exportAllSessions: vi.fn(),
    deleteSession: vi.fn()
  })
}))

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  root = null
  rootMargin = ''
  thresholds = []
  constructor() {}
  observe() {}
  disconnect() {}
  unobserve() {}
  takeRecords() { return [] }
} as any

describe('HRPanel', () => {
  it('renders panel header with title and actions', () => {
    const wrapper = mount(HRPanel, {
      global: {
        components: {
          BaseButton,
          BaseCard,
          BaseInput,
          BaseSelect,
          BaseModal
        },
        stubs: {
          SessionCard: true,
          SessionDetail: true,
          CreateSession: true
        }
      }
    })

    expect(wrapper.find('.panel-title').text()).toBe('HR Панель')
    expect(wrapper.find('.panel-subtitle').text()).toContain('Управление интервью')
  })

  it('renders statistics cards', () => {
    const wrapper = mount(HRPanel, {
      global: {
        components: {
          BaseButton,
          BaseCard,
          BaseInput,
          BaseSelect,
          BaseModal
        },
        stubs: {
          SessionCard: true,
          SessionDetail: true,
          CreateSession: true
        }
      }
    })

    const statCards = wrapper.findAll('.stat-card')
    expect(statCards.length).toBe(4)
  })

  it('renders filters section', () => {
    const wrapper = mount(HRPanel, {
      global: {
        components: {
          BaseButton,
          BaseCard,
          BaseInput,
          BaseSelect,
          BaseModal
        },
        stubs: {
          SessionCard: true,
          SessionDetail: true,
          CreateSession: true
        }
      }
    })

    expect(wrapper.find('.filters-section').exists()).toBe(true)
    expect(wrapper.find('.filters-title').text()).toBe('Фильтры и поиск')
  })

  it('renders table section with proper header', () => {
    const wrapper = mount(HRPanel, {
      global: {
        components: {
          BaseButton,
          BaseCard,
          BaseInput,
          BaseSelect,
          BaseModal
        },
        stubs: {
          SessionCard: true,
          SessionDetail: true,
          CreateSession: true
        }
      }
    })

    expect(wrapper.find('.table-section').exists()).toBe(true)
    expect(wrapper.find('.table-title').text()).toBe('Сессии интервью')
  })

  it('shows empty state when no sessions', () => {
    const wrapper = mount(HRPanel, {
      global: {
        components: {
          BaseButton,
          BaseCard,
          BaseInput,
          BaseSelect,
          BaseModal
        },
        stubs: {
          SessionCard: true,
          SessionDetail: true,
          CreateSession: true
        }
      }
    })

    expect(wrapper.find('.empty-state').exists()).toBe(true)
    expect(wrapper.find('.empty-title').text()).toBe('Сессии не найдены')
  })
})