const LINK_PATTERN = /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

// Renders "[label](https://...)" markdown-style links inside plain text as
// real <a> tags. The whole string is HTML-escaped first, so only well-formed
// http(s) links can ever produce a tag - everything else stays inert text.
export function linkifyHtml(text) {
  return escapeHtml(text).replace(
    LINK_PATTERN,
    (match, label, url) =>
      `<a href="${url}" target="_blank" rel="noopener noreferrer" class="link link-primary">${label}</a>`,
  )
}
