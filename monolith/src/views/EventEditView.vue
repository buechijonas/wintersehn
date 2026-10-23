<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div
    class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1"
  >
    <div class="mx-auto w-full max-w-150">
      <h2 class="text-xl font-light my-4">Ereignis bearbeiten</h2>

      <div v-if="!draft && !error" class="skeleton h-96 w-full"></div>

      <BaseCard v-else-if="draft" class="p-6">
        <form class="fieldset" @submit.prevent="save">
          <label class="label" for="event-title">Titel</label>
          <input
            id="event-title"
            v-model.trim="draft.title"
            type="text"
            class="input w-full"
            required
          />
          <label class="label mt-4" for="event-date">Datum</label>
          <input id="event-date" v-model="draft.date" type="date" class="input w-full" required />
          <label class="label mt-4" for="event-text">Text</label>
          <textarea
            id="event-text"
            v-model="draft.text"
            class="textarea w-full min-h-96 [field-sizing:content] text-base leading-relaxed"
          ></textarea>

          <p v-if="error" class="text-error text-sm mt-3">{{ error }}</p>

          <div class="flex items-center justify-between gap-4 mt-4">
            <DeleteButton :disabled="saving" @click="$refs.confirmDialog.open()" />
            <div class="flex gap-4">
              <CancelButton :to="detailRoute" />
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
    title="Ereignis löschen"
    :message="`Möchtest du «${event?.title}» wirklich löschen?`"
    @confirm="remove"
  />
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import CancelButton from '@core/components/common/CancelButton.vue'
import ConfirmDialog from '@core/components/common/ConfirmDialog.vue'
import DeleteButton from '@core/components/common/DeleteButton.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import eventMixin from '@/mixins/eventMixin.js'

export default {
  name: 'EventEditView',
  components: {
    AppIcon,
    BaseBreadcrumbs,
    BaseButton,
    BaseCard,
    CancelButton,
    ConfirmDialog,
    DeleteButton,
  },
  mixins: [asyncActionMixin, eventMixin],
  data() {
    return {
      draft: null,
    }
  },
  computed: {
    detailRoute() {
      return { name: 'event', params: this.$route.params }
    },
    breadcrumbs() {
      return [
        ...this.baseBreadcrumbs,
        { label: this.event?.title ?? '…', to: this.detailRoute },
        { label: 'Bearbeiten' },
      ]
    },
  },
  watch: {
    event(event) {
      this.draft = event && { ...event }
    },
  },
  methods: {
    save() {
      const { title, date, text } = this.draft
      return this.runAction(async () => {
        await this.dossiersStore.updateEvent(this.uuid, this.event.uuid, { title, date, text })
        this.$router.push(this.detailRoute)
      })
    },
    remove() {
      return this.runAction(async () => {
        await this.dossiersStore.deleteEvent(this.uuid, this.event.uuid)
        this.$router.push(this.dossierRoute)
      })
    },
  },
}
</script>
