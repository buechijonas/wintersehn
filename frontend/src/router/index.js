import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores/auth.js'
import HomeView from '@/views/HomeView.vue'
import MediaView from '@/views/MediaView.vue'
import AboutView from '@/views/AboutView.vue'
import EthosView from '@/views/EthosView.vue'
import CvView from '@/views/CvView.vue'
import CvSectionView from '@/views/CvSectionView.vue'
import CountriesView from '@/views/CountriesView.vue'
import ProjectsView from '@/views/ProjectsView.vue'
import ImpressumView from '@/views/legal/ImpressumView.vue'
import PrivacyView from '@/views/legal/PrivacyView.vue'
import TermsView from '@/views/legal/TermsView.vue'
import DisclaimerView from '@/views/legal/DisclaimerView.vue'
import CookieView from '@/views/legal/CookieView.vue'
import LoginView from '@/views/auth/LoginView.vue'
import SignupView from '@/views/auth/SignupView.vue'
import LogoutView from '@/views/auth/LogoutView.vue'
import VerifyPendingView from '@/views/auth/VerifyPendingView.vue'
import SettingsView from '@/views/SettingsView.vue'
import AccountEditView from '@/views/AccountEditView.vue'
import PasswordEditView from '@/views/PasswordEditView.vue'
import AdminView from '@/views/AdminView.vue'
import AdminContentView from '@/views/AdminContentView.vue'
import AdminLegalView from '@/views/AdminLegalView.vue'
import AdminAddressView from '@/views/AdminAddressView.vue'
import AdminEthosView from '@/views/AdminEthosView.vue'
import AdminEthosItemCreateView from '@/views/AdminEthosItemCreateView.vue'
import AdminCountriesView from '@/views/AdminCountriesView.vue'
import AdminCountriesItemCreateView from '@/views/AdminCountriesItemCreateView.vue'
import AdminCvView from '@/views/AdminCvView.vue'
import AdminCvSectionView from '@/views/AdminCvSectionView.vue'
import AdminCvEntryCreateView from '@/views/AdminCvEntryCreateView.vue'
import AdminMediaView from '@/views/AdminMediaView.vue'
import AdminMediaItemCreateView from '@/views/AdminMediaItemCreateView.vue'
import AdminRolesView from '@/views/AdminRolesView.vue'
import AdminUsersView from '@/views/AdminUsersView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { activeNavigation: 'dashboard' },
    },
    {
      path: '/media',
      name: 'media',
      component: MediaView,
      meta: { activeNavigation: 'media' },
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
      meta: { requiresAuth: true, permission: 'can_view_about', activeNavigation: 'about' },
    },
    {
      path: '/ethos',
      name: 'ethos',
      component: EthosView,
      meta: { requiresAuth: true, permission: 'can_view_ethos', activeNavigation: 'ethos' },
    },
    {
      path: '/cv',
      name: 'cv',
      component: CvView,
      meta: { requiresAuth: true, permission: 'can_view_cv', activeNavigation: 'cv' },
    },
    {
      path: '/cv/:key',
      name: 'cv-section',
      component: CvSectionView,
      meta: { requiresAuth: true, permission: 'can_view_cv', activeNavigation: 'cv' },
    },
    {
      path: '/countries',
      name: 'countries',
      component: CountriesView,
      meta: {
        requiresAuth: true,
        permission: 'can_view_countries',
        activeNavigation: 'countries',
      },
    },
    {
      path: '/projects',
      name: 'projects',
      component: ProjectsView,
      meta: { requiresAuth: true, activeNavigation: 'projects' },
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
      path: '/cookies',
      name: 'cookies',
      component: CookieView,
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
      meta: { requiresAuth: true },
    },
    {
      path: '/settings/account',
      name: 'settings-account',
      component: AccountEditView,
      meta: { requiresAuth: true },
    },
    {
      path: '/settings/password',
      name: 'settings-password',
      component: PasswordEditView,
      meta: { requiresAuth: true },
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/address',
      name: 'admin-address',
      component: AdminAddressView,
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/roles',
      name: 'admin-roles',
      component: AdminRolesView,
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/users',
      name: 'admin-users',
      component: AdminUsersView,
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/ethos',
      name: 'admin-ethos',
      component: AdminEthosView,
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/ethos/:section/create',
      name: 'admin-ethos-item-create',
      component: AdminEthosItemCreateView,
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/countries',
      name: 'admin-countries',
      component: AdminCountriesView,
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/countries/:section/create',
      name: 'admin-countries-item-create',
      component: AdminCountriesItemCreateView,
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/cv',
      name: 'admin-cv',
      component: AdminCvView,
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/cv/:key/create',
      name: 'admin-cv-entry-create',
      component: AdminCvEntryCreateView,
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/cv/:key',
      name: 'admin-cv-section',
      component: AdminCvSectionView,
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/media',
      name: 'admin-media',
      component: AdminMediaView,
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/media/:section/create',
      name: 'admin-media-item-create',
      component: AdminMediaItemCreateView,
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/impressum',
      name: 'admin-impressum',
      component: AdminLegalView,
      props: { contentKey: 'impressum', label: 'Impressum' },
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/privacy',
      name: 'admin-privacy',
      component: AdminLegalView,
      props: { contentKey: 'privacy', label: 'Datenschutzerklärung' },
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/cookies',
      name: 'admin-cookies',
      component: AdminLegalView,
      props: { contentKey: 'cookies', label: 'Cookierichtlinie' },
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/terms',
      name: 'admin-terms',
      component: AdminLegalView,
      props: { contentKey: 'terms', label: 'Nutzungsrichtlinien' },
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/disclaimer',
      name: 'admin-disclaimer',
      component: AdminLegalView,
      props: { contentKey: 'disclaimer', label: 'Haftungsausschluss' },
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/:key',
      name: 'admin-content',
      component: AdminContentView,
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
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

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return '/login'
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
})

export default router
