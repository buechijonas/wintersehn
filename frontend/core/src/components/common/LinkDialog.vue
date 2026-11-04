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
      <BaseButton variant="neutral" @click="cancel">
        <AppIcon name="cross" />
        Abbrechen
      </BaseButton>
      <BaseButton variant="primary" @click="confirm">
        <AppIcon name="disk" />
        Speichern
      </BaseButton>
    </template>
  </BaseDialog>
</template>

<script>
import BaseDialog from '@core/components/common/BaseDialog.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import AppIcon from '@core/components/common/AppIcon.vue'

export default {
  name: 'LinkDialog',
  components: { BaseDialog, BaseButton, AppIcon },
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
