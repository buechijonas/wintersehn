<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div
    class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1"
  >
    <div class="mx-auto w-full max-w-250">
      <h2 class="text-xl font-light my-4">Referenz bearbeiten</h2>

      <div v-if="!draft && !error" class="skeleton h-96 w-full"></div>

      <BaseCard v-else-if="draft" class="p-6">
        <form class="fieldset" @submit.prevent="save">
          <IconPickerField
            v-if="reference.kind === 'chat'"
            v-model="draft.icon"
            :icons="social"
            label="Plattform"
            class="mb-4"
          />
          <label class="label" for="reference-title">Titel</label>
          <input
            id="reference-title"
            v-model.trim="draft.title"
            type="text"
            maxlength="200"
            class="input w-full"
            required
          />
          <template v-if="reference.kind === 'text'">
            <label class="label mt-4" for="reference-text">Text</label>
            <MarkdownEditor id="reference-text" v-model="draft.text" />
          </template>

          <p v-if="error" class="text-error text-sm mt-3">{{ error }}</p>

          <div class="flex items-center justify-between gap-4 mt-4">
            <DeleteButton :disabled="saving" @click="$refs.confirmDialog.open()" />
            <div class="flex gap-4">
              <CancelButton :to="referenceRoute" />
              <BaseButton type="submit" variant="primary" :disabled="saving">
                <AppIcon name="disk" />
                Speichern
              </BaseButton>
            </div>
          </div>
        </form>
      </BaseCard>
    </div>
  </div>

  <ConfirmDialog
    ref="confirmDialog"
    title="Referenz löschen"
    :message="`Möchtest du «${reference?.title}» wirklich löschen?`"
    @confirm="remove"
  />
</template>

<script>
import { social } from '@core/assets/social.js'
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import CancelButton from '@core/components/common/CancelButton.vue'
import ConfirmDialog from '@core/components/common/ConfirmDialog.vue'
import DeleteButton from '@core/components/common/DeleteButton.vue'
import IconPickerField from '@core/components/common/IconPickerField.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import MarkdownEditor from '@/components/MarkdownEditor.vue'
import eventMixin from '@/mixins/eventMixin.js'
import eventReferenceMixin from '@/mixins/eventReferenceMixin.js'

export default {
  name: 'EventReferenceEditView',
  components: {
    AppIcon,
    BaseBreadcrumbs,
    BaseButton,
    BaseCard,
    CancelButton,
    ConfirmDialog,
    DeleteButton,
    IconPickerField,
    MarkdownEditor,
  },
  mixins: [asyncActionMixin, eventMixin, eventReferenceMixin],
  data() {
    return {
      social,
      draft: null,
    }
  },
  computed: {
    breadcrumbs() {
      return [
        ...this.referenceBreadcrumbs,
        { label: this.reference?.title ?? '…', to: this.referenceRoute },
        { label: 'Bearbeiten' },
      ]
    },
  },
  watch: {
    reference(reference) {
      const { icon, title, text } = reference ?? {}
      this.draft = reference && { icon, title, text }
    },
  },
  methods: {
    save() {
      return this.runAction(async () => {
        await this.dossiersStore.updateEventReference(
          this.uuid,
          this.eventUuid,
          this.reference.uuid,
          this.draft,
        )
        this.$router.push(this.referenceRoute)
      })
    },
    remove() {
      return this.runAction(async () => {
        await this.dossiersStore.deleteEventReference(
          this.uuid,
          this.eventUuid,
          this.reference.uuid,
        )
        this.$router.push(this.eventRoute)
      })
    },
  },
}
</script>
