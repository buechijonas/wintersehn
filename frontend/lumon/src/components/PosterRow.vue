<template>
  <section class="flex flex-col gap-3">
    <h2 class="text-xs tracking-wide opacity-60">{{ title }}</h2>
    <div class="-mx-6 flex snap-x gap-4 overflow-x-auto px-6 pb-2 [scrollbar-width:thin]">
      <template v-if="loading">
        <div v-for="n in 8" :key="n" class="skeleton aspect-[2/3] w-36 shrink-0"></div>
      </template>
      <PosterCard
        v-for="item in items"
        v-else
        :key="`${item.media_type}-${item.tmdb_id}`"
        :item="item"
        class="w-36 shrink-0 snap-start"
      />
    </div>
  </section>
</template>

<script>
import PosterCard from '@/components/PosterCard.vue'

export default {
  name: 'PosterRow',
  components: { PosterCard },
  props: {
    title: { type: String, required: true },
    items: { type: Array, default: () => [] },
    loading: { type: Boolean, default: false },
  },
}
</script>
