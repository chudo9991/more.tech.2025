import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseDialog from '../BaseDialog.vue'
import BaseModal from '../BaseModal.vue'
import BaseButton from '../BaseButton.vue'

// Mock Teleport for testing
const TeleportStub = {
  name: 'Teleport',
  props: ['to'],
  template: '<div><slot /></div>'
}

describe('BaseDialog', () => {
  describe('Rendering', () => {
    it('renders dialog with message', () => {
      const wrapper = mount(BaseDialog, {
        props: { 
          modelValue: true,
          message: 'Are you sure you want to continue?'
        },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      expect(wrapper.text()).toContain('Are you sure you want to continue?')
    })

    it('renders dialog with title', () => {
      const wrapper = mount(BaseDialog, {
        props: { 
          modelValue: true,
          title: 'Confirmation',
          message: 'Please confirm your action'
        },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      expect(wrapper.text()).toContain('Confirmation')
    })

    it('renders custom content in default slot', () => {
      const wrapper = mount(BaseDialog, {
        props: { modelValue: true },
        slots: { default: '<p class="custom-content">Custom dialog content</p>' },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      expect(wrapper.find('.custom-content').exists()).toBe(true)
      expect(wrapper.text()).toContain('Custom dialog content')
    })
  })

  describe('Dialog Types', () => {
    const types = ['info', 'success', 'warning', 'error', 'confirm'] as const

    types.forEach(type => {
      it(`renders correct icon for ${type} type`, () => {
        const wrapper = mount(BaseDialog, {
          props: { 
            modelValue: true,
            type,
            message: `This is a ${type} dialog`
          },
          global: {
            components: { BaseModal, BaseButton },
            stubs: { Teleport: TeleportStub }
          }
        })
        
        const iconContainer = wrapper.find('.w-12.h-12.rounded-full')
        expect(iconContainer.exists()).toBe(true)
        
        // Check for type-specific icon classes (not the close button)
        const icon = iconContainer.find('i[class*="mdi mdi-"]')
        expect(icon.exists()).toBe(true)
        
        switch (type) {
          case 'info':
            expect(icon.classes()).toContain('mdi mdi-information')
            expect(icon.classes()).toContain('text-info-500')
            break
          case 'success':
            expect(icon.classes()).toContain('mdi mdi-check-circle')
            expect(icon.classes()).toContain('text-success-500')
            break
          case 'warning':
            expect(icon.classes()).toContain('mdi mdi-alert')
            expect(icon.classes()).toContain('text-warning-500')
            break
          case 'error':
            expect(icon.classes()).toContain('mdi mdi-alert-circle')
            expect(icon.classes()).toContain('text-error-500')
            break
          case 'confirm':
            expect(icon.classes()).toContain('mdi mdi-help-circle')
            expect(icon.classes()).toContain('text-primary-500')
            break
        }
      })

      it(`applies correct button variant for ${type} type`, () => {
        const wrapper = mount(BaseDialog, {
          props: { 
            modelValue: true,
            type,
            message: 'Test message'
          },
          global: {
            components: { BaseModal, BaseButton },
            stubs: { Teleport: TeleportStub }
          }
        })
        
        const buttons = wrapper.findAllComponents(BaseButton)
        const confirmButton = buttons.find(btn => btn.text().includes('OK'))
        
        if (type === 'error') {
          expect(confirmButton?.props('variant')).toBe('danger')
        } else {
          expect(confirmButton?.props('variant')).toBe('primary')
        }
      })
    })
  })

  describe('Custom Icon', () => {
    it('renders custom icon when provided', () => {
      const wrapper = mount(BaseDialog, {
        props: { 
          modelValue: true,
          icon: 'mdi mdi-star',
          message: 'Custom icon dialog'
        },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const icon = wrapper.find('i.mdi mdi-star')
      expect(icon.exists()).toBe(true)
    })

    it('prioritizes custom icon over type icon', () => {
      const wrapper = mount(BaseDialog, {
        props: { 
          modelValue: true,
          type: 'error',
          icon: 'mdi mdi-custom',
          message: 'Custom icon overrides type'
        },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const customIcon = wrapper.find('i.mdi mdi-custom')
      const typeIcon = wrapper.find('i.mdi mdi-alert-circle')
      
      expect(customIcon.exists()).toBe(true)
      expect(typeIcon.exists()).toBe(false)
    })
  })

  describe('Action Buttons', () => {
    it('renders both confirm and cancel buttons by default', () => {
      const wrapper = mount(BaseDialog, {
        props: { 
          modelValue: true,
          message: 'Test dialog'
        },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const buttons = wrapper.findAllComponents(BaseButton)
      expect(buttons).toHaveLength(2)
      
      const cancelButton = buttons.find(btn => btn.text().includes('Cancel'))
      const confirmButton = buttons.find(btn => btn.text().includes('OK'))
      
      expect(cancelButton?.exists()).toBe(true)
      expect(confirmButton?.exists()).toBe(true)
    })

    it('hides cancel button when showCancel is false', () => {
      const wrapper = mount(BaseDialog, {
        props: { 
          modelValue: true,
          message: 'Test dialog',
          showCancel: false
        },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const buttons = wrapper.findAllComponents(BaseButton)
      expect(buttons).toHaveLength(1)
      
      const confirmButton = buttons.find(btn => btn.text().includes('OK'))
      expect(confirmButton?.exists()).toBe(true)
    })

    it('uses custom button text', () => {
      const wrapper = mount(BaseDialog, {
        props: { 
          modelValue: true,
          message: 'Test dialog',
          confirmText: 'Yes, Delete',
          cancelText: 'No, Keep'
        },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      expect(wrapper.text()).toContain('Yes, Delete')
      expect(wrapper.text()).toContain('No, Keep')
    })

    it('applies correct button size', () => {
      const wrapper = mount(BaseDialog, {
        props: { 
          modelValue: true,
          message: 'Test dialog',
          buttonSize: 'lg'
        },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const buttons = wrapper.findAllComponents(BaseButton)
      buttons.forEach(button => {
        expect(button.props('size')).toBe('lg')
      })
    })
  })

  describe('Loading State', () => {
    it('shows loading state on confirm button', () => {
      const wrapper = mount(BaseDialog, {
        props: { 
          modelValue: true,
          message: 'Test dialog',
          loading: true
        },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const buttons = wrapper.findAllComponents(BaseButton)
      const confirmButton = buttons.find(btn => btn.text().includes('OK'))
      const cancelButton = buttons.find(btn => btn.text().includes('Cancel'))
      
      expect(confirmButton?.props('loading')).toBe(true)
      expect(cancelButton?.props('disabled')).toBe(true)
    })
  })

  describe('Events', () => {
    it('emits confirm event when confirm button is clicked', async () => {
      const wrapper = mount(BaseDialog, {
        props: { 
          modelValue: true,
          message: 'Test dialog'
        },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const buttons = wrapper.findAllComponents(BaseButton)
      const confirmButton = buttons.find(btn => btn.text().includes('OK'))
      
      await confirmButton?.trigger('click')
      
      expect(wrapper.emitted('confirm')).toBeTruthy()
      expect(wrapper.emitted('update:modelValue')).toBeTruthy()
      expect(wrapper.emitted('update:modelValue')?.[0]).toEqual([false])
    })

    it('emits cancel event when cancel button is clicked', async () => {
      const wrapper = mount(BaseDialog, {
        props: { 
          modelValue: true,
          message: 'Test dialog'
        },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const buttons = wrapper.findAllComponents(BaseButton)
      const cancelButton = buttons.find(btn => btn.text().includes('Cancel'))
      
      await cancelButton?.trigger('click')
      
      expect(wrapper.emitted('cancel')).toBeTruthy()
      expect(wrapper.emitted('update:modelValue')).toBeTruthy()
      expect(wrapper.emitted('update:modelValue')?.[0]).toEqual([false])
    })

    it('does not auto-close when loading after confirm', async () => {
      const wrapper = mount(BaseDialog, {
        props: { 
          modelValue: true,
          message: 'Test dialog',
          loading: true
        },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const buttons = wrapper.findAllComponents(BaseButton)
      const confirmButton = buttons.find(btn => btn.text().includes('OK'))
      
      // Simulate clicking the confirm button
      await confirmButton?.vm.$emit('click')
      
      expect(wrapper.emitted('confirm')).toBeTruthy()
      expect(wrapper.emitted('update:modelValue')).toBeFalsy()
    })

    it('forwards modal events', async () => {
      const wrapper = mount(BaseDialog, {
        props: { 
          modelValue: true,
          message: 'Test dialog'
        },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const modal = wrapper.findComponent(BaseModal)
      
      // Simulate modal events
      await modal.vm.$emit('after-enter')
      await modal.vm.$emit('after-leave')
      await modal.vm.$emit('close')
      
      expect(wrapper.emitted('after-enter')).toBeTruthy()
      expect(wrapper.emitted('after-leave')).toBeTruthy()
      expect(wrapper.emitted('close')).toBeTruthy()
    })
  })

  describe('Layout', () => {
    it('applies correct layout classes with icon', () => {
      const wrapper = mount(BaseDialog, {
        props: { 
          modelValue: true,
          type: 'info',
          message: 'Test dialog'
        },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const content = wrapper.find('.flex.gap-4')
      expect(content.exists()).toBe(true)
      
      const messageContainer = wrapper.find('.flex-1.pt-2')
      expect(messageContainer.exists()).toBe(true)
    })

    it('applies correct layout classes with default icon', () => {
      const wrapper = mount(BaseDialog, {
        props: { 
          modelValue: true,
          message: 'Test dialog'
          // Default type is 'info', so it will have an icon
        },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      // Should have icon-specific layout classes with default type
      const content = wrapper.find('.flex.gap-4')
      expect(content.exists()).toBe(true)
    })

    it('renders footer with correct button layout', () => {
      const wrapper = mount(BaseDialog, {
        props: { 
          modelValue: true,
          message: 'Test dialog'
        },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const footer = wrapper.find('.flex.justify-end.gap-3')
      expect(footer.exists()).toBe(true)
    })
  })

  describe('Modal Props Forwarding', () => {
    it('forwards modal props correctly', () => {
      const wrapper = mount(BaseDialog, {
        props: { 
          modelValue: true,
          message: 'Test dialog',
          width: '500px',
          persistent: true,
          scrollable: true
        },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const modal = wrapper.findComponent(BaseModal)
      expect(modal.props('width')).toBe('500px')
      expect(modal.props('persistent')).toBe(true)
      expect(modal.props('scrollable')).toBe(true)
    })
  })

  describe('Default Props', () => {
    it('uses default props when none provided', () => {
      const wrapper = mount(BaseDialog, {
        props: { 
          modelValue: true,
          message: 'Default dialog'
        },
        global: {
          components: { BaseModal, BaseButton },
          stubs: { Teleport: TeleportStub }
        }
      })
      
      // Default type: info
      const icon = wrapper.find('i.mdi mdi-information')
      expect(icon.exists()).toBe(true)
      
      // Default confirmText: OK
      expect(wrapper.text()).toContain('OK')
      
      // Default cancelText: Cancel
      expect(wrapper.text()).toContain('Cancel')
      
      // Default showCancel: true
      const buttons = wrapper.findAllComponents(BaseButton)
      expect(buttons).toHaveLength(2)
      
      // Default buttonSize: md
      buttons.forEach(button => {
        expect(button.props('size')).toBe('md')
      })
    })
  })
})