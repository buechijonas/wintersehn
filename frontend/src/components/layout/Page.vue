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
  <div class="page relative">
    <div class="border absolute left-0 top-0" />
    <Navigation class="navigation" :active-navigation="activeNavigation" />
    <div class="content bg-base-200">
      <Header />
      <slot />
    </div>
  </div>
</template>

<style lang="scss">
.page {
  display: grid;
  grid-template-columns: 8px auto 1fr;
  grid-template-rows: auto;
  grid-template-areas: '. navigation content';
  min-height: 100vh;
}

.navigation {
  grid-area: navigation;
}

.content {
  grid-area: content;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.border {
  z-index: 20;
  width: 8px;
  height: 100%;
  background: #b42b5f;
  border: none;
}
</style>
