export const apps = [
  {
    key: 'search',
    label: 'Suche',
    description: 'Private Suche über Tor, ohne Tracking und ohne Suchprofil.',
    url: import.meta.env.VITE_SEARCH_URL ?? 'https://search.wintersehn.ch',
  },
  {
    key: 'govex',
    label: 'GOVEX',
    description: 'Ein Konto für alle Apps. Profil, Passwort und Sicherheit an einem Ort.',
    url: import.meta.env.VITE_GOVEX_URL ?? 'https://auth.neotyra.com',
  },
  {
    key: 'wintersehn',
    label: 'Wintersehn',
    description: 'Portfolio mit Lebenslauf, Projekten, Reisen und Medien.',
    url: import.meta.env.VITE_WINTERSEHN_URL ?? 'https://wintersehn.ch',
  },
  {
    key: 'monolith',
    label: 'MONOLITH',
    description: 'Dossiers, Ereignisse und Netzwerke, verschlüsselt gespeichert.',
    url: import.meta.env.VITE_MONOLITH_URL ?? 'https://monolith.wintersehn.ch',
    permission: 'can_view_admin',
  },
  {
    key: 'swissfy',
    label: 'swissfy',
    description: 'Soziales Netzwerk mit Beiträgen, Reels, Freunden und verschlüsselten Chats.',
    url: import.meta.env.VITE_SWISSFY_URL ?? 'https://swissfy.ch',
  },
].map((app) => ({ ...app, icon: `/icons/apps/${app.key}.png`, host: new URL(app.url).host }))
