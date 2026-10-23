<template>
  <BaseDialog ref="dialog" :title="title">
    <label v-if="label" class="label" for="section-dialog-title">{{ label }}</label>
    <input
      id="section-dialog-title"
      ref="input"
      v-model="value"
      type="text"
      :placeholder="placeholder"
      :aria-label="label ? null : placeholder"
      class="input w-full"
      @keyup.enter="confirm"
    />

    <template #actions>
      <BaseButton variant="neutral" @click="cancel">
        <AppIcon name="cross" />
        Abbrechen
      </BaseButton>
      <BaseButton variant="primary" @click="confirm">
        <AppIcon :name="confirmIcon" />
        {{ confirmLabel }}
      </BaseButton>
    </template>
  </BaseDialog>
</template>

<script>
import BaseDialog from '@core/components/common/BaseDialog.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import AppIcon from '@core/components/common/AppIcon.vue'

export default {
  name: 'SectionDialog',
  components: { BaseDialog, BaseButton, AppIcon },
  props: {
    title: { type: String, default: 'Abschnitt hinzufügen' },
    placeholder: { type: String, default: 'Neuer Abschnitt' },
    label: { type: String, default: 'Titel' },
    confirmLabel: { type: String, default: 'Hinzufügen' },
    confirmIcon: { type: String, default: 'plus' },
  },
  emits: ['confirm'],
  data() {
    return { value: '' }
  },
  methods: {
    open(value = '') {
      this.value = value
      this.$refs.dialog?.open()
      this.$nextTick(() => this.$refs.input?.focus())
    },
    confirm() {
      const value = this.value.trim()
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
