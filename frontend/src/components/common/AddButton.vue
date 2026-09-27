<template>
  <BaseButton variant="primary" :to="to" class="hidden lg:inline-flex" @click="$emit('click')">
    <AppIcon name="plus" />
    {{ label }}
  </BaseButton>
  <BaseButton
    variant="primary"
    shape="circle"
    :to="to"
    :title="label"
    class="fixed bottom-18 right-6 z-5 size-14 lg:hidden"
    @click="$emit('click')"
  >
    <AppIcon name="plus" :alt="label" />
  </BaseButton>
</template>

<script>
import AppIcon from '@/components/common/AppIcon.vue'
import BaseButton from '@/components/common/BaseButton.vue'

export default {
  name: 'AddButton',
  components: { AppIcon, BaseButton },
  props: {
    label: { type: String, required: true },
    to: { type: [String, Object], default: null },
  },
  emits: ['click'],
}
</script>
