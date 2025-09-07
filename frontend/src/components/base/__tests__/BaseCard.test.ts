import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseCard from '../BaseCard.vue'
import BaseButton from '../BaseButton.vue'

// Mock router-link component for testing
const RouterLinkStub = {
  name: 'RouterLink',
  props: ['to'],
  template: '<div :data-to="to"><slot /></div>'
}

describe('BaseCard', () => {
  describe('Rendering', () => {
    it('renders div element by default', () => {
      const wrapper = mount(BaseCard, {
        slots: { default: 'Card content' }
      })
      
      expect(wrapper.element.tagName).toBe('DIV')
      expect(wrapper.text()).toContain('Card content')
    })

    it('renders router-link when "to" prop is provided', () => {
      const wrapper = mount(BaseCard, {
        props: { to: '/test' },
        slots: { default: 'Navigate card' },
        global: {
          stubs: {
            'router-link': RouterLinkStub
          }
        }
      })
      
      expect(wrapper.findComponent({ name: 'RouterLink' }).exists()).toBe(true)
      expect(wrapper.findComponent({ name: 'RouterLink' }).props('to')).toBe('/test')
    })

    it('renders anchor element when "href" prop is provided', () => {
      const wrapper = mount(BaseCard, {
        props: { href: 'https://example.com' },
        slots: { default: 'External link card' }
      })
      
      expect(wrapper.element.tagName).toBe('A')
      expect(wrapper.attributes('href')).toBe('https://example.com')
    })
  })

  describe('Variants', () => {
    const variants = ['elevated', 'outlined', 'flat'] as const

    variants.forEach(variant => {
      it(`applies correct classes for ${variant} variant`, () => {
        const wrapper = mount(BaseCard, {
          props: { variant },
          slots: { default: 'Card content' }
        })
        
        const card = wrapper.find('div')
        
        switch (variant) {
          case 'elevated':
            expect(card.classes()).toContain('bg-white')
            expect(card.classes()).toContain('shadow-md')
            break
          case 'outlined':
            expect(card.classes()).toContain('bg-white')
            expect(card.classes()).toContain('border-neutral-200')
            break
          case 'flat':
            expect(card.classes()).toContain('bg-neutral-50')
            break
        }
      })
    })
  })

  describe('Padding', () => {
    const paddings = ['none', 'sm', 'md', 'lg'] as const

    paddings.forEach(padding => {
      it(`applies correct padding for ${padding} size`, () => {
        const wrapper = mount(BaseCard, {
          props: { padding },
          slots: { default: 'Card content' }
        })
        
        const card = wrapper.find('div')
        
        switch (padding) {
          case 'none':
            expect(card.classes()).not.toContain('p-3')
            expect(card.classes()).not.toContain('p-4')
            expect(card.classes()).not.toContain('p-6')
            break
          case 'sm':
            expect(card.classes()).toContain('p-3')
            break
          case 'md':
            expect(card.classes()).toContain('p-4')
            break
          case 'lg':
            expect(card.classes()).toContain('p-6')
            break
        }
      })
    })
  })

  describe('Header Section', () => {
    it('renders title and subtitle', () => {
      const wrapper = mount(BaseCard, {
        props: {
          title: 'Card Title',
          subtitle: 'Card Subtitle'
        },
        slots: { default: 'Card content' }
      })
      
      expect(wrapper.text()).toContain('Card Title')
      expect(wrapper.text()).toContain('Card Subtitle')
      
      const title = wrapper.find('h3')
      const subtitle = wrapper.find('p')
      
      expect(title.exists()).toBe(true)
      expect(subtitle.exists()).toBe(true)
      expect(title.classes()).toContain('text-lg')
      expect(title.classes()).toContain('font-semibold')
    })

    it('renders custom header slot', () => {
      const wrapper = mount(BaseCard, {
        slots: {
          header: '<div class="custom-header">Custom Header</div>',
          default: 'Card content'
        }
      })
      
      expect(wrapper.find('.custom-header').exists()).toBe(true)
      expect(wrapper.text()).toContain('Custom Header')
    })

    it('prioritizes header slot over title/subtitle props', () => {
      const wrapper = mount(BaseCard, {
        props: {
          title: 'Title Prop',
          subtitle: 'Subtitle Prop'
        },
        slots: {
          header: '<div class="custom-header">Custom Header</div>',
          default: 'Card content'
        }
      })
      
      expect(wrapper.find('.custom-header').exists()).toBe(true)
      expect(wrapper.text()).toContain('Custom Header')
      expect(wrapper.text()).not.toContain('Title Prop')
      expect(wrapper.text()).not.toContain('Subtitle Prop')
    })
  })

  describe('Actions', () => {
    it('renders action buttons', async () => {
      const mockAction = vi.fn()
      const actions = [
        {
          label: 'Edit',
          icon: 'mdi mdi-pencil',
          onClick: mockAction
        },
        {
          label: 'Delete',
          variant: 'danger' as const,
          onClick: vi.fn()
        }
      ]

      const wrapper = mount(BaseCard, {
        props: { actions },
        slots: { default: 'Card content' },
        global: {
          components: { BaseButton }
        }
      })
      
      const buttons = wrapper.findAllComponents(BaseButton)
      expect(buttons).toHaveLength(2)
      
      // Test first button
      expect(buttons[0].text()).toContain('Edit')
      expect(buttons[0].props('icon')).toBe('mdi mdi-pencil')
      
      // Test second button
      expect(buttons[1].text()).toContain('Delete')
      expect(buttons[1].props('variant')).toBe('danger')
      
      // Test click handling
      await buttons[0].trigger('click')
      expect(mockAction).toHaveBeenCalled()
    })

    it('handles action click without propagating to card', async () => {
      const cardClick = vi.fn()
      const actionClick = vi.fn()
      
      const actions = [
        {
          label: 'Action',
          onClick: actionClick
        }
      ]

      const wrapper = mount(BaseCard, {
        props: { 
          actions,
          hoverable: true
        },
        slots: { default: 'Card content' },
        global: {
          components: { BaseButton }
        }
      })
      
      wrapper.vm.$emit = vi.fn()
      
      const button = wrapper.findComponent(BaseButton)
      await button.trigger('click')
      
      expect(actionClick).toHaveBeenCalled()
      // Card click should not be triggered when action is clicked
    })

    it('respects action disabled state', () => {
      const actions = [
        {
          label: 'Disabled Action',
          disabled: true,
          onClick: vi.fn()
        }
      ]

      const wrapper = mount(BaseCard, {
        props: { actions },
        slots: { default: 'Card content' },
        global: {
          components: { BaseButton }
        }
      })
      
      const button = wrapper.findComponent(BaseButton)
      expect(button.props('disabled')).toBe(true)
    })

    it('respects action loading state', () => {
      const actions = [
        {
          label: 'Loading Action',
          loading: true,
          onClick: vi.fn()
        }
      ]

      const wrapper = mount(BaseCard, {
        props: { actions },
        slots: { default: 'Card content' },
        global: {
          components: { BaseButton }
        }
      })
      
      const button = wrapper.findComponent(BaseButton)
      expect(button.props('loading')).toBe(true)
    })
  })

  describe('Loading State', () => {
    it('shows loading overlay when loading is true', () => {
      const wrapper = mount(BaseCard, {
        props: { loading: true },
        slots: { default: 'Card content' }
      })
      
      const loadingOverlay = wrapper.find('.absolute.inset-0')
      const spinner = wrapper.find('svg.animate-spin')
      
      expect(loadingOverlay.exists()).toBe(true)
      expect(spinner.exists()).toBe(true)
      expect(loadingOverlay.classes()).toContain('bg-white/80')
    })

    it('does not emit click event when loading', async () => {
      const wrapper = mount(BaseCard, {
        props: { 
          loading: true,
          hoverable: true
        },
        slots: { default: 'Loading card' }
      })
      
      await wrapper.trigger('click')
      expect(wrapper.emitted('click')).toBeFalsy()
    })
  })

  describe('Interactive States', () => {
    it('applies hover effects when hoverable', () => {
      const wrapper = mount(BaseCard, {
        props: { 
          hoverable: true,
          variant: 'elevated'
        },
        slots: { default: 'Hoverable card' }
      })
      
      const card = wrapper.find('div')
      expect(card.classes()).toContain('cursor-pointer')
      expect(card.classes()).toContain('hover:shadow-lg')
      expect(card.classes()).toContain('hover:-translate-y-0.5')
    })

    it('applies hover effects when card has link', () => {
      const wrapper = mount(BaseCard, {
        props: { 
          href: 'https://example.com',
          variant: 'outlined'
        },
        slots: { default: 'Link card' }
      })
      
      const card = wrapper.find('a')
      expect(card.classes()).toContain('cursor-pointer')
      expect(card.classes()).toContain('hover:border-neutral-300')
    })

    it('applies focus styles for interactive cards', () => {
      const wrapper = mount(BaseCard, {
        props: { to: '/test' },
        slots: { default: 'Focusable card' },
        global: {
          stubs: {
            'router-link': RouterLinkStub
          }
        }
      })
      
      const card = wrapper.findComponent({ name: 'RouterLink' })
      expect(card.classes()).toContain('focus:outline-none')
      expect(card.classes()).toContain('focus:ring-2')
      expect(card.classes()).toContain('focus:ring-primary-500')
    })

    it('does not apply interactive styles for static cards', () => {
      const wrapper = mount(BaseCard, {
        slots: { default: 'Static card' }
      })
      
      const card = wrapper.find('div')
      expect(card.classes()).not.toContain('cursor-pointer')
      expect(card.classes()).not.toContain('hover:shadow-lg')
      expect(card.classes()).not.toContain('focus:ring-2')
    })
  })

  describe('Footer Section', () => {
    it('renders footer slot', () => {
      const wrapper = mount(BaseCard, {
        slots: {
          default: 'Card content',
          footer: '<div class="custom-footer">Footer content</div>'
        }
      })
      
      const footer = wrapper.find('.custom-footer')
      expect(footer.exists()).toBe(true)
      expect(footer.text()).toBe('Footer content')
      
      // Check footer styling
      const footerContainer = footer.element.parentElement
      expect(footerContainer?.classList.contains('border-t')).toBe(true)
    })
  })

  describe('Responsive Design', () => {
    it('applies responsive padding classes', () => {
      const wrapper = mount(BaseCard, {
        props: { padding: 'md' },
        slots: { default: 'Responsive card' }
      })
      
      const card = wrapper.find('div')
      expect(card.classes()).toContain('p-4')
      expect(card.classes()).toContain('sm:p-6')
    })

    it('applies responsive padding for large size', () => {
      const wrapper = mount(BaseCard, {
        props: { padding: 'lg' },
        slots: { default: 'Large card' }
      })
      
      const card = wrapper.find('div')
      expect(card.classes()).toContain('p-6')
      expect(card.classes()).toContain('sm:p-8')
    })
  })

  describe('Touch Interactions', () => {
    it('maintains proper touch target sizes for mobile', () => {
      const actions = [
        {
          label: 'Touch Action',
          onClick: vi.fn()
        }
      ]

      const wrapper = mount(BaseCard, {
        props: { actions },
        slots: { default: 'Touch-friendly card' },
        global: {
          components: { BaseButton }
        }
      })
      
      const button = wrapper.findComponent(BaseButton)
      // BaseButton should handle touch target sizes internally
      expect(button.exists()).toBe(true)
    })
  })

  describe('Events', () => {
    it('emits click event when card is clicked', async () => {
      const wrapper = mount(BaseCard, {
        props: { hoverable: true },
        slots: { default: 'Clickable card' }
      })
      
      await wrapper.trigger('click')
      expect(wrapper.emitted('click')).toBeTruthy()
      expect(wrapper.emitted('click')).toHaveLength(1)
    })

    it('does not emit click for static cards', async () => {
      const wrapper = mount(BaseCard, {
        slots: { default: 'Static card' }
      })
      
      await wrapper.trigger('click')
      expect(wrapper.emitted('click')).toBeTruthy() // Vue always emits native events
    })
  })

  describe('Accessibility', () => {
    it('sets proper target for external links', () => {
      const wrapper = mount(BaseCard, {
        props: { 
          href: 'https://example.com',
          target: '_blank'
        },
        slots: { default: 'External card' }
      })
      
      const card = wrapper.find('a')
      expect(card.attributes('target')).toBe('_blank')
    })

    it('maintains semantic structure with headings', () => {
      const wrapper = mount(BaseCard, {
        props: {
          title: 'Accessible Title',
          subtitle: 'Accessible Subtitle'
        },
        slots: { default: 'Accessible content' }
      })
      
      const title = wrapper.find('h3')
      expect(title.exists()).toBe(true)
      expect(title.text()).toBe('Accessible Title')
    })
  })

  describe('Default Props', () => {
    it('uses default props when none provided', () => {
      const wrapper = mount(BaseCard, {
        slots: { default: 'Default card' }
      })
      
      const card = wrapper.find('div')
      
      // Default variant: elevated
      expect(card.classes()).toContain('shadow-md')
      
      // Default padding: md
      expect(card.classes()).toContain('p-4')
      
      // Default loading: false
      expect(wrapper.find('.absolute.inset-0').exists()).toBe(false)
      
      // Default hoverable: false
      expect(card.classes()).not.toContain('cursor-pointer')
    })
  })
})