import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { apiFetch, extractErrorMessage } from '@/lib/api.js'

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

  async function login(username, password) {
    const response = await apiFetch('/api/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    })
    const data = await response.json().catch(() => null)
    if (!response.ok) {
      throw new Error(extractErrorMessage(data, 'Anmeldung fehlgeschlagen.'))
    }
    user.value = data
    return data
  }

  async function signup({ username, email, password }) {
    const response = await apiFetch('/api/auth/signup/', {
      method: 'POST',
      body: JSON.stringify({ username, email, password }),
    })
    const data = await response.json().catch(() => null)
    if (!response.ok) {
      throw new Error(extractErrorMessage(data, 'Registrierung fehlgeschlagen.'))
    }
    user.value = data
    return data
  }

  async function logout() {
    const response = await apiFetch('/api/auth/logout/', { method: 'POST' })
    if (!response.ok) {
      const data = await response.json().catch(() => null)
      throw new Error(extractErrorMessage(data, 'Abmelden fehlgeschlagen.'))
    }
    user.value = null
  }

  async function acceptConsent(field) {
    const response = await apiFetch(`/api/auth/consent/${field}/`, { method: 'POST' })
    const data = await response.json().catch(() => null)
    if (!response.ok) {
      throw new Error(extractErrorMessage(data, 'Zustimmung fehlgeschlagen.'))
    }
    user.value = { ...user.value, consent: data }
  }

  async function updateProfile(fields) {
    const response = await apiFetch('/api/auth/me/', {
      method: 'PATCH',
      body: JSON.stringify(fields),
    })
    const data = await response.json().catch(() => null)
    if (!response.ok) {
      throw new Error(extractErrorMessage(data, 'Speichern fehlgeschlagen.'))
    }
    user.value = data
    return data
  }

  async function changePassword(currentPassword, newPassword) {
    const response = await apiFetch('/api/auth/password/', {
      method: 'POST',
      body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
    })
    if (!response.ok) {
      const data = await response.json().catch(() => null)
      throw new Error(extractErrorMessage(data, 'Passwort ändern fehlgeschlagen.'))
    }
  }

  return {
    user,
    ready,
    isAuthenticated,
    fetchMe,
    login,
    signup,
    logout,
    acceptConsent,
    updateProfile,
    changePassword,
  }
})
