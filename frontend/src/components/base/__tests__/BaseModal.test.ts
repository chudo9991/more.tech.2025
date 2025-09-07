import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseModal from '../BaseModal.vue'

// Mock Teleport for testing
const TeleportStub = {
  name: 'Teleport',
  props: ['to'],
  template: '<div><slot /></div>'
}

describe('BaseModal', () => {
  let originalBodyOverflow: string

  beforeEach(() => {
    // Store original body overflow
    originalBodyOverflow = document.body.style.overflow
    
    // Mock focus methods
    HTMLElement.prototype.focus = vi.fn()
    
    // Mock querySelector for focus management
    document.querySelector = vi.fn()
    document.querySelectorAll = vi.fn(() => [] as any)
  })

  afterEach(() => {
    // Restore body overflow
    document.body.style.overflow = originalBodyOverflow
    
    // Clear all mocks
    vi.clearAllMocks()
  })

  describe('Rendering', () => {
    it('renders modal when modelValue is true', () => {
      const wrapper = mount(BaseModal, {
        props: { modelValue: true },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      expect(wrapper.text()).toContain('Modal content')
      expect(wrapper.find('[role="dialog"]').exists()).toBe(true)
    })

    it('does not render modal when modelValue is false', () => {
      const wrapper = mount(BaseModal, {
        props: { modelValue: false },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      expect(wrapper.find('[role="dialog"]').exists()).toBe(false)
    })

    it('renders title when provided', () => {
      const wrapper = mount(BaseModal, {
        props: { 
          modelValue: true,
          title: 'Test Modal'
        },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const title = wrapper.find('h2')
      expect(title.exists()).toBe(true)
      expect(title.text()).toBe('Test Modal')
    })

    it('renders custom header slot', () => {
      const wrapper = mount(BaseModal, {
        props: { modelValue: true },
        slots: { 
          header: '<div class="custom-header">Custom Header</div>',
          default: 'Modal content'
        },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      expect(wrapper.find('.custom-header').exists()).toBe(true)
      expect(wrapper.text()).toContain('Custom Header')
    })

    it('renders footer slot', () => {
      const wrapper = mount(BaseModal, {
        props: { modelValue: true },
        slots: { 
          default: 'Modal content',
          footer: '<div class="custom-footer">Footer content</div>'
        },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      expect(wrapper.find('.custom-footer').exists()).toBe(true)
      expect(wrapper.text()).toContain('Footer content')
    })
  })

  describe('Close Button', () => {
    it('renders close button by default', () => {
      const wrapper = mount(BaseModal, {
        props: { 
          modelValue: true,
          title: 'Test Modal'
        },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const closeButton = wrapper.find('button')
      expect(closeButton.exists()).toBe(true)
      expect(closeButton.find('i.mdi mdi-close').exists()).toBe(true)
    })

    it('hides close button when showCloseButton is false', () => {
      const wrapper = mount(BaseModal, {
        props: { 
          modelValue: true,
          title: 'Test Modal',
          showCloseButton: false
        },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const closeButton = wrapper.find('button')
      expect(closeButton.exists()).toBe(false)
    })

    it('emits close event when close button is clicked', async () => {
      const wrapper = mount(BaseModal, {
        props: { 
          modelValue: true,
          title: 'Test Modal'
        },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const closeButton = wrapper.find('button')
      await closeButton.trigger('click')
      
      expect(wrapper.emitted('update:modelValue')).toBeTruthy()
      expect(wrapper.emitted('update:modelValue')?.[0]).toEqual([false])
      expect(wrapper.emitted('close')).toBeTruthy()
    })
  })

  describe('Backdrop Interaction', () => {
    it('closes modal when backdrop is clicked (non-persistent)', async () => {
      const wrapper = mount(BaseModal, {
        props: { 
          modelValue: true,
          persistent: false
        },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const overlay = wrapper.find('.fixed.inset-0')
      await overlay.trigger('click')
      
      expect(wrapper.emitted('update:modelValue')).toBeTruthy()
      expect(wrapper.emitted('update:modelValue')?.[0]).toEqual([false])
    })

    it('does not close modal when backdrop is clicked (persistent)', async () => {
      const wrapper = mount(BaseModal, {
        props: { 
          modelValue: true,
          persistent: true
        },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const overlay = wrapper.find('.fixed.inset-0')
      await overlay.trigger('click')
      
      expect(wrapper.emitted('update:modelValue')).toBeFalsy()
    })

    it('does not close when modal content is clicked', async () => {
      const wrapper = mount(BaseModal, {
        props: { modelValue: true },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const modal = wrapper.find('[role="dialog"]')
      await modal.trigger('click')
      
      expect(wrapper.emitted('update:modelValue')).toBeFalsy()
    })
  })

  describe('Keyboard Interaction', () => {
    it('closes modal when Escape key is pressed (non-persistent)', async () => {
      const wrapper = mount(BaseModal, {
        props: { 
          modelValue: true,
          persistent: false
        },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const overlay = wrapper.find('.fixed.inset-0')
      await overlay.trigger('keydown.esc')
      
      expect(wrapper.emitted('update:modelValue')).toBeTruthy()
      expect(wrapper.emitted('update:modelValue')?.[0]).toEqual([false])
    })

    it('does not close when Escape is pressed (persistent)', async () => {
      const wrapper = mount(BaseModal, {
        props: { 
          modelValue: true,
          persistent: true
        },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const overlay = wrapper.find('.fixed.inset-0')
      await overlay.trigger('keydown.esc')
      
      expect(wrapper.emitted('update:modelValue')).toBeFalsy()
    })
  })

  describe('Sizing', () => {
    it('applies custom width and maxWidth', () => {
      const wrapper = mount(BaseModal, {
        props: { 
          modelValue: true,
          width: '600px',
          maxWidth: '800px'
        },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const modal = wrapper.find('[role="dialog"]')
      expect(modal.classes()).toContain('w-[600px]')
      expect(modal.classes()).toContain('max-w-[800px]')
    })

    it('applies fullscreen classes', () => {
      const wrapper = mount(BaseModal, {
        props: { 
          modelValue: true,
          fullscreen: true
        },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const modal = wrapper.find('[role="dialog"]')
      expect(modal.classes()).toContain('w-full')
      expect(modal.classes()).toContain('h-full')
      expect(modal.classes()).toContain('max-w-none')
      expect(modal.classes()).toContain('rounded-none')
    })

    it('applies default max-width when none specified', () => {
      const wrapper = mount(BaseModal, {
        props: { modelValue: true },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const modal = wrapper.find('[role="dialog"]')
      expect(modal.classes()).toContain('max-w-lg')
    })
  })

  describe('Scrollable Mode', () => {
    it('applies scrollable classes when scrollable is true', () => {
      const wrapper = mount(BaseModal, {
        props: { 
          modelValue: true,
          scrollable: true,
          title: 'Scrollable Modal'
        },
        slots: { 
          default: 'Modal content',
          footer: 'Footer content'
        },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const modal = wrapper.find('[role="dialog"]')
      const header = wrapper.find('.flex.items-center.justify-between')
      const content = wrapper.find('[id^="modal-content-"]')
      
      expect(modal.classes()).toContain('flex')
      expect(modal.classes()).toContain('flex-col')
      expect(header.classes()).toContain('border-b')
      expect(content.classes()).toContain('flex-1')
      expect(content.classes()).toContain('overflow-y-auto')
    })
  })

  describe('Accessibility', () => {
    it('sets proper ARIA attributes', () => {
      const wrapper = mount(BaseModal, {
        props: { 
          modelValue: true,
          title: 'Accessible Modal'
        },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const modal = wrapper.find('[role="dialog"]')
      const title = wrapper.find('h2')
      const content = wrapper.find('[id^="modal-content-"]')
      
      expect(modal.attributes('role')).toBe('dialog')
      expect(modal.attributes('aria-modal')).toBe('true')
      expect(modal.attributes('aria-labelledby')).toBe(title.attributes('id'))
      expect(modal.attributes('aria-describedby')).toBe(content.attributes('id'))
      expect(modal.attributes('tabindex')).toBe('-1')
    })

    it('sets proper aria-label for close button', () => {
      const wrapper = mount(BaseModal, {
        props: { 
          modelValue: true,
          title: 'Test Modal',
          closeAriaLabel: 'Close this modal'
        },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const closeButton = wrapper.find('button')
      expect(closeButton.attributes('aria-label')).toBe('Close this modal')
    })
  })

  describe('Z-Index', () => {
    it('applies custom z-index', () => {
      const wrapper = mount(BaseModal, {
        props: { 
          modelValue: true,
          zIndex: 2000
        },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const overlay = wrapper.find('.fixed.inset-0')
      expect(overlay.classes()).toContain('z-[2000]')
    })

    it('uses default z-index when none specified', () => {
      const wrapper = mount(BaseModal, {
        props: { modelValue: true },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const overlay = wrapper.find('.fixed.inset-0')
      expect(overlay.classes()).toContain('z-[1050]')
    })
  })

  describe('Events', () => {
    it('emits after-enter event', async () => {
      const wrapper = mount(BaseModal, {
        props: { modelValue: true },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      // Simulate transition end
      await wrapper.vm.handleAfterEnter()
      
      expect(wrapper.emitted('after-enter')).toBeTruthy()
    })

    it('emits after-leave event', async () => {
      const wrapper = mount(BaseModal, {
        props: { modelValue: false },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      // Simulate transition end
      await wrapper.vm.handleAfterLeave()
      
      expect(wrapper.emitted('after-leave')).toBeTruthy()
    })
  })

  describe('Body Scroll Lock', () => {
    it('locks body scroll when modal opens', async () => {
      mount(BaseModal, {
        props: { modelValue: true },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      expect(document.body.style.overflow).toBe('hidden')
    })

    it('unlocks body scroll when modal closes', async () => {
      const wrapper = mount(BaseModal, {
        props: { modelValue: true },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      await wrapper.setProps({ modelValue: false })
      
      expect(document.body.style.overflow).toBe('')
    })
  })

  describe('Default Props', () => {
    it('uses default props when none provided', () => {
      const wrapper = mount(BaseModal, {
        props: { modelValue: true },
        slots: { default: 'Modal content' },
        global: {
          stubs: { Teleport: TeleportStub }
        }
      })
      
      const modal = wrapper.find('[role="dialog"]')
      const overlay = wrapper.find('.fixed.inset-0')
      
      // Default persistent: false (can be closed)
      // Default showCloseButton: true
      expect(wrapper.find('button').exists()).toBe(true)
      
      // Default z-index: 1050
      expect(overlay.classes()).toContain('z-[1050]')
      
      // Default scrollable: false
      expect(modal.classes()).not.toContain('flex-col')
    })
  })
})