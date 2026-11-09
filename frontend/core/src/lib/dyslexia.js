import { sharedSetting } from '@core/lib/sharedSetting.js'

export const dyslexiaFont = sharedSetting('wntrs-dyslexia-font', {
  parse: (value) => value === 'on',
  serialize: (enabled) => (enabled ? 'on' : 'off'),
  apply(enabled) {
    const root = document.documentElement
    if (enabled) root.setAttribute('data-dyslexia', 'on')
    else root.removeAttribute('data-dyslexia')
  },
})
