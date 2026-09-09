function getCookie(name) {
  const match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'))
  return match ? decodeURIComponent(match[1]) : null
}

export async function apiFetch(url, options = {}) {
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

export function extractErrorMessage(data, fallback) {
  if (!data) return fallback
  if (data.detail) return data.detail
  const firstField = Object.values(data)[0]
  if (Array.isArray(firstField)) return firstField[0]
  return fallback
}
