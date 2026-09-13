<script setup>
import { RouterLink } from 'vue-router'
import { icons } from '@/assets/icons.js'
import { footerLinks } from '@/data/footer.js'
</script>

<template>
  <footer
    class="app-footer flex justify-evenly items-center bg-base-100 border-t border-wntrs-gray border-solid lg:justify-center lg:bg-transparent lg:border-0"
  >
    <component
      :is="link.disabled ? 'div' : RouterLink"
      v-for="link in footerLinks"
      :key="link.label"
      v-bind="link.disabled ? { 'aria-disabled': 'true' } : { to: link.to }"
      class="max-lg:btn max-lg:btn-square max-lg:btn-ghost max-lg:btn-sm lg:card mx-0 lg:mx-2 lg:bg-base-100 lg:shadow-none lg:border-[#e3e5e8] lg:border-solid lg:border-1"
    >
      <div class="lg:card-body flex flex-row items-center justify-center text-xs p-0 lg:p-4">
        <img class="size-5 lg:size-4 lg:m-auto" :alt="link.label" :src="icons[link.icon]" />
        <p
          class="hidden lg:inline font-medium"
          :class="link.disabled ? 'disabled' : 'color-dark-gray'"
        >
          {{ link.label }}
        </p>
      </div>
    </component>
  </footer>
</template>

<style>
.app-footer {
  height: 48px;
  width: 100%;
  flex-shrink: 0;
}
@media (max-width: 1023.98px) {
  .app-footer {
    margin-top: auto;
    position: sticky;
    bottom: 0;
  }
}
@media (min-width: 1024px) {
  .app-footer {
    height: auto;
    width: auto;
  }
}
</style>
