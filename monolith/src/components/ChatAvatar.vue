<template>
  <img
    v-if="src && !failed"
    :src="src"
    :alt="participant.name"
    class="size-8 shrink-0 rounded-full object-cover"
    @error="failed = true"
  />
  <span
    v-else
    class="size-8 shrink-0 rounded-full bg-base-300 flex items-center justify-center text-xs font-bold"
    :title="participant.name"
  >
    {{ participant.name.charAt(0).toUpperCase() }}
  </span>
</template>

<script>
export default {
  name: 'ChatAvatar',
  props: {
    participant: { type: Object, required: true },
    src: { type: String, default: null },
  },
  data() {
    return {
      failed: false,
    }
  },
  watch: {
    src() {
      this.failed = false
    },
  },
}
</script>
