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

export function matchesDomain(host, domains) {
  const plain = stripWww(host)
  return domains.some((domain) => plain === domain || plain.endsWith(`.${domain}`))
}
