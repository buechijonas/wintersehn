<template>
  <BaseCard tag="form" class="flex flex-col gap-4 rounded-box p-4" @submit.prevent="submit">
    <div class="grid gap-4 md:grid-cols-2">
      <CardSide
        v-for="side in sides"
        :key="side.key"
        v-model:text="draft[side.key]"
        :label="side.label"
        :image-url="draft[`${side.key}_image_url`]"
        @update:image="setImage(side.key, $event)"
        @error="error = $event"
      />
    </div>
    <p v-if="error" class="text-sm text-error">{{ error }}</p>
    <div class="flex gap-2">
      <BaseButton type="submit" variant="primary">
        <AppIcon name="disk" />
        {{ card ? 'Speichern' : 'Karte hinzufügen' }}
      </BaseButton>
      <BaseButton v-if="card" @click="$emit('cancel')">
        <AppIcon name="cross" />
        Abbrechen
      </BaseButton>
    </div>
  </BaseCard>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import CardSide from '@/components/CardSide.vue'

const EMPTY = {
  front: '',
  back: '',
  front_image: null,
  back_image: null,
  front_image_url: null,
  back_image_url: null,
}

export default {
  name: 'FlashcardForm',
  components: { AppIcon, BaseButton, BaseCard, CardSide },
  props: {
    card: { type: Object, default: null },
  },
  emits: ['submit', 'cancel'],
  data() {
    return {
      draft: { ...EMPTY, ...this.card },
      error: '',
      sides: [
        { key: 'front', label: 'Vorderseite' },
        { key: 'back', label: 'Rückseite' },
      ],
    }
  },
  methods: {
    setImage(side, image) {
      this.draft[`${side}_image`] = image?.uuid ?? null
      this.draft[`${side}_image_url`] = image?.url ?? null
    },
    submit() {
      const { front, back, front_image, back_image } = this.draft
      this.$emit('submit', { front, back, front_image, back_image })
      if (!this.card) this.draft = { ...EMPTY }
    },
  },
}
</script>
