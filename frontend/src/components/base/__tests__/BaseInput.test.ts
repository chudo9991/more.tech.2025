import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseInput from '../BaseInput.vue'

describe('BaseInput', () => {
  describe('Rendering', () => {
    it('renders input element by default', () => {
      const wrapper = mount(BaseInput, {
        props: { modelValue: 'test value' }
      })
      
      const input = wrapper.find('input')
      expect(input.exists()).toBe(true)
      expect(input.element.value).toBe('test value')
    })

    it('renders textarea when type is textarea', () => {
      const wrapper = mount(BaseInput, {
        props: { 
          type: 'textarea',
          modelValue: 'textarea content'
        }
      })
      
      const textarea = wrapper.find('textarea')
      expect(textarea.exists()).toBe(true)
      expect(textarea.element.value).toBe('textarea content')
    })

    it('renders label when provided', () => {
      const wrapper = mount(BaseInput, {
        props: { 
          label: 'Test Label',
          required: true
        }
      })
      
      const label = wrapper.find('label')
      expect(label.exists()).toBe(true)
      expect(label.text()).toContain('Test Label')
      expect(label.text()).toContain('*') // Required indicator
    })
  })

  describe('Input Types', () => {
    const inputTypes = ['text', 'email', 'password', 'number', 'tel', 'url', 'search'] as const

    inputTypes.forEach(type => {
      it(`renders correct input type for ${type}`, () => {
        const wrapper = mount(BaseInput, {
          props: { type }
        })
        
        const input = wrapper.find('input')
        expect(input.attributes('type')).toBe(type)
      })
    })
  })

  describe('Sizes', () => {
    const sizes = ['sm', 'md', 'lg'] as const

    sizes.forEach(size => {
      it(`applies correct classes for ${size} size`, () => {
        const wrapper = mount(BaseInput, {
          props: { size }
        })
        
        const input = wrapper.find('input')
        
        switch (size) {
          case 'sm':
            expect(input.classes()).toContain('h-9')
            expect(input.classes()).toContain('text-sm')
            break
          case 'md':
            expect(input.classes()).toContain('h-10')
            expect(input.classes()).toContain('text-base')
            break
          case 'lg':
            expect(input.classes()).toContain('h-12')
            expect(input.classes()).toContain('text-lg')
            break
        }
      })
    })
  })

  describe('Variants', () => {
    const variants = ['outlined', 'filled', 'underlined'] as const

    variants.forEach(variant => {
      it(`applies correct classes for ${variant} variant`, () => {
        const wrapper = mount(BaseInput, {
          props: { variant }
        })
        
        const input = wrapper.find('input')
        
        switch (variant) {
          case 'outlined':
            expect(input.classes()).toContain('border')
            expect(input.classes()).toContain('bg-white')
            break
          case 'filled':
            expect(input.classes()).toContain('bg-neutral-50')
            expect(input.classes()).toContain('border-b-2')
            break
          case 'underlined':
            expect(input.classes()).toContain('bg-transparent')
            expect(input.classes()).toContain('border-b-2')
            break
        }
      })
    })
  })

  describe('Icons', () => {
    it('renders prepend icon', () => {
      const wrapper = mount(BaseInput, {
        props: { prependIcon: 'mdi mdi-account' }
      })
      
      const icon = wrapper.find('i.mdi mdi-account')
      expect(icon.exists()).toBe(true)
      
      const input = wrapper.find('input')
      expect(input.classes()).toContain('pl-11') // Adjusted padding for icon
    })

    it('renders append icon', () => {
      const wrapper = mount(BaseInput, {
        props: { appendIcon: 'mdi mdi-eye' }
      })
      
      const icon = wrapper.find('i.mdi mdi-eye')
      expect(icon.exists()).toBe(true)
      
      const input = wrapper.find('input')
      expect(input.classes()).toContain('pr-11') // Adjusted padding for icon
    })

    it('renders clear button when clearable and has value', async () => {
      const wrapper = mount(BaseInput, {
        props: { 
          clearable: true,
          modelValue: 'some value'
        }
      })
      
      const clearButton = wrapper.find('button')
      expect(clearButton.exists()).toBe(true)
      expect(clearButton.find('i.mdi mdi-close').exists()).toBe(true)
      
      // Test clear functionality
      await clearButton.trigger('click')
      expect(wrapper.emitted('update:modelValue')).toBeTruthy()
      expect(wrapper.emitted('update:modelValue')?.[0]).toEqual([''])
      expect(wrapper.emitted('clear')).toBeTruthy()
    })

    it('does not render clear button when no value', () => {
      const wrapper = mount(BaseInput, {
        props: { 
          clearable: true,
          modelValue: ''
        }
      })
      
      const clearButton = wrapper.find('button')
      expect(clearButton.exists()).toBe(false)
    })
  })

  describe('Validation States', () => {
    it('shows error state with message', () => {
      const wrapper = mount(BaseInput, {
        props: { 
          error: 'This field is required',
          label: 'Test Field'
        }
      })
      
      const input = wrapper.find('input')
      const label = wrapper.find('label')
      const errorMessage = wrapper.find('[role="alert"]')
      
      expect(input.classes()).toContain('border-error-300')
      expect(input.attributes('aria-invalid')).toBe('true')
      expect(label.classes()).toContain('text-error-700')
      expect(errorMessage.exists()).toBe(true)
      expect(errorMessage.text()).toBe('This field is required')
    })

    it('shows error state with array of messages', () => {
      const wrapper = mount(BaseInput, {
        props: { 
          error: ['First error', 'Second error']
        }
      })
      
      const errorMessage = wrapper.find('[role="alert"]')
      expect(errorMessage.exists()).toBe(true)
      expect(errorMessage.text()).toBe('First error') // Shows first error
    })

    it('shows success state', () => {
      const wrapper = mount(BaseInput, {
        props: { 
          success: 'Input is valid'
        }
      })
      
      const successMessage = wrapper.find('.text-success-600')
      expect(successMessage.exists()).toBe(true)
      expect(successMessage.text()).toBe('Input is valid')
    })

    it('shows hint text when no error', () => {
      const wrapper = mount(BaseInput, {
        props: { 
          hint: 'Enter your email address'
        }
      })
      
      const hintMessage = wrapper.find('.text-neutral-600')
      expect(hintMessage.exists()).toBe(true)
      expect(hintMessage.text()).toBe('Enter your email address')
    })

    it('prioritizes error over hint', () => {
      const wrapper = mount(BaseInput, {
        props: { 
          hint: 'This is a hint',
          error: 'This is an error'
        }
      })
      
      const errorMessage = wrapper.find('[role="alert"]')
      const hintMessage = wrapper.find('.text-neutral-600')
      
      expect(errorMessage.exists()).toBe(true)
      expect(hintMessage.exists()).toBe(false)
    })
  })

  describe('Disabled State', () => {
    it('disables input when disabled prop is true', () => {
      const wrapper = mount(BaseInput, {
        props: { disabled: true }
      })
      
      const input = wrapper.find('input')
      expect(input.attributes('disabled')).toBeDefined()
      expect(input.classes()).toContain('opacity-50')
      expect(input.classes()).toContain('cursor-not-allowed')
    })

    it('does not show clear button when disabled', () => {
      const wrapper = mount(BaseInput, {
        props: { 
          disabled: true,
          clearable: true,
          modelValue: 'some value'
        }
      })
      
      const clearButton = wrapper.find('button')
      expect(clearButton.exists()).toBe(false)
    })
  })

  describe('Readonly State', () => {
    it('sets readonly attribute', () => {
      const wrapper = mount(BaseInput, {
        props: { readonly: true }
      })
      
      const input = wrapper.find('input')
      expect(input.attributes('readonly')).toBeDefined()
    })

    it('does not show clear button when readonly', () => {
      const wrapper = mount(BaseInput, {
        props: { 
          readonly: true,
          clearable: true,
          modelValue: 'some value'
        }
      })
      
      const clearButton = wrapper.find('button')
      expect(clearButton.exists()).toBe(false)
    })
  })

  describe('Events', () => {
    it('emits update:modelValue on input', async () => {
      const wrapper = mount(BaseInput)
      
      const input = wrapper.find('input')
      await input.setValue('new value')
      
      expect(wrapper.emitted('update:modelValue')).toBeTruthy()
      expect(wrapper.emitted('update:modelValue')?.[0]).toEqual(['new value'])
    })

    it('emits number value for number input', async () => {
      const wrapper = mount(BaseInput, {
        props: { type: 'number' }
      })
      
      const input = wrapper.find('input')
      await input.setValue('123')
      
      expect(wrapper.emitted('update:modelValue')).toBeTruthy()
      expect(wrapper.emitted('update:modelValue')?.[0]).toEqual([123])
    })

    it('emits focus and blur events', async () => {
      const wrapper = mount(BaseInput)
      
      const input = wrapper.find('input')
      await input.trigger('focus')
      await input.trigger('blur')
      
      expect(wrapper.emitted('focus')).toBeTruthy()
      expect(wrapper.emitted('blur')).toBeTruthy()
    })

    it('emits change event', async () => {
      const wrapper = mount(BaseInput)
      
      const input = wrapper.find('input')
      await input.trigger('change')
      
      expect(wrapper.emitted('change')).toBeTruthy()
    })
  })

  describe('Accessibility', () => {
    it('sets proper ARIA attributes', () => {
      const wrapper = mount(BaseInput, {
        props: { 
          label: 'Test Input',
          hint: 'This is a hint',
          required: true
        }
      })
      
      const input = wrapper.find('input')
      const label = wrapper.find('label')
      
      expect(input.attributes('required')).toBeDefined()
      expect(input.attributes('aria-describedby')).toBeTruthy()
      expect(label.attributes('for')).toBe(input.attributes('id'))
    })

    it('sets aria-invalid when there is an error', () => {
      const wrapper = mount(BaseInput, {
        props: { error: 'Invalid input' }
      })
      
      const input = wrapper.find('input')
      expect(input.attributes('aria-invalid')).toBe('true')
    })

    it('associates error message with input', () => {
      const wrapper = mount(BaseInput, {
        props: { error: 'Invalid input' }
      })
      
      const input = wrapper.find('input')
      const errorMessage = wrapper.find('[role="alert"]')
      
      expect(input.attributes('aria-describedby')).toContain(errorMessage.attributes('id'))
    })
  })

  describe('Textarea Specific', () => {
    it('sets rows attribute for textarea', () => {
      const wrapper = mount(BaseInput, {
        props: { 
          type: 'textarea',
          rows: 5
        }
      })
      
      const textarea = wrapper.find('textarea')
      expect(textarea.attributes('rows')).toBe('5')
    })

    it('applies correct padding for textarea', () => {
      const wrapper = mount(BaseInput, {
        props: { 
          type: 'textarea',
          size: 'md'
        }
      })
      
      const textarea = wrapper.find('textarea')
      expect(textarea.classes()).toContain('px-4')
      expect(textarea.classes()).toContain('py-3')
    })
  })

  describe('Exposed Methods', () => {
    it('exposes focus method', () => {
      const wrapper = mount(BaseInput)
      
      expect(wrapper.vm.focus).toBeDefined()
      expect(typeof wrapper.vm.focus).toBe('function')
    })

    it('exposes blur method', () => {
      const wrapper = mount(BaseInput)
      
      expect(wrapper.vm.blur).toBeDefined()
      expect(typeof wrapper.vm.blur).toBe('function')
    })

    it('exposes select method', () => {
      const wrapper = mount(BaseInput)
      
      expect(wrapper.vm.select).toBeDefined()
      expect(typeof wrapper.vm.select).toBe('function')
    })
  })

  describe('Default Props', () => {
    it('uses default props when none provided', () => {
      const wrapper = mount(BaseInput)
      
      const input = wrapper.find('input')
      
      // Default type: text
      expect(input.attributes('type')).toBe('text')
      
      // Default size: md
      expect(input.classes()).toContain('h-10')
      
      // Default variant: outlined
      expect(input.classes()).toContain('border')
      expect(input.classes()).toContain('bg-white')
    })
  })
})