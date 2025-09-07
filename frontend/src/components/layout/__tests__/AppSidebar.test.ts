import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import AppSidebar from '../AppSidebar.vue'

describe('AppSidebar', () => {
  it('renders properly', () => {
    const wrapper = mount(AppSidebar, {
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
    expect(wrapper.find('.app-sidebar').exists()).toBe(true)
    const brandText = wrapper.find('.brand-text')
    if (brandText.exists()) {
      expect(brandText.text()).toContain('ИИ-Интервью')
    }
  })

  it('toggles collapsed state when collapse button is clicked', async () => {
    const wrapper = mount(AppSidebar, {
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
    
    const collapseToggle = wrapper.find('.collapse-toggle')
    expect(collapseToggle.exists()).toBe(true)
    
    await collapseToggle.trigger('click')
    expect(wrapper.emitted('update:collapsed')).toBeTruthy()
  })

  it('shows navigation items', () => {
    const wrapper = mount(AppSidebar, {
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
    
    const navItems = wrapper.findAll('.nav-item')
    expect(navItems.length).toBeGreaterThan(0)
  })

  it('handles collapsed prop correctly', () => {
    const wrapper = mount(AppSidebar, {
      props: { collapsed: true },
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
    
    expect(wrapper.find('.sidebar-collapsed').exists()).toBe(true)
  })
})