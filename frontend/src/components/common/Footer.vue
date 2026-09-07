<script setup>
import { RouterLink } from 'vue-router'
import { icons } from '@/assets/icons.js'
import { footerLinks } from '@/data/footer.js'
</script>

<template>
  <footer class="flex justify-center align-center">
    <component
      :is="link.disabled ? 'div' : RouterLink"
      v-for="link in footerLinks"
      :key="link.label"
      v-bind="link.disabled ? { 'aria-disabled': 'true' } : { to: link.to }"
      class="card mx-2 bg-base-100 shadow-none border-wntrs-gray border-solid border-1"
    >
      <div class="card-body flex flex-row text-xs p-4">
        <img class="size-4 m-auto" :alt="link.label" :src="icons[link.icon]" />
        <p class="font-medium" :class="link.disabled ? 'disabled' : 'color-dark-gray'">
          {{ link.label }}
        </p>
      </div>
    </component>
  </footer>
</template>
