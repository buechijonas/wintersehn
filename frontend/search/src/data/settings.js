export const searchChoices = {
  engines: ['brave', 'duckduckgo', 'mojeek', 'qwant', 'startpage', 'wikipedia'],
  language: ['all', 'de', 'en', 'fr', 'it'],
  method: ['post', 'get'],
  pagination: ['pages', 'infinite'],
  pageLength: [1, 2, 3],
  timeout: [3, 5, 10],
  network: ['tor', 'vpn', 'proxy', 'direct'],
  riskyLinks: ['allow', 'warn', 'block'],
}

export const defaultSearchSettings = {
  engines: searchChoices.engines,
  language: 'de',
  method: 'post',
  pagination: 'pages',
  pageLength: 1,
  timeout: 5,
  network: 'tor',
  riskyLinks: 'warn',
  blocklistEnabled: false,
  blocklist: [],
  allowlistEnabled: false,
  allowlist: [],
}

export const settingsTabs = [
  { key: 'account', label: 'Account' },
  { key: 'appearance', label: 'Darstellung' },
  { key: 'privacy', label: 'Datenschutz' },
  { key: 'security', label: 'Sicherheit' },
  { key: 'filter', label: 'Filter' },
  { key: 'donate', label: 'Spenden' },
  { key: 'sponsors', label: 'Sponsoren', permission: 'can_view_admin' },
]

export const donateUrl = 'https://buymeacoffee.com/wintersehn'

export const engineLabels = {
  brave: {
    label: 'Brave',
    description:
      'Eigener Index, kein Nutzerprofil. Läuft über die offizielle API, wenn eingerichtet.',
  },
  duckduckgo: { label: 'DuckDuckGo', description: 'Kein Tracking, Ergebnisse u. a. von Bing.' },
  mojeek: { label: 'Mojeek', description: 'Eigener Index aus Grossbritannien, kein Tracking.' },
  qwant: { label: 'Qwant', description: 'Europäische Suchmaschine, kein Tracking.' },
  startpage: { label: 'Startpage', description: 'Google-Ergebnisse ohne Google-Tracking.' },
  wikipedia: {
    label: 'Wikipedia',
    description: 'Enzyklopädie und Wikimedia Commons, kein Tracking.',
  },
}

export const failureLabels = {
  'too many requests': 'zu viele Anfragen',
  CAPTCHA: 'Captcha',
  timeout: 'Zeitüberschreitung',
  'access denied': 'Zugriff verweigert',
  'HTTP connection error': 'keine Verbindung',
  'parsing error': 'unlesbare Antwort',
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

export const riskyLinkLabels = {
  allow: 'Öffnen',
  warn: 'Warnen',
  block: 'Sperren',
}

export const networkLabels = {
  tor: 'Tor',
  vpn: 'VPN',
  proxy: 'Eigener Proxy',
  direct: 'Direkt',
}

export const networkDescriptions = {
  tor: 'Anfragen laufen über Tor. Suchanbieter sehen weder dich noch den Server, dafür ist es langsamer und Captchas sind häufiger.',
  vpn: 'Anfragen laufen über einen VPN-Anbieter. Suchanbieter sehen dessen IP. Der VPN-Anbieter sieht, welche Suchanbieter angefragt werden, dank HTTPS aber nicht die Suchbegriffe.',
  direct:
    'Anfragen gehen ohne Umweg vom Server an die Suchanbieter. Am schnellsten und mit wenig Captchas. Die Anbieter sehen die IP des Servers, nie deine, können aber alle Anfragen dieses Servers einander zuordnen.',
  proxy:
    'Anfragen laufen über einen eigenen Proxy des Betreibers. Suchanbieter sehen die IP dieses Proxys. Der Proxy sieht, welche Suchanbieter angefragt werden, dank HTTPS aber nicht die Suchbegriffe.',
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
  'Zeichen hinter der Adresse warnen vor unverschlüsselten oder schlecht abgesicherten Seiten.',
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
