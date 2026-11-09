<template>
  <div class="flex">
    <img class="max-h-64" :src="src" :alt="alt" />
  </div>
</template>

<script>
export default {
  name: 'LegalIllustration',
  props: {
    src: { type: String, required: true },
    alt: { type: String, default: '' },
  },
}
</script>
