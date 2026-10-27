<template>
  <BaseCard
    :tag="destination ? 'router-link' : 'div'"
    :to="destination?.to"
    class="flex items-center gap-4 p-4"
    :class="{ 'hover:bg-base-200': destination }"
  >
    <img
      v-if="destination"
      class="size-12 shrink-0"
      :src="flags[destination.icon]"
      :alt="destination.label"
    />
    <div class="flex flex-col min-w-0">
      <span class="text-xs uppercase tracking-wide text-wntrs-muted">Nächstes Ziel</span>
      <span class="text-lg truncate">{{ destination?.label ?? 'Noch nicht festgelegt' }}</span>
    </div>
    <div v-if="destination" class="ml-auto flex flex-col items-end text-right shrink-0">
      <span class="text-sm">{{ countdown }}</span>
      <span v-if="destination.date" class="text-xs text-wntrs-slate">{{ formattedDate }}</span>
    </div>
  </BaseCard>
</template>

<script>
import BaseCard from '@core/components/common/BaseCard.vue'
import { countries } from '@core/assets/images.js'

const relativeDays = new Intl.RelativeTimeFormat('de', { numeric: 'auto' })
const longDate = new Intl.DateTimeFormat('de-CH', { dateStyle: 'long' })

export default {
  name: 'DestinationCard',
  components: { BaseCard },
  props: {
    destination: { type: Object, default: null },
  },
  data() {
    return { flags: countries }
  },
  computed: {
    countdown() {
      const days = this.destination.days_left
      return days === null ? 'Datum offen' : relativeDays.format(days, 'day')
    },
    formattedDate() {
      return longDate.format(new Date(this.destination.date))
    },
  },
}
</script>
