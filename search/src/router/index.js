import { createRouter, createWebHistory } from 'vue-router'

import { coreRoutes, installGuards } from '@core/router/index.js'
import SearchView from '@/views/SearchView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      name: 'search',
      component: SearchView,
    },
    {
      path: '/results',
      name: 'results',
      component: () => import('@/views/ResultsView.vue'),
    },
    ...coreRoutes.filter((route) => route.name !== 'settings'),
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/SettingsView.vue'),
    },
  ],
})

installGuards(router, 'Suche', { search: 'Suche', results: 'Ergebnisse' })

export default router
