import DOMPurify from 'dompurify'
import { marked } from 'marked'

DOMPurify.addHook('afterSanitizeAttributes', (node) => {
  if (node.tagName !== 'A') return
  node.setAttribute('target', '_blank')
  node.setAttribute('rel', 'noopener noreferrer')
})

export function renderMarkdown(text) {
  return DOMPurify.sanitize(marked.parse(text ?? '', { gfm: true, breaks: true }))
}
