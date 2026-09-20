<template>
  <BaseButton
    variant="neutral"
    :shape="shape ?? (hasLabel ? null : 'circle')"
    size="sm"
    class="text-error"
  >
    <AppIcon name="trash" class="size-4 icon-tint-error" alt="" />
    <slot />
  </BaseButton>
</template>

<script>
import BaseButton from '@/components/common/BaseButton.vue'
import AppIcon from '@/components/common/AppIcon.vue'

export default {
  name: 'DeleteButton',
  components: { BaseButton, AppIcon },
  props: {
    shape: { type: String, default: null },
  },
  computed: {
    hasLabel() {
      return !!this.$slots.default
    },
  },
}
</script>
