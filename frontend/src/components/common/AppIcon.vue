<template>
  <span
    role="img"
    :aria-label="alt || null"
    :aria-hidden="alt ? null : 'true'"
    class="app-icon inline-block size-4 shrink-0 bg-current"
    :style="{ maskImage }"
  />
</template>

<script>
import { icons } from '@/assets/icons'

export default {
  name: 'AppIcon',
  props: {
    name: { type: String, required: true },
    alt: { type: String, default: '' },
  },
  computed: {
    maskImage() {
      return `url("${icons[this.name]}")`
    },
  },
}
</script>

<style scoped>
.app-icon {
  mask-repeat: no-repeat;
  mask-position: center;
  mask-size: contain;
}
</style>
