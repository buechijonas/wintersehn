<script setup>
import IconLabelCard from '@/components/common/IconLabelCard.vue'

defineProps({
  title: { type: String, required: true },
  items: { type: Array, required: true },
})
</script>

<template>
  <div class="mx-auto w-200">
    <h2 class="title-category my-4">{{ title }}</h2>
    <div class="flex flex-wrap gap-2">
      <IconLabelCard
        v-for="item in items"
        :key="item.label"
        :icon="item.icon"
        :label="item.label"
        :to="item.to"
        :icon-set="item.iconSet ?? 'flats'"
      />
    </div>
  </div>
</template>
