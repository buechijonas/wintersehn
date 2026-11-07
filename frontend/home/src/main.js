import '@fontsource/manrope/700.css'
import './assets/main.css'
import '@core/lib/theme.js'
import '@core/lib/dyslexia.js'
import '@core/lib/contrast.js'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from '@core/App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.provide('app', {
  title: 'Home',
  layout: 'sidebar',
  navigationItems: [],
  legalLinks: [],
  hideBreadcrumbs: true,
})

app.mount('#app')
