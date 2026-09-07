<script setup>
defineProps({
  src: { type: String, required: true },
  alt: { type: String, default: '' },
})
</script>

<template>
  <div class="flex justify-center my-8">
    <img class="max-h-64" :src="src" :alt="alt" />
  </div>
</template>
