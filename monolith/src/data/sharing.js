import { addictionLabels, frequencyLabels } from '@/data/addictions.js'
import { formatDate, formatField, metaFields } from '@/data/dossierFields.js'
import { platformName } from '@/data/platforms.js'
import { statusLabels } from '@/data/statuses.js'
import { topics } from '@/data/topics.js'
import { sectionLabels } from '@/data/tabs.js'
import { conductLabels, formatPoints } from '@/data/trust.js'

export const visibilities = [
  { value: 'visible', label: 'Sichtbar', title: 'Sichtbar' },
  { value: 'value', label: 'Teilzensiert', title: 'Bezeichnung sichtbar, Wert zensiert' },
  { value: 'full', label: 'Zensiert', title: 'Bezeichnung und Wert zensiert' },
]

export const titleVisibilities = visibilities.filter(({ value }) => value !== 'value')

const fieldLabels = Object.fromEntries(metaFields.map(({ key, label }) => [key, label]))

const trustLabels = {
  summary: () => 'Vertrauenspunkte',
  entry: ({ conduct, points }) => `${conductLabels[conduct]} (${formatPoints(points)})`,
}

const trustValues = {
  summary: ({ points, level }) => `${formatPoints(points)} · Kreis ${level ?? '–'}`,
  entry: ({ date, text }) => `${formatDate(date)} – ${text}`,
}

const formatters = {
  meta: {
    label: (key) => fieldLabels[key],
    value: (value, key) => formatField(key, value) || '–',
  },
  character: {
    label: () => 'Charakter',
    value: (tags) => tags.join(', '),
  },
  events: {
    label: ({ date, title }) => `${formatDate(date)} · ${title}`,
    value: (text) => text || '–',
  },
  relationships: {
    label: (title) => title,
    value: (status) => statusLabels[status] ?? '–',
  },
  trust: {
    label: (label) => trustLabels[label.kind](label),
    value: (value, label) => trustValues[label.kind](value),
  },
  ideology: {
    label: (topic) => topics[topic].label,
    value: (tags) => tags.join(', '),
  },
  addictions: {
    label: (kind) => addictionLabels[kind],
    value: (frequency) => frequencyLabels[frequency],
  },
  references: {
    label: ({ icon, name }) => `${platformName(icon)}: ${name}`,
    value: (url) => url,
  },
}

export function formatLabel(section, label) {
  return formatters[section].label(label)
}

export function formatValue(section, value, label) {
  return formatters[section].value(value, label)
}

export function labelShown(item) {
  return item.visibility !== 'full'
}

export function valueShown(item) {
  return item.visibility === 'visible'
}

export function activeTab(route) {
  return Number(route.query.tab ?? 0)
}

function crumb(label, shown, to) {
  return shown ? { label, to } : { cipher: true, to }
}

export function sharedBreadcrumbs(document, tab, root) {
  const section = document.sections[tab] ?? document.sections[0]
  const crumbs = [
    crumb(document.title.value, valueShown(document.title)),
    crumb(sectionLabels[section.key], document.breadcrumbs.tab && section.key),
  ]
  return root ? [crumb(root.label, document.breadcrumbs.root, root.to), ...crumbs] : crumbs
}
