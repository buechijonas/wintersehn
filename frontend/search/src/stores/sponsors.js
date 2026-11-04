import { computed, ref } from 'vue'
import { acceptHMRUpdate, defineStore } from 'pinia'
import { apiFetch, extractErrorMessage } from '@core/lib/api.js'

const ENDPOINT = '/api/search/sponsors/'

async function request(url, fallback, options = {}) {
  const response = await apiFetch(url, options)
  const body = response.status === 204 ? null : await response.json().catch(() => null)
  if (!response.ok) {
    throw new Error(extractErrorMessage(body, fallback))
  }
  return body
}

const json = (method, data) => ({ method, body: JSON.stringify(data) })

function toResult(sponsor) {
  return {
    key: `sponsor-${sponsor.uuid}`,
    title: sponsor.title,
    url: sponsor.url,
    host: new URL(sponsor.url).hostname,
    content: sponsor.description,
  }
}

export const useSponsorsStore = defineStore('sponsors', () => {
  const items = ref([])
  const turn = ref(Math.floor(Math.random() * 1000))

  const current = computed(() => {
    if (!items.value.length) return null
    return toResult(items.value[turn.value % items.value.length])
  })

  function rotate() {
    turn.value += 1
  }

  async function fetchSponsors() {
    items.value = await request(ENDPOINT, 'Sponsoren konnten nicht geladen werden.')
  }

  async function createSponsor(data) {
    await request(ENDPOINT, 'Sponsor konnte nicht gespeichert werden.', json('POST', data))
    await fetchSponsors()
  }

  async function updateSponsor(uuid, data) {
    await request(
      `${ENDPOINT}${uuid}/`,
      'Sponsor konnte nicht gespeichert werden.',
      json('PUT', data),
    )
    await fetchSponsors()
  }

  async function deleteSponsor(uuid) {
    await request(`${ENDPOINT}${uuid}/`, 'Sponsor konnte nicht gelöscht werden.', {
      method: 'DELETE',
    })
    await fetchSponsors()
  }

  return { items, current, rotate, fetchSponsors, createSponsor, updateSponsor, deleteSponsor }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useSponsorsStore, import.meta.hot))
}
