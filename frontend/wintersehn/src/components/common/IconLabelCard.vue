<template>
  <BaseCard
    :tag="tag"
    :to="path(to)"
    :href="url(to)"
    :target="url(to) && '_blank'"
    :rel="url(to) && 'noopener noreferrer'"
    class="size-40 shrink-0 flex items-center justify-center p-4"
    :class="{ 'hover:bg-base-200': tag !== 'div' }"
  >
    <div class="flex flex-col items-center text-center gap-4 w-full">
      <div class="relative size-16 shrink-0">
        <div v-if="!imgLoaded" class="skeleton absolute inset-0 rounded-full"></div>
        <img
          class="size-16"
          :class="{ invisible: !imgLoaded }"
          :alt="label"
          :src="sources[iconSet][icon]"
          @load="imgLoaded = true"
        />
      </div>
      <p class="text-wntrs-slate text-sm line-clamp-2 text-ellipsis w-full">{{ label }}</p>
    </div>
  </BaseCard>
</template>

<script>
import BaseCard from '@core/components/common/BaseCard.vue'
import { flats, countries, logos } from '@core/assets/images.js'
import { icons } from '@core/assets/icons.js'
import { path, url } from '@core/lib/link.js'

export default {
  name: 'IconLabelCard',
  components: { BaseCard },
  props: {
    icon: { type: String, required: true },
    label: { type: String, required: true },
    to: { type: String, default: null },
    iconSet: { type: String, default: 'flats' },
  },
  data() {
    return { sources: { flats, icons, countries, logos }, imgLoaded: false }
  },
  computed: {
    tag() {
      if (path(this.to)) return 'router-link'
      if (url(this.to)) return 'a'
      return 'div'
    },
  },
  methods: {
    path,
    url,
  },
}
</script>
