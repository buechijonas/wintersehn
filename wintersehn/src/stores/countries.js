import { ref } from 'vue'
import { defineStore } from 'pinia'
import { apiFetch, extractErrorMessage } from '@core/lib/api.js'

export const useCountriesStore = defineStore('countries', () => {
  const map = ref(null)

  async function request(url, options, fallback) {
    const response = await apiFetch(url, options)
    const body = await response.json().catch(() => null)
    if (!response.ok) {
      throw new Error(extractErrorMessage(body, fallback))
    }
    map.value = body
    return body
  }

  function fetchMap() {
    return request('/api/content/countries/map/', {}, 'Karte konnte nicht geladen werden.')
  }

  function saveDestination(destination) {
    return request(
      '/api/content/countries/destination/',
      { method: 'PUT', body: JSON.stringify(destination) },
      'Speichern fehlgeschlagen.',
    )
  }

  function clearDestination() {
    return request(
      '/api/content/countries/destination/',
      { method: 'DELETE' },
      'Löschen fehlgeschlagen.',
    )
  }

  return { map, fetchMap, saveDestination, clearDestination }
})
