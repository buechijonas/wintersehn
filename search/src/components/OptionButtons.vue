<template>
  <div class="flex flex-wrap gap-2">
    <BaseButton
      v-for="option in options"
      :key="option"
      size="sm"
      :variant="modelValue === option ? 'primary' : 'neutral'"
      @click="$emit('update:modelValue', option)"
    >
      {{ labels[option] }}
    </BaseButton>
  </div>
</template>

<script>
import BaseButton from '@core/components/common/BaseButton.vue'

export default {
  name: 'OptionButtons',
  components: { BaseButton },
  props: {
    modelValue: { type: [String, Number], required: true },
    options: { type: Array, required: true },
    labels: { type: Object, required: true },
  },
  emits: ['update:modelValue'],
}
</script>
