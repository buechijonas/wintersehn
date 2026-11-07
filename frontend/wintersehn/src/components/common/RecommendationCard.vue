<template>
  <BaseCard
    :tag="item.url ? 'a' : 'div'"
    :href="item.url"
    :target="item.url && '_blank'"
    :rel="item.url && 'noopener noreferrer'"
    class="flex min-w-0 flex-col gap-3 p-4"
    :class="{ 'hover:bg-base-200': item.url, 'border-dashed!': item.planned }"
  >
    <div class="flex items-center justify-between gap-2 text-xs">
      <span class="truncate text-wntrs-muted">
        {{ item.category }}<template v-if="item.description"> · {{ item.description }}</template>
      </span>
      <span v-if="item.footprint" class="shrink-0 font-medium">
        <template v-for="(step, index) in footprintSteps" :key="index">
          <span v-if="index" class="text-wntrs-muted"> → </span>
          <span :class="footprintClass(step)">{{ step }}</span>
        </template>
      </span>
    </div>
    <div class="flex min-w-0 flex-wrap items-center gap-x-3 gap-y-2">
      <span
        v-for="replaced in item.replaces ?? []"
        :key="replaced.name"
        class="flex min-w-0 items-center gap-2 text-wntrs-muted"
      >
        <img class="size-5 shrink-0 grayscale opacity-40" :src="brands[replaced.icon]" alt="" />
        <span class="truncate line-through">{{ replaced.name }}</span>
        <img
          v-if="replaced.country"
          class="size-3 shrink-0 opacity-60"
          :alt="replaced.country"
          :src="countries[flag(replaced.country)]"
        />
      </span>
      <AppIcon
        v-if="item.replaces?.length"
        name="angle-left"
        class="size-3! rotate-180 text-wntrs-muted"
      />
      <span
        class="flex min-w-0 items-center gap-2 font-medium"
        :class="{ 'line-through text-wntrs-muted': item.dropped }"
      >
        <img
          v-if="item.icon"
          class="size-6 shrink-0 rounded-sm"
          :class="{ 'grayscale opacity-40': item.dropped }"
          :src="brands[item.icon]"
          alt=""
        />
        <span class="truncate">{{ item.name }}</span>
        <img
          v-if="item.country"
          class="size-3 shrink-0"
          :class="{ 'opacity-60': item.dropped }"
          :alt="item.country"
          :src="countries[flag(item.country)]"
        />
      </span>
    </div>
    <p v-if="item.reason" class="text-sm text-wntrs-muted">{{ item.reason }}</p>
  </BaseCard>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import { countries, logos, social } from '@core/assets/images.js'

export default {
  name: 'RecommendationCard',
  components: { AppIcon, BaseCard },
  props: {
    item: { type: Object, required: true },
    flags: { type: Object, default: () => ({}) },
  },
  data() {
    return { countries, brands: { ...logos, ...social } }
  },
  computed: {
    footprintSteps() {
      if (this.item.dropped) return [this.item.footprint, 0]
      return [
        ...(this.item.replaces ?? []).map((replaced) => replaced.footprint),
        this.item.footprint,
      ]
    },
  },
  methods: {
    flag(country) {
      return this.flags[country] ?? country
    },
    footprintClass(footprint) {
      if (footprint <= 3) return 'text-success/70'
      if (footprint <= 6) return 'text-warning/70'
      return 'text-error/70'
    },
  },
}
</script>
