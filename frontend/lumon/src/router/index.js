import { createRouter, createWebHistory } from 'vue-router'

import { coreRoutes, installAdminGuard, installGuards } from '@core/router/index.js'
import SearchView from '@/views/SearchView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      name: 'search',
      component: SearchView,
      meta: { activeNavigation: 'search' },
    },
    {
      path: '/series',
      name: 'series',
      component: () => import('@/views/BrowseView.vue'),
      meta: { activeNavigation: 'tv', mediaType: 'tv' },
    },
    {
      path: '/movies',
      name: 'movies',
      component: () => import('@/views/BrowseView.vue'),
      meta: { activeNavigation: 'movie', mediaType: 'movie' },
    },
    {
      path: '/tv/:id',
      name: 'series-title',
      component: () => import('@/views/TitleView.vue'),
      meta: { activeNavigation: 'tv', mediaType: 'tv' },
    },
    {
      path: '/movie/:id',
      name: 'movie-title',
      component: () => import('@/views/TitleView.vue'),
      meta: { activeNavigation: 'movie', mediaType: 'movie' },
    },
    {
      path: '/play/:id',
      name: 'play',
      component: () => import('@/views/PlayerView.vue'),
      meta: { activeNavigation: null },
    },
    ...coreRoutes,
  ],
})

installAdminGuard(router, import.meta.env.VITE_WINTERSEHN_URL ?? 'https://wintersehn.ch')
installGuards(router, 'LUMON', {
  search: 'Suche',
  series: 'Serien',
  movies: 'Filme',
  'series-title': 'Serie',
  'movie-title': 'Film',
  play: 'Abspielen',
})

export default router
