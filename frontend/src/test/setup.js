import { vi } from 'vitest'

// Mock Element Plus components globally
vi.mock('element-plus', () => ({
  ElMessage: {
    success: vi.fn(),
    error: vi.fn(),
    warning: vi.fn(),
    info: vi.fn()
  },
  ElMessageBox: {
    confirm: vi.fn(),
    alert: vi.fn()
  },
  ElNotification: {
    success: vi.fn(),
    error: vi.fn(),
    warning: vi.fn(),
    info: vi.fn()
  }
}))

// Mock Vue Router
vi.mock('vue-router', () => ({
  useRoute: () => ({
    params: { id: 'test-id' },
    query: {}
  }),
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    go: vi.fn()
  })
}))

// Mock environment variables
vi.mock('import.meta.env', () => ({
  VITE_API_URL: 'http://localhost:8000',
  MODE: 'test'
}))

// Global test utilities
global.console = {
  ...console,
  // Suppress console warnings in tests
  warn: vi.fn(),
  error: vi.fn()
}
