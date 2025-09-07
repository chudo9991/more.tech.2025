import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import AppFooter from '../AppFooter.vue'

describe('AppFooter', () => {
  it('renders properly', () => {
    const wrapper = mount(AppFooter, {
      global: {
        stubs: {
          'router-link': true
        }
      }
    })
    expect(wrapper.find('.app-footer').exists()).toBe(true)
    expect(wrapper.find('.brand-title').text()).toContain('Система ИИ-Интервью')
  })

  it('displays company information', () => {
    const companyInfo = {
      name: 'Test Company',
      description: 'Test Description',
      email: 'test@example.com'
    }
    
    const wrapper = mount(AppFooter, {
      props: { companyInfo },
      global: {
        stubs: {
          'router-link': true
        }
      }
    })
    
    expect(wrapper.find('.brand-title').text()).toBe('Test Company')
    expect(wrapper.find('.brand-description').text()).toBe('Test Description')
    expect(wrapper.text()).toContain('test@example.com')
  })

  it('shows social links when enabled', () => {
    const wrapper = mount(AppFooter, {
      props: { showSocialLinks: true },
      global: {
        stubs: {
          'router-link': true
        }
      }
    })
    
    expect(wrapper.find('.social-section').exists()).toBe(true)
    expect(wrapper.findAll('.social-link').length).toBeGreaterThan(0)
  })

  it('displays system status correctly', () => {
    const wrapper = mount(AppFooter, {
      props: { systemStatus: 'online' },
      global: {
        stubs: {
          'router-link': true
        }
      }
    })
    
    expect(wrapper.find('.status-online').exists()).toBe(true)
    expect(wrapper.find('.status-text').text()).toBe('Система работает')
  })
})