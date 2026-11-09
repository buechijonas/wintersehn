<template>
  <RouterLink
    :to="`/${item.media_type}/${item.catalog_id}`"
    class="group flex min-w-0 flex-col gap-2"
  >
    <div
      class="relative aspect-[2/3] overflow-hidden rounded-box border border-wntrs-border bg-base-200"
    >
      <img
        v-if="item.poster"
        :src="item.poster"
        :alt="item.title"
        loading="lazy"
        class="size-full object-cover transition-transform group-hover:scale-105"
      />
      <span v-else class="flex size-full items-center justify-center p-3 text-center text-sm">
        {{ item.title }}
      </span>
      <span
        v-if="item.saved"
        class="absolute top-2 right-2 flex size-7 items-center justify-center rounded-full bg-primary text-primary-content"
        title="In meiner Liste"
      >
        <AppIcon name="bookmark" class="size-3.5!" />
      </span>
    </div>
    <div class="min-w-0">
      <p class="truncate text-sm font-medium">{{ item.title }}</p>
      <p class="text-xs text-wntrs-muted">
        {{ item.year ?? '–' }} · {{ item.media_type === 'tv' ? 'Serie' : 'Film' }}
      </p>
    </div>
  </RouterLink>
</template>

<script>
import { RouterLink } from 'vue-router'
import AppIcon from '@core/components/common/AppIcon.vue'

export default {
  name: 'PosterCard',
  components: { RouterLink, AppIcon },
  props: {
    item: { type: Object, required: true },
  },
}
</script>
