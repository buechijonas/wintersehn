<template>
  <BaseButton
    v-if="modelValue"
    variant="neutral"
    shape="square"
    size="sm"
    title="Fertig"
    @click="$emit('update:modelValue', false)"
  >
    <AppIcon name="check-circle" alt="Fertig" />
  </BaseButton>
  <EditButton v-else @click="$emit('update:modelValue', true)" />
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import EditButton from '@core/components/common/EditButton.vue'

export default {
  name: 'EditToggle',
  components: { AppIcon, BaseButton, EditButton },
  props: {
    modelValue: { type: Boolean, default: false },
  },
  emits: ['update:modelValue'],
}
</script>
