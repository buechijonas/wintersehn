export const addictionGroups = [
  {
    label: 'Genussmittel',
    kinds: [
      { value: 'alcohol', label: 'Alkohol' },
      { value: 'cigarettes', label: 'Zigaretten' },
      { value: 'vapes', label: 'Vapes' },
      { value: 'snus', label: 'Snus' },
      { value: 'caffeine', label: 'Koffein' },
    ],
  },
  {
    label: 'Drogen',
    kinds: [
      { value: 'cannabis', label: 'Cannabis' },
      { value: 'cocaine', label: 'Kokain' },
      { value: 'mdma', label: 'MDMA / Ecstasy' },
      { value: 'amphetamines', label: 'Amphetamine' },
      { value: 'ketamine', label: 'Ketamin' },
      { value: 'psychedelics', label: 'Psychedelika' },
      { value: 'opioids', label: 'Opioide' },
      { value: 'sedatives', label: 'Beruhigungsmittel' },
    ],
  },
  {
    label: 'Verhalten',
    kinds: [
      { value: 'casino', label: 'Casino' },
      { value: 'sports_betting', label: 'Sportwetten' },
      { value: 'gaming', label: 'Gaming' },
      { value: 'social_media', label: 'Social Media' },
      { value: 'pornography', label: 'Pornografie' },
      { value: 'shopping', label: 'Kaufsucht' },
    ],
  },
]

export const addictionLabels = Object.fromEntries(
  addictionGroups.flatMap((group) => group.kinds).map(({ value, label }) => [value, label]),
)

export const frequencies = [
  { value: 'daily', label: 'Täglich' },
  { value: 'weekly', label: 'Wöchentlich' },
  { value: 'monthly', label: 'Monatlich' },
  { value: 'occasionally', label: 'Gelegentlich' },
  { value: 'former', label: 'Ehemalig' },
]

export const frequencyLabels = Object.fromEntries(
  frequencies.map(({ value, label }) => [value, label]),
)
