<template>
  <div>
    <div class="flex items-center justify-between gap-4 text-sm">
      <span class="font-bold">{{ label }}</span>
      <span v-if="value === null" class="text-xs text-wntrs-muted">Nicht einstufbar</span>
    </div>
    <div
      class="relative h-1.5 mt-3 rounded-full bg-base-300"
      role="meter"
      aria-valuemin="-100"
      aria-valuemax="100"
      :aria-valuenow="value ?? undefined"
      :aria-label="`${label}: ${poles.join(' – ')}`"
    >
      <span
        v-if="value !== null"
        class="absolute top-1/2 size-3 -translate-x-1/2 -translate-y-1/2 rounded-full bg-primary"
        :style="{ left: `${(value + 100) / 2}%` }"
      ></span>
    </div>
    <div class="flex justify-between gap-4 mt-1 text-xs text-wntrs-muted">
      <span>{{ poles[0] }}</span>
      <span class="text-right">{{ poles[1] }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SpectrumBar',
  props: {
    label: { type: String, required: true },
    poles: { type: Array, required: true },
    value: { type: Number, default: null },
  },
}
</script>
