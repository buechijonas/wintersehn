export const statuses = [
  { value: 'parent', label: 'Eltern' },
  { value: 'sibling', label: 'Geschwister' },
  { value: 'relative', label: 'Verwandt' },
  { value: 'partner', label: 'Partner' },
  { value: 'friend', label: 'Freund' },
  { value: 'homie', label: 'Homie' },
  { value: 'colleague', label: 'Kollege' },
  { value: 'acquaintance', label: 'Bekannt' },
]

export const statusLabels = {
  ...Object.fromEntries(statuses.map(({ value, label }) => [value, label])),
  child: 'Kind',
}

export const inverseStatus = { parent: 'child' }
