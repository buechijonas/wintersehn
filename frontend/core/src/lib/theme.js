import { sharedSetting } from '@core/lib/sharedSetting.js'

const VALID_MODES = ['auto', 'light', 'dark']
const THEMES = { light: 'wntrs', dark: 'dark' }

export const themeMode = sharedSetting('theme', {
  parse: (value) => (VALID_MODES.includes(value) ? value : 'auto'),
  serialize: (mode) => mode,
  apply(mode) {
    const root = document.documentElement
    if (THEMES[mode]) root.setAttribute('data-theme', THEMES[mode])
    else root.removeAttribute('data-theme')
  },
})
