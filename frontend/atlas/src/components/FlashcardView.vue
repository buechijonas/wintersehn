<template>
  <div class="grid gap-4 md:grid-cols-2">
    <div v-for="side in sides" :key="side.key" class="flex flex-col gap-2">
      <span class="text-xs text-wntrs-muted">{{ side.label }}</span>
      <img
        v-if="card[`${side.key}_image_url`]"
        :src="card[`${side.key}_image_url`]"
        alt=""
        class="max-h-48 self-start rounded-box object-contain"
      />
      <p class="whitespace-pre-line">{{ card[side.key] }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FlashcardView',
  props: {
    card: { type: Object, required: true },
  },
  data() {
    return {
      sides: [
        { key: 'front', label: 'Vorderseite' },
        { key: 'back', label: 'Rückseite' },
      ],
    }
  },
}
</script>
