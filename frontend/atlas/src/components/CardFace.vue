<template>
  <div class="flex flex-col items-center gap-4 text-center">
    <span class="text-xs text-wntrs-muted">{{ label }}</span>
    <img v-if="image" :src="image" alt="" class="max-h-60 rounded-box object-contain" />
    <span class="whitespace-pre-line text-xl text-wntrs-title">{{ text }}</span>
  </div>
</template>

<script>
export default {
  name: 'CardFace',
  props: {
    label: { type: String, required: true },
    text: { type: String, default: '' },
    image: { type: String, default: null },
  },
}
</script>
