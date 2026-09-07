import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

function getCookie(name) {
  const match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'))
  return match ? decodeURIComponent(match[1]) : null
}

async function apiFetch(url, options = {}) {
  const isUnsafe = options.method && options.method !== 'GET'
  return fetch(url, {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...(isUnsafe ? { 'X-CSRFToken': getCookie('csrftoken') } : {}),
      ...options.headers,
    },
    ...options,
  })
}

function extractErrorMessage(data, fallback) {
  if (!data) return fallback
  if (data.detail) return data.detail
  const firstField = Object.values(data)[0]
  if (Array.isArray(firstField)) return firstField[0]
  return fallback
}

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

  return { user, ready, isAuthenticated, fetchMe, login, signup, logout }
})
