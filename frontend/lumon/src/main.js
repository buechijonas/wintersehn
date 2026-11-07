import '@fontsource/manrope/700.css'
import '@fontsource/bebas-neue/400.css'
import './assets/main.css'
import '@core/lib/theme.js'
import '@core/lib/dyslexia.js'
import '@core/lib/contrast.js'
import { lumonStyle } from './lib/style.js'

import { computed, createApp } from 'vue'
import { createPinia } from 'pinia'

import App from '@core/App.vue'
import router from './router'
import { navigationItems } from './data/navigation.js'
import StyleSettings from './components/StyleSettings.vue'
import packageJson from '../package.json'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.provide('app', {
  title: 'LUMON',
  layout: 'sidebar',
  version: packageJson.version,
  navigationItems,
  legalLinks: [],
  appearanceSettings: StyleSettings,
  topNavigation: computed(() => lumonStyle.value === 'netflix'),
  appSwitches: [
    { label: 'Suche', url: import.meta.env.VITE_SEARCH_URL ?? 'https://search.wintersehn.ch' },
    { label: 'Wintersehn', url: import.meta.env.VITE_WINTERSEHN_URL ?? 'https://wintersehn.ch' },
    { label: 'ATLAS', url: import.meta.env.VITE_ATLAS_URL ?? 'https://atlas.wintersehn.ch' },
  ],
})

app.mount('#app')
