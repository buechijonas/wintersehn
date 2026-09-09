import { reactive } from 'vue'
import { defineStore } from 'pinia'
import { apiFetch, extractErrorMessage } from '@/lib/api.js'

export const useContentStore = defineStore('content', () => {
  const items = reactive({})

  async function fetchContent(key) {
    if (items[key]) return items[key].data

    const response = await apiFetch(`/api/content/${key}/`)
    if (!response.ok) {
      throw new Error('Inhalt konnte nicht geladen werden.')
    }
    const body = await response.json()
    items[key] = { data: body.data, updatedAt: body.updated_at }
    return body.data
  }

  async function saveContent(key, data) {
    const response = await apiFetch(`/api/content/${key}/`, {
      method: 'PUT',
      body: JSON.stringify({ data }),
    })
    const body = await response.json().catch(() => null)
    if (!response.ok) {
      throw new Error(extractErrorMessage(body, 'Speichern fehlgeschlagen.'))
    }
    items[key] = { data: body.data, updatedAt: body.updated_at }
    return body.data
  }

  return { items, fetchContent, saveContent }
})
