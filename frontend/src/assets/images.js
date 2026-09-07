const modules = import.meta.glob('./images/undraws/*.svg', { eager: true, import: 'default' })

export const undraws = Object.fromEntries(
  Object.entries(modules).map(([path, src]) => [path.split('/').pop().replace('.svg', ''), src]),
)
