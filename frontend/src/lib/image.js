const UPLOAD_PATTERN = /^\/media\/uploads\/([0-9a-f]{32}\.(?:jpg|png|webp))$/

const DENSITIES = [1, 2, 3]

function thumbnailUrl(name, size) {
  return `/api/content/images/${name}/?size=${size}`
}

// Square crop for a fixed-size `object-cover` box, sharp on high-density screens.
export function squareImage(src, size) {
  const name = src.match(UPLOAD_PATTERN)?.[1]
  if (!name) return { src }
  return {
    src: thumbnailUrl(name, size),
    srcset: DENSITIES.map((d) => `${thumbnailUrl(name, size * d)} ${d}x`).join(', '),
  }
}
