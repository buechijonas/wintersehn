function getCookie(name) {
  const match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'))
  return match ? decodeURIComponent(match[1]) : null
}

export async function apiFetch(url, options = {}) {
  const isUnsafe = options.method && options.method !== 'GET'
  const isRaw = options.body instanceof FormData || options.body instanceof Blob
  return fetch(url, {
    credentials: 'include',
    ...options,
    headers: {
      ...(isRaw ? {} : { 'Content-Type': 'application/json' }),
      ...(isUnsafe ? { 'X-CSRFToken': getCookie('wntrs_csrftoken') } : {}),
      ...options.headers,
    },
  })
}

export function extractErrorMessage(data, fallback) {
  if (!data) return fallback
  if (data.detail) return data.detail
  const firstField = Object.values(data)[0]
  if (Array.isArray(firstField)) return firstField[0]
  return fallback
}

export async function request(url, fallback, options = {}) {
  const response = await apiFetch(url, options)
  const body = response.status === 204 ? null : await response.json().catch(() => null)
  if (!response.ok) {
    throw new Error(extractErrorMessage(body, fallback))
  }
  return body
}

export const json = (method, data) => ({ method, body: JSON.stringify(data) })
