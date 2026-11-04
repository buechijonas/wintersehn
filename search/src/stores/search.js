import { nextTick, ref, watch } from 'vue'
import { acceptHMRUpdate, defineStore } from 'pinia'
import { apiFetch } from '@core/lib/api.js'
import { useAuthStore } from '@core/stores/auth.js'
import { categories, defaultSearchSettings } from '@/data/settings.js'
import { matchesDomain } from '@/lib/domains.js'

const STORAGE_KEY = 'search-settings'
const SCOPE_KEY = 'search-settings-scope'
const SAVE_DELAY = 500

function readSettings() {
  try {
    return { ...defaultSearchSettings, ...JSON.parse(localStorage.getItem(STORAGE_KEY)) }
  } catch {
    return { ...defaultSearchSettings }
  }
}

function readScope() {
  try {
    return localStorage.getItem(SCOPE_KEY) === 'account' ? 'account' : 'browser'
  } catch {
    return 'browser'
  }
}

function writeLocal(key, value) {
  try {
    localStorage.setItem(key, value)
  } catch {
    return
  }
}

function saveAccountSettings(settings) {
  return apiFetch('/api/search/settings/', {
    method: 'PUT',
    body: JSON.stringify({ data: settings }),
  })
}

function isVisible(result, settings) {
  if (settings.blocklistEnabled && matchesDomain(result.host, settings.blocklist)) return false
  if (!settings.allowlistEnabled || !settings.allowlist.length) return true
  return matchesDomain(result.host, settings.allowlist)
}

function proxiedImage(src) {
  if (src?.startsWith('/')) return `/searxng${src}`
  if (src?.startsWith('data:image/')) return src
  return null
}

function toResult(item) {
  return {
    key: item.img_src || item.url,
    title: item.title,
    url: item.url,
    host: new URL(item.url).hostname,
    content: item.content,
    image: proxiedImage(item.thumbnail_src || item.thumbnail || item.img_src),
  }
}

export const useSearchStore = defineStore('search', () => {
  const query = ref('')
  const result = ref(null)
  const settings = ref(readSettings())
  const scope = ref(readScope())

  let saveTimer = null
  let loadingAccount = false

  function usesAccount() {
    return scope.value === 'account' && useAuthStore().isAuthenticated
  }

  function persist(value) {
    if (loadingAccount) return
    if (!usesAccount()) return writeLocal(STORAGE_KEY, JSON.stringify(value))
    clearTimeout(saveTimer)
    saveTimer = setTimeout(() => saveAccountSettings(value), SAVE_DELAY)
  }

  watch(settings, persist, { deep: true })

  async function loadAccountSettings() {
    if (!usesAccount()) return
    const response = await apiFetch('/api/search/settings/')
    if (!response.ok) return
    const { data } = await response.json()
    loadingAccount = true
    settings.value = { ...defaultSearchSettings, ...data }
    await nextTick()
    loadingAccount = false
  }

  function setScope(value) {
    scope.value = value
    writeLocal(SCOPE_KEY, value)
    if (value === 'account') return saveAccountSettings(settings.value)
    writeLocal(STORAGE_KEY, JSON.stringify(settings.value))
  }

  let latestSearch = 0

  function categoryEngines(category) {
    const { engines } = categories.find(({ key }) => key === category)
    return settings.value.engines.map((engine) => engines[engine]).filter(Boolean)
  }

  async function fetchPage(q, pageno, category) {
    const engines = categoryEngines(category)
    if (!engines.length) throw new Error('Für diese Kategorie ist kein Suchanbieter aktiv.')
    const params = new URLSearchParams({
      q,
      pageno,
      format: 'json',
      engines: engines.join(','),
      language: settings.value.language,
    })
    const isGet = settings.value.method === 'get'
    const response = await fetch(isGet ? `/searxng/search?${params}` : '/searxng/search', {
      method: isGet ? 'GET' : 'POST',
      body: isGet ? null : params,
      credentials: 'omit',
      referrerPolicy: 'no-referrer',
    }).catch(() => null)
    if (!response?.ok) throw new Error('Die Suchmaschine ist nicht erreichbar.')
    return response.json()
  }

  async function fetchResults(q, page, category) {
    const length = settings.value.pageLength
    const pagenos = Array.from({ length }, (_, index) => (page - 1) * length + index + 1)
    const pages = await Promise.all(pagenos.map((pageno) => fetchPage(q, pageno, category)))
    const results = pages
      .flatMap((data) => data.results)
      .map(toResult)
      .filter((item) => isVisible(item, settings.value))
    return {
      query: q,
      page,
      category,
      results: [...new Map(results.map((item) => [item.key, item])).values()],
      suggestions: pages[0].suggestions,
    }
  }

  async function search(q, page = 1, category = 'general') {
    const current = ++latestSearch
    query.value = q
    const body = await fetchResults(q, page, category)
    if (current === latestSearch) result.value = { ...body, done: !body.results.length }
  }

  async function loadMore() {
    const current = latestSearch
    const { query: q, page, category } = result.value
    const body = await fetchResults(q, page + 1, category)
    if (current !== latestSearch) return
    const keys = new Set(result.value.results.map(({ key }) => key))
    const results = body.results.filter(({ key }) => !keys.has(key))
    result.value = {
      ...body,
      results: [...result.value.results, ...results],
      done: !results.length,
    }
  }

  return {
    query,
    result,
    settings,
    scope,
    search,
    loadMore,
    loadAccountSettings,
    setScope,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useSearchStore, import.meta.hot))
}
