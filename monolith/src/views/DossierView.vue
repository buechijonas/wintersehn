<template>
  <BaseBreadcrumbs :items="breadcrumbs">
    <template v-if="dossier" #actions>
      <EditButton title="Umbenennen" @click="$refs.renameDialog.open(dossier.title)" />
    </template>
  </BaseBreadcrumbs>
  <div
    class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1"
  >
    <div class="mx-auto w-full max-w-150 pt-4">
      <div v-if="!dossier && !error" class="flex flex-col gap-4">
        <div class="skeleton h-12 w-full"></div>
        <div class="skeleton h-64 w-full"></div>
      </div>

      <template v-else-if="dossier">
        <BaseTabs :tabs="tabs" :active="activeTab" />

        <BaseCard v-if="activeTab === 'meta'" class="px-6 border-t-0">
          <div class="flex justify-end pt-4">
            <EditButton :to="{ name: 'dossier-edit', params: { uuid: dossier.uuid } }" />
          </div>
          <dl class="flex flex-col divide-y divide-wntrs-border">
            <div
              v-for="field in fields"
              :key="field.key"
              class="flex items-center justify-between gap-4 py-3 text-sm"
            >
              <dt class="text-wntrs-muted shrink-0">{{ field.label }}</dt>
              <dd class="truncate">{{ formatField(field.key, dossier[field.key]) || '–' }}</dd>
            </div>
          </dl>
        </BaseCard>

        <DossierCharacterTab v-else-if="activeTab === 'character'" :uuid="dossier.uuid" />

        <DossierEventsTab v-else-if="activeTab === 'events'" :uuid="dossier.uuid" />

        <DossierRelationshipsTab v-else-if="activeTab === 'relationships'" :uuid="dossier.uuid" />

        <DossierStancesTab v-else-if="activeTab === 'ideology'" :uuid="dossier.uuid" />

        <DossierTrustTab v-else-if="activeTab === 'trust'" :uuid="dossier.uuid" />

        <DossierAddictionsTab v-else-if="activeTab === 'addictions'" :uuid="dossier.uuid" />

        <DossierReferencesTab v-else-if="activeTab === 'references'" :uuid="dossier.uuid" />

        <DossierLinkTab v-else-if="activeTab === 'link'" :uuid="dossier.uuid" />

        <DossierSharesTab v-else-if="activeTab === 'shares'" :uuid="dossier.uuid" />
      </template>

      <p v-if="error" class="text-error text-sm mt-4 text-center">{{ error }}</p>
    </div>
  </div>

  <SectionDialog
    ref="renameDialog"
    title="Akte umbenennen"
    placeholder="Titel"
    label=""
    confirm-label="Speichern"
    confirm-icon="disk"
    @confirm="rename"
  />
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import BaseTabs from '@core/components/common/BaseTabs.vue'
import EditButton from '@core/components/common/EditButton.vue'
import SectionDialog from '@core/components/common/SectionDialog.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import DossierAddictionsTab from '@/components/DossierAddictionsTab.vue'
import DossierCharacterTab from '@/components/DossierCharacterTab.vue'
import DossierEventsTab from '@/components/DossierEventsTab.vue'
import DossierLinkTab from '@/components/DossierLinkTab.vue'
import DossierReferencesTab from '@/components/DossierReferencesTab.vue'
import DossierRelationshipsTab from '@/components/DossierRelationshipsTab.vue'
import DossierSharesTab from '@/components/DossierSharesTab.vue'
import DossierStancesTab from '@/components/DossierStancesTab.vue'
import DossierTrustTab from '@/components/DossierTrustTab.vue'
import { formatField, metaFields } from '@/data/dossierFields.js'
import { sectionTabs } from '@/data/tabs.js'
import { useDossiersStore } from '@/stores/dossiers.js'

const TABS = [
  ...sectionTabs,
  { key: 'link', label: 'Verknüpfung' },
  { key: 'shares', label: 'Freigaben' },
]

export default {
  name: 'DossierView',
  components: {
    BaseBreadcrumbs,
    BaseCard,
    BaseTabs,
    DossierAddictionsTab,
    DossierCharacterTab,
    DossierEventsTab,
    DossierLinkTab,
    DossierReferencesTab,
    DossierRelationshipsTab,
    DossierSharesTab,
    DossierStancesTab,
    DossierTrustTab,
    EditButton,
    SectionDialog,
  },
  mixins: [asyncActionMixin],
  data() {
    return {
      fields: metaFields,
      tabs: TABS,
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
    dossier() {
      return this.dossiersStore.current
    },
    activeTab() {
      return this.$route.query.tab ?? TABS[0].key
    },
    breadcrumbs() {
      return [{ label: 'Personalakten', to: '/' }, { label: this.dossier?.title ?? '…' }]
    },
  },
  watch: {
    '$route.params.uuid': {
      immediate: true,
      handler(uuid) {
        return this.runAction(() => this.dossiersStore.fetchDossier(uuid))
      },
    },
  },
  methods: {
    formatField,
    rename(title) {
      return this.runAction(() => this.dossiersStore.updateDossier(this.dossier.uuid, { title }))
    },
  },
}
</script>
