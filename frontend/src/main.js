import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'

// Импорт базовых компонентов
import { BaseButton } from '@/components/base'

// Import Element Plus CSS first
import 'element-plus/dist/index.css'
// Import our custom styles after Element Plus
import './styles/main.css'

const app = createApp(App)

// Register Element Plus icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// Регистрация базовых компонентов глобально
app.component('BaseButton', BaseButton)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app')
