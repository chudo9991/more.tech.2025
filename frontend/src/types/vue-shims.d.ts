// Vue module declarations
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// Explicit Vue module declaration to fix TypeScript resolution
declare module 'vue' {
  export * from '@vue/runtime-dom'
  export * from '@vue/reactivity'
  export * from '@vue/runtime-core'
  
  // Explicitly declare lifecycle functions to ensure they're available
  export declare const onMounted: (hook: Function, target?: any) => void
  export declare const onUnmounted: (hook: Function, target?: any) => void
  export declare const onBeforeMount: (hook: Function, target?: any) => void
  export declare const onBeforeUnmount: (hook: Function, target?: any) => void
}

// Vuetify module declarations
declare module 'vuetify' {
  import type { App } from 'vue'
  
  export interface VuetifyOptions {
    components?: Record<string, any>
    directives?: Record<string, any>
    icons?: any
    theme?: any
    defaults?: any
    display?: any
    locale?: any
    date?: any
  }
  
  export function createVuetify(options?: VuetifyOptions): {
    install(app: App): void
  }
}

declare module 'vuetify/components' {
  export * from 'vuetify/lib/components'
}

declare module 'vuetify/directives' {
  export * from 'vuetify/lib/directives'
}

declare module 'vuetify/iconsets/mdi' {
  export const aliases: Record<string, string>
  export const mdi: any
}

// TailwindCSS module declarations
declare module 'tailwindcss/plugin' {
  const plugin: any
  export default plugin
}

// Chart.js module declarations
declare module 'chart.js' {
  export * from 'chart.js/dist/chart.js'
}

declare module 'vue-chartjs' {
  import type { DefineComponent } from 'vue'
  export const Line: DefineComponent
  export const Bar: DefineComponent
  export const Doughnut: DefineComponent
  export const Pie: DefineComponent
  export const PolarArea: DefineComponent
  export const Radar: DefineComponent
  export const Scatter: DefineComponent
  export const Bubble: DefineComponent
}

// Pinia store type augmentation
declare module 'pinia' {
  export interface DefineStoreOptionsBase<S, Store> {
    // Add any custom store options here
  }
}

// Vue Router type augmentation
declare module 'vue-router' {
  interface RouteMeta {
    title?: string
    requiresAuth?: boolean
    roles?: string[]
    layout?: string
    icon?: string
    hidden?: boolean
    breadcrumb?: boolean
  }
}

// Global component types
declare module '@vue/runtime-core' {
  export interface GlobalComponents {
    // Register global components here for better TypeScript support
    RouterLink: typeof import('vue-router')['RouterLink']
    RouterView: typeof import('vue-router')['RouterView']
  }
  
  export interface ComponentCustomProperties {
    // Add global properties here
    $vuetify: any
  }
}

// Environment variables
declare module 'process' {
  global {
    namespace NodeJS {
      interface ProcessEnv {
        NODE_ENV: 'development' | 'production' | 'test'
        VITE_API_BASE_URL?: string
        VITE_APP_TITLE?: string
        VITE_APP_VERSION?: string
      }
    }
  }
}

// Vite specific types
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_APP_TITLE: string
  readonly VITE_APP_VERSION: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

declare module '@vue/runtime-core' {
  export interface GlobalProperties {
    // Add global properties here if needed
  }
}

// Vite environment variables
interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_APP_TITLE: string
  // Add more env variables as needed
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}