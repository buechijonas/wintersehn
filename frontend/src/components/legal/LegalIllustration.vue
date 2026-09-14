<template>
  <div class="flex justify-center my-8">
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
