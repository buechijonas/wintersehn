<template>
  <div class="flex flex-col gap-6">
    <p v-if="error" class="text-error text-sm">{{ error }}</p>

    <section>
      <h3 class="text-xl my-4">Sponsoren</h3>
      <p class="text-sm text-wntrs-muted mb-4">
        Erscheinen zuoberst in den Suchresultaten unter «Alle» und wechseln sich bei jeder Suche ab.
        Sie sind als «Sponsored» markiert.
      </p>
      <BaseCard v-if="sponsorsStore.items.length" tag="ul" class="divide-y divide-wntrs-border">
        <li
          v-for="sponsor in sponsorsStore.items"
          :key="sponsor.uuid"
          class="flex items-start justify-between gap-4 p-4"
        >
          <span class="flex min-w-0 flex-col gap-1">
            <span class="font-medium">{{ sponsor.title }}</span>
            <span class="text-xs text-wntrs-muted truncate">{{ sponsor.url }}</span>
            <span v-if="sponsor.description" class="text-sm text-wntrs-slate">
              {{ sponsor.description }}
            </span>
          </span>
          <span class="flex shrink-0 gap-2">
            <EditButton @click="edit(sponsor)" />
            <DeleteButton @click="remove(sponsor)" />
          </span>
        </li>
      </BaseCard>
      <BaseCard v-else class="p-6">
        <p class="text-sm text-wntrs-muted">Noch keine Sponsoren.</p>
      </BaseCard>
    </section>

    <section>
      <h3 class="text-xl my-4">{{ editing ? 'Sponsor bearbeiten' : 'Sponsor hinzufügen' }}</h3>
      <BaseCard tag="form" class="p-6 flex flex-col gap-4" @submit.prevent="save">
        <input
          v-model.trim="form.title"
          type="text"
          placeholder="Titel"
          aria-label="Titel"
          maxlength="120"
          class="input w-full"
        />
        <input
          v-model.trim="form.url"
          type="url"
          inputmode="url"
          placeholder="https://…"
          aria-label="Link"
          class="input w-full"
        />
        <textarea
          v-model.trim="form.description"
          placeholder="Beschreibung"
          aria-label="Beschreibung"
          maxlength="300"
          rows="3"
          class="textarea w-full"
        ></textarea>
        <div class="flex justify-end gap-2">
          <CancelButton v-if="editing" @click="reset" />
          <BaseButton
            type="submit"
            variant="primary"
            :disabled="saving || !form.title || !form.url"
          >
            <AppIcon name="disk" />
            Speichern
          </BaseButton>
        </div>
      </BaseCard>
    </section>

    <ConfirmDialog
      ref="confirmDialog"
      :title="dialogTitle"
      :message="dialogMessage"
      @confirm="onConfirmDelete"
    />
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import CancelButton from '@core/components/common/CancelButton.vue'
import ConfirmDialog from '@core/components/common/ConfirmDialog.vue'
import DeleteButton from '@core/components/common/DeleteButton.vue'
import EditButton from '@core/components/common/EditButton.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import confirmDeleteMixin from '@core/mixins/confirmDeleteMixin.js'
import { useSponsorsStore } from '@/stores/sponsors.js'

const emptyForm = () => ({ title: '', url: '', description: '' })

export default {
  name: 'SponsorSettings',
  components: {
    AppIcon,
    BaseButton,
    BaseCard,
    CancelButton,
    ConfirmDialog,
    DeleteButton,
    EditButton,
  },
  mixins: [asyncActionMixin, confirmDeleteMixin],
  data() {
    return {
      editing: null,
      form: emptyForm(),
    }
  },
  computed: {
    sponsorsStore() {
      return useSponsorsStore()
    },
  },
  mounted() {
    return this.runAction(() => this.sponsorsStore.fetchSponsors())
  },
  methods: {
    edit(sponsor) {
      this.editing = sponsor.uuid
      this.form = { title: sponsor.title, url: sponsor.url, description: sponsor.description }
    },
    reset() {
      this.editing = null
      this.form = emptyForm()
    },
    async save() {
      const saved = await this.runAction(async () => {
        if (this.editing) await this.sponsorsStore.updateSponsor(this.editing, this.form)
        else await this.sponsorsStore.createSponsor(this.form)
        return true
      })
      if (saved) this.reset()
    },
    remove(sponsor) {
      this.confirmRemoval(
        'Sponsor löschen',
        `Möchtest du «${sponsor.title}» wirklich löschen?`,
        () => this.runAction(() => this.sponsorsStore.deleteSponsor(sponsor.uuid)),
      )
    },
  },
}
</script>
