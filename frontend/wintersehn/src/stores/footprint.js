import { ref } from 'vue'
import { defineStore } from 'pinia'
import { apiFetch, extractErrorMessage } from '@core/lib/api.js'

export const useFootprintStore = defineStore('footprint', () => {
  const footprint = ref(null)

  async function fetchFootprint() {
    const response = await apiFetch('/api/content/news/footprint/')
    const body = await response.json().catch(() => null)
    if (!response.ok) {
      throw new Error(extractErrorMessage(body, 'Privacy-Faktor konnte nicht geladen werden.'))
    }
    footprint.value = body
    return body
  }

  return { footprint, fetchFootprint }
})
