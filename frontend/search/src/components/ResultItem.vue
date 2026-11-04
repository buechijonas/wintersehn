<template>
  <a :href="item.url" :rel="rel" class="group flex gap-4">
    <img
      v-if="withImage && item.image"
      :src="item.image"
      alt=""
      loading="lazy"
      decoding="async"
      class="aspect-video w-36 shrink-0 rounded-box object-cover bg-base-200"
    />
    <span class="flex min-w-0 flex-1 flex-col gap-1">
      <span class="flex items-center justify-between gap-2">
        <span class="flex min-w-0 items-center gap-2 text-xs">
          <slot name="prefix" />
          <span class="text-wntrs-muted truncate">{{ item.host }}</span>
        </span>
        <slot name="badge" />
      </span>
      <span class="text-lg text-wntrs-title group-hover:underline">{{ item.title }}</span>
      <span v-if="item.content" class="text-sm text-wntrs-slate line-clamp-2">
        {{ item.content }}
      </span>
    </span>
  </a>
</template>

<script>
export default {
  name: 'ResultItem',
  props: {
    item: { type: Object, required: true },
    withImage: { type: Boolean, default: false },
    rel: { type: String, default: 'noopener noreferrer' },
  },
}
</script>
