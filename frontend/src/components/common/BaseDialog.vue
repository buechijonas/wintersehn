<template>
  <dialog ref="dialog" class="modal">
    <div class="modal-box">
      <form method="dialog">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
      </form>
      <h3 v-if="title" class="text-lg font-bold">{{ title }}</h3>
      <p v-if="description" class="py-4">{{ description }}</p>
      <div v-if="buttons.length" class="modal-action">
        <button
          v-for="button in buttons"
          :key="button.value"
          type="button"
          class="btn shadow-none"
          :class="button.class"
          @click="handleClick(button)"
        >
          {{ button.label }}
        </button>
      </div>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button>close</button>
    </form>
  </dialog>
</template>

<script>
export default {
  name: 'BaseDialog',
  props: {
    title: { type: String, default: '' },
    description: { type: String, default: '' },
    buttons: { type: Array, default: () => [] },
  },
  emits: ['action'],
  methods: {
    open() {
      this.$refs.dialog?.showModal()
    },
    close() {
      this.$refs.dialog?.close()
    },
    handleClick(button) {
      this.$refs.dialog?.close()
      this.$emit('action', button.value)
    },
  },
}
</script>
