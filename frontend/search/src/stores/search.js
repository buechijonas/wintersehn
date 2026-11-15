import { nextTick, ref, watch } from 'vue'
import { acceptHMRUpdate, defineStore } from 'pinia'
import { apiFetch } from '@core/lib/api.js'
import { clearSharedSettings } from '@core/lib/sharedSetting.js'
import { useAuthStore } from '@core/stores/auth.js'
import { categories, defaultSearchSettings } from '@/data/settings.js'
import { matchesDomain } from '@/lib/domains.js'

const STORAGE_KEY = 'wntrs-search-settings'
const SCOPE_KEY = 'wntrs-search-settings-scope'
const SAVE_DELAY = 500
const HOST_PATTERN = /^([a-z0-9-]{1,63}\.)+[a-z]{2,63}$/
const MAX_HOSTS = 30
const CACHE_TTL = 5 * 60 * 1000
const SIMILAR_WORDS = 8
const FALLBACK_NETWORKS = { tor: 'strict', strict: 'tor' }

function storageFor(scope) {
  return scope === 'session' ? sessionStorage : localStorage
}

function readSettings(scope) {
  try {
    return { ...defaultSearchSettings, ...JSON.parse(storageFor(scope).getItem(STORAGE_KEY)) }
  } catch {
    return { ...defaultSearchSettings }
  }
}

function readScope() {
  try {
    const scope = localStorage.getItem(SCOPE_KEY)
    return ['account', 'session'].includes(scope) ? scope : 'browser'
  } catch {
    return 'browser'
  }
}

function writeStorage(storage, key, value) {
  try {
    storage.setItem(key, value)
  } catch {
    return
  }
}

