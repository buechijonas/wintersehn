<template>
  <dialog ref="dialog" class="modal">
    <div class="modal-box">
      <form method="dialog">
        <BaseButton type="submit" variant="ghost" shape="circle" size="sm" class="absolute right-2 top-2">
          ✕
        </BaseButton>
      </form>
      <slot name="header">
        <h3 v-if="title" class="text-lg font-bold">{{ title }}</h3>
      </slot>
      <div class="py-4">
        <slot>
          <p v-if="description">{{ description }}</p>
        </slot>
      </div>
      <div v-if="buttons.length || $slots.actions" class="modal-action">
        <slot name="actions">
          <BaseButton
            v-for="button in buttons"
            :key="button.value"
            :variant="button.variant ?? 'neutral'"
            @click="handleClick(button)"
          >
            {{ button.label }}
          </BaseButton>
        </slot>
      </div>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button>close</button>
    </form>
  </dialog>
</template>

<script>
import BaseButton from '@/components/common/BaseButton.vue'

export default {
  name: 'BaseDialog',
  components: { BaseButton },
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
