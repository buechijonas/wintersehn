const PLATFORM_NAMES = {
  '4chan': '4chan',
  epicgames: 'Epic Games',
  github: 'GitHub',
  gog: 'GOG',
  linkedin: 'LinkedIn',
  peertube: 'PeerTube',
  protonmail: 'Proton Mail',
  teamspeak: 'TeamSpeak',
  tiktok: 'TikTok',
  whatsapp: 'WhatsApp',
  x: 'X',
  youtube: 'YouTube',
}

export function platformName(icon) {
  return PLATFORM_NAMES[icon] ?? icon.charAt(0).toUpperCase() + icon.slice(1)
}
