<template>
  <li class="flex gap-4 px-6 py-4 text-sm">
    <div class="flex flex-col gap-0.5 flex-1 min-w-0">
      <span class="font-mono italic text-xs text-wntrs-muted">
        {{ formatDate(entry.date) }}
      </span>
      <span class="font-bold">{{ conductLabels[entry.conduct] }}</span>
      <span class="break-words whitespace-pre-line">{{ entry.text }}</span>
      <ul v-if="entry.traits.length" class="flex flex-wrap gap-1.5 mt-1">
        <li v-for="trait in entry.traits" :key="trait" class="badge badge-sm badge-soft">
          {{ trait }}
        </li>
      </ul>
      <RouterLink
        v-if="entry.event && showEvent"
        :to="{ name: 'event', params: { uuid, event: entry.event } }"
        class="text-xs text-primary truncate hover:underline"
      >
        {{ entry.event_title }}
      </RouterLink>
    </div>
    <div class="flex items-start gap-2 shrink-0">
      <TrustPoints :points="entry.points" />
      <slot></slot>
    </div>
  </li>
</template>

<script>
import { RouterLink } from 'vue-router'
import TrustPoints from '@/components/TrustPoints.vue'
import { formatDate } from '@/data/dossierFields.js'
import { conductLabels } from '@/data/trust.js'

export default {
  name: 'TrustEntryRow',
  components: { RouterLink, TrustPoints },
  props: {
    uuid: { type: String, required: true },
    entry: { type: Object, required: true },
    showEvent: { type: Boolean, default: true },
  },
  data() {
    return { conductLabels }
  },
  methods: {
    formatDate,
  },
}
</script>
