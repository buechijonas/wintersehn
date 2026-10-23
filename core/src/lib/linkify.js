const LINK_PATTERN = /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

export function linkifyHtml(text) {
  return escapeHtml(text).replace(
    LINK_PATTERN,
    (match, label, url) =>
      `<a href="${url}" target="_blank" rel="noopener noreferrer" class="link link-primary">${label}</a>`,
  )
}
