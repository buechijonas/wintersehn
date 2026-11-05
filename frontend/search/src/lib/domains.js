function stripWww(host) {
  return host.replace(/^www\./, '')
}

export function toDomain(input) {
  const value = input.trim().toLowerCase()
  if (!value) return null
  try {
    return stripWww(new URL(value.includes('://') ? value : `https://${value}`).hostname)
  } catch {
    return null
  }
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

function matchesHost(host, domain) {
  if (!domain.endsWith('.*')) return host === domain || host.endsWith(`.${domain}`)
  const base = escapeRegExp(domain.slice(0, -2))
  return new RegExp(`(^|\\.)${base}\\.[a-z0-9-]+(\\.[a-z]{2,3})?$`).test(host)
}

function matchesPath(pathname, path) {
  return !path || pathname === path || pathname.startsWith(`${path}/`)
}

export function matchesDomain(url, entries) {
  const { hostname, pathname } = new URL(url)
  const plain = stripWww(hostname)
  return entries.some((entry) => {
    const [domain, ...segments] = entry.split('/')
    const path = segments.length ? `/${segments.join('/')}` : ''
    return matchesHost(plain, domain) && matchesPath(pathname, path)
  })
}
