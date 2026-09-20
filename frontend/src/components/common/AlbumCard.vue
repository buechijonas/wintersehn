<template>
  <BaseCard
    :tag="to ? 'router-link' : 'div'"
    :to="to"
    class="size-40 shrink-0 relative overflow-hidden block"
    :class="{ 'hover:bg-base-200 group': to }"
  >
    <template v-if="thumbnail">
      <img
        class="size-full object-cover"
        :class="{ 'group-hover:opacity-80 transition-opacity': to }"
        :src="thumbnail"
        :alt="title"
      />
      <div
        class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/70 to-transparent px-2 pt-6 pb-2"
      >
        <p class="text-white text-sm line-clamp-2 text-ellipsis w-full">{{ title }}</p>
      </div>
    </template>
    <div v-else class="size-full flex items-center justify-center p-4 text-center">
      <p class="text-wntrs-slate text-sm line-clamp-2 text-ellipsis w-full">{{ title }}</p>
    </div>
  </BaseCard>
</template>

<script>
import BaseCard from '@/components/common/BaseCard.vue'

export default {
  name: 'AlbumCard',
  components: { BaseCard },
  props: {
    title: { type: String, required: true },
    thumbnail: { type: String, default: '' },
    to: { type: [String, Object], default: null },
  },
}
</script>
