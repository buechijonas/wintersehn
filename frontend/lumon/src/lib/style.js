import { sharedSetting } from '@core/lib/sharedSetting.js'

export const STYLES = ['standard', 'netflix']

export const lumonStyle = sharedSetting('wntrs-lumon-style', {
  parse: (value) => (STYLES.includes(value) ? value : 'standard'),
  serialize: (style) => style,
  apply(style) {
    if (style === 'netflix') document.body.setAttribute('data-theme', 'cinema')
    else document.body.removeAttribute('data-theme')
  },
})
