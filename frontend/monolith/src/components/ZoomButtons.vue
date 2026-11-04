<template>
  <BaseButton
    variant="neutral"
    shape="square"
    size="sm"
    title="Verkleinern"
    @click="$emit('zoom', 1 / ZOOM_STEP)"
  >
    <AppIcon name="minus" alt="Verkleinern" />
  </BaseButton>
  <BaseButton
    variant="neutral"
    shape="square"
    size="sm"
    title="Vergrössern"
    @click="$emit('zoom', ZOOM_STEP)"
  >
    <AppIcon name="plus" alt="Vergrössern" />
  </BaseButton>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'

const ZOOM_STEP = 1.25

export default {
  name: 'ZoomButtons',
  components: { AppIcon, BaseButton },
  emits: ['zoom'],
  data() {
    return { ZOOM_STEP }
  },
}
</script>
