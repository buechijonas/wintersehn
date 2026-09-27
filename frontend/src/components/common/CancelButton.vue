<template>
  <BaseButton :to="to">
    <AppIcon name="cross" />
    <slot>Abbrechen</slot>
  </BaseButton>
</template>

<script>
import AppIcon from '@/components/common/AppIcon.vue'
import BaseButton from '@/components/common/BaseButton.vue'

export default {
  name: 'CancelButton',
  components: { AppIcon, BaseButton },
  props: {
    to: {
      type: [String, Object],
      default: null,
    },
  },
}
</script>
