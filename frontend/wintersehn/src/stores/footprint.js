import { ref } from 'vue'
import { defineStore } from 'pinia'
import { request } from '@core/lib/api.js'

export const useFootprintStore = defineStore('footprint', () => {
  const footprint = ref(null)

  async function fetchFootprint() {
    footprint.value = await request(
      '/api/content/news/footprint/',
      'Privacy-Faktor konnte nicht geladen werden.',
    )
    return footprint.value
  }

  return { footprint, fetchFootprint }
})
