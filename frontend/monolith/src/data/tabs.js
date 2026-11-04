export const sectionTabs = [
  { key: 'meta', label: 'Meta' },
  { key: 'character', label: 'Charakter' },
  { key: 'events', label: 'Ereignisse' },
  { key: 'relationships', label: 'Beziehungen' },
  { key: 'trust', label: 'Vertrauen' },
  { key: 'ideology', label: 'Ideologie' },
  { key: 'addictions', label: 'Sucht' },
  { key: 'references', label: 'Referenzen' },
]

export const sectionLabels = Object.fromEntries(sectionTabs.map(({ key, label }) => [key, label]))
