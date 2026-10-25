<template>
  <div class="flex items-center gap-2" :title="`${remaining} / ${health} Health`">
    <progress
      class="progress flex-1"
      :class="tone"
      :value="remaining"
      :max="health"
      aria-label="Health"
    ></progress>
    <span class="font-mono text-xs tabular-nums text-wntrs-muted shrink-0">
      {{ remaining }}/{{ health }}
    </span>
  </div>
</template>

<script>
export default {
  name: 'HealthBar',
  props: {
    remaining: { type: Number, required: true },
    health: { type: Number, required: true },
  },
  computed: {
    tone() {
      const ratio = this.remaining / this.health
      if (ratio > 0.6) return 'progress-success'
      if (ratio > 0.3) return 'progress-warning'
      return 'progress-error'
    },
  },
}
</script>
