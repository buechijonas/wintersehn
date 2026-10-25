<template>
  <BaseDialog ref="dialog" title="Referenz hinzufügen">
    <form :id="formId" class="fieldset" @submit.prevent="confirm">
      <div class="join w-full">
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
    </form>

    <template #actions>
      <BaseButton variant="neutral" @click="$refs.dialog.close()">
        <AppIcon name="cross" />
        Abbrechen
      </BaseButton>
      <BaseButton type="submit" :form="formId" variant="primary">
        <AppIcon name="plus" />
        Hinzufügen
      </BaseButton>
    </template>
  </BaseDialog>
</template>

<script>
import { social } from '@core/assets/social.js'
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseDialog from '@core/components/common/BaseDialog.vue'
import IconPickerField from '@core/components/common/IconPickerField.vue'
import { referenceKinds } from '@/data/eventReferences.js'
import { platformName } from '@/data/platforms.js'

function emptyDraft() {
  return { kind: 'chat', icon: '', title: '' }
}

export default {
  name: 'EventReferenceDialog',
  components: { AppIcon, BaseButton, BaseDialog, IconPickerField },
  emits: ['confirm'],
  data() {
    return {
      referenceKinds,
      social,
      formId: 'event-reference-dialog-form',
      draft: emptyDraft(),
    }
  },
  watch: {
    'draft.icon'(icon, previous) {
      const untouched = !this.draft.title || this.draft.title === platformName(previous || ' ')
      if (icon && untouched) this.draft.title = platformName(icon)
    },
  },
  methods: {
    open() {
      this.draft = emptyDraft()
      this.$refs.dialog.open()
      this.$nextTick(() => this.$refs.input.focus())
    },
    confirm() {
      this.$refs.dialog.close()
      this.$emit('confirm', { ...this.draft })
    },
  },
}
</script>
