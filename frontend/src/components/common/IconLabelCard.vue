<template>
  <BaseCard
    :tag="to ? 'router-link' : 'div'"
    :to="to"
    class="size-40 shrink-0 flex items-center justify-center p-4"
  >
    <div class="flex flex-col items-center text-center gap-4">
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
      <p class="text-wntrs-slate text-sm">{{ label }}</p>
    </div>
  </BaseCard>
</template>

<script>
import BaseCard from '@/components/common/BaseCard.vue'
import { flats, countries } from '@/assets/images.js'
import { icons } from '@/assets/icons.js'

export default {
  name: 'IconLabelCard',
  components: { BaseCard },
  props: {
    icon: { type: String, required: true },
    label: { type: String, required: true },
    to: { type: [String, Object], default: null },
    iconSet: { type: String, default: 'flats' },
  },
  data() {
    return { sources: { flats, icons, countries }, imgLoaded: false }
  },
}
</script>
