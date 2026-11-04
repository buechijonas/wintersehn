export function slugify(text) {
  const slug = text
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
  return slug || 'artikel'
}

export function uniqueSlug(text, existingSlugs) {
  const base = slugify(text)
  if (!existingSlugs.has(base)) return base

  let suffix = 2
  while (existingSlugs.has(`${base}-${suffix}`)) suffix += 1
  return `${base}-${suffix}`
}
