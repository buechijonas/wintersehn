<template>
  <div class="flex items-center justify-between gap-4">
    <h2 class="text-xs tracking-wide opacity-60">{{ title }}</h2>
    <RouterLink
      v-if="to"
      :to="to"
      class="flex items-center gap-1 text-xs text-wntrs-muted hover:text-base-content"
    >
      Alle
      <AppIcon name="angle-left" class="size-3! rotate-180" />
    </RouterLink>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'
import AppIcon from '@core/components/common/AppIcon.vue'

export default {
  name: 'SectionTitle',
  components: { RouterLink, AppIcon },
  props: {
    title: { type: String, required: true },
    to: { type: String, default: null },
  },
}
</script>
