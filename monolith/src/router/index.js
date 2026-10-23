import { createRouter, createWebHistory } from 'vue-router'

import { coreRoutes, installGuards } from '@core/router/index.js'
import { useAuthStore } from '@core/stores/auth.js'
import HomeView from '@/views/HomeView.vue'
import DossierView from '@/views/DossierView.vue'
import DossierEditView from '@/views/DossierEditView.vue'
import NetworkView from '@/views/NetworkView.vue'
import TrustView from '@/views/TrustView.vue'
import EventView from '@/views/EventView.vue'
import EventEditView from '@/views/EventEditView.vue'
import ShareEditView from '@/views/ShareEditView.vue'
import SharedDossierView from '@/views/SharedDossierView.vue'
import SharedLinkView from '@/views/SharedLinkView.vue'
import SharedListView from '@/views/SharedListView.vue'

const WINTERSEHN_URL = import.meta.env.VITE_WINTERSEHN_URL ?? 'https://wintersehn.ch'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { activeNavigation: 'dossiers' },
    },
    {
      path: '/dossiers/:uuid',
      name: 'dossier',
      component: DossierView,
      meta: { activeNavigation: 'dossiers' },
    },
    {
      path: '/dossiers/:uuid/edit',
      name: 'dossier-edit',
      component: DossierEditView,
      meta: { activeNavigation: 'dossiers' },
    },
    {
      path: '/dossiers/:uuid/events/:event',
      name: 'event',
      component: EventView,
      meta: { activeNavigation: 'dossiers' },
    },
    {
      path: '/dossiers/:uuid/events/:event/edit',
      name: 'event-edit',
      component: EventEditView,
      meta: { activeNavigation: 'dossiers' },
    },
    {
      path: '/dossiers/:uuid/shares/:share',
      name: 'share-edit',
      component: ShareEditView,
      meta: { activeNavigation: 'dossiers' },
    },
    {
      path: '/shared',
      name: 'shared',
      component: SharedListView,
      meta: { activeNavigation: 'shared' },
    },
    {
      path: '/shared/:share',
      name: 'shared-dossier',
      component: SharedDossierView,
      meta: { activeNavigation: 'shared' },
    },
    {
      path: '/share/:token',
      name: 'shared-link',
      component: SharedLinkView,
      meta: { public: true },
    },
    {
      path: '/network',
      name: 'network',
      component: NetworkView,
      meta: { activeNavigation: 'network' },
    },
    {
      path: '/trust',
      name: 'trust',
      component: TrustView,
      meta: { activeNavigation: 'trust' },
    },
    ...coreRoutes,
  ],
})

const PAGE_TITLES = {
  home: 'Personalakten',
  dossier: 'Personalakte',
  'dossier-edit': 'Meta bearbeiten',
  network: 'Netzwerk',
  trust: 'Vertrauenskreise',
  event: 'Ereignis',
  'event-edit': 'Ereignis bearbeiten',
  'share-edit': 'Freigabe',
  shared: 'Mit mir geteilt',
  'shared-dossier': 'Geteilte Akte',
  'shared-link': 'Geteilte Akte',
}

const SHARED_ROUTES = new Set(['shared', 'shared-dossier', 'settings', 'logout'])

function canViewShared(user) {
  return Boolean(user?.verified && Object.values(user.consent).every(Boolean))
}

function hasAccess(user) {
  return canViewShared(user) && user.can_view_monolith
}

router.beforeEach((to) => {
  const authStore = useAuthStore()
  if (to.meta.public || !authStore.ready || hasAccess(authStore.user)) {
    return true
  }
  if (canViewShared(authStore.user)) {
    return SHARED_ROUTES.has(to.name) || { name: 'shared' }
  }
  window.location.replace(WINTERSEHN_URL)
  return false
})

installGuards(router, 'MONOLITH', PAGE_TITLES)

export default router
