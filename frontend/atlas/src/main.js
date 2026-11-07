import '@fontsource/manrope/700.css'
import './assets/main.css'
import '@core/lib/theme.js'
import '@core/lib/dyslexia.js'
import '@core/lib/contrast.js'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from '@core/App.vue'
import router from './router'
import { navigationItems } from './data/navigation.js'
import packageJson from '../package.json'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.provide('app', {
  title: 'ATLAS',
  layout: 'sidebar',
  version: packageJson.version,
  navigationItems,
  legalLinks: [],
  appSwitches: [
    { label: 'Suche', url: import.meta.env.VITE_SEARCH_URL ?? 'https://search.wintersehn.ch' },
    { label: 'Wintersehn', url: import.meta.env.VITE_WINTERSEHN_URL ?? 'https://wintersehn.ch' },
  ],
})

app.mount('#app')
