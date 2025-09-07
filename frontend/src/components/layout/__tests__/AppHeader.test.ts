import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import AppHeader from '../AppHeader.vue'

describe('AppHeader', () => {
  it('renders properly', () => {
    const wrapper = mount(AppHeader, {
      global: {
        stubs: {
          'router-link': true
        },
        mocks: {
          $route: {
            path: '/'
          }
        }
      }
    })
    expect(wrapper.find('.app-header').exists()).toBe(true)
    const brandText = wrapper.find('.brand-text')
    if (brandText.exists()) {
      expect(brandText.text()).toContain('Система ИИ-Интервью')
    }
  })

  it('shows user information when user prop is provided', () => {
    const user = {
      name: 'Test User',
      role: 'hr' as const
    }
    
    const wrapper = mount(AppHeader, {
      props: { user },
      global: {
        stubs: {
          'router-link': true
        },
        mocks: {
          $route: {
            path: '/'
          }
        }
      }
    })
    
    expect(wrapper.find('.user-name').text()).toBe('Test User')
  })

  it('toggles mobile menu when hamburger is clicked', async () => {
    const wrapper = mount(AppHeader, {
      global: {
        stubs: {
          'router-link': true
        },
        mocks: {
          $route: {
            path: '/'
          }
        }
      }
    })
    
    const mobileToggle = wrapper.find('.mobile-menu-toggle')
    expect(mobileToggle.exists()).toBe(true)
    
    await mobileToggle.trigger('click')
    expect(wrapper.find('.mobile-nav').exists()).toBe(true)
  })
})