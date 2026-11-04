import { nextTick, ref, watch } from 'vue'
import { acceptHMRUpdate, defineStore } from 'pinia'
import { apiFetch } from '@core/lib/api.js'
import { useAuthStore } from '@core/stores/auth.js'
import { categories, defaultSearchSettings } from '@/data/settings.js'
import { matchesDomain } from '@/lib/domains.js'

const STORAGE_KEY = 'search-settings'
const SCOPE_KEY = 'search-settings-scope'
const SAVE_DELAY = 500
const HOST_PATTERN = /^([a-z0-9-]{1,63}\.)+[a-z]{2,63}$/
const MAX_HOSTS = 30
const CACHE_TTL = 5 * 60 * 1000

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

function toFailure([engine, reason]) {
  return {
    provider: engine.split(/[ .]/)[0].replace('wikicommons', 'wikipedia'),
    reason: reason.replace(/^(Suspended|Ausgesetzt): /, ''),
  }
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
  const networks = ref(['tor'])
  const hostRatings = ref({})
  const pendingHosts = ref([])
  const checkedHosts = new Set()
  const resultCache = new Map()

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

  async function fetchNetworks() {
    const response = await fetch('/searxng/config', { credentials: 'same-origin' }).catch(
      () => null,
    )
    if (!response?.headers.get('content-type')?.includes('application/json')) return
    const names = (await response.json()).engines.map(({ name }) => name)
    const extra = ['vpn', 'proxy', 'direct'].filter((network) =>
      names.some((name) => name.endsWith(` ${network}`)),
    )
    networks.value = ['tor', ...extra]
  }

  function activeNetwork() {
    return networks.value.includes(settings.value.network) ? settings.value.network : 'tor'
  }

  function categoryEngines(category) {
    const { engines } = categories.find(({ key }) => key === category)
    const network = activeNetwork()
    const suffix = network === 'tor' ? '' : ` ${network}`
    return settings.value.engines
      .map((engine) => engines[engine])
      .filter(Boolean)
      .map((engine) => `${engine}${suffix}`)
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
      timeout_limit: settings.value.timeout,
    })
    const isGet = settings.value.method === 'get'
    const response = await fetch(isGet ? `/searxng/search?${params}` : '/searxng/search', {
      method: isGet ? 'GET' : 'POST',
      body: isGet ? null : params,
      credentials: 'same-origin',
      referrerPolicy: 'no-referrer',
    }).catch(() => null)
    if (!response?.ok) throw new Error('Die Suchmaschine ist nicht erreichbar.')
    if (!response.headers.get('content-type')?.includes('application/json')) {
      throw new Error('Die Sicherheitsprüfung ist abgelaufen. Bitte lade die Seite neu.')
    }
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
    const failures = pages.flatMap((data) => data.unresponsive_engines).map(toFailure)
    return {
      query: q,
      page,
      category,
      results: [...new Map(results.map((item) => [item.key, item])).values()],
      failures: [...new Map(failures.map((item) => [item.provider, item])).values()],
      suggestions: pages[0].suggestions,
    }
  }

  async function rateHosts(items) {
    const hosts = [...new Set(items.map(({ host }) => host))]
      .filter((host) => HOST_PATTERN.test(host) && !checkedHosts.has(host))
      .slice(0, MAX_HOSTS)
    if (!hosts.length) return
    hosts.forEach((host) => checkedHosts.add(host))
    pendingHosts.value = [...pendingHosts.value, ...hosts]
    const response = await apiFetch('/api/search/host-ratings/', {
      method: 'POST',
      body: JSON.stringify({ hosts }),
    }).catch(() => null)
    const reports = response?.ok ? (await response.json()).hosts : {}
    hostRatings.value = { ...hostRatings.value, ...reports }
    pendingHosts.value = pendingHosts.value.filter((host) => !hosts.includes(host))
  }

  function cachedResults(q, page, category) {
    const key = JSON.stringify([q, page, category, settings.value])
    const hit = resultCache.get(key)
    if (hit && Date.now() - hit.time < CACHE_TTL) return hit.promise
    const promise = fetchResults(q, page, category)
    resultCache.set(key, { promise, time: Date.now() })
    promise
      .then((body) => body.results.length || resultCache.delete(key))
      .catch(() => resultCache.delete(key))
    return promise
  }

  async function search(q, page = 1, category = 'general') {
    const current = ++latestSearch
    query.value = q
    const body = await cachedResults(q, page, category)
    if (current !== latestSearch) return
    result.value = { ...body, done: !body.results.length }
    rateHosts(body.results)
  }

  async function loadMore() {
    const current = latestSearch
    const { query: q, page, category } = result.value
    const body = await cachedResults(q, page + 1, category)
    if (current !== latestSearch) return
    const keys = new Set(result.value.results.map(({ key }) => key))
    const results = body.results.filter(({ key }) => !keys.has(key))
    result.value = {
      ...body,
      results: [...result.value.results, ...results],
      done: !results.length,
    }
    rateHosts(results)
  }

  return {
    query,
    result,
    settings,
    scope,
    networks,
    hostRatings,
    pendingHosts,
    search,
    fetchNetworks,
    activeNetwork,
    loadMore,
    loadAccountSettings,
    setScope,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useSearchStore, import.meta.hot))
}
