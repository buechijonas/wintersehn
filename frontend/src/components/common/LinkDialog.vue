<template>
  <BaseDialog ref="dialog" title="Link einfügen">
    <label class="label" for="link-dialog-url">URL</label>
    <input
      id="link-dialog-url"
      ref="input"
      v-model="url"
      type="url"
      placeholder="https://..."
      class="input w-full"
      @keyup.enter="confirm"
    />

    <template #actions>
      <BaseButton variant="neutral" @click="cancel">Abbrechen</BaseButton>
      <BaseButton variant="primary" @click="confirm">Speichern</BaseButton>
    </template>
  </BaseDialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import BaseButton from '@/components/common/BaseButton.vue'

export default {
  name: 'LinkDialog',
  components: { BaseDialog, BaseButton },
  emits: ['confirm'],
  data() {
    return { url: '' }
  },
  methods: {
    open() {
      this.url = ''
      this.$refs.dialog?.open()
      this.$nextTick(() => this.$refs.input?.focus())
    },
    confirm() {
      const value = this.url.trim()
      if (!value) return
      this.$refs.dialog?.close()
      this.$emit('confirm', value)
    },
    cancel() {
      this.$refs.dialog?.close()
    },
  },
}
</script>
