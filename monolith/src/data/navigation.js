const monolithOnly = { disabled: true, permission: 'can_view_monolith', cipher: true }

export const navigationItems = [
  { key: 'dossiers', label: 'Personalakten', icon: 'portfolio', to: '/', ...monolithOnly },
  {
    key: 'network',
    label: 'Netzwerk',
    icon: 'network-analytic',
    to: '/network',
    ...monolithOnly,
  },
  { key: 'trust', label: 'Vertrauenskreise', icon: 'solar-system', to: '/trust', ...monolithOnly },
  {
    key: 'shared',
    label: 'Mit mir geteilt',
    icon: 'share-square',
    to: '/shared',
    requiresAuth: true,
  },
]
