const profileModules = import.meta.glob('./images/profile/*.svg', {
  eager: true,
  import: 'default',
})

export const profiles = Object.fromEntries(
  Object.entries(profileModules).map(([path, src]) => [
    path.split('/').pop().replace('.svg', ''),
    src,
  ]),
)
