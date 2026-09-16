<template>
  <div class="relative grid min-h-[100dvh] grid-cols-[8px_auto_1fr]">
    <div class="absolute top-0 left-0 z-20 h-full w-2 bg-primary" />
    <BaseNavigation class="col-start-2" :active-navigation="activeNavigation" />
    <div class="col-start-3 flex min-w-0 flex-col bg-base-200">
      <BaseHeader />
      <slot />
    </div>
  </div>
</template>

<script>
import BaseNavigation from '@/components/common/BaseNavigation.vue'
import BaseHeader from '@/components/common/BaseHeader.vue'

export default {
  name: 'BasePage',
  components: { BaseNavigation, BaseHeader },
  props: {
    activeNavigation: {
      type: String,
      default: null,
    },
  },
}
</script>
