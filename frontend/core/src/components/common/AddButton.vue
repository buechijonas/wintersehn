<template>
  <BaseButton
    variant="primary"
    :size="size"
    :to="to"
    class="hidden lg:inline-flex"
    @click="$emit('click')"
  >
    <AppIcon name="plus" />
    {{ label }}
  </BaseButton>
  <BaseButton
    variant="primary"
    shape="circle"
    :to="to"
    :title="label"
    class="fixed bottom-[calc(var(--footer-height)+1.5rem)] right-6 z-5 size-14 lg:hidden"
    @click="$emit('click')"
  >
    <AppIcon name="plus" :alt="label" class="size-6!" />
  </BaseButton>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'

export default {
  name: 'AddButton',
  components: { AppIcon, BaseButton },
  props: {
    label: { type: String, required: true },
    to: { type: [String, Object], default: null },
    size: { type: String, default: 'md' },
  },
  emits: ['click'],
}
</script>
