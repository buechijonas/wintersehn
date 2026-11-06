<template>
  <div class="flex flex-col gap-2">
    <span class="text-xs text-wntrs-muted">{{ label }}</span>
    <textarea
      :value="text"
      :aria-label="label"
      rows="3"
      class="textarea w-full border-wntrs-border focus:border-primary focus:outline-none"
      @input="$emit('update:text', $event.target.value)"
    ></textarea>
    <div class="flex items-center gap-2">
      <img
        v-if="imageUrl"
        :src="`${imageUrl}?size=256`"
        alt=""
        class="h-16 rounded-box object-cover"
      />
      <ImageUploadButton
        :label="imageUrl ? 'Bild ersetzen' : 'Bild'"
        @uploaded="$emit('update:image', $event)"
        @error="$emit('error', $event)"
      />
      <BaseButton v-if="imageUrl" size="sm" variant="ghost" @click="$emit('update:image', null)">
        <AppIcon name="cross" />
        Bild entfernen
      </BaseButton>
    </div>
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import ImageUploadButton from '@/components/ImageUploadButton.vue'

export default {
  name: 'CardSide',
  components: { AppIcon, BaseButton, ImageUploadButton },
  props: {
    label: { type: String, required: true },
    text: { type: String, required: true },
    imageUrl: { type: String, default: null },
  },
  emits: ['update:text', 'update:image', 'error'],
}
</script>
