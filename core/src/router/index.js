import { useAuthStore } from '@core/stores/auth.js'
import LoginView from '@core/views/auth/LoginView.vue'
import LogoutView from '@core/views/auth/LogoutView.vue'
import VerifyPendingView from '@core/views/auth/VerifyPendingView.vue'
import SettingsView from '@core/views/SettingsView.vue'

export const coreRoutes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/logout',
    name: 'logout',
    component: LogoutView,
  },
  {
    path: '/verify-pending',
    name: 'verify-pending',
    component: VerifyPendingView,
    meta: { requiresAuth: true },
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingsView,
  },
]

const CORE_PAGE_TITLES = {
  login: 'Anmelden',
  logout: 'Abmelden',
  'verify-pending': 'Verifizierung ausstehend',
  settings: 'Einstellungen',
}

export const CONSENT_GATES = [
  { field: 'privacy', path: '/privacy' },
  { field: 'terms', path: '/terms' },
  { field: 'disclaimer', path: '/disclaimer' },
  { field: 'cookies', path: '/cookies' },
]

function guard(to, consentGates) {
  const authStore = useAuthStore()
  if (!authStore.ready) {
    return true
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return '/login'
  }

  if (!authStore.isAuthenticated || to.name === 'logout') {
    return true
  }

  const consent = authStore.user.consent
  for (const gate of consentGates) {
    if (!consent[gate.field]) {
      return to.path === gate.path ? true : gate.path
    }
  }

  if (to.name === 'verify-pending') {
    return authStore.user.verified ? '/' : true
  }

  if (!authStore.user.verified) {
    return '/verify-pending'
  }

  if (to.meta.permission && !authStore.user[to.meta.permission]) {
    return '/'
  }

  return true
}

export function installGuards(router, appName, pageTitles, consentGates = []) {
  const titles = { ...CORE_PAGE_TITLES, ...pageTitles }
  router.beforeEach((to) => guard(to, consentGates))
  router.afterEach((to) => {
    const title = titles[to.name]
    document.title = title ? `${title} – ${appName}` : appName
  })
}
