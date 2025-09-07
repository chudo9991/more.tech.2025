import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import VacanciesList from '../VacanciesList.vue'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import BaseSelect from '@/components/base/BaseSelect.vue'

// Mock the router
vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: vi.fn()
  })
}))

// Mock fetch
global.fetch = vi.fn()

describe('VacanciesList', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    // Mock successful API responses
    vi.mocked(global.fetch).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ items: [], total: 0 })
    } as any)
  })

  it('renders page header with title and actions', () => {
    const wrapper = mount(VacanciesList, {
      global: {
        components: {
          BaseButton,
          BaseCard,
          BaseInput,
          BaseSelect
        },
        stubs: {
          VacancyCard: true
        }
      }
    })

    expect(wrapper.find('.page-title').text()).toBe('Управление вакансиями')
    expect(wrapper.find('.page-subtitle').text()).toContain('Создавайте и управляйте вакансиями')
  })

  it('renders statistics cards', () => {
    const wrapper = mount(VacanciesList, {
      global: {
        components: {
          BaseButton,
          BaseCard,
          BaseInput,
          BaseSelect
        },
        stubs: {
          VacancyCard: true
        }
      }
    })

    const statCards = wrapper.findAll('.stat-card')
    expect(statCards.length).toBe(4)
  })

  it('renders filters sidebar', () => {
    const wrapper = mount(VacanciesList, {
      global: {
        components: {
          BaseButton,
          BaseCard,
          BaseInput,
          BaseSelect
        },
        stubs: {
          VacancyCard: true
        }
      }
    })

    expect(wrapper.find('.filters-sidebar').exists()).toBe(true)
    expect(wrapper.find('.filters-title').text()).toBe('Фильтры')
  })

  it('renders search controls and view mode toggles', () => {
    const wrapper = mount(VacanciesList, {
      global: {
        components: {
          BaseButton,
          BaseCard,
          BaseInput,
          BaseSelect
        },
        stubs: {
          VacancyCard: true
        }
      }
    })

    expect(wrapper.find('.search-controls').exists()).toBe(true)
    expect(wrapper.find('.view-controls').exists()).toBe(true)
  })

  it('shows empty state when no vacancies', () => {
    const wrapper = mount(VacanciesList, {
      global: {
        components: {
          BaseButton,
          BaseCard,
          BaseInput,
          BaseSelect
        },
        stubs: {
          VacancyCard: true
        }
      }
    })

    expect(wrapper.find('.empty-state').exists()).toBe(true)
    expect(wrapper.find('.empty-title').text()).toBe('Вакансии не найдены')
  })

  it('toggles between grid and list view modes', async () => {
    const wrapper = mount(VacanciesList, {
      global: {
        components: {
          BaseButton,
          BaseCard,
          BaseInput,
          BaseSelect
        },
        stubs: {
          VacancyCard: true
        }
      }
    })

    // Should start in grid mode
    expect(wrapper.vm.viewMode).toBe('grid')

    // Find and click the list view button
    const listViewButton = wrapper.findAll('.view-controls button').find(btn => 
      btn.text().includes('Список')
    )
    
    if (listViewButton) {
      await listViewButton.trigger('click')
      expect(wrapper.vm.viewMode).toBe('list')
    }
  })
})