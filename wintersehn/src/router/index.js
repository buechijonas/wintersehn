import { createRouter, createWebHistory } from 'vue-router'

import { coreRoutes, installGuards, CONSENT_GATES } from '@core/router/index.js'
import HomeView from '@/views/HomeView.vue'
import MediaView from '@/views/MediaView.vue'
import ArticleView from '@/views/ArticleView.vue'
import NewsView from '@/views/NewsView.vue'
import ArticlePostView from '@/views/ArticlePostView.vue'
import AboutView from '@/views/AboutView.vue'
import EthosView from '@/views/EthosView.vue'
import CvView from '@/views/CvView.vue'
import CvSectionView from '@/views/CvSectionView.vue'
import CountriesView from '@/views/CountriesView.vue'
import CountryDetailView from '@/views/CountryDetailView.vue'
import AlbumView from '@/views/AlbumView.vue'
import ProjectsView from '@/views/ProjectsView.vue'
import ImpressumView from '@/views/legal/ImpressumView.vue'
import PrivacyView from '@/views/legal/PrivacyView.vue'
import TermsView from '@/views/legal/TermsView.vue'
import DisclaimerView from '@/views/legal/DisclaimerView.vue'
import CookieView from '@/views/legal/CookieView.vue'
import AdminView from '@/views/AdminView.vue'
import AdminContentView from '@/views/AdminContentView.vue'
import AdminLegalView from '@/views/AdminLegalView.vue'
import AdminAddressView from '@/views/AdminAddressView.vue'
import AdminEthosView from '@/views/AdminEthosView.vue'
import AdminEthosItemCreateView from '@/views/AdminEthosItemCreateView.vue'
import AdminCountriesView from '@/views/AdminCountriesView.vue'
import AdminCountriesItemCreateView from '@/views/AdminCountriesItemCreateView.vue'
import AdminCountryAlbumsView from '@/views/AdminCountryAlbumsView.vue'
import AdminAlbumEditView from '@/views/AdminAlbumEditView.vue'
import AdminCvView from '@/views/AdminCvView.vue'
import AdminCvSectionView from '@/views/AdminCvSectionView.vue'
import AdminCvEntryCreateView from '@/views/AdminCvEntryCreateView.vue'
import AdminArticleView from '@/views/AdminArticleView.vue'
import AdminArticleItemCreateView from '@/views/AdminArticleItemCreateView.vue'
import AdminArticlePostView from '@/views/AdminArticlePostView.vue'
import AdminMediaView from '@/views/AdminMediaView.vue'
import AdminMediaItemCreateView from '@/views/AdminMediaItemCreateView.vue'
import AdminRolesView from '@/views/AdminRolesView.vue'
import AdminRoleCreateView from '@/views/AdminRoleCreateView.vue'
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
      path: '/article',
      name: 'article',
      component: ArticleView,
      meta: { activeNavigation: 'article' },
    },
    {
      path: '/article/:slug',
      name: 'article-post',
      component: ArticlePostView,
      meta: { activeNavigation: 'article' },
    },
    {
      path: '/news',
      name: 'news',
      component: NewsView,
      meta: { activeNavigation: 'news' },
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
      path: '/countries/:section/:item',
      name: 'country-detail',
      component: CountryDetailView,
      meta: {
        requiresAuth: true,
        permission: 'can_view_countries',
        activeNavigation: 'countries',
      },
    },
    {
      path: '/countries/:section/:item/:album',
      name: 'album-detail',
      component: AlbumView,
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
    ...coreRoutes,
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
      path: '/admin/roles/create',
      name: 'admin-role-create',
      component: AdminRoleCreateView,
      meta: { requiresAuth: true, permission: 'can_add_role', activeNavigation: 'admin' },
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
      path: '/admin/countries/:section/:item/albums',
      name: 'admin-country-albums',
      component: AdminCountryAlbumsView,
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/countries/:section/:item/albums/:album',
      name: 'admin-album-edit',
      component: AdminAlbumEditView,
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
      path: '/admin/article',
      name: 'admin-article',
      component: AdminArticleView,
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/article/create',
      name: 'admin-article-item-create',
      component: AdminArticleItemCreateView,
      meta: { requiresAuth: true, permission: 'can_view_admin', activeNavigation: 'admin' },
    },
    {
      path: '/admin/article/:slug',
      name: 'admin-article-post',
      component: AdminArticlePostView,
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

const PAGE_TITLES = {
  home: 'Dashboard',
  media: 'Kanäle',
  article: 'Artikeln',
  'article-post': 'Artikel',
  news: 'Medien',
  about: 'Über mich',
  ethos: 'Ethos',
  cv: 'Lebenslauf',
  'cv-section': 'Lebenslauf',
  countries: 'Länder',
  'country-detail': 'Länder',
  'album-detail': 'Länder',
  projects: 'Projekte',
  impressum: 'Impressum',
  privacy: 'Datenschutzerklärung',
  terms: 'Nutzungsrichtlinien',
  disclaimer: 'Haftungsausschluss',
  cookies: 'Cookierichtlinien',
  'settings-account': 'Konto bearbeiten',
  admin: 'Admin',
  'admin-address': 'Adresse',
  'admin-roles': 'Rollen & Rechte',
  'admin-role-create': 'Neue Rolle',
  'admin-users': 'Nutzer',
  'admin-ethos': 'Ethos',
  'admin-ethos-item-create': 'Neuer Eintrag',
  'admin-countries': 'Länder',
  'admin-countries-item-create': 'Neuer Eintrag',
  'admin-country-albums': 'Alben',
  'admin-album-edit': 'Album',
  'admin-cv': 'Lebenslauf',
  'admin-cv-entry-create': 'Neuer Eintrag',
  'admin-cv-section': 'Lebenslauf',
  'admin-article': 'Artikeln',
  'admin-article-item-create': 'Neuer Artikel',
  'admin-article-post': 'Artikel',
  'admin-media': 'Kanäle',
  'admin-media-item-create': 'Neuer Eintrag',
  'admin-impressum': 'Impressum',
  'admin-privacy': 'Datenschutzerklärung',
  'admin-cookies': 'Cookierichtlinien',
  'admin-terms': 'Nutzungsrichtlinien',
  'admin-disclaimer': 'Haftungsausschluss',
  'admin-content': 'Admin',
}

installGuards(router, 'Wintersehn', PAGE_TITLES, CONSENT_GATES)

export default router
