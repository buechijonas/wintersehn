<script setup>
import Navigation from '@/components/common/Navigation.vue'
import Header from '@/components/common/Header.vue'

defineProps({
  activeNavigation: {
    type: String,
    default: null,
  },
})
</script>

<template>
  <div class="relative grid min-h-screen grid-cols-[8px_auto_1fr]">
    <div class="absolute top-0 left-0 z-20 h-full w-2 bg-primary" />
    <Navigation class="col-start-2" :active-navigation="activeNavigation" />
    <div class="col-start-3 flex min-w-0 flex-col bg-base-200">
      <Header />
      <slot />
    </div>
  </div>
</template>
