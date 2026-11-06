import { sharedSetting } from '@core/lib/sharedSetting.js'

export const contrastMode = sharedSetting('contrast-mode', {
  parse: (value) => value === 'on',
  serialize: (enabled) => (enabled ? 'on' : 'off'),
  apply(enabled) {
    const root = document.documentElement
    if (enabled) root.setAttribute('data-contrast', 'on')
    else root.removeAttribute('data-contrast')
  },
})
