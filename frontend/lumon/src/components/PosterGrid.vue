<template>
  <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 xl:grid-cols-6">
    <template v-if="loading">
      <div v-for="n in 12" :key="n" class="skeleton aspect-[2/3]"></div>
    </template>
    <PosterCard
      v-for="item in items"
      v-else
      :key="`${item.media_type}-${item.tmdb_id}`"
      :item="item"
    />
  </div>
</template>

<script>
import PosterCard from '@/components/PosterCard.vue'

export default {
  name: 'PosterGrid',
  components: { PosterCard },
  props: {
    items: { type: Array, default: () => [] },
    loading: { type: Boolean, default: false },
  },
}
</script>
