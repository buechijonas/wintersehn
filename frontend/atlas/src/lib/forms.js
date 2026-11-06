import { subjectBreadcrumbs } from '@/lib/breadcrumbs.js'

const institutionCrumbs = (institution) => [
  { label: 'Institutionen', to: '/' },
  { label: institution?.name ?? '', to: institution && `/institutions/${institution.uuid}` },
]

export const formTypes = {
  institution: {
    createTitle: 'Neue Institution',
    editTitle: 'Institution bearbeiten',
    field: 'name',
    label: 'Name',
    placeholder: 'z.B. gibb BMS',
    parent: () => null,
    createPath: () => '/institutions/',
    itemPath: (uuid) => `/institutions/${uuid}/`,
    target: (item) => `/institutions/${item.uuid}`,
    afterDelete: () => '/',
    breadcrumbs: ({ item }) =>
      item ? institutionCrumbs(item) : [{ label: 'Institutionen', to: '/' }],
    deleteMessage: (item) =>
      `${item.name} mit allen Fächern, Dokumentationen und Lernsets löschen?`,
  },
  subject: {
    createTitle: 'Neues Fach',
    editTitle: 'Fach bearbeiten',
    field: 'name',
    label: 'Name',
    placeholder: 'z.B. Mathematik',
    parent: (uuid) => `/institutions/${uuid}/`,
    createPath: (uuid) => `/institutions/${uuid}/subjects/`,
    itemPath: (uuid) => `/subjects/${uuid}/`,
    target: (item) => `/subjects/${item.uuid}`,
    afterDelete: (item) => `/institutions/${item.institution.uuid}`,
    breadcrumbs: ({ parent, item }) =>
      item ? subjectBreadcrumbs(item) : institutionCrumbs(parent),
    deleteMessage: (item) => `${item.name} mit allen Dokumentationen und Lernsets löschen?`,
  },
  learningSet: {
    createTitle: 'Neues Lernset',
    editTitle: 'Lernset bearbeiten',
    field: 'title',
    label: 'Titel',
    placeholder: 'z.B. Formeln',
    parent: (uuid) => `/subjects/${uuid}/`,
    createPath: (uuid) => `/subjects/${uuid}/learning-sets/`,
    itemPath: (uuid) => `/learning-sets/${uuid}/`,
    target: (item) => `/learning-sets/${item.uuid}`,
    afterDelete: (item) => `/subjects/${item.subject.uuid}`,
    breadcrumbs: ({ parent, item }) =>
      item
        ? [
            ...subjectBreadcrumbs(item.subject),
            { label: item.title, to: `/learning-sets/${item.uuid}` },
          ]
        : subjectBreadcrumbs(parent),
    deleteMessage: (item) => `${item.title} mit allen Karten löschen?`,
  },
}
