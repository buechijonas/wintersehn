<template>
  <div class="join shrink-0" role="radiogroup" :aria-label="label">
    <button
      v-for="option in options"
      :key="option.value"
      type="button"
      role="radio"
      class="btn btn-xs join-item"
      :class="modelValue === option.value ? 'btn-primary' : 'btn-neutral btn-soft'"
      :aria-checked="modelValue === option.value"
      :title="option.title"
      @click="$emit('update:modelValue', option.value)"
    >
      {{ option.label }}
    </button>
  </div>
</template>

<script>
import { visibilities } from '@/data/sharing.js'

export default {
  name: 'VisibilityToggle',
  props: {
    modelValue: { type: String, default: null },
    options: { type: Array, default: () => visibilities },
    label: { type: String, default: 'Sichtbarkeit' },
  },
  emits: ['update:modelValue'],
}
</script>
