<template>
  <img :src="icons[name]" :alt="alt" class="app-icon" />
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

<style scoped>
:where([data-theme='dark']) .app-icon:not(.icon-error):not(.icon-success):not(.icon-primary) {
  filter: invert(1);
}
@media (prefers-color-scheme: dark) {
  :where(:root:not([data-theme]))
    .app-icon:not(.icon-error):not(.icon-success):not(.icon-primary) {
    filter: invert(1);
  }
}
</style>
