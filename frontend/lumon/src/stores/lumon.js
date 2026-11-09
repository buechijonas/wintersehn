import { acceptHMRUpdate, defineStore } from 'pinia'
import { json, request } from '@core/lib/api.js'

const API = '/api/lumon'
const CHUNK_SIZE = 8 * 1024 * 1024

export const useLumonStore = defineStore('lumon', () => {
  const load = (path, fallback) => request(`${API}${path}`, fallback)

  const save = ({ catalog_id, media_type }) =>
    request(
      `${API}/titles/`,
      'Titel konnte nicht gemerkt werden.',
      json('POST', { catalog_id, media_type }),
    )

  const forget = (uuid) =>
    request(`${API}/titles/${uuid}/`, 'Titel konnte nicht entfernt werden.', {
      method: 'DELETE',
    })

  const progress = (id, data) =>
    request(`${API}/media/${id}/progress/`, 'Fortschritt konnte nicht gespeichert werden.', {
      ...json('POST', data),
      keepalive: true,
    })

  async function upload(target, file, onProgress) {
    const { uuid } = await request(
      `${API}/uploads/`,
      'Upload konnte nicht gestartet werden.',
      json('POST', { ...target, filename: file.name, size: file.size }),
    )
    try {
      for (let offset = 0; offset < file.size; offset += CHUNK_SIZE) {
        await request(`${API}/uploads/${uuid}/chunk/?offset=${offset}`, 'Upload abgebrochen.', {
          method: 'PUT',
          body: file.slice(offset, offset + CHUNK_SIZE),
          headers: { 'Content-Type': 'application/octet-stream' },
        })
        onProgress(Math.min(offset + CHUNK_SIZE, file.size) / file.size)
      }
      await request(
        `${API}/uploads/${uuid}/complete/`,
        'Upload konnte nicht abgeschlossen werden.',
        {
          method: 'POST',
        },
      )
    } catch (error) {
      await request(`${API}/uploads/${uuid}/`, '', { method: 'DELETE' }).catch(() => null)
      throw error
    }
  }

  const detect = (catalogId, filenames, defaultSeason) =>
    request(
      `${API}/catalog/tv/${catalogId}/detect/`,
      'Folgen konnten nicht erkannt werden.',
      json('POST', { filenames, default_season: defaultSeason }),
    )

  return { load, save, forget, progress, upload, detect }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useLumonStore, import.meta.hot))
}
