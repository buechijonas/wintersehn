import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores/auth.js'
import HomeView from '@/views/HomeView.vue'
import MediaView from '@/views/MediaView.vue'
import ImpressumView from '@/views/legal/ImpressumView.vue'
import PrivacyView from '@/views/legal/PrivacyView.vue'
import TermsView from '@/views/legal/TermsView.vue'
import DisclaimerView from '@/views/legal/DisclaimerView.vue'
import LoginView from '@/views/auth/LoginView.vue'
import SignupView from '@/views/auth/SignupView.vue'
import LogoutView from '@/views/auth/LogoutView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/media',
      name: 'media',
      component: MediaView,
    },
    {
      path: '/impressum',
      name: 'impressum',
      component: ImpressumView,
    },
    {
      path: '/privacy',
      name: 'privacy',
      component: PrivacyView,
    },
    {
      path: '/terms',
      name: 'terms',
      component: TermsView,
    },
    {
      path: '/disclaimer',
      name: 'disclaimer',
      component: DisclaimerView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogoutView,
    },
  ],
})

const CONSENT_GATES = [
  { field: 'privacy', path: '/privacy' },
  { field: 'terms', path: '/terms' },
  { field: 'disclaimer', path: '/disclaimer' },
]

router.beforeEach(async (to) => {
  const authStore = useAuthStore()
  if (!authStore.ready) {
    await authStore.fetchMe()
  }

  if (!authStore.isAuthenticated || to.name === 'logout') {
    return true
  }

  const consent = authStore.user.consent
  for (const gate of CONSENT_GATES) {
    if (!consent[gate.field]) {
      return to.path === gate.path ? true : gate.path
    }
  }

  return true
})

export default router
