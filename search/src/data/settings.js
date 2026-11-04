export const searchChoices = {
  engines: ['brave', 'duckduckgo', 'mojeek', 'qwant', 'startpage', 'wikipedia'],
  language: ['all', 'de', 'en', 'fr', 'it'],
  method: ['post', 'get'],
  pagination: ['pages', 'infinite'],
  pageLength: [1, 2, 3],
  timeout: [3, 5, 10],
}

export const defaultSearchSettings = {
  engines: searchChoices.engines,
  language: 'de',
  method: 'post',
  pagination: 'pages',
  pageLength: 1,
  timeout: 5,
  blocklistEnabled: false,
  blocklist: [],
  allowlistEnabled: false,
  allowlist: [],
}

export const settingsTabs = [
  { key: 'account', label: 'Account' },
  { key: 'appearance', label: 'Darstellung' },
  { key: 'privacy', label: 'Datenschutz' },
  { key: 'filter', label: 'Filter' },
]

export const engineLabels = {
  brave: { label: 'Brave', description: 'Eigener Index, kein Nutzerprofil.' },
  duckduckgo: { label: 'DuckDuckGo', description: 'Kein Tracking, Ergebnisse u. a. von Bing.' },
  mojeek: { label: 'Mojeek', description: 'Eigener Index aus Grossbritannien, kein Tracking.' },
  qwant: { label: 'Qwant', description: 'Europäische Suchmaschine, kein Tracking.' },
  startpage: { label: 'Startpage', description: 'Google-Ergebnisse ohne Google-Tracking.' },
  wikipedia: {
    label: 'Wikipedia',
    description: 'Enzyklopädie und Wikimedia Commons, kein Tracking.',
  },
}

export const languageLabels = {
  all: 'Keine',
  de: 'Deutsch',
  en: 'Englisch',
  fr: 'Französisch',
  it: 'Italienisch',
}

export const methodLabels = {
  post: 'POST',
  get: 'GET',
}

export const storageLabels = {
  browser: 'Dieser Browser',
  account: 'Konto',
}

export const paginationLabels = {
  pages: 'Seiten',
  infinite: 'Endless Scrolling',
}

export const timeoutLabels = {
  3: 'Schnell',
  5: 'Ausgewogen',
  10: 'Gründlich',
}

export const pageLengthLabels = {
  1: 'Kurz',
  2: 'Mittel',
  3: 'Lang',
}

export const protections = [
  'Suchanfragen werden nirgends gespeichert.',
  'Einstellungen bleiben in deinem Browser, nicht auf dem Server.',
  'Suchanbieter sehen weder deine IP noch Cookies oder Browserdaten.',
  'Zielseiten erhalten keinen Referrer.',
  'Tracking-Parameter werden aus Treffer-Links entfernt.',
  'Keine Autovervollständigung, keine Favicons, keine Statistiken.',
]

export const categories = [
  {
    key: 'general',
    label: 'Alle',
    engines: {
      brave: 'brave',
      duckduckgo: 'duckduckgo',
      mojeek: 'mojeek',
      qwant: 'qwant',
      startpage: 'startpage',
      wikipedia: 'wikipedia',
    },
  },
  {
    key: 'images',
    label: 'Bilder',
    engines: {
      brave: 'brave.images',
      duckduckgo: 'duckduckgo images',
      mojeek: 'mojeek images',
      qwant: 'qwant images',
      startpage: 'startpage images',
      wikipedia: 'wikicommons.images',
    },
  },
  {
    key: 'videos',
    label: 'Videos',
    engines: {
      brave: 'brave.videos',
      duckduckgo: 'duckduckgo videos',
      qwant: 'qwant videos',
      wikipedia: 'wikicommons.videos',
    },
  },
  {
    key: 'news',
    label: 'News',
    engines: {
      brave: 'brave.news',
      duckduckgo: 'duckduckgo news',
      mojeek: 'mojeek news',
      qwant: 'qwant news',
      startpage: 'startpage news',
    },
  },
]
