<template>
  <img v-if="visible" :src="src" :alt="alt" loading="lazy" decoding="async" />
  <button
    v-else
    type="button"
    class="flex cursor-pointer items-center justify-center gap-2 text-xs text-wntrs-muted"
    @click.prevent.stop="revealed = true"
  >
    <AppIcon name="picture" />
    Bild laden
  </button>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import { useSearchStore } from '@/stores/search.js'

export default {
  name: 'ResultImage',
  components: { AppIcon },
  props: {
    src: { type: String, required: true },
    alt: { type: String, default: '' },
  },
  data() {
    return {
      revealed: false,
    }
  },
  computed: {
    visible() {
      return this.revealed || useSearchStore().settings.imageLoading === 'auto'
    },
  },
}
</script>
