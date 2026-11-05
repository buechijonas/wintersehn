export const searchChoices = {
  engines: ['brave', 'duckduckgo', 'mojeek', 'qwant', 'startpage', 'wikipedia'],
  language: ['all', 'de', 'en', 'fr', 'it'],
  method: ['post', 'get'],
  pagination: ['pages', 'infinite'],
  pageLength: [1, 2, 3],
  timeout: [3, 5, 10],
  network: ['tor', 'strict', 'vpn', 'proxy', 'direct'],
  riskyLinks: ['allow', 'warn', 'block'],
  imageLoading: ['auto', 'click'],
  httpLinks: ['keep', 'upgrade', 'hide'],
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
  imageLoading: 'auto',
  httpLinks: 'keep',
  confirmLinks: false,
  privacyScreen: false,
  panicKey: false,
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

export const panicUrl = 'https://www.wikipedia.org'

export const independentEngines = ['brave', 'mojeek', 'wikipedia']

export const bigTechDomains = [
  'google.*',
  'youtube.*',
  'youtu.be',
  'blogger.com',
  'blogspot.*',
  'gmail.com',
  'googleusercontent.com',
  'googleapis.com',
  'gstatic.com',
  'googleblog.com',
  'withgoogle.com',
  'goo.gl',
  'g.co',
  'android.com',
  'chrome.com',
  'chromium.org',
  'doubleclick.net',
  'googleadservices.com',
  'googlesyndication.com',
  'googletagmanager.com',
  'google-analytics.com',
  'deepmind.com',
  'waze.com',
  'fitbit.com',
  'nest.com',
  'kaggle.com',
  'waymo.com',
  'facebook.*',
  'fb.com',
  'fb.me',
  'fb.watch',
  'instagram.*',
  'instagr.am',
  'threads.net',
  'threads.com',
  'whatsapp.com',
  'whatsapp.net',
  'wa.me',
  'messenger.com',
  'meta.com',
  'meta.ai',
  'oculus.com',
  'workplace.com',
  'amazon.*',
  'amzn.to',
  'amzn.com',
  'audible.*',
  'twitch.tv',
  'imdb.com',
  'primevideo.com',
  'goodreads.com',
  'ring.com',
  'zappos.com',
  'alexa.com',
  'abebooks.com',
  'wholefoodsmarket.com',
  'apple.com',
  'icloud.com',
  'me.com',
  'mac.com',
  'itunes.com',
  'apple.news',
  'beatsbydre.com',
  'microsoft.com',
  'msn.com',
  'bing.com',
  'live.com',
  'outlook.com',
  'hotmail.com',
  'office.com',
  'microsoft365.com',
  'cloud.microsoft',
  'windows.com',
  'azure.com',
  'sharepoint.com',
  'onedrive.com',
  'skype.com',
  'xbox.com',
  'visualstudio.com',
  'minecraft.net',
  'linkedin.com',
  'lnkd.in',
  'github.com',
  'tiktok.com',
  'tiktokv.com',
  'tiktokcdn.com',
  'bytedance.com',
  'capcut.com',
  'lemon8-app.com',
  'x.com',
  'twitter.com',
  't.co',
  'x.ai',
  'grok.com',
  'openai.com',
  'chatgpt.com',
  'chat.com',
  'sora.com',
  'anthropic.com',
  'claude.ai',
  'perplexity.ai',
  'deepseek.com',
]

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
  session: 'Nur diese Sitzung',
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
  strict: 'Tor streng',
  vpn: 'VPN',
  proxy: 'Eigener Proxy',
  direct: 'Direkt',
}

export const networkDescriptions = {
  strict:
    'Wie Tor, aber aufeinanderfolgende Suchen nehmen jeweils einen anderen Weg. So lassen sich deine Suchen auch bei einem Anbieter kaum verknüpfen. Etwas langsamer.',
  tor: 'Anfragen laufen über Tor. Suchanbieter sehen weder dich noch den Server, dafür ist es langsamer und Captchas sind häufiger.',
  vpn: 'Anfragen laufen über einen VPN-Anbieter. Suchanbieter sehen dessen IP. Der VPN-Anbieter sieht, welche Suchanbieter angefragt werden, dank HTTPS aber nicht die Suchbegriffe.',
  direct:
    'Anfragen gehen ohne Umweg vom Server an die Suchanbieter. Am schnellsten und mit wenig Captchas. Die Anbieter sehen die IP des Servers, nie deine, können aber alle Anfragen dieses Servers einander zuordnen.',
  proxy:
    'Anfragen laufen über einen eigenen Proxy des Betreibers. Suchanbieter sehen die IP dieses Proxys. Der Proxy sieht, welche Suchanbieter angefragt werden, dank HTTPS aber nicht die Suchbegriffe.',
}

export const imageLoadingLabels = {
  auto: 'Sofort',
  click: 'Auf Klick',
}

export const httpLinkLabels = {
  keep: 'Belassen',
  upgrade: 'Auf HTTPS umstellen',
  hide: 'Ausblenden',
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

export const filterTemplates = [
  {
    key: 'bigTech',
    label: 'Big Tech ausblenden',
    description:
      'Setzt Google, Meta, Amazon, Apple, Microsoft, TikTok, X, OpenAI und weitere KI-Dienste mit allen Subdomains und Länderendungen auf die Blacklist.',
    icon: 'link-slash-alt',
    list: 'blocklist',
    domains: bigTechDomains,
  },
  {
    key: 'childProtection',
    label: 'Kinderschutz (DE)',
    description:
      'Setzt kindgerechte deutschsprachige Seiten auf die Whitelist. Es erscheinen nur noch Treffer von diesen Seiten.',
    icon: 'shield-check',
    list: 'allowlist',
    domains: null,
  },
]
