<template>
  <BaseButton :size="size" variant="primary" :to="`/play/${media.id}`">
    <AppIcon name="play" />
    {{ label }}
  </BaseButton>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import { clock, resumable } from '@/lib/time.js'

export default {
  name: 'PlayButton',
  components: { AppIcon, BaseButton },
  props: {
    media: { type: Object, required: true },
    size: { type: String, default: 'md' },
    withSubtitle: { type: Boolean, default: true },
  },
  computed: {
    label() {
      const action = resumable(this.media)
        ? `Weiterschauen · ${clock(this.media.position)}`
        : 'Abspielen'
      return this.withSubtitle && this.media.subtitle
        ? `${action} · ${this.media.subtitle}`
        : action
    },
  },
}
</script>
