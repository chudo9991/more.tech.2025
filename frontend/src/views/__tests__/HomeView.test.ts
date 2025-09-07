import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import HomeView from '../HomeView.vue'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseCard from '@/components/base/BaseCard.vue'

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

describe('HomeView', () => {
  it('renders hero section with title and description', () => {
    const wrapper = mount(HomeView, {
      global: {
        components: {
          BaseButton,
          BaseCard
        },
        stubs: {
          'router-link': true
        }
      }
    })

    expect(wrapper.find('.hero-title').text()).toContain('Система ИИ-Интервью')
    expect(wrapper.find('.hero-description').text()).toContain('Революционная платформа')
  })

  it('renders feature cards', () => {
    const wrapper = mount(HomeView, {
      global: {
        components: {
          BaseButton,
          BaseCard
        },
        stubs: {
          'router-link': true
        }
      }
    })

    const featureCards = wrapper.findAll('.feature-card')
    expect(featureCards.length).toBeGreaterThan(0)
  })

  it('renders CTA buttons', () => {
    const wrapper = mount(HomeView, {
      global: {
        components: {
          BaseButton,
          BaseCard
        },
        stubs: {
          'router-link': true
        }
      }
    })

    const heroActions = wrapper.find('.hero-actions')
    expect(heroActions.exists()).toBe(true)
    
    // Check that BaseButton components are rendered
    const baseButtons = wrapper.findAllComponents(BaseButton)
    expect(baseButtons.length).toBeGreaterThanOrEqual(2)
  })

  it('renders statistics section', () => {
    const wrapper = mount(HomeView, {
      global: {
        components: {
          BaseButton,
          BaseCard
        },
        stubs: {
          'router-link': true
        }
      }
    })

    expect(wrapper.find('.stats-section').exists()).toBe(true)
    const statItems = wrapper.findAll('.stat-item')
    expect(statItems.length).toBeGreaterThan(0)
  })
})