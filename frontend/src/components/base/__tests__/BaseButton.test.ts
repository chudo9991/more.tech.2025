import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseButton from '../BaseButton.vue'

// Mock router-link component for testing
const RouterLinkStub = {
  name: 'RouterLink',
  props: ['to'],
  template: '<a :href="typeof to === \'string\' ? to : \'#\'"><slot /></a>'
}

describe('BaseButton', () => {
  describe('Rendering', () => {
    it('renders button element by default', () => {
      const wrapper = mount(BaseButton, {
        slots: { default: 'Click me' }
      })
      
      expect(wrapper.element.tagName).toBe('BUTTON')
      expect(wrapper.text()).toBe('Click me')
    })

    it('renders router-link when "to" prop is provided', () => {
      const wrapper = mount(BaseButton, {
        props: { to: '/test' },
        slots: { default: 'Navigate' },
        global: {
          stubs: {
            'router-link': RouterLinkStub
          }
        }
      })
      
      expect(wrapper.element.tagName).toBe('A')
    })

    it('renders anchor element when "href" prop is provided', () => {
      const wrapper = mount(BaseButton, {
        props: { href: 'https://example.com' },
        slots: { default: 'External Link' }
      })
      
      expect(wrapper.element.tagName).toBe('A')
      expect(wrapper.attributes('href')).toBe('https://example.com')
    })
  })

  describe('Variants', () => {
    const variants = ['primary', 'secondary', 'outline', 'ghost', 'danger'] as const

    variants.forEach(variant => {
      it(`applies correct classes for ${variant} variant`, () => {
        const wrapper = mount(BaseButton, {
          props: { variant },
          slots: { default: 'Button' }
        })
        
        const button = wrapper.find('button')
        expect(button.classes()).toContain('inline-flex')
        expect(button.classes()).toContain('items-center')
        expect(button.classes()).toContain('justify-center')
        
        // Check variant-specific classes
        switch (variant) {
          case 'primary':
            expect(button.classes()).toContain('bg-primary-500')
            expect(button.classes()).toContain('text-white')
            break
          case 'secondary':
            expect(button.classes()).toContain('bg-neutral-100')
            expect(button.classes()).toContain('text-neutral-900')
            break
          case 'outline':
            expect(button.classes()).toContain('bg-transparent')
            expect(button.classes()).toContain('text-primary-600')
            expect(button.classes()).toContain('border-primary-500')
            break
          case 'ghost':
            expect(button.classes()).toContain('bg-transparent')
            expect(button.classes()).toContain('text-neutral-700')
            break
          case 'danger':
            expect(button.classes()).toContain('bg-error-500')
            expect(button.classes()).toContain('text-white')
            break
        }
      })
    })
  })

  describe('Sizes', () => {
    const sizes = ['sm', 'md', 'lg'] as const

    sizes.forEach(size => {
      it(`applies correct classes for ${size} size`, () => {
        const wrapper = mount(BaseButton, {
          props: { size },
          slots: { default: 'Button' }
        })
        
        const button = wrapper.find('button')
        
        switch (size) {
          case 'sm':
            expect(button.classes()).toContain('h-8')
            expect(button.classes()).toContain('px-3')
            expect(button.classes()).toContain('text-sm')
            break
          case 'md':
            expect(button.classes()).toContain('h-10')
            expect(button.classes()).toContain('px-4')
            expect(button.classes()).toContain('text-base')
            break
          case 'lg':
            expect(button.classes()).toContain('h-12')
            expect(button.classes()).toContain('px-6')
            expect(button.classes()).toContain('text-lg')
            break
        }
      })

      it(`applies correct classes for ${size} size with icon only`, () => {
        const wrapper = mount(BaseButton, {
          props: { 
            size,
            icon: 'mdi mdi-plus'
          }
        })
        
        const button = wrapper.find('button')
        
        switch (size) {
          case 'sm':
            expect(button.classes()).toContain('h-8')
            expect(button.classes()).toContain('w-8')
            break
          case 'md':
            expect(button.classes()).toContain('h-10')
            expect(button.classes()).toContain('w-10')
            break
          case 'lg':
            expect(button.classes()).toContain('h-12')
            expect(button.classes()).toContain('w-12')
            break
        }
      })
    })
  })

  describe('Touch Targets', () => {
    it('meets minimum touch target size for small buttons', () => {
      const wrapper = mount(BaseButton, {
        props: { size: 'sm' },
        slots: { default: 'Small Button' }
      })
      
      const button = wrapper.find('button')
      // Small buttons should be at least 32px (h-8 = 2rem = 32px)
      expect(button.classes()).toContain('h-8')
    })

    it('meets minimum touch target size for icon-only buttons', () => {
      const wrapper = mount(BaseButton, {
        props: { 
          size: 'sm',
          icon: 'mdi mdi-plus'
        }
      })
      
      const button = wrapper.find('button')
      // Icon-only buttons should be square and at least 32px
      expect(button.classes()).toContain('h-8')
      expect(button.classes()).toContain('w-8')
    })
  })

  describe('Loading State', () => {
    it('shows loading spinner when loading is true', () => {
      const wrapper = mount(BaseButton, {
        props: { loading: true },
        slots: { default: 'Loading Button' }
      })
      
      const spinner = wrapper.find('svg.animate-spin')
      expect(spinner.exists()).toBe(true)
      
      // Should not show icon when loading
      const icon = wrapper.find('i')
      expect(icon.exists()).toBe(false)
    })

    it('disables button when loading', () => {
      const wrapper = mount(BaseButton, {
        props: { loading: true },
        slots: { default: 'Loading Button' }
      })
      
      const button = wrapper.find('button')
      expect(button.attributes('disabled')).toBeDefined()
    })

    it('does not emit click event when loading', async () => {
      const wrapper = mount(BaseButton, {
        props: { loading: true },
        slots: { default: 'Loading Button' }
      })
      
      await wrapper.trigger('click')
      expect(wrapper.emitted('click')).toBeFalsy()
    })
  })

  describe('Disabled State', () => {
    it('disables button when disabled prop is true', () => {
      const wrapper = mount(BaseButton, {
        props: { disabled: true },
        slots: { default: 'Disabled Button' }
      })
      
      const button = wrapper.find('button')
      expect(button.attributes('disabled')).toBeDefined()
      expect(button.classes()).toContain('disabled:opacity-50')
      expect(button.classes()).toContain('disabled:cursor-not-allowed')
    })

    it('does not emit click event when disabled', async () => {
      const wrapper = mount(BaseButton, {
        props: { disabled: true },
        slots: { default: 'Disabled Button' }
      })
      
      await wrapper.trigger('click')
      expect(wrapper.emitted('click')).toBeFalsy()
    })
  })

  describe('Icon Support', () => {
    it('renders left icon by default', () => {
      const wrapper = mount(BaseButton, {
        props: { 
          icon: 'mdi mdi-plus',
          iconPosition: 'left'
        },
        slots: { default: 'Add Item' }
      })
      
      const icon = wrapper.find('i.mdi mdi-plus')
      expect(icon.exists()).toBe(true)
      
      // Icon should come before text
      const spans = wrapper.findAll('span')
      const iconSpan = spans.find(span => span.find('i.mdi mdi-plus').exists())
      const textSpan = spans.find(span => span.text() === 'Add Item')
      
      expect(iconSpan).toBeTruthy()
      expect(textSpan).toBeTruthy()
    })

    it('renders right icon when iconPosition is right', () => {
      const wrapper = mount(BaseButton, {
        props: { 
          icon: 'mdi mdi-arrow-right',
          iconPosition: 'right'
        },
        slots: { default: 'Next' }
      })
      
      const icon = wrapper.find('i.mdi mdi-arrow-right')
      expect(icon.exists()).toBe(true)
    })

    it('renders icon-only button when no slot content', () => {
      const wrapper = mount(BaseButton, {
        props: { 
          icon: 'mdi mdi-close',
          ariaLabel: 'Close'
        }
      })
      
      const button = wrapper.find('button')
      const icon = wrapper.find('i.mdi mdi-close')
      
      expect(icon.exists()).toBe(true)
      expect(button.classes()).toContain('w-10') // Should be square
      expect(button.attributes('aria-label')).toBe('Close')
    })

    it('applies correct icon size based on button size', () => {
      const wrapper = mount(BaseButton, {
        props: { 
          icon: 'mdi mdi-plus',
          size: 'lg'
        },
        slots: { default: 'Large Button' }
      })
      
      const icon = wrapper.find('i.mdi mdi-plus')
      expect(icon.classes()).toContain('text-lg')
    })
  })

  describe('Events', () => {
    it('emits click event when clicked', async () => {
      const wrapper = mount(BaseButton, {
        slots: { default: 'Click me' }
      })
      
      await wrapper.trigger('click')
      expect(wrapper.emitted('click')).toBeTruthy()
      expect(wrapper.emitted('click')).toHaveLength(1)
    })

    it('passes click event object to handler', async () => {
      const clickHandler = vi.fn()
      const wrapper = mount(BaseButton, {
        props: { onClick: clickHandler },
        slots: { default: 'Click me' }
      })
      
      await wrapper.trigger('click')
      expect(wrapper.emitted('click')).toBeTruthy()
    })
  })

  describe('Accessibility', () => {
    it('sets correct button type', () => {
      const wrapper = mount(BaseButton, {
        props: { type: 'submit' },
        slots: { default: 'Submit' }
      })
      
      const button = wrapper.find('button')
      expect(button.attributes('type')).toBe('submit')
    })

    it('sets aria-label for icon-only buttons', () => {
      const wrapper = mount(BaseButton, {
        props: { 
          icon: 'mdi mdi-close',
          ariaLabel: 'Close dialog'
        }
      })
      
      const button = wrapper.find('button')
      expect(button.attributes('aria-label')).toBe('Close dialog')
    })

    it('sets aria-describedby when provided', () => {
      const wrapper = mount(BaseButton, {
        props: { ariaDescribedby: 'help-text' },
        slots: { default: 'Help' }
      })
      
      const button = wrapper.find('button')
      expect(button.attributes('aria-describedby')).toBe('help-text')
    })

    it('has focus ring classes for keyboard navigation', () => {
      const wrapper = mount(BaseButton, {
        slots: { default: 'Focus me' }
      })
      
      const button = wrapper.find('button')
      expect(button.classes()).toContain('focus:outline-none')
      expect(button.classes()).toContain('focus:ring-2')
      expect(button.classes()).toContain('focus:ring-offset-2')
    })
  })

  describe('Link Functionality', () => {
    it('sets target attribute for external links', () => {
      const wrapper = mount(BaseButton, {
        props: { 
          href: 'https://example.com',
          target: '_blank'
        },
        slots: { default: 'External Link' }
      })
      
      const link = wrapper.find('a')
      expect(link.attributes('target')).toBe('_blank')
    })

    it('handles router navigation', () => {
      const wrapper = mount(BaseButton, {
        props: { to: '/test' },
        slots: { default: 'Navigate' },
        global: {
          stubs: {
            'router-link': RouterLinkStub
          }
        }
      })
      
      // Check that router-link component is used
      expect(wrapper.findComponent({ name: 'RouterLink' }).exists()).toBe(true)
      expect(wrapper.findComponent({ name: 'RouterLink' }).props('to')).toBe('/test')
    })
  })

  describe('Default Props', () => {
    it('uses default props when none provided', () => {
      const wrapper = mount(BaseButton, {
        slots: { default: 'Default Button' }
      })
      
      const button = wrapper.find('button')
      
      // Default variant: primary
      expect(button.classes()).toContain('bg-primary-500')
      
      // Default size: md
      expect(button.classes()).toContain('h-10')
      
      // Default type: button
      expect(button.attributes('type')).toBe('button')
      
      // Default iconPosition: left (not visible without icon)
      // Default loading: false
      expect(wrapper.find('svg.animate-spin').exists()).toBe(false)
      
      // Default disabled: false
      expect(button.attributes('disabled')).toBeUndefined()
    })
  })
})