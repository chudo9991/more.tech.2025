import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseCheckbox from '../BaseCheckbox.vue'

describe('BaseCheckbox', () => {
  describe('Rendering', () => {
    it('renders checkbox with label', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { label: 'Accept terms' }
      })
      
      const checkbox = wrapper.find('input[type="checkbox"]')
      const label = wrapper.find('label')
      
      expect(checkbox.exists()).toBe(true)
      expect(label.exists()).toBe(true)
      expect(label.text()).toContain('Accept terms')
    })

    it('renders checkbox with slot content', () => {
      const wrapper = mount(BaseCheckbox, {
        slots: { default: 'Custom label content' }
      })
      
      const label = wrapper.find('label')
      expect(label.text()).toContain('Custom label content')
    })

    it('prioritizes slot content over label prop', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { label: 'Prop label' },
        slots: { default: 'Slot label' }
      })
      
      const label = wrapper.find('label')
      expect(label.text()).toContain('Slot label')
      expect(label.text()).not.toContain('Prop label')
    })
  })

  describe('Checked State', () => {
    it('shows as checked when modelValue is true', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { 
          modelValue: true,
          label: 'Checked box'
        }
      })
      
      const checkbox = wrapper.find('input[type="checkbox"]')
      const checkIcon = wrapper.find('i.mdi mdi-check')
      
      expect((checkbox.element as HTMLInputElement).checked).toBe(true)
      expect(checkIcon.exists()).toBe(true)
    })

    it('shows as unchecked when modelValue is false', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { 
          modelValue: false,
          label: 'Unchecked box'
        }
      })
      
      const checkbox = wrapper.find('input[type="checkbox"]')
      const checkIcon = wrapper.find('i.mdi mdi-check')
      
      expect((checkbox.element as HTMLInputElement).checked).toBe(false)
      expect(checkIcon.exists()).toBe(false)
    })

    it('handles array modelValue (multiple checkboxes)', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { 
          modelValue: ['option1', 'option3'],
          value: 'option1',
          label: 'Option 1'
        }
      })
      
      const checkbox = wrapper.find('input[type="checkbox"]')
      expect((checkbox.element as HTMLInputElement).checked).toBe(true)
    })

    it('shows unchecked for array modelValue when value not included', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { 
          modelValue: ['option1', 'option3'],
          value: 'option2',
          label: 'Option 2'
        }
      })
      
      const checkbox = wrapper.find('input[type="checkbox"]')
      expect((checkbox.element as HTMLInputElement).checked).toBe(false)
    })
  })

  describe('Indeterminate State', () => {
    it('shows indeterminate icon when indeterminate is true', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { 
          indeterminate: true,
          label: 'Indeterminate box'
        }
      })
      
      const minusIcon = wrapper.find('i.mdi mdi-minus')
      const checkIcon = wrapper.find('i.mdi mdi-check')
      
      expect(minusIcon.exists()).toBe(true)
      expect(checkIcon.exists()).toBe(false)
    })
  })

  describe('Sizes', () => {
    const sizes = ['sm', 'md', 'lg'] as const

    sizes.forEach(size => {
      it(`applies correct classes for ${size} size`, () => {
        const wrapper = mount(BaseCheckbox, {
          props: { 
            size,
            label: 'Test checkbox'
          }
        })
        
        const checkboxDiv = wrapper.find('.flex.items-center.justify-center')
        
        switch (size) {
          case 'sm':
            expect(checkboxDiv.classes()).toContain('h-4')
            expect(checkboxDiv.classes()).toContain('w-4')
            break
          case 'md':
            expect(checkboxDiv.classes()).toContain('h-5')
            expect(checkboxDiv.classes()).toContain('w-5')
            break
          case 'lg':
            expect(checkboxDiv.classes()).toContain('h-6')
            expect(checkboxDiv.classes()).toContain('w-6')
            break
        }
      })
    })
  })

  describe('Colors', () => {
    const colors = ['primary', 'success', 'warning', 'error'] as const

    colors.forEach(color => {
      it(`applies correct color classes for ${color} when checked`, () => {
        const wrapper = mount(BaseCheckbox, {
          props: { 
            color,
            modelValue: true,
            label: 'Colored checkbox'
          }
        })
        
        const checkboxDiv = wrapper.find('.flex.items-center.justify-center')
        expect(checkboxDiv.classes()).toContain(`bg-${color}-500`)
        expect(checkboxDiv.classes()).toContain(`border-${color}-500`)
      })

      it(`applies correct border color for ${color} when unchecked`, () => {
        const wrapper = mount(BaseCheckbox, {
          props: { 
            color,
            modelValue: false,
            label: 'Colored checkbox'
          }
        })
        
        const checkboxDiv = wrapper.find('.flex.items-center.justify-center')
        expect(checkboxDiv.classes()).toContain('border-neutral-300')
      })
    })
  })

  describe('Validation States', () => {
    it('shows error state with message', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { 
          error: 'You must accept the terms',
          label: 'Accept terms'
        }
      })
      
      const checkbox = wrapper.find('input[type="checkbox"]')
      const errorMessage = wrapper.find('[role="alert"]')
      const checkboxDiv = wrapper.find('.flex.items-center.justify-center')
      
      expect(checkbox.attributes('aria-invalid')).toBe('true')
      expect(errorMessage.exists()).toBe(true)
      expect(errorMessage.text()).toBe('You must accept the terms')
      expect(checkboxDiv.classes()).toContain('border-error-300')
    })

    it('shows error state with array of messages', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { 
          error: ['First error', 'Second error'],
          label: 'Test checkbox'
        }
      })
      
      const errorMessage = wrapper.find('[role="alert"]')
      expect(errorMessage.exists()).toBe(true)
      expect(errorMessage.text()).toBe('First error') // Shows first error
    })

    it('shows hint text when no error', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { 
          hint: 'Check this box to continue',
          label: 'Continue'
        }
      })
      
      const hintMessage = wrapper.find('.text-neutral-600')
      expect(hintMessage.exists()).toBe(true)
      expect(hintMessage.text()).toBe('Check this box to continue')
    })

    it('prioritizes error over hint', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { 
          hint: 'This is a hint',
          error: 'This is an error',
          label: 'Test checkbox'
        }
      })
      
      const errorMessage = wrapper.find('[role="alert"]')
      const hintMessage = wrapper.find('.text-neutral-600')
      
      expect(errorMessage.exists()).toBe(true)
      expect(hintMessage.exists()).toBe(false)
    })
  })

  describe('Disabled State', () => {
    it('disables checkbox when disabled prop is true', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { 
          disabled: true,
          label: 'Disabled checkbox'
        }
      })
      
      const checkbox = wrapper.find('input[type="checkbox"]')
      const label = wrapper.find('label')
      
      expect(checkbox.attributes('disabled')).toBeDefined()
      expect(label.classes()).toContain('opacity-50')
      expect(label.classes()).toContain('cursor-not-allowed')
    })
  })

  describe('Events', () => {
    it('emits update:modelValue on change (boolean)', async () => {
      const wrapper = mount(BaseCheckbox, {
        props: { 
          modelValue: false,
          label: 'Test checkbox'
        }
      })
      
      const checkbox = wrapper.find('input[type="checkbox"]')
      await checkbox.setValue(true)
      
      expect(wrapper.emitted('update:modelValue')).toBeTruthy()
      expect(wrapper.emitted('update:modelValue')?.[0]).toEqual([true])
      expect(wrapper.emitted('change')).toBeTruthy()
    })

    it('emits update:modelValue on change (array)', async () => {
      const wrapper = mount(BaseCheckbox, {
        props: { 
          modelValue: ['option1'],
          value: 'option2',
          label: 'Option 2'
        }
      })
      
      const checkbox = wrapper.find('input[type="checkbox"]')
      await checkbox.setValue(true)
      
      expect(wrapper.emitted('update:modelValue')).toBeTruthy()
      expect(wrapper.emitted('update:modelValue')?.[0]).toEqual([['option1', 'option2']])
    })

    it('removes value from array when unchecked', async () => {
      const wrapper = mount(BaseCheckbox, {
        props: { 
          modelValue: ['option1', 'option2'],
          value: 'option2',
          label: 'Option 2'
        }
      })
      
      const checkbox = wrapper.find('input[type="checkbox"]')
      await checkbox.setValue(false)
      
      expect(wrapper.emitted('update:modelValue')).toBeTruthy()
      expect(wrapper.emitted('update:modelValue')?.[0]).toEqual([['option1']])
    })

    it('emits focus and blur events', async () => {
      const wrapper = mount(BaseCheckbox, {
        props: { label: 'Test checkbox' }
      })
      
      const checkbox = wrapper.find('input[type="checkbox"]')
      await checkbox.trigger('focus')
      await checkbox.trigger('blur')
      
      expect(wrapper.emitted('focus')).toBeTruthy()
      expect(wrapper.emitted('blur')).toBeTruthy()
    })
  })

  describe('Accessibility', () => {
    it('sets proper ARIA attributes', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { 
          label: 'Test Checkbox',
          hint: 'This is a hint',
          required: true
        }
      })
      
      const checkbox = wrapper.find('input[type="checkbox"]')
      const label = wrapper.find('label')
      
      expect(checkbox.attributes('required')).toBeDefined()
      expect(checkbox.attributes('aria-describedby')).toBeTruthy()
      expect(label.attributes('for')).toBe(checkbox.attributes('id'))
    })

    it('sets aria-invalid when there is an error', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { 
          error: 'Invalid checkbox',
          label: 'Test checkbox'
        }
      })
      
      const checkbox = wrapper.find('input[type="checkbox"]')
      expect(checkbox.attributes('aria-invalid')).toBe('true')
    })

    it('associates error message with checkbox', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { 
          error: 'Invalid checkbox',
          label: 'Test checkbox'
        }
      })
      
      const checkbox = wrapper.find('input[type="checkbox"]')
      const errorMessage = wrapper.find('[role="alert"]')
      
      expect(checkbox.attributes('aria-describedby')).toContain(errorMessage.attributes('id'))
    })

    it('uses sr-only class for hidden checkbox', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { label: 'Test checkbox' }
      })
      
      const checkbox = wrapper.find('input[type="checkbox"]')
      expect(checkbox.classes()).toContain('sr-only')
    })
  })

  describe('Exposed Methods', () => {
    it('exposes focus method', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { label: 'Test checkbox' }
      })
      
      expect(wrapper.vm.focus).toBeDefined()
      expect(typeof wrapper.vm.focus).toBe('function')
    })

    it('exposes blur method', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { label: 'Test checkbox' }
      })
      
      expect(wrapper.vm.blur).toBeDefined()
      expect(typeof wrapper.vm.blur).toBe('function')
    })
  })

  describe('Default Props', () => {
    it('uses default props when none provided', () => {
      const wrapper = mount(BaseCheckbox, {
        props: { label: 'Default checkbox' }
      })
      
      const checkboxDiv = wrapper.find('.flex.items-center.justify-center')
      
      // Default size: md
      expect(checkboxDiv.classes()).toContain('h-5')
      expect(checkboxDiv.classes()).toContain('w-5')
      
      // Default color: primary (when unchecked, shows neutral border)
      expect(checkboxDiv.classes()).toContain('border-neutral-300')
    })
  })
})