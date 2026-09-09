const undrawModules = import.meta.glob('./images/undraws/*.svg', { eager: true, import: 'default' })
const flatModules = import.meta.glob('./images/flats/*.svg', { eager: true, import: 'default' })
const countryModules = import.meta.glob('./images/countries/*.svg', { eager: true, import: 'default' })
const profileModules = import.meta.glob('./images/profile/*.svg', { eager: true, import: 'default' })

export const undraws = Object.fromEntries(
  Object.entries(undrawModules).map(([path, src]) => [
    path.split('/').pop().replace('.svg', ''),
    src,
  ]),
)

export const flats = Object.fromEntries(
  Object.entries(flatModules).map(([path, src]) => [
    path.split('/').pop().replace('.svg', ''),
    src,
  ]),
)

export const countries = Object.fromEntries(
  Object.entries(countryModules).map(([path, src]) => [
    path.split('/').pop().replace('.svg', ''),
    src,
  ]),
)

export const profiles = Object.fromEntries(
  Object.entries(profileModules).map(([path, src]) => [
    path.split('/').pop().replace('.svg', ''),
    src,
  ]),
)
