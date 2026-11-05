<template>
  <ul class="grid grid-cols-2 gap-4 sm:grid-cols-3" :class="columnClasses[columns]">
    <li v-for="item in results" :key="item.key" class="flex min-w-0 flex-col gap-1">
      <a
        :href="item.url"
        rel="noopener noreferrer"
        class="block rounded-box"
        :class="{ 'ring-2 ring-primary ring-offset-2 ring-offset-base-100': item.key === selected }"
        @click.prevent="$emit('select', item)"
      >
        <ResultImage
          v-if="item.image"
          :src="item.image"
          :alt="item.title"
          class="aspect-square w-full rounded-box object-cover bg-base-200"
        />
      </a>
      <div class="flex min-h-5 items-center gap-2">
        <span class="truncate text-xs" :class="hostClass(item)">{{ item.host }}</span>
        <RatingMarker
          v-if="ratingOf(item, hostRatings)"
          :rating="ratingOf(item, hostRatings)"
          :report="hostRatings[item.host]?.grade ? hostRatings[item.host] : null"
          :host="item.host"
          class="ml-auto"
        />
        <span
          v-else-if="pendingHosts.includes(item.host)"
          class="loading loading-spinner ml-auto size-3.5 text-wntrs-muted"
          aria-label="Sicherheit wird geprüft"
        ></span>
      </div>
    </li>
  </ul>
</template>

<script>
import RatingMarker from '@/components/RatingMarker.vue'
import ResultImage from '@/components/ResultImage.vue'
import { ratingOf } from '@/data/ratings.js'

const COLUMN_CLASSES = {
  1: 'lg:grid-cols-1',
  2: 'lg:grid-cols-2',
  3: 'lg:grid-cols-3',
  4: 'lg:grid-cols-4',
  5: 'lg:grid-cols-5',
}

const hostClasses = { secure: 'text-wntrs-secure', insecure: 'text-error', lookalike: 'text-error' }

export default {
  name: 'ImageGrid',
  components: { RatingMarker, ResultImage },
  props: {
    results: { type: Array, required: true },
    hostRatings: { type: Object, default: () => ({}) },
    pendingHosts: { type: Array, default: () => [] },
    selected: { type: String, default: null },
    columns: { type: Number, default: 5 },
  },
  emits: ['select'],
  data() {
    return {
      columnClasses: COLUMN_CLASSES,
    }
  },
  methods: {
    ratingOf,
    hostClass(item) {
      return hostClasses[ratingOf(item, this.hostRatings)] ?? 'text-wntrs-muted'
    },
  },
}
</script>
