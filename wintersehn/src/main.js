import './assets/main.css'
import '@core/lib/theme.js'
import '@core/lib/dyslexia.js'
import '@core/lib/contrast.js'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from '@core/App.vue'
import router from './router'
import { navigationItems } from './data/navigation.js'
import { footerLinks } from './data/footer.js'
import packageJson from '../package.json'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.provide('app', {
  name: packageJson.name,
  version: packageJson.version,
  navigationItems,
  footerLinks,
  hasAdmin: true,
  displayName: (user) => (user?.verified ? 'Jonas S. Büchi' : packageJson.name),
})

app.mount('#app')
