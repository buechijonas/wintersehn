<template>
  <BaseCard class="border-t-0">
    <div class="flex justify-end px-6 pt-4">
      <EditToggle v-model="editing" />
    </div>

    <form
      v-if="editing"
      class="fieldset px-6 pt-4 pb-4 border-b border-wntrs-border"
      @submit.prevent="add"
    >
      <IconPickerField v-model="draft.icon" :icons="social" label="Plattform" />
      <input
        v-model.trim="draft.name"
        type="text"
        placeholder="Name"
        aria-label="Name"
        class="input w-full mt-4"
        required
      />
      <input
        v-model.trim="draft.url"
        type="url"
        placeholder="https://…"
        aria-label="Link"
        class="input w-full mt-2"
        required
      />
      <div class="flex justify-end mt-4">
        <BaseButton type="submit" :disabled="saving || !draft.icon">
          <AppIcon name="plus" />
          Hinzufügen
        </BaseButton>
      </div>
    </form>

    <div v-if="!references && !error" class="flex items-center gap-4 px-6 py-4">
      <div class="skeleton size-10 shrink-0"></div>
      <div class="skeleton h-4 w-40"></div>
    </div>

    <ul v-else-if="references?.length" class="flex flex-col divide-y divide-wntrs-border">
      <li
        v-for="reference in references"
        :key="reference.uuid"
        class="flex items-center gap-4 px-6 py-4"
      >
        <img
          class="size-10 shrink-0"
          :alt="platformName(reference.icon)"
          :src="social[reference.icon] ?? icons['link-alt']"
        />
        <div class="flex flex-col min-w-0 flex-1 text-sm">
          <span class="font-bold truncate">{{ reference.name }}</span>
          <span class="text-wntrs-muted truncate">{{ platformName(reference.icon) }}</span>
        </div>
        <BaseButton
          v-if="editing"
          variant="neutral"
          shape="square"
          size="sm"
          title="Entfernen"
          :disabled="saving"
          @click="remove(reference)"
        >
          <AppIcon name="trash" alt="Entfernen" />
        </BaseButton>
        <BaseButton
          v-else
          variant="ghost"
          shape="square"
          :href="reference.url"
          target="_blank"
          rel="noopener noreferrer"
          :title="`${platformName(reference.icon)} öffnen`"
        >
          <AppIcon name="share-square" :alt="`${platformName(reference.icon)} öffnen`" />
        </BaseButton>
      </li>
    </ul>

    <p v-else-if="references" class="px-6 py-4 text-sm text-wntrs-muted">Noch keine Referenzen.</p>

    <p v-if="error" class="text-error text-sm px-6 py-4">{{ error }}</p>
  </BaseCard>
</template>

<script>
import { icons } from '@core/assets/icons.js'
import { social } from '@core/assets/social.js'
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import IconPickerField from '@core/components/common/IconPickerField.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import EditToggle from '@/components/EditToggle.vue'
import { platformName } from '@/data/platforms.js'
import { useDossiersStore } from '@/stores/dossiers.js'

const EMPTY_DRAFT = { icon: '', name: '', url: '' }

export default {
  name: 'DossierReferencesTab',
  components: { AppIcon, BaseButton, BaseCard, EditToggle, IconPickerField },
  mixins: [asyncActionMixin],
  props: {
    uuid: { type: String, required: true },
  },
  data() {
    return {
      icons,
      social,
      references: null,
      editing: false,
      draft: { ...EMPTY_DRAFT },
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
  },
  watch: {
    editing() {
      this.draft = { ...EMPTY_DRAFT }
    },
    uuid: {
      immediate: true,
      handler() {
        this.references = null
        this.editing = false
        return this.runAction(async () => {
          this.references = await this.dossiersStore.fetchReferences(this.uuid)
        })
      },
    },
  },
  methods: {
    platformName,
    add() {
      return this.runAction(async () => {
        const reference = await this.dossiersStore.addReference(this.uuid, this.draft)
        this.references = [...this.references, reference]
        this.draft = { ...EMPTY_DRAFT }
      })
    },
    remove(reference) {
      return this.runAction(async () => {
        await this.dossiersStore.removeReference(this.uuid, reference.uuid)
        this.references = this.references.filter((r) => r !== reference)
      })
    },
  },
}
</script>
