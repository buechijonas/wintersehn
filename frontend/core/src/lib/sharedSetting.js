import { ref, watch } from 'vue'

const MAX_AGE = 60 * 60 * 24 * 365
const settings = []

function cookieDomain() {
  const { hostname } = window.location
  if (hostname === 'localhost' || hostname.endsWith('.onion') || /^[\d.:]+$/.test(hostname)) {
    return ''
  }
  return `; domain=${hostname.split('.').slice(-2).join('.')}`
}

function writeCookie(key, value, maxAge) {
  const secure = window.location.protocol === 'https:' ? '; secure' : ''
  document.cookie = `${key}=${encodeURIComponent(value)}; path=/; max-age=${maxAge}; samesite=lax${cookieDomain()}${secure}`
}

function readStored(key) {
  const match = document.cookie.match(new RegExp(`(?:^|; )${key}=([^;]*)`))
  if (match) return decodeURIComponent(match[1])
  try {
    return localStorage.getItem(key)
  } catch {
    return null
  }
}

export function sharedSetting(key, { parse, serialize, apply }) {
  const setting = ref(parse(readStored(key)))
  settings.push({ key, setting, parse })
  watch(
    setting,
    (value) => {
      apply(value)
      writeCookie(key, serialize(value), MAX_AGE)
    },
    { immediate: true },
  )
  return setting
}

export function clearSharedSettings() {
  settings.forEach(({ key }) => writeCookie(key, '', 0))
}

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState !== 'visible') return
  settings.forEach(({ key, setting, parse }) => {
    setting.value = parse(readStored(key))
  })
})
