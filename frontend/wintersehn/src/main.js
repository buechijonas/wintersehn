import './assets/main.css'
import '@core/lib/theme.js'
import '@core/lib/dyslexia.js'
import '@core/lib/contrast.js'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from '@core/App.vue'
import router from './router'
import { navigationItems } from './data/navigation.js'
import { legalLinks } from './data/legal.js'
import packageJson from '../package.json'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.provide('app', {
  name: packageJson.name,
  title: 'Wintersehn',
  layout: 'sidebar',
  version: packageJson.version,
  navigationItems,
  legalLinks,
  hasAdmin: true,
  appSwitches: [
    { label: 'Suche', url: import.meta.env.VITE_SEARCH_URL ?? 'https://search.wintersehn.ch' },
    {
      label: 'ATLAS',
      url: import.meta.env.VITE_ATLAS_URL ?? 'https://atlas.wintersehn.ch',
      permission: 'can_view_admin',
    },
  ],
  displayName: (user) => (user?.verified ? 'Jonas S. Büchi' : 'Wintersehn'),
})

app.mount('#app')
