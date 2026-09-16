<template>
  <BaseButton :to="to">
    <slot>Abbrechen</slot>
  </BaseButton>
</template>

<script>
import BaseButton from '@/components/common/BaseButton.vue'

export default {
  name: 'CancelButton',
  components: { BaseButton },
  props: {
    to: {
      type: [String, Object],
      default: null,
    },
  },
}
</script>
