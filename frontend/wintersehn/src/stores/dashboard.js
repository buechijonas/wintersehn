import { ref } from 'vue'
import { defineStore } from 'pinia'
import { request } from '@core/lib/api.js'

export const useDashboardStore = defineStore('dashboard', () => {
  const dashboard = ref(null)

  async function fetchDashboard() {
    dashboard.value = await request(
      '/api/content/dashboard/',
      'Dashboard konnte nicht geladen werden.',
    )
    return dashboard.value
  }

  return { dashboard, fetchDashboard }
})
