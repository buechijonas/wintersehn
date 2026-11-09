import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { apiFetch, request } from '@core/lib/api.js'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const ready = ref(false)
  const isAuthenticated = computed(() => user.value !== null)

  async function fetchMe() {
    try {
      const response = await apiFetch('/api/auth/me/')
      const data = response.ok ? await response.json() : null
      user.value = data?.user ?? null
    } finally {
      ready.value = true
    }
  }

  function startGovexLogin() {
    window.location.href = '/api/auth/oidc/login/'
  }

  function openGovexAccount() {
    window.location.href = '/api/auth/oidc/account/'
  }

  async function logout() {
    await request('/api/auth/logout/', 'Abmelden fehlgeschlagen.', { method: 'POST' })
    user.value = null
  }

  async function acceptConsent(field) {
    const consent = await request(`/api/auth/consent/${field}/`, 'Zustimmung fehlgeschlagen.', {
      method: 'POST',
    })
    user.value = { ...user.value, consent }
  }

  return {
    user,
    ready,
    isAuthenticated,
    fetchMe,
    startGovexLogin,
    openGovexAccount,
    logout,
    acceptConsent,
  }
})