function removeStorage(storage, key) {
  try {
    storage.removeItem(key)
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
  if (settings.httpLinks === 'hide' && result.url.startsWith('http:')) return false
  if (settings.blocklistEnabled && matchesDomain(result.url, settings.blocklist)) return false
  if (!settings.allowlistEnabled || !settings.allowlist.length) return true
  return matchesDomain(result.url, settings.allowlist)
}

function proxiedImage(src) {
  if (src?.startsWith('/')) return `/searxng${src}`
  if (src?.startsWith('data:image/')) return src
  return null
}

function withHttpLinks(item, mode) {
  if (mode !== 'upgrade' || !item.url.startsWith('http:')) return item
  return { ...item, url: `https:${item.url.slice(5)}` }
}

function toBlocked(answer) {
  if (!answer) return null
  const link = answer.url && {
    key: answer.url,
    url: answer.url,
    host: new URL(answer.url).hostname,
    title: answer.link_title,
    content: answer.content,
  }
  return { message: answer.answer, link }
}

function toFailure([engine, reason]) {
  return {
    provider: engine
      .split(/[ .]/)[0]
      .replace('wikicommons', 'wikipedia')
      .replace('sepiasearch', 'peertube')
      .replace('braveapi', 'brave'),
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
    full: proxiedImage(item.img_src),
    resolution: item.resolution || null,
  }
}

function uniqueBy(items, key) {
  return [...new Map(items.map((item) => [item[key], item])).values()]
}

function combineParts(parts) {
  return {
    results: uniqueBy(
      parts.flatMap((part) => part.results),
      'key',
    ),
    failures: uniqueBy(
      parts.flatMap((part) => part.failures),
      'provider',
    ),
    suggestions: [...new Set(parts.flatMap((part) => part.suggestions))],
    blocked: parts.map((part) => part.blocked).find(Boolean) ?? null,
  }
}

function similarQuery(item) {
  const words = (item.title || item.host).replace(/\.[a-z0-9]{2,4}$/i, '').split(/[\s_-]+/)
  return words.filter(Boolean).slice(0, SIMILAR_WORDS).join(' ')
}

export const useSearchStore = defineStore('search', () => {
  const query = ref('')
  const result = ref(null)
  const scope = ref(readScope())
  const settings = ref(readSettings(scope.value))
  const networks = ref(['tor'])
  const braveApi = ref(false)
  const engineNames = ref(null)
  const onion = ref(null)
  const childProtection = ref({ required: false, domains: [] })
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
    if (!usesAccount())
      return writeStorage(storageFor(scope.value), STORAGE_KEY, JSON.stringify(value))
    clearTimeout(saveTimer)
    saveTimer = setTimeout(() => saveAccountSettings(value), SAVE_DELAY)
  }

  function enforceChildProtection() {
    if (!childProtection.value.required) return
    const { domains } = childProtection.value
    const current = settings.value
    if (current.allowlistEnabled && current.allowlist.join() === domains.join()) return
    current.allowlist = [...domains]
    current.allowlistEnabled = true
  }

  watch(settings, enforceChildProtection, { deep: true })
  watch(settings, persist, { deep: true })

  async function fetchChildProtection() {
    const response = await apiFetch('/api/search/child-protection/').catch(() => null)
    if (!response?.ok) return
    childProtection.value = await response.json()
    enforceChildProtection()
  }

  async function loadAccountSettings() {
    if (!usesAccount()) return
    const response = await apiFetch('/api/search/settings/')
    if (!response.ok) return
    const { data } = await response.json()
    loadingAccount = true
    settings.value = { ...defaultSearchSettings, ...data }
    enforceChildProtection()
    await nextTick()
    loadingAccount = false
  }

  function setScope(value) {
    scope.value = value
    writeStorage(localStorage, SCOPE_KEY, value)
    removeStorage(value === 'session' ? localStorage : sessionStorage, STORAGE_KEY)
    if (value === 'account') return saveAccountSettings(settings.value)
    writeStorage(storageFor(value), STORAGE_KEY, JSON.stringify(settings.value))
  }

  function clearLocalData() {
    clearSharedSettings()
    try {
      localStorage.clear()
      sessionStorage.clear()
    } catch {
      return
    }
    window.location.replace('/')
  }

  let latestSearch = 0

  async function fetchNetworks() {
    const response = await fetch('/searxng/config', { credentials: 'same-origin' }).catch(
      () => null,
    )
    if (!response?.headers.get('content-type')?.includes('application/json')) return
    const onionLocation = response.headers.get('onion-location')
    onion.value = onionLocation ? new URL(onionLocation).origin : null
    const names = (await response.json()).engines.map(({ name }) => name)
    networks.value = names.some((name) => name.endsWith(' strict')) ? ['tor', 'strict'] : ['tor']
    braveApi.value = names.includes('braveapi')
    engineNames.value = names
  }

  function hasEngine(name) {
    if (!engineNames.value) return true
    return engineNames.value.some((item) => item === name || item.startsWith(`${name} `))
  }

  function isAvailable(engine) {
    if (engine === 'brave' && braveApi.value) return true
    return categories.some(({ engines }) => engines[engine] && hasEngine(engines[engine]))
  }

  function activeNetwork() {
    return networks.value.includes(settings.value.network) ? settings.value.network : 'tor'
  }

  function fallbackNetwork(network) {
    const fallback = FALLBACK_NETWORKS[network]
    return networks.value.includes(fallback) ? fallback : null
  }

  function engineName(category, provider, network) {
    const { engines } = categories.find(({ key }) => key === category)
    const useBraveApi = braveApi.value && category === 'general' && provider === 'brave'
    const name = useBraveApi ? 'braveapi' : engines[provider]
    if (!name) return null
    const engine = network === 'tor' ? name : `${name} ${network}`
    return !engineNames.value || engineNames.value.includes(engine) ? engine : null
  }

  function categoryProviders(category) {
    const { engines } = categories.find(({ key }) => key === category)
    return Object.keys(engines).filter(
      (provider) =>
        settings.value.engines.includes(provider) &&
        engineName(category, provider, activeNetwork()),
    )
  }

  async function fetchPage(q, pageno, engine) {
    const params = new URLSearchParams({
      q,
      pageno,
      format: 'json',
      engines: engine,
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

  async function fetchNetworkPart(q, page, category, provider, network) {
    const engine = engineName(category, provider, network)
    const length = settings.value.pageLength
    const pagenos = Array.from({ length }, (_, index) => (page - 1) * length + index + 1)
    const pages = await Promise.all(pagenos.map((pageno) => fetchPage(q, pageno, engine)))
    return {
      results: pages
        .flatMap((data) => data.results)
        .map(toResult)
        .map((item) => withHttpLinks(item, settings.value.httpLinks))
        .filter((item) => isVisible(item, settings.value)),
      failures: pages.flatMap((data) => data.unresponsive_engines).map(toFailure),
      suggestions: pages[0].suggestions,
      blocked: toBlocked(pages[0].answers.find(({ category }) => category)),
    }
  }

  async function fetchPart(q, page, category, provider) {
    const network = activeNetwork()
    const part = await fetchNetworkPart(q, page, category, provider, network)
    const fallback = fallbackNetwork(network)
    if (part.results.length || !part.failures.length) return part
    if (!fallback || !engineName(category, provider, fallback)) return part
    return fetchNetworkPart(q, page, category, provider, fallback)
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

  function cachedPart(q, page, category, provider) {
    const key = JSON.stringify([q, page, category, provider, settings.value])
    const hit = resultCache.get(key)
    if (hit && Date.now() - hit.time < CACHE_TTL) return hit.promise
    const promise = fetchPart(q, page, category, provider)
    resultCache.set(key, { promise, time: Date.now() })
    promise
      .then((part) => part.results.length || resultCache.delete(key))
      .catch(() => resultCache.delete(key))
    return promise.catch((error) => ({
      error,
      results: [],
      failures: [{ provider, reason: error.message }],
      suggestions: [],
      blocked: null,
    }))
  }

  function fetchParts(q, page, category) {
    const providers = categoryProviders(category)
    if (!providers.length) throw new Error('Für diese Kategorie ist kein Suchanbieter aktiv.')
    return providers.map((provider) => cachedPart(q, page, category, provider))
  }

  async function fetchAll(q, page, category) {
    const parts = await Promise.all(fetchParts(q, page, category))
    if (parts.every(({ error }) => error)) throw parts[0].error
    return { query: q, page, category, ...combineParts(parts), pending: 0 }
  }

  async function search(q, page = 1, category = 'general') {
    const current = ++latestSearch
    query.value = q
    const parts = fetchParts(q, page, category)
    const arrived = []
    const shown = parts.map((promise) =>
      promise.then((part) => {
        arrived.push(part)
        if (current !== latestSearch) return
        const pending = parts.length - arrived.length
        const body = combineParts(arrived)
        result.value = {
          query: q,
          page,
          category,
          ...body,
          pending,
          done: !pending && !body.results.length,
        }
        rateHosts(part.results)
      }),
    )
    const firstResults = parts.map((promise) =>
      promise.then((part) => part.results.length || Promise.reject(part.error)),
    )
    await Promise.any(firstResults).catch(() => Promise.all(shown))
    if (arrived.every(({ error }) => error)) throw arrived[0].error
  }

  async function similarImages(item, page) {
    const body = await fetchAll(similarQuery(item), page, 'images')
    rateHosts(body.results)
    return body.results.filter(({ key }) => key !== item.key)
  }

  async function loadMore() {
    const current = latestSearch
    const { query: q, page, category } = result.value
    const body = await fetchAll(q, page + 1, category)
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
    onion,
    childProtection,
    hostRatings,
    pendingHosts,
    search,
    fetchNetworks,
    isAvailable,
    fetchChildProtection,
    activeNetwork,
    loadMore,
    similarImages,
    loadAccountSettings,
    setScope,
    clearLocalData,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useSearchStore, import.meta.hot))
}
