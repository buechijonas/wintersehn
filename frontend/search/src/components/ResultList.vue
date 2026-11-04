<template>
  <ul class="flex flex-col gap-2 max-sm:-mx-4 sm:gap-8">
    <li
      v-for="item in results"
      :key="item.key"
      class="max-sm:rounded-box max-sm:border max-sm:border-wntrs-border max-sm:px-3 max-sm:py-3"
    >
      <a :href="item.url" rel="noopener noreferrer" class="group flex gap-4">
        <img
          v-if="withImages && item.image"
          :src="item.image"
          alt=""
          loading="lazy"
          decoding="async"
          class="aspect-video w-36 shrink-0 rounded-box object-cover bg-base-200"
        />
        <span class="flex min-w-0 flex-col gap-1">
          <span class="text-xs text-wntrs-muted truncate">{{ item.host }}</span>
          <span class="text-lg text-wntrs-title group-hover:underline">{{ item.title }}</span>
          <span v-if="item.content" class="text-sm text-wntrs-slate line-clamp-2">
            {{ item.content }}
          </span>
        </span>
      </a>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'ResultList',
  props: {
    results: { type: Array, required: true },
    withImages: { type: Boolean, default: false },
  },
}
</script>
