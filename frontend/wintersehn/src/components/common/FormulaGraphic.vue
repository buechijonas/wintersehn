<template>
  <svg viewBox="0 0 480 200" class="mx-auto max-h-64 w-full text-base-content" role="img" :aria-label="label">
    <defs>
      <marker
        :id="arrowId"
        viewBox="0 0 10 10"
        refX="9"
        refY="5"
        markerWidth="6"
        markerHeight="6"
        orient="auto-start-reverse"
      >
        <path d="M0 0L10 5L0 10z" class="fill-current" />
      </marker>
    </defs>

    <g v-if="name === 'forces'" class="font-serif italic" font-size="14">
      <line
        x1="70"
        y1="100"
        x2="190"
        y2="100"
        class="stroke-current opacity-40"
        stroke-dasharray="4 4"
      />
      <line
        x1="70"
        y1="100"
        x2="20"
        y2="100"
        class="stroke-primary"
        stroke-width="2"
        :marker-end="arrow"
      />
      <line
        x1="190"
        y1="100"
        x2="240"
        y2="100"
        class="stroke-primary"
        stroke-width="2"
        :marker-end="arrow"
      />
      <circle cx="70" cy="100" r="14" class="fill-base-200 stroke-current" />
      <circle cx="190" cy="100" r="14" class="fill-base-200 stroke-current" />
      <text x="130" y="90" text-anchor="middle" class="fill-current">d</text>
      <text x="30" y="85" class="fill-primary">Δv</text>
      <text x="215" y="85" class="fill-primary">Δv</text>
      <text x="130" y="150" text-anchor="middle" class="fill-current opacity-60" font-size="12">
        nicht verbunden: abstossen
      </text>

      <line x1="320" y1="100" x2="440" y2="100" class="stroke-current" stroke-width="2" />
      <line
        x1="345"
        y1="100"
        x2="320"
        y2="100"
        class="stroke-primary"
        stroke-width="2"
        :marker-end="arrow"
      />
      <line
        x1="415"
        y1="100"
        x2="440"
        y2="100"
        class="stroke-primary"
        stroke-width="2"
        :marker-end="arrow"
      />
      <circle cx="345" cy="100" r="14" class="fill-base-200 stroke-current" />
      <circle cx="415" cy="100" r="14" class="fill-base-200 stroke-current" />
      <line
        x1="320"
        y1="130"
        x2="440"
        y2="130"
        class="stroke-current opacity-60"
        :marker-start="arrow"
        :marker-end="arrow"
      />
      <text x="380" y="122" text-anchor="middle" class="fill-current">Lₘᵢₙ</text>
      <text x="380" y="150" text-anchor="middle" class="fill-current opacity-60" font-size="12">
        verbunden: auf Mindestlänge
      </text>
    </g>

    <g v-else-if="name === 'crossing'" class="font-serif italic" font-size="14">
      <line x1="40" y1="160" x2="200" y2="40" class="stroke-current" stroke-width="2" />
      <line x1="40" y1="40" x2="200" y2="160" class="stroke-primary" stroke-width="2" />
      <circle cx="120" cy="100" r="5" class="fill-error" />
      <text x="28" y="175" class="fill-current">A</text>
      <text x="204" y="38" class="fill-current">B</text>
      <text x="28" y="35" class="fill-primary">C</text>
      <text x="204" y="175" class="fill-primary">D</text>
      <text x="120" y="190" text-anchor="middle" class="fill-current opacity-60" font-size="12">
        C und D auf verschiedenen Seiten von AB
      </text>

      <line x1="280" y1="150" x2="460" y2="150" class="stroke-current" stroke-width="2" />
      <circle cx="280" cy="150" r="4" class="fill-current" />
      <circle cx="460" cy="150" r="4" class="fill-current" />
      <circle cx="390" cy="60" r="10" class="fill-base-200 stroke-primary" stroke-width="2" />
      <line x1="390" y1="70" x2="390" y2="150" class="stroke-primary" stroke-dasharray="4 4" />
      <circle cx="390" cy="150" r="5" class="fill-primary" />
      <text x="268" y="172" class="fill-current">A</text>
      <text x="456" y="172" class="fill-current">B</text>
      <text x="406" y="64" class="fill-primary">P</text>
      <text x="390" y="172" text-anchor="middle" class="fill-primary">t</text>
      <text x="370" y="190" text-anchor="middle" class="fill-current opacity-60" font-size="12">
        nächster Punkt auf der Linie
      </text>
    </g>

    <g v-else-if="name === 'zoom'" class="font-serif italic" font-size="14">
      <rect
        x="150"
        y="70"
        width="120"
        height="70"
        class="fill-none stroke-current opacity-60"
        stroke-dasharray="4 4"
      />
      <rect
        x="90"
        y="30"
        width="240"
        height="140"
        class="fill-none stroke-primary"
        stroke-width="2"
      />
      <line x1="210" y1="105" x2="90" y2="30" class="stroke-current opacity-30" />
      <line x1="210" y1="105" x2="330" y2="30" class="stroke-current opacity-30" />
      <line x1="210" y1="105" x2="90" y2="170" class="stroke-current opacity-30" />
      <line x1="210" y1="105" x2="330" y2="170" class="stroke-current opacity-30" />
      <circle cx="210" cy="105" r="5" class="fill-error" />
      <text x="218" y="100" class="fill-error">o</text>
      <text x="156" y="88" class="fill-current opacity-60">k</text>
      <text x="96" y="48" class="fill-primary">k′</text>
      <text x="400" y="95" text-anchor="middle" class="fill-current opacity-60" font-size="12">
        o bleibt fix,
      </text>
      <text x="400" y="113" text-anchor="middle" class="fill-current opacity-60" font-size="12">
        alles andere skaliert
      </text>
    </g>

    <g v-else-if="name === 'circles'" class="font-serif italic" font-size="14">
      <circle cx="150" cy="100" r="22" class="fill-primary opacity-20" />
      <circle cx="150" cy="100" r="50" class="fill-none stroke-current opacity-40" />
      <circle cx="150" cy="100" r="78" class="fill-none stroke-current opacity-40" />
      <circle
        cx="150"
        cy="100"
        r="36"
        class="fill-none stroke-current opacity-20"
        stroke-dasharray="3 3"
      />
      <circle
        cx="150"
        cy="100"
        r="64"
        class="fill-none stroke-current opacity-20"
        stroke-dasharray="3 3"
      />
      <line
        x1="150"
        y1="100"
        x2="150"
        y2="36"
        class="stroke-current opacity-40"
        stroke-dasharray="3 3"
      />
      <line x1="150" y1="100" x2="205" y2="68" class="stroke-primary" />
      <path d="M150 80 A20 20 0 0 1 167 90" class="fill-none stroke-primary" />
      <circle
        v-for="dot in ringDots"
        :key="dot.key"
        :cx="dot.x"
        :cy="dot.y"
        r="6"
        class="fill-primary"
      />
      <text x="166" y="78" class="fill-primary">θ</text>
      <text x="150" y="105" text-anchor="middle" class="fill-current">r₀</text>
      <text x="235" y="100" class="fill-current">w</text>
      <text x="370" y="85" text-anchor="middle" class="fill-current opacity-60" font-size="12">
        gleichmässig verteilt,
      </text>
      <text x="370" y="103" text-anchor="middle" class="fill-current opacity-60" font-size="12">
        Start oben bei −π/2
      </text>
    </g>

    <g v-else-if="name === 'blind-index'" class="font-serif italic" font-size="14">
      <rect x="20" y="40" width="90" height="40" rx="6" class="fill-base-200 stroke-current" />
      <rect x="20" y="120" width="90" height="40" rx="6" class="fill-base-200 stroke-current" />
      <text x="65" y="65" text-anchor="middle" class="fill-current">x = «wien»</text>
      <text x="65" y="145" text-anchor="middle" class="fill-current">x = «wien»</text>
      <rect
        x="180"
        y="70"
        width="120"
        height="60"
        rx="6"
        class="fill-primary opacity-15 stroke-primary"
      />
      <text x="240" y="105" text-anchor="middle" class="fill-primary not-italic" font-size="13">
        HMAC-SHA256
      </text>
      <text x="240" y="30" text-anchor="middle" class="fill-current">k</text>
      <line x1="240" y1="36" x2="240" y2="68" class="stroke-current" :marker-end="arrow" />
      <line x1="110" y1="60" x2="178" y2="92" class="stroke-current" :marker-end="arrow" />
      <line x1="110" y1="140" x2="178" y2="108" class="stroke-current" :marker-end="arrow" />
      <line x1="300" y1="100" x2="348" y2="100" class="stroke-current" :marker-end="arrow" />
      <rect x="350" y="80" width="110" height="40" rx="6" class="fill-base-200 stroke-current" />
      <text
        x="405"
        y="105"
        text-anchor="middle"
        class="fill-current not-italic font-mono"
        font-size="12"
      >
        h = 9f3a…
      </text>
      <text x="405" y="150" text-anchor="middle" class="fill-current opacity-60" font-size="12">
        gleich bei gleichem x,
      </text>
      <text x="405" y="168" text-anchor="middle" class="fill-current opacity-60" font-size="12">
        ohne k nicht umkehrbar
      </text>
    </g>
  </svg>
</template>

<script>
const RINGS = [
  { radius: 36, count: 3 },
  { radius: 64, count: 5 },
]

export default {
  name: 'FormulaGraphic',
  props: {
    name: { type: String, required: true },
    label: { type: String, default: '' },
  },
  computed: {
    arrowId() {
      return `formula-arrow-${this.name}`
    },
    arrow() {
      return `url(#${this.arrowId})`
    },
    ringDots() {
      return RINGS.flatMap(({ radius, count }) =>
        Array.from({ length: count }, (_, index) => {
          const angle = -Math.PI / 2 + ((index + 0.5) / count) * 2 * Math.PI
          return {
            key: `${radius}-${index}`,
            x: 150 + radius * Math.cos(angle),
            y: 100 + radius * Math.sin(angle),
          }
        }),
      )
    },
  },
}
</script>
