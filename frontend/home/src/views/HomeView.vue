<template>
  <ul class="grid flex-1 content-start gap-4 px-6 pt-6 pb-16 sm:grid-cols-2 lg:grid-cols-3">
    <li v-for="app in visibleApps" :key="app.key">
      <BaseCard
        tag="a"
        :href="app.url"
        class="flex h-full items-start gap-4 rounded-box p-4 transition-colors hover:bg-base-200"
      >
        <img :src="app.icon" alt="" class="size-10 shrink-0 rounded-box" />
        <span class="flex min-w-0 flex-col gap-0.5">
          <span class="text-wntrs-title">{{ app.label }}</span>
          <span class="text-sm text-wntrs-muted">{{ app.description }}</span>
          <span class="truncate text-xs text-wntrs-muted">{{ app.host }}</span>
        </span>
      </BaseCard>
    </li>
  </ul>
</template>

<script>
import BaseCard from '@core/components/common/BaseCard.vue'
import { useAuthStore } from '@core/stores/auth.js'
import { apps } from '@/data/apps.js'

export default {
  name: 'HomeView',
  components: { BaseCard },
  computed: {
    visibleApps() {
      const user = useAuthStore().user
      return apps.filter((app) => !app.permission || user?.[app.permission])
    },
  },
}
</script>
