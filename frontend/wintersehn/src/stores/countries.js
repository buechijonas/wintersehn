import { ref } from 'vue'
import { defineStore } from 'pinia'
import { json, request } from '@core/lib/api.js'

export const useCountriesStore = defineStore('countries', () => {
  const map = ref(null)

  async function load(url, fallback, options) {
    map.value = await request(url, fallback, options)
    return map.value
  }

  function fetchMap() {
    return load('/api/content/countries/map/', 'Karte konnte nicht geladen werden.')
  }

  function saveDestination(destination) {
    return load(
      '/api/content/countries/destination/',
      'Speichern fehlgeschlagen.',
      json('PUT', destination),
    )
  }

  function clearDestination() {
    return load('/api/content/countries/destination/', 'Löschen fehlgeschlagen.', {
      method: 'DELETE',
    })
  }

  return { map, fetchMap, saveDestination, clearDestination }
})
