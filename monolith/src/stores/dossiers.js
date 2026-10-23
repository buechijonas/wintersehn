import { ref } from 'vue'
import { acceptHMRUpdate, defineStore } from 'pinia'
import { apiFetch, extractErrorMessage } from '@core/lib/api.js'

async function request(url, fallback, options = {}) {
  const response = await apiFetch(url, options)
  const body = response.status === 204 ? null : await response.json().catch(() => null)
  if (!response.ok) {
    throw new Error(extractErrorMessage(body, fallback))
  }
  return body
}

const json = (method, data) => ({ method, body: JSON.stringify(data) })

export const useDossiersStore = defineStore('dossiers', () => {
  const items = ref(null)
  const current = ref(null)
  const networkSettings = ref(null)

  let latestSearch = 0

  async function fetchDossiers(query = '') {
    const search = ++latestSearch
    const dossiers = await request(
      `/api/monolith/dossiers/?${new URLSearchParams({ q: query })}`,
      'Akten konnten nicht geladen werden.',
    )
    if (search === latestSearch) items.value = dossiers
  }

  async function createDossier(title, query = '') {
    await request(
      '/api/monolith/dossiers/',
      'Akte konnte nicht erstellt werden.',
      json('POST', { title }),
    )
    await fetchDossiers(query)
  }

  async function fetchDossier(uuid) {
    current.value = null
    current.value = await request(
      `/api/monolith/dossiers/${uuid}/`,
      'Akte konnte nicht geladen werden.',
    )
  }

  async function updateDossier(uuid, data) {
    current.value = await request(
      `/api/monolith/dossiers/${uuid}/`,
      'Speichern fehlgeschlagen.',
      json('PATCH', data),
    )
  }

  function fetchRelationships(uuid) {
    return request(
      `/api/monolith/dossiers/${uuid}/relationships/`,
      'Beziehungen konnten nicht geladen werden.',
    )
  }

  function addRelationship(uuid, person) {
    return request(
      `/api/monolith/dossiers/${uuid}/relationships/`,
      'Beziehung konnte nicht hinzugefügt werden.',
      json('POST', { person }),
    )
  }

  function updateRelationship(uuid, person, status) {
    return request(
      `/api/monolith/dossiers/${uuid}/relationships/${person}/`,
      'Status konnte nicht gespeichert werden.',
      json('PATCH', { status }),
    )
  }

  function removeRelationship(uuid, person) {
    return request(
      `/api/monolith/dossiers/${uuid}/relationships/${person}/`,
      'Beziehung konnte nicht entfernt werden.',
      { method: 'DELETE' },
    )
  }

  function fetchEvents(uuid) {
    return request(
      `/api/monolith/dossiers/${uuid}/events/`,
      'Ereignisse konnten nicht geladen werden.',
    )
  }

  function createEvent(uuid, data) {
    return request(
      `/api/monolith/dossiers/${uuid}/events/`,
      'Ereignis konnte nicht erstellt werden.',
      json('POST', data),
    )
  }

  function fetchEvent(uuid, event) {
    return request(
      `/api/monolith/dossiers/${uuid}/events/${event}/`,
      'Ereignis konnte nicht geladen werden.',
    )
  }

  function updateEvent(uuid, event, data) {
    return request(
      `/api/monolith/dossiers/${uuid}/events/${event}/`,
      'Speichern fehlgeschlagen.',
      json('PATCH', data),
    )
  }

  function deleteEvent(uuid, event) {
    return request(
      `/api/monolith/dossiers/${uuid}/events/${event}/`,
      'Ereignis konnte nicht gelöscht werden.',
      { method: 'DELETE' },
    )
  }

  function linkEvent(uuid, event, links) {
    return request(
      `/api/monolith/dossiers/${uuid}/events/${event}/links/`,
      'Verknüpfung konnte nicht gespeichert werden.',
      json('PUT', links),
    )
  }

  function fetchAddictions(uuid) {
    return request(
      `/api/monolith/dossiers/${uuid}/addictions/`,
      'Süchte konnten nicht geladen werden.',
    )
  }

  function addAddiction(uuid, data) {
    return request(
      `/api/monolith/dossiers/${uuid}/addictions/`,
      'Sucht konnte nicht hinzugefügt werden.',
      json('POST', data),
    )
  }

  function updateAddiction(uuid, kind, frequency) {
    return request(
      `/api/monolith/dossiers/${uuid}/addictions/${kind}/`,
      'Konsum konnte nicht gespeichert werden.',
      json('PATCH', { frequency }),
    )
  }

  function removeAddiction(uuid, kind) {
    return request(
      `/api/monolith/dossiers/${uuid}/addictions/${kind}/`,
      'Sucht konnte nicht entfernt werden.',
      { method: 'DELETE' },
    )
  }

  function fetchReferences(uuid) {
    return request(
      `/api/monolith/dossiers/${uuid}/references/`,
      'Referenzen konnten nicht geladen werden.',
    )
  }

  function addReference(uuid, data) {
    return request(
      `/api/monolith/dossiers/${uuid}/references/`,
      'Referenz konnte nicht hinzugefügt werden.',
      json('POST', data),
    )
  }

  function removeReference(uuid, reference) {
    return request(
      `/api/monolith/dossiers/${uuid}/references/${reference}/`,
      'Referenz konnte nicht entfernt werden.',
      { method: 'DELETE' },
    )
  }

  function fetchStances(uuid) {
    return request(
      `/api/monolith/dossiers/${uuid}/stances/`,
      'Ideologie konnte nicht geladen werden.',
    )
  }

  function fetchStanceSummary(uuid) {
    return request(
      `/api/monolith/dossiers/${uuid}/stances/summary/`,
      'Gesamtfazit konnte nicht geladen werden.',
    )
  }

  function saveStance(uuid, topic, data) {
    return request(
      `/api/monolith/dossiers/${uuid}/stances/${topic}/`,
      'Speichern fehlgeschlagen.',
      json('PUT', data),
    )
  }

  function fetchNetwork() {
    return request('/api/monolith/network/', 'Netzwerk konnte nicht geladen werden.')
  }

  async function fetchNetworkSettings() {
    networkSettings.value ??= await request(
      '/api/monolith/network/settings/',
      'Einstellungen konnten nicht geladen werden.',
    )
    return networkSettings.value
  }

  async function saveNetworkSettings(data) {
    networkSettings.value = await request(
      '/api/monolith/network/settings/',
      'Einstellungen konnten nicht gespeichert werden.',
      json('PUT', data),
    )
  }

  function fetchTrust() {
    return request('/api/monolith/trust/', 'Vertrauenskreise konnten nicht geladen werden.')
  }

  function setTrust(uuid, level) {
    return request(
      `/api/monolith/trust/${uuid}/`,
      'Vertrauenskreis konnte nicht gespeichert werden.',
      json('PUT', { level }),
    )
  }

  function removeTrust(uuid) {
    return request(`/api/monolith/trust/${uuid}/`, 'Zuordnung konnte nicht entfernt werden.', {
      method: 'DELETE',
    })
  }

  function fetchTrustEntries(uuid) {
    return request(
      `/api/monolith/dossiers/${uuid}/trust/`,
      'Vertrauenspunkte konnten nicht geladen werden.',
    )
  }

  function addTrustEntry(uuid, data) {
    return request(
      `/api/monolith/dossiers/${uuid}/trust/`,
      'Eintrag konnte nicht hinzugefügt werden.',
      json('POST', data),
    )
  }

  function removeTrustEntry(uuid, entry) {
    return request(
      `/api/monolith/dossiers/${uuid}/trust/${entry}/`,
      'Eintrag konnte nicht entfernt werden.',
      { method: 'DELETE' },
    )
  }

  function fetchShares(uuid) {
    return request(
      `/api/monolith/dossiers/${uuid}/shares/`,
      'Freigaben konnten nicht geladen werden.',
    )
  }

  function createShare(uuid, data) {
    return request(
      `/api/monolith/dossiers/${uuid}/shares/`,
      'Freigabe konnte nicht erstellt werden.',
      json('POST', data),
    )
  }

  function fetchShare(uuid, share) {
    return request(
      `/api/monolith/dossiers/${uuid}/shares/${share}/`,
      'Freigabe konnte nicht geladen werden.',
    )
  }

  function saveShareRules(uuid, share, rules) {
    return request(
      `/api/monolith/dossiers/${uuid}/shares/${share}/`,
      'Freigabe konnte nicht gespeichert werden.',
      json('PUT', { rules }),
    )
  }

  function deleteShare(uuid, share) {
    return request(
      `/api/monolith/dossiers/${uuid}/shares/${share}/`,
      'Freigabe konnte nicht widerrufen werden.',
      { method: 'DELETE' },
    )
  }

  function fetchSharePreview(uuid, share) {
    return request(
      `/api/monolith/dossiers/${uuid}/shares/${share}/preview/`,
      'Vorschau konnte nicht geladen werden.',
    )
  }

  function fetchSharedWithMe() {
    return request('/api/monolith/shared/', 'Geteilte Akten konnten nicht geladen werden.')
  }

  function fetchSharedDossier(share) {
    return request(`/api/monolith/shared/${share}/`, 'Akte konnte nicht geladen werden.')
  }

  function updateShare(uuid, share, data) {
    return request(
      `/api/monolith/dossiers/${uuid}/shares/${share}/`,
      'Freigabe konnte nicht gespeichert werden.',
      json('PATCH', data),
    )
  }

  async function openSharedLink(token, password) {
    const response = await apiFetch(`/api/monolith/share/${token}/`, json('POST', { password }))
    const body = await response.json().catch(() => null)
    if (response.status === 403) return { passwordRequired: true }
    if (response.status === 429)
      throw new Error('Zu viele Versuche. Bitte später erneut versuchen.')
    if (!response.ok)
      throw new Error(extractErrorMessage(body, 'Link konnte nicht geöffnet werden.'))
    return { document: body }
  }

  function searchGovex(query) {
    return request(
      `/api/monolith/govex/?${new URLSearchParams({ q: query })}`,
      'govex-Suche fehlgeschlagen.',
    )
  }

  function fetchGovex(uuid) {
    return request(
      `/api/monolith/dossiers/${uuid}/govex/`,
      'Verknüpfung konnte nicht geladen werden.',
    )
  }

  function linkGovex(uuid, sub) {
    return request(
      `/api/monolith/dossiers/${uuid}/govex/`,
      'Verknüpfen fehlgeschlagen.',
      json('PUT', { sub }),
    )
  }

  function unlinkGovex(uuid) {
    return request(`/api/monolith/dossiers/${uuid}/govex/`, 'Lösen fehlgeschlagen.', {
      method: 'DELETE',
    })
  }

  function fetchSwissfy(uuid) {
    return request(
      `/api/monolith/dossiers/${uuid}/swissfy/`,
      'swissfy-Konto konnte nicht geladen werden.',
    )
  }

  function swissfyPictureUrl(uuid) {
    return `/api/monolith/dossiers/${uuid}/swissfy/picture/`
  }

  return {
    items,
    current,
    networkSettings,
    fetchDossiers,
    createDossier,
    fetchDossier,
    updateDossier,
    fetchRelationships,
    addRelationship,
    updateRelationship,
    removeRelationship,
    fetchEvents,
    createEvent,
    fetchEvent,
    updateEvent,
    deleteEvent,
    linkEvent,
    fetchAddictions,
    addAddiction,
    updateAddiction,
    removeAddiction,
    fetchReferences,
    addReference,
    removeReference,
    fetchStances,
    fetchStanceSummary,
    saveStance,
    fetchNetwork,
    fetchNetworkSettings,
    saveNetworkSettings,
    fetchTrust,
    setTrust,
    removeTrust,
    fetchTrustEntries,
    addTrustEntry,
    removeTrustEntry,
    fetchShares,
    createShare,
    fetchShare,
    saveShareRules,
    deleteShare,
    fetchSharePreview,
    fetchSharedWithMe,
    fetchSharedDossier,
    updateShare,
    openSharedLink,
    searchGovex,
    fetchGovex,
    linkGovex,
    unlinkGovex,
    fetchSwissfy,
    swissfyPictureUrl,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useDossiersStore, import.meta.hot))
}
