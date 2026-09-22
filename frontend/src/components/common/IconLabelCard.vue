<template>
  <BaseCard
    :tag="path(to) ? 'router-link' : 'div'"
    :to="path(to)"
    class="size-40 shrink-0 flex items-center justify-center p-4"
    :class="{ 'hover:bg-base-200': path(to) }"
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
import BaseCard from '@/components/common/BaseCard.vue'
import { flats, countries } from '@/assets/images.js'
import { icons } from '@/assets/icons.js'
import { path } from '@/lib/link.js'

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
    return { sources: { flats, icons, countries }, imgLoaded: false }
  },
  methods: {
    path,
  },
}
</script>
