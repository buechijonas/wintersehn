import '@fontsource/manrope/700.css'
import './assets/main.css'
import '@core/lib/theme.js'
import '@core/lib/dyslexia.js'
import '@core/lib/contrast.js'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.provide('app', {
  footerLinks: [],
  hideBreadcrumbs: true,
  appSwitches: [
    {
      label: 'swissfy',
      url: import.meta.env.VITE_SWISSFY_URL ?? 'https://swissfy.ch',
      icon: '/icons/apps/swissfy.png',
    },
    { label: 'Wintersehn', url: import.meta.env.VITE_WINTERSEHN_URL ?? 'https://wintersehn.ch' },
    {
      label: 'MONOLITH',
      url: import.meta.env.VITE_MONOLITH_URL ?? 'https://monolith.wintersehn.ch',
      permission: 'can_view_admin',
    },
  ],
})

app.mount('#app')
