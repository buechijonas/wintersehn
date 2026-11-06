import { createRouter, createWebHistory } from 'vue-router'

import { coreRoutes, installAdminGuard, installGuards } from '@core/router/index.js'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    ...coreRoutes,
  ],
})

installAdminGuard(router, import.meta.env.VITE_WINTERSEHN_URL ?? 'https://wintersehn.ch')
installGuards(router, 'Home', { home: 'Home' })

export default router
