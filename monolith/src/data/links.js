import { addictionLabels, frequencyLabels } from '@/data/addictions.js'
import { platformName } from '@/data/platforms.js'
import { statusLabels } from '@/data/statuses.js'
import { topics } from '@/data/topics.js'

export const linkTypes = ['stances', 'traits', 'addictions', 'references', 'relationships']

export function link(type, ref, text) {
  return { type, ref, text, key: JSON.stringify([type, ref]) }
}

export function stanceLink({ topic, tag }) {
  return link('stances', { topic, tag }, `${topics[topic].label}: ${tag}`)
}

export function traitLink(tag) {
  return link('traits', tag, `Charakter: ${tag}`)
}

export function addictionLink({ kind, frequency }) {
  return link('addictions', kind, `${addictionLabels[kind]} · ${frequencyLabels[frequency]}`)
}

export function referenceLink({ uuid, icon, name }) {
  return link('references', uuid, `${platformName(icon)}: ${name}`)
}

export function relationshipLink({ person, status }) {
  const text = [person.title, statusLabels[status]].filter(Boolean).join(' · ')
  return link('relationships', person.uuid, text)
}

export function eventLinks(event) {
  return [
    ...event.stances.map(stanceLink),
    ...event.traits.map(traitLink),
    ...event.addictions.map(addictionLink),
    ...event.references.map(referenceLink),
    ...event.relationships.map(relationshipLink),
  ]
}
