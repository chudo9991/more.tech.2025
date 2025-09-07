import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Styles
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'

// Custom theme configuration
const customTheme = {
  dark: false,
  colors: {
    // Primary colors matching TailwindCSS config
    primary: '#0ea5e9',
    'primary-darken-1': '#0284c7',
    'primary-lighten-1': '#38bdf8',
    
    // Secondary colors
    secondary: '#64748b',
    'secondary-darken-1': '#475569',
    'secondary-lighten-1': '#94a3b8',
    
    // Semantic colors
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    info: '#3b82f6',
    
    // Surface colors
    surface: '#ffffff',
    'surface-variant': '#f8fafc',
    'on-surface': '#0f172a',
    'on-surface-variant': '#64748b',
    
    // Background
    background: '#f8fafc',
    'on-background': '#0f172a',
  }
}

const darkTheme = {
  dark: true,
  colors: {
    // Primary colors
    primary: '#38bdf8',
    'primary-darken-1': '#0ea5e9',
    'primary-lighten-1': '#7dd3fc',
    
    // Secondary colors
    secondary: '#94a3b8',
    'secondary-darken-1': '#64748b',
    'secondary-lighten-1': '#cbd5e1',
    
    // Semantic colors
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    info: '#3b82f6',
    
    // Surface colors
    surface: '#1e293b',
    'surface-variant': '#334155',
    'on-surface': '#f1f5f9',
    'on-surface-variant': '#cbd5e1',
    
    // Background
    background: '#0f172a',
    'on-background': '#f1f5f9',
  }
}

export default createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    defaultTheme: 'customTheme',
    themes: {
      customTheme,
      darkTheme,
    },
    variations: {
      colors: ['primary', 'secondary', 'success', 'warning', 'error', 'info'],
      lighten: 5,
      darken: 5,
    },
  },
  defaults: {
    // Global component defaults
    VBtn: {
      style: 'text-transform: none;', // Disable uppercase transformation
      rounded: 'md',
    },
    VCard: {
      rounded: 'lg',
      elevation: 2,
    },
    VTextField: {
      variant: 'outlined',
      density: 'comfortable',
    },
    VSelect: {
      variant: 'outlined',
      density: 'comfortable',
    },
    VTextarea: {
      variant: 'outlined',
      density: 'comfortable',
    },
    VCheckbox: {
      density: 'comfortable',
    },
    VRadio: {
      density: 'comfortable',
    },
    VSwitch: {
      density: 'comfortable',
    },
    VDataTable: {
      density: 'comfortable',
    },
  },
  display: {
    mobileBreakpoint: 'sm',
    thresholds: {
      xs: 0,
      sm: 640,
      md: 768,
      lg: 1024,
      xl: 1280,
      xxl: 1536,
    },
  },
})