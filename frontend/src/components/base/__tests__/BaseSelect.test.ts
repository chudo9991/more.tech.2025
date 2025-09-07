import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseSelect from '../BaseSelect.vue'

const mockItems = [
  { title: 'Option 1', value: 'option1' },
  { title: 'Option 2', value: 'option2' },
  { title: 'Option 3', value: 'option3', disabled: true }
]

describe('BaseSelect', () => {
  describe('Rendering', () => {
    it('renders select element with options', () => {
      const wrapper = mount(BaseSelect, {
        props: { items: mockItems }
      })
      
      const select = wrapper.find('select')
      const options = wrapper.findAll('option')
      
      expect(select.exists()).toBe(true)
      expect(options).toHaveLength(3)
      expect(options[0].text()).toBe('Option 1')
      expect(options[1].text()).toBe('Option 2')
      expect(options[2].text()).toBe('Option 3')
    })

    it('renders placeholder option when provided', () => {
      const wrapper = mount(BaseSelect, {
        props: { 
          items: mockItems,
          placeholder: 'Select an option'
        }
      })
      
      const options = wrapper.findAll('option')
      expect(options[0].text()).toBe('Select an option')
      expect(options[0].attributes('disabled')).toBeDefined()
      expect(options[0].attributes('value')).toBe('')
    })

    it('renders label when provided', () => {
      const wrapper = mount(BaseSelect, {
        props: { 
          items: mockItems,
          label: 'Test Select',
          required: true
        }
      })
      
      const label = wrapper.find('label')
      expect(label.exists()).toBe(true)
      expect(label.text()).toContain('Test Select')
      expect(label.text()).toContain('*') // Required indicator
    })

    it('renders dropdown arrow', () => {
      const wrapper = mount(BaseSelect, {
        props: { items: mockItems }
      })
      
      const arrow = wrapper.find('i.mdi mdi-chevron-down')
      expect(arrow.exists()).toBe(true)
    })
  })

  describe('Sizes', () => {
    const sizes = ['sm', 'md', 'lg'] as const

    sizes.forEach(size => {
      it(`applies correct classes for ${size} size`, () => {
        const wrapper = mount(BaseSelect, {
          props: { items: mockItems, size }
        })
        
        const select = wrapper.find('select')
        
        switch (size) {
          case 'sm':
            expect(select.classes()).toContain('h-9')
            expect(select.classes()).toContain('text-sm')
            break
          case 'md':
            expect(select.classes()).toContain('h-10')
            expect(select.classes()).toContain('text-base')
            break
          case 'lg':
            expect(select.classes()).toContain('h-12')
            expect(select.classes()).toContain('text-lg')
            break
        }
      })
    })
  })

  describe('Variants', () => {
    const variants = ['outlined', 'filled', 'underlined'] as const

    variants.forEach(variant => {
      it(`applies correct classes for ${variant} variant`, () => {
        const wrapper = mount(BaseSelect, {
          props: { items: mockItems, variant }
        })
        
        const select = wrapper.find('select')
        
        switch (variant) {
          case 'outlined':
            expect(select.classes()).toContain('border')
            expect(select.classes()).toContain('bg-white')
            break
          case 'filled':
            expect(select.classes()).toContain('bg-neutral-50')
            expect(select.classes()).toContain('border-b-2')
            break
          case 'underlined':
            expect(select.classes()).toContain('bg-transparent')
            expect(select.classes()).toContain('border-b-2')
            break
        }
      })
    })
  })

  describe('Icons', () => {
    it('renders prepend icon', () => {
      const wrapper = mount(BaseSelect, {
        props: { 
          items: mockItems,
          prependIcon: 'mdi mdi-account'
        }
      })
      
      const icon = wrapper.find('i.mdi mdi-account')
      expect(icon.exists()).toBe(true)
      
      const select = wrapper.find('select')
      expect(select.classes()).toContain('pl-11') // Adjusted padding for icon
    })
  })

  describe('Option Values', () => {
    it('sets correct option values', () => {
      const wrapper = mount(BaseSelect, {
        props: { items: mockItems }
      })
      
      const options = wrapper.findAll('option')
      expect(options[0].attributes('value')).toBe('option1')
      expect(options[1].attributes('value')).toBe('option2')
      expect(options[2].attributes('value')).toBe('option3')
    })

    it('handles disabled options', () => {
      const wrapper = mount(BaseSelect, {
        props: { items: mockItems }
      })
      
      const options = wrapper.findAll('option')
      expect(options[2].attributes('disabled')).toBeDefined()
    })

    it('uses custom itemTitle and itemValue functions', () => {
      const customItems = [
        { name: 'First', id: 1 },
        { name: 'Second', id: 2 }
      ]

      const wrapper = mount(BaseSelect, {
        props: { 
          items: customItems,
          itemTitle: (item: any) => item.name,
          itemValue: (item: any) => item.id
        }
      })
      
      const options = wrapper.findAll('option')
      expect(options[0].text()).toBe('First')
      expect(options[0].attributes('value')).toBe('1')
      expect(options[1].text()).toBe('Second')
      expect(options[1].attributes('value')).toBe('2')
    })
  })

  describe('Selection', () => {
    it('selects correct option based on modelValue', () => {
      const wrapper = mount(BaseSelect, {
        props: { 
          items: mockItems,
          modelValue: 'option2'
        }
      })
      
      const select = wrapper.find('select')
      expect(select.element.value).toBe('option2')
    })

    it('shows placeholder as selected when no modelValue', () => {
      const wrapper = mount(BaseSelect, {
        props: { 
          items: mockItems,
          placeholder: 'Choose option'
        }
      })
      
      const placeholderOption = wrapper.find('option[value=""]')
      expect(placeholderOption.attributes('selected')).toBeDefined()
    })
  })

  describe('Validation States', () => {
    it('shows error state with message', () => {
      const wrapper = mount(BaseSelect, {
        props: { 
          items: mockItems,
          error: 'Please select an option',
          label: 'Test Select'
        }
      })
      
      const select = wrapper.find('select')
      const label = wrapper.find('label')
      const errorMessage = wrapper.find('[role="alert"]')
      
      expect(select.classes()).toContain('border-error-300')
      expect(select.attributes('aria-invalid')).toBe('true')
      expect(label.classes()).toContain('text-error-700')
      expect(errorMessage.exists()).toBe(true)
      expect(errorMessage.text()).toBe('Please select an option')
    })

    it('shows error state with array of messages', () => {
      const wrapper = mount(BaseSelect, {
        props: { 
          items: mockItems,
          error: ['First error', 'Second error']
        }
      })
      
      const errorMessage = wrapper.find('[role="alert"]')
      expect(errorMessage.exists()).toBe(true)
      expect(errorMessage.text()).toBe('First error') // Shows first error
    })

    it('shows success state', () => {
      const wrapper = mount(BaseSelect, {
        props: { 
          items: mockItems,
          success: 'Good choice!'
        }
      })
      
      const successMessage = wrapper.find('.text-success-600')
      expect(successMessage.exists()).toBe(true)
      expect(successMessage.text()).toBe('Good choice!')
    })

    it('shows hint text when no error', () => {
      const wrapper = mount(BaseSelect, {
        props: { 
          items: mockItems,
          hint: 'Choose your preferred option'
        }
      })
      
      const hintMessage = wrapper.find('.text-neutral-600')
      expect(hintMessage.exists()).toBe(true)
      expect(hintMessage.text()).toBe('Choose your preferred option')
    })
  })

  describe('Disabled State', () => {
    it('disables select when disabled prop is true', () => {
      const wrapper = mount(BaseSelect, {
        props: { 
          items: mockItems,
          disabled: true
        }
      })
      
      const select = wrapper.find('select')
      expect(select.attributes('disabled')).toBeDefined()
      expect(select.classes()).toContain('opacity-50')
      expect(select.classes()).toContain('cursor-not-allowed')
    })
  })

  describe('Events', () => {
    it('emits update:modelValue on change', async () => {
      const wrapper = mount(BaseSelect, {
        props: { items: mockItems }
      })
      
      const select = wrapper.find('select')
      await select.setValue('option2')
      
      expect(wrapper.emitted('update:modelValue')).toBeTruthy()
      expect(wrapper.emitted('update:modelValue')?.[0]).toEqual(['option2'])
      expect(wrapper.emitted('change')).toBeTruthy()
    })

    it('emits focus and blur events', async () => {
      const wrapper = mount(BaseSelect, {
        props: { items: mockItems }
      })
      
      const select = wrapper.find('select')
      await select.trigger('focus')
      await select.trigger('blur')
      
      expect(wrapper.emitted('focus')).toBeTruthy()
      expect(wrapper.emitted('blur')).toBeTruthy()
    })
  })

  describe('Accessibility', () => {
    it('sets proper ARIA attributes', () => {
      const wrapper = mount(BaseSelect, {
        props: { 
          items: mockItems,
          label: 'Test Select',
          hint: 'This is a hint',
          required: true
        }
      })
      
      const select = wrapper.find('select')
      const label = wrapper.find('label')
      
      expect(select.attributes('required')).toBeDefined()
      expect(select.attributes('aria-describedby')).toBeTruthy()
      expect(label.attributes('for')).toBe(select.attributes('id'))
    })

    it('sets aria-invalid when there is an error', () => {
      const wrapper = mount(BaseSelect, {
        props: { 
          items: mockItems,
          error: 'Invalid selection'
        }
      })
      
      const select = wrapper.find('select')
      expect(select.attributes('aria-invalid')).toBe('true')
    })

    it('associates error message with select', () => {
      const wrapper = mount(BaseSelect, {
        props: { 
          items: mockItems,
          error: 'Invalid selection'
        }
      })
      
      const select = wrapper.find('select')
      const errorMessage = wrapper.find('[role="alert"]')
      
      expect(select.attributes('aria-describedby')).toContain(errorMessage.attributes('id'))
    })
  })

  describe('Exposed Methods', () => {
    it('exposes focus method', () => {
      const wrapper = mount(BaseSelect, {
        props: { items: mockItems }
      })
      
      expect(wrapper.vm.focus).toBeDefined()
      expect(typeof wrapper.vm.focus).toBe('function')
    })

    it('exposes blur method', () => {
      const wrapper = mount(BaseSelect, {
        props: { items: mockItems }
      })
      
      expect(wrapper.vm.blur).toBeDefined()
      expect(typeof wrapper.vm.blur).toBe('function')
    })
  })

  describe('Default Props', () => {
    it('uses default props when none provided', () => {
      const wrapper = mount(BaseSelect, {
        props: { items: mockItems }
      })
      
      const select = wrapper.find('select')
      
      // Default size: md
      expect(select.classes()).toContain('h-10')
      
      // Default variant: outlined
      expect(select.classes()).toContain('border')
      expect(select.classes()).toContain('bg-white')
    })
  })
})