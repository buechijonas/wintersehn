<script setup>
import { icons } from '@/assets/icons'

defineProps({
  name: { type: String, required: true },
  alt: { type: String, default: '' },
})
</script>

<template>
  <img :src="icons[name]" :alt="alt" />
</template>
