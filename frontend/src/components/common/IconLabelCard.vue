<script setup>
import Card from '@/components/common/Card.vue'
import { flats, countries } from '@/assets/images.js'
import { icons } from '@/assets/icons.js'

const props = defineProps({
  icon: { type: String, required: true },
  label: { type: String, required: true },
  to: { type: [String, Object], default: null },
  iconSet: { type: String, default: 'flats' },
})

const sources = { flats, icons, countries }
</script>

<template>
  <Card
    :tag="to ? 'router-link' : 'div'"
    :to="to"
    class="size-40 shrink-0 flex items-center justify-center p-4"
  >
    <div class="flex flex-col items-center text-center gap-4">
      <img class="size-16" :alt="label" :src="sources[props.iconSet][icon]" />
      <p class="color-dark-gray text-sm">{{ label }}</p>
    </div>
  </Card>
</template>
