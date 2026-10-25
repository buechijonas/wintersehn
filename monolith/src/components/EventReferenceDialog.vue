<template>
  <BaseDialog ref="dialog" :title="title">
    <form :id="formId" class="fieldset" @submit.prevent="confirm">
      <div v-if="!editing" class="join w-full">
        <BaseButton
          v-for="(kind, key) in referenceKinds"
          :key="key"
          class="join-item flex-1"
          :variant="draft.kind === key ? 'primary' : 'neutral'"
          @click="draft.kind = key"
        >
          {{ kind.label }}
        </BaseButton>
      </div>
      <IconPickerField
        v-if="draft.kind === 'chat'"
        v-model="draft.icon"
        :icons="social"
        label="Plattform"
        class="mt-2"
      />
      <label class="label mt-2" :for="`${formId}-title`">Titel</label>
      <input
        :id="`${formId}-title`"
        ref="input"
        v-model.trim="draft.title"
        type="text"
        maxlength="200"
        class="input w-full"
        required
      />
      <template v-if="draft.kind === 'text'">
        <label class="label mt-2" :for="`${formId}-text`">Text</label>
        <textarea
          :id="`${formId}-text`"
          v-model="draft.text"
          class="textarea w-full min-h-40 [field-sizing:content] leading-relaxed"
        ></textarea>
      </template>
    </form>

    <template #actions>
      <DeleteButton v-if="editing" class="mr-auto" @click="remove" />
      <BaseButton variant="neutral" @click="$refs.dialog.close()">
        <AppIcon name="cross" />
        Abbrechen
      </BaseButton>
      <BaseButton type="submit" :form="formId" variant="primary">
        <AppIcon :name="editing ? 'disk' : 'plus'" />
        {{ editing ? 'Speichern' : 'Hinzufügen' }}
      </BaseButton>
    </template>
  </BaseDialog>
</template>

<script>
import { social } from '@core/assets/social.js'
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseDialog from '@core/components/common/BaseDialog.vue'
import DeleteButton from '@core/components/common/DeleteButton.vue'
import IconPickerField from '@core/components/common/IconPickerField.vue'
import { referenceKinds } from '@/data/eventReferences.js'
import { platformName } from '@/data/platforms.js'

function emptyDraft() {
  return { kind: 'chat', icon: '', title: '', text: '' }
}

export default {
  name: 'EventReferenceDialog',
  components: { AppIcon, BaseButton, BaseDialog, DeleteButton, IconPickerField },
  emits: ['confirm', 'remove'],
  data() {
    return {
      referenceKinds,
      social,
      formId: 'event-reference-dialog-form',
      editing: false,
      draft: emptyDraft(),
    }
  },
  computed: {
    title() {
      return this.editing ? 'Referenz bearbeiten' : 'Referenz hinzufügen'
    },
  },
  watch: {
    'draft.icon'(icon, previous) {
      const untouched = !this.draft.title || this.draft.title === platformName(previous || ' ')
      if (icon && untouched) this.draft.title = platformName(icon)
    },
  },
  methods: {
    open(reference = null) {
      this.editing = Boolean(reference)
      this.draft = reference
        ? {
            kind: reference.kind,
            icon: reference.icon,
            title: reference.title,
            text: reference.text,
          }
        : emptyDraft()
      this.$refs.dialog.open()
      this.$nextTick(() => this.$refs.input.focus())
    },
    confirm() {
      this.$refs.dialog.close()
      this.$emit('confirm', { ...this.draft })
    },
    remove() {
      this.$refs.dialog.close()
      this.$emit('remove')
    },
  },
}
</script>
