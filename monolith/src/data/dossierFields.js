import { cantons } from '@/data/cantons.js'

const DATE_FORMAT = new Intl.DateTimeFormat('de-CH', { dateStyle: 'long' })

export const metaFields = [
  { key: 'birthdate', label: 'Geburtsdatum', type: 'date' },
  { key: 'street', label: 'Strasse', type: 'text' },
  {
    key: 'postal_code',
    label: 'PLZ',
    type: 'text',
    attrs: { inputmode: 'numeric', maxlength: 4, pattern: '\\d{4}' },
  },
  { key: 'canton', label: 'Kanton', options: cantons },
  { key: 'nationality', label: 'Nationalität', type: 'text' },
  { key: 'ethnicity', label: 'Ethnie', type: 'text' },
]

export function formatDate(value) {
  return value && DATE_FORMAT.format(new Date(value))
}

const FORMATTERS = {
  birthdate: formatDate,
  canton: (value) => cantons.find((canton) => canton.value === value)?.label,
}

export function formatField(key, value) {
  return FORMATTERS[key]?.(value) ?? value
}
