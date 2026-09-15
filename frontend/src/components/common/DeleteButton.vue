<template>
  <BaseButton variant="ghost" :shape="hasLabel ? null : 'circle'" size="xs" class="text-error">
    <AppIcon name="trash" class="size-4 icon-error" alt="" />
    <slot />
  </BaseButton>
</template>

<script>
import BaseButton from '@/components/common/BaseButton.vue'
import AppIcon from '@/components/common/AppIcon.vue'

export default {
  name: 'DeleteButton',
  components: { BaseButton, AppIcon },
  computed: {
    hasLabel() {
      return !!this.$slots.default
    },
  },
}
</script>

<style scoped>
.icon-error {
  filter: brightness(0) saturate(100%) invert(62%) sepia(21%) saturate(11611%) hue-rotate(320deg)
    brightness(116%) contrast(109%);
}
</style>
