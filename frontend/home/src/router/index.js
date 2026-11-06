import { createRouter, createWebHistory } from 'vue-router'

import { coreRoutes, installGuards } from '@core/router/index.js'
import { useAuthStore } from '@core/stores/auth.js'
import HomeView from '@/views/HomeView.vue'

const WINTERSEHN_URL = import.meta.env.VITE_WINTERSEHN_URL ?? 'https://wintersehn.ch'
const PUBLIC_ROUTES = new Set(['login', 'logout'])

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

router.beforeEach((to) => {
  const authStore = useAuthStore()
  if (!authStore.ready || PUBLIC_ROUTES.has(to.name) || authStore.user?.can_view_admin) {
    return true
  }
  if (!authStore.isAuthenticated) {
    return '/login'
  }
  window.location.replace(WINTERSEHN_URL)
  return false
})

installGuards(router, 'Home', { home: 'Home' })

export default router
