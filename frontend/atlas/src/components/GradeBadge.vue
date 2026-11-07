<template>
  <span
    v-if="value"
    class="badge badge-soft shrink-0 font-medium"
    :class="[toneClasses[tone], sizeClasses[size]]"
  >
    {{ value }}
  </span>
</template>

<script>
export default {
  name: 'GradeBadge',
  props: {
    value: { type: String, default: null },
    tone: { type: String, default: null },
    size: { type: String, default: 'md' },
  },
  data() {
    return {
      toneClasses: { error: 'badge-error', warning: 'badge-warning', success: 'badge-success' },
      sizeClasses: { md: '', lg: 'badge-lg text-base' },
    }
  },
}
</script>
