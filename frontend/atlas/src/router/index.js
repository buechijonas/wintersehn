import { createRouter, createWebHistory } from 'vue-router'

import { coreRoutes, installAdminGuard, installGuards } from '@core/router/index.js'
import FormView from '@/views/FormView.vue'
import InstitutionsView from '@/views/InstitutionsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      name: 'institutions',
      component: InstitutionsView,
      meta: { activeNavigation: 'institutions' },
    },
    {
      path: '/institutions/new',
      name: 'institution-new',
      component: FormView,
      meta: { activeNavigation: 'institutions', form: 'institution', mode: 'create' },
    },
    {
      path: '/institutions/:uuid/edit',
      name: 'institution-edit',
      component: FormView,
      meta: { activeNavigation: 'institutions', form: 'institution', mode: 'edit' },
    },
    {
      path: '/institutions/:uuid/subjects/new',
      name: 'subject-new',
      component: FormView,
      meta: { activeNavigation: 'institutions', form: 'subject', mode: 'create' },
    },
    {
      path: '/subjects/:uuid/edit',
      name: 'subject-edit',
      component: FormView,
      meta: { activeNavigation: 'institutions', form: 'subject', mode: 'edit' },
    },
    {
      path: '/subjects/:uuid/documentations/new',
      name: 'documentation-new',
      component: () => import('@/views/DocumentationEditView.vue'),
      meta: { activeNavigation: 'documentations', mode: 'create' },
    },
    {
      path: '/subjects/:uuid/learning-sets/new',
      name: 'learning-set-new',
      component: FormView,
      meta: { activeNavigation: 'learning-sets', form: 'learningSet', mode: 'create' },
    },
    {
      path: '/subjects/:uuid/exams/new',
      name: 'exam-new',
      component: () => import('@/views/ExamFormView.vue'),
      meta: { activeNavigation: 'institutions', mode: 'create' },
    },
    {
      path: '/exams/:uuid/edit',
      name: 'exam-edit',
      component: () => import('@/views/ExamFormView.vue'),
      meta: { activeNavigation: 'institutions', mode: 'edit' },
    },
    {
      path: '/learning-sets/:uuid/edit',
      name: 'learning-set-edit',
      component: FormView,
      meta: { activeNavigation: 'learning-sets', form: 'learningSet', mode: 'edit' },
    },
    {
      path: '/institutions/:uuid',
      name: 'institution',
      component: () => import('@/views/InstitutionView.vue'),
      meta: { activeNavigation: 'institutions' },
    },
    {
      path: '/subjects/:uuid',
      name: 'subject',
      component: () => import('@/views/SubjectView.vue'),
      meta: { activeNavigation: 'institutions' },
    },
    {
      path: '/documentations',
      name: 'documentations',
      component: () => import('@/views/DocumentationsView.vue'),
      meta: { activeNavigation: 'documentations' },
    },
    {
      path: '/documentations/:uuid',
      name: 'documentation',
      component: () => import('@/views/DocumentationView.vue'),
      meta: { activeNavigation: 'documentations' },
    },
    {
      path: '/documentations/:uuid/edit',
      name: 'documentation-edit',
      component: () => import('@/views/DocumentationEditView.vue'),
      meta: { activeNavigation: 'documentations', mode: 'edit' },
    },
    {
      path: '/learning-sets',
      name: 'learning-sets',
      component: () => import('@/views/LearningSetsView.vue'),
      meta: { activeNavigation: 'learning-sets' },
    },
    {
      path: '/learning-sets/:uuid',
      name: 'learning-set',
      component: () => import('@/views/LearningSetView.vue'),
      meta: { activeNavigation: 'learning-sets' },
    },
    {
      path: '/learning-sets/:uuid/browse',
      name: 'learning-set-browse',
      component: () => import('@/views/BrowseView.vue'),
      meta: { activeNavigation: 'learning-sets' },
    },
    {
      path: '/learning-sets/:uuid/learn',
      name: 'learning-set-learn',
      component: () => import('@/views/LearnView.vue'),
      meta: { activeNavigation: 'learning-sets' },
    },
    {
      path: '/learning-sets/:uuid/cards',
      name: 'learning-set-cards',
      component: () => import('@/views/CardsView.vue'),
      meta: { activeNavigation: 'learning-sets' },
    },
    ...coreRoutes,
  ],
})

installAdminGuard(router, import.meta.env.VITE_WINTERSEHN_URL ?? 'https://wintersehn.ch')
installGuards(router, 'ATLAS', {
  institutions: 'Institutionen',
  institution: 'Institution',
  'institution-new': 'Neue Institution',
  'subject-new': 'Neues Fach',
  'documentation-new': 'Neue Dokumentation',
  'learning-set-new': 'Neues Lernset',
  'institution-edit': 'Institution bearbeiten',
  'subject-edit': 'Fach bearbeiten',
  'learning-set-edit': 'Lernset bearbeiten',
  'exam-new': 'Neue Prüfung',
  'exam-edit': 'Prüfung bearbeiten',
  subject: 'Fach',
  documentations: 'Dokumentationen',
  documentation: 'Dokumentation',
  'documentation-edit': 'Dokumentation bearbeiten',
  'learning-sets': 'Lernsets',
  'learning-set': 'Lernset',
  'learning-set-cards': 'Karten',
  'learning-set-browse': 'Karten blättern',
  'learning-set-learn': 'Lernen',
})

export default router
