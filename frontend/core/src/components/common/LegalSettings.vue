<template>
  <BaseCard class="flex flex-col p-2">
    <RouterLink
      v-for="link in app.legalLinks"
      :key="link.label"
      :to="link.to"
      class="flex h-12 items-center gap-3 rounded-box px-4 text-sm text-wntrs-slate hover:bg-base-200"
    >
      <img class="size-4" alt="" :src="icons[link.icon]" />
      <span>{{ link.label }}</span>
      <AppIcon name="angle-left" class="ml-auto size-3! rotate-180" />
    </RouterLink>
  </BaseCard>
</template>

<script>
import { RouterLink } from 'vue-router'
import { icons } from '@core/assets/icons.js'
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseCard from '@core/components/common/BaseCard.vue'

export default {
  name: 'LegalSettings',
  components: { RouterLink, AppIcon, BaseCard },
  inject: ['app'],
  data() {
    return { icons }
  },
}
</script>
