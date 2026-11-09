import { reactive } from 'vue'
import { defineStore } from 'pinia'
import { json, request } from '@core/lib/api.js'

export const useContentStore = defineStore('content', () => {
  const items = reactive({})

  function remember(key, body) {
    items[key] = { data: body.data, updatedAt: body.updated_at }
    return body.data
  }

  async function fetchContent(key) {
    if (items[key]) return items[key].data
    return remember(
      key,
      await request(`/api/content/${key}/`, 'Inhalt konnte nicht geladen werden.'),
    )
  }

  async function saveContent(key, data) {
    return remember(
      key,
      await request(`/api/content/${key}/`, 'Speichern fehlgeschlagen.', json('PUT', { data })),
    )
  }

  async function uploadImage(file) {
    const body = new FormData()
    body.append('file', file)
    const response = await request('/api/content/uploads/', 'Hochladen fehlgeschlagen.', {
      method: 'POST',
      body,
    })
    return response.url
  }

  return { items, fetchContent, saveContent, uploadImage }
})
