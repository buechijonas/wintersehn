<template>
  <span
    class="font-mono font-bold text-sm tabular-nums"
    :class="points > 0 ? 'text-success' : points < 0 ? 'text-error' : 'text-wntrs-muted'"
    :title="`${formatPoints(points)} Vertrauenspunkte`"
  >
    {{ formatPoints(points) }}
  </span>
</template>

<script>
import { formatPoints } from '@/data/trust.js'

export default {
  name: 'TrustPoints',
  props: {
    points: { type: Number, required: true },
  },
  methods: {
    formatPoints,
  },
}
</script>
