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
  <div class="page">
    <div class="border" />
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
  grid-template-columns: 10px auto 1fr;
  grid-template-rows: auto;
  grid-template-areas: '. navigation content';
  position: relative;
  min-height: 100vh;
}

.navigation {
  grid-area: navigation;
}

.content {
  grid-area: content;
}

.border {
  position: absolute;
  z-index: 20;
  left: 0;
  top: 0;
  width: 8px;
  height: 100%;
  background: #b42b5f;
  border: none;
}
</style>
