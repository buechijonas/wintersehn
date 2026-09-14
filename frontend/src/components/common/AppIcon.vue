<template>
  <img :src="icons[name]" :alt="alt" />
</template>

<script>
import { icons } from '@/assets/icons'

export default {
  name: 'AppIcon',
  props: {
    name: { type: String, required: true },
    alt: { type: String, default: '' },
  },
  data() {
    return { icons }
  },
}
</script>
