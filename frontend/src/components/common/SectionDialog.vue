<template>
  <BaseDialog ref="dialog" title="Abschnitt hinzufügen">
    <label class="label" for="section-dialog-title">Titel</label>
    <input
      id="section-dialog-title"
      ref="input"
      v-model="title"
      type="text"
      placeholder="Neuer Abschnitt"
      class="input w-full"
      @keyup.enter="confirm"
    />

    <template #actions>
      <BaseButton variant="neutral" @click="cancel">
        <AppIcon name="cross" />
        Abbrechen
      </BaseButton>
      <BaseButton variant="primary" @click="confirm">
        <AppIcon name="plus" />
        Hinzufügen
      </BaseButton>
    </template>
  </BaseDialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import AppIcon from '@/components/common/AppIcon.vue'

export default {
  name: 'SectionDialog',
  components: { BaseDialog, BaseButton, AppIcon },
  emits: ['confirm'],
  data() {
    return { title: '' }
  },
  methods: {
    open() {
      this.title = ''
      this.$refs.dialog?.open()
      this.$nextTick(() => this.$refs.input?.focus())
    },
    confirm() {
      const value = this.title.trim()
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
