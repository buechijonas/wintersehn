import { icons } from '@core/assets/icons.js'
import { social } from '@core/assets/social.js'

export const referenceKinds = {
  text: { label: 'Text', icon: 'blog-text' },
  chat: { label: 'Chat-Simulation', icon: 'user' },
}

export function referenceIcon(reference) {
  return social[reference.icon] ?? icons[referenceKinds[reference.kind].icon]
}

export function referenceSummary(reference) {
  if (reference.kind === 'text') return referenceKinds.text.label
  const { participants, messages } = reference
  return `Chat · ${participants.length} Teilnehmer · ${messages.length} Nachrichten`
}

export const chatSides = {
  left: 'Links',
  right: 'Rechts',
}

export function messageData({ sender, text, image, attack, target }) {
  const hit = attack && target && target !== sender
  return { sender, text, image, attack: hit ? attack : 0, target: hit ? target : null }
}
