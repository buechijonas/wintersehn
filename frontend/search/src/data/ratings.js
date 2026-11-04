export const ratingIcons = {
  secure: {
    name: 'shield-check',
    class: 'text-wntrs-secure',
    tone: 'max-sm:bg-wntrs-secure/15',
    label: 'Gut abgesichert laut Mozilla Observatory',
  },
  neutral: {
    name: 'link',
    class: 'text-wntrs-muted',
    tone: 'max-sm:bg-base-200',
    label: 'Mittelmässig abgesichert laut Mozilla Observatory',
  },
  http: {
    name: 'triangle-warning',
    class: 'text-warning',
    tone: 'max-sm:bg-warning/15',
    label: 'Unverschlüsselte Verbindung (http)',
  },
  insecure: {
    name: 'octagon-xmark',
    class: 'text-error',
    tone: 'max-sm:bg-error/15',
    label: 'Schlecht abgesichert laut Mozilla Observatory',
  },
}

export const testLabels = {
  'content-security-policy': 'Content Security Policy',
  cookies: 'Sichere Cookies',
  'cross-origin-embedder-policy': 'Cross-Origin Embedder Policy',
  'cross-origin-opener-policy': 'Cross-Origin Opener Policy',
  'cross-origin-resource-policy': 'Cross-Origin Resource Policy',
  'cross-origin-resource-sharing': 'Cross-Origin Resource Sharing',
  redirection: 'Weiterleitung auf HTTPS',
  'referrer-policy': 'Referrer Policy',
  'strict-transport-security': 'Erzwungenes HTTPS (HSTS)',
  'subresource-integrity': 'Subresource Integrity',
  'x-content-type-options': 'Schutz vor falschen Dateitypen',
  'x-frame-options': 'Schutz vor Clickjacking',
}

export function ratingOf(item, reports) {
  if (item.url.startsWith('http:')) return 'http'
  return reports[item.host]?.rating ?? null
}

export const ratingLegend = [
  { rating: 'secure', text: 'Gut abgesichert, Mozilla Observatory Note A+ bis A-.' },
  { rating: 'neutral', text: 'Mittelmässig abgesichert, Note B+ bis C-.' },
  { rating: 'insecure', text: 'Schlecht abgesichert, Note D+ bis F.' },
  { rating: 'http', text: 'Unverschlüsselte Verbindung (http), unabhängig von der Note.' },
]
