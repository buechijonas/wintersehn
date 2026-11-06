import { acceptHMRUpdate, defineStore } from 'pinia'
import { apiFetch, extractErrorMessage, json, request } from '@core/lib/api.js'

const API = '/api/atlas'

export const useAtlasStore = defineStore('atlas', () => {
  const load = (path, fallback) => request(`${API}${path}`, fallback)
  const send = (path, method, data, fallback) =>
    request(`${API}${path}`, fallback, json(method, data))
  const remove = (path, fallback) => request(`${API}${path}`, fallback, { method: 'DELETE' })

  async function uploadImage(file) {
    const body = new FormData()
    body.append('file', file)
    const response = await apiFetch(`${API}/images/`, { method: 'POST', body })
    const data = await response.json().catch(() => null)
    if (!response.ok)
      throw new Error(extractErrorMessage(data, 'Bild konnte nicht hochgeladen werden.'))
    return data
  }

  return { load, send, remove, uploadImage }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAtlasStore, import.meta.hot))
}
