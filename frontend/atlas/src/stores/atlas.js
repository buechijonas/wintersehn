import { acceptHMRUpdate, defineStore } from 'pinia'
import { json, request } from '@core/lib/api.js'

const API = '/api/atlas'

export const useAtlasStore = defineStore('atlas', () => {
  const load = (path, fallback) => request(`${API}${path}`, fallback)
  const send = (path, method, data, fallback) =>
    request(`${API}${path}`, fallback, json(method, data))
  const remove = (path, fallback) => request(`${API}${path}`, fallback, { method: 'DELETE' })

  function uploadImage(file) {
    const body = new FormData()
    body.append('file', file)
    return request(`${API}/images/`, 'Bild konnte nicht hochgeladen werden.', {
      method: 'POST',
      body,
    })
  }

  return { load, send, remove, uploadImage }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAtlasStore, import.meta.hot))
}
