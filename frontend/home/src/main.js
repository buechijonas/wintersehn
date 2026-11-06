import '@fontsource/manrope/700.css'
import './assets/main.css'
import '@core/lib/theme.js'
import '@core/lib/dyslexia.js'
import '@core/lib/contrast.js'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { apps } from '@/data/apps.js'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.provide('app', {
  footerLinks: [],
  hideBreadcrumbs: true,
  appSwitches: apps,
})

app.mount('#app')
