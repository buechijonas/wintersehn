<script setup>
defineProps({
  tag: { type: String, default: 'div' },
})
</script>

<template>
  <component :is="tag" class="bg-base-100 shadow-none border-wntrs-border border-solid border-1">
    <slot />
  </component>
</template>
