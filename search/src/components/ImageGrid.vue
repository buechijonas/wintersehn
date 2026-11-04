<template>
  <ul class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-5">
    <li v-for="item in results" :key="item.key">
      <a :href="item.url" rel="noopener noreferrer" class="group flex flex-col gap-1">
        <img
          v-if="item.image"
          :src="item.image"
          :alt="item.title"
          loading="lazy"
          decoding="async"
          class="aspect-square w-full rounded-box object-cover bg-base-200"
        />
        <span class="text-xs text-wntrs-muted truncate group-hover:underline">
          {{ item.host }}
        </span>
      </a>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'ImageGrid',
  props: {
    results: { type: Array, required: true },
  },
}
</script>
