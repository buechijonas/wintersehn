<template>
  <BaseBreadcrumbs :items="breadcrumbs">
    <template #actions>
      <AddButton label="Akte" size="sm" @click="$refs.dossierDialog.open()" />
    </template>
  </BaseBreadcrumbs>
  <div
    class="flex flex-col pb-8 sm:px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1"
  >
    <div class="mx-auto w-full max-w-150 sm:pt-4">
      <div class="max-sm:px-6 max-sm:pt-4 pb-4">
        <input
          v-model.trim="query"
          type="search"
          placeholder="Personen suchen"
          aria-label="Personen suchen"
          class="input w-full"
        />
      </div>

      <div v-if="!dossiersStore.items && !error" class="flex flex-col gap-3">
        <div v-for="n in 3" :key="n" class="flex items-center gap-3 p-4">
          <div class="skeleton size-6 lg:size-5 shrink-0"></div>
          <div class="skeleton h-4 w-40"></div>
        </div>
      </div>

      <BaseCard
        v-else-if="dossiersStore.items?.length"
        tag="ul"
        class="divide-y divide-wntrs-border max-sm:border-x-0 max-sm:border-t-0"
      >
        <li v-for="dossier in dossiersStore.items" :key="dossier.uuid">
          <RouterLink
            :to="{ name: 'dossier', params: { uuid: dossier.uuid } }"
            class="flex items-center gap-4 p-4 hover:bg-base-200"
          >
            <DossierLabel :dossier="dossier" />
            <TrustPoints :points="dossier.points" />
          </RouterLink>
        </li>
      </BaseCard>

      <BaseCard v-else-if="dossiersStore.items" class="p-6 max-sm:border-x-0 max-sm:border-t-0">
        <p class="text-wntrs-muted">{{ query ? 'Keine Treffer.' : 'Noch keine Akten.' }}</p>
      </BaseCard>

      <p v-if="error" class="text-error text-sm mt-4 text-center">{{ error }}</p>
    </div>
  </div>

  <SectionDialog
    ref="dossierDialog"
    title="Akte hinzufügen"
    placeholder="Titel"
    label=""
    @confirm="createDossier"
  />
</template>

<script>
import { RouterLink } from 'vue-router'
import AddButton from '@core/components/common/AddButton.vue'
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import SectionDialog from '@core/components/common/SectionDialog.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import DossierLabel from '@/components/DossierLabel.vue'
import TrustPoints from '@/components/TrustPoints.vue'
import { useDossiersStore } from '@/stores/dossiers.js'

const SEARCH_DELAY = 300

export default {
  name: 'HomeView',
  components: {
    RouterLink,
    AddButton,
    DossierLabel,
    BaseBreadcrumbs,
    BaseCard,
    SectionDialog,
    TrustPoints,
  },
  mixins: [asyncActionMixin],
  data() {
    return {
      breadcrumbs: [{ label: 'Personalakten', to: '/' }],
      query: '',
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
  },
  watch: {
    query(query) {
      clearTimeout(this.searchTimer)
      this.searchTimer = setTimeout(() => this.search(query), SEARCH_DELAY)
    },
  },
  mounted() {
    return this.search('')
  },
  beforeUnmount() {
    clearTimeout(this.searchTimer)
  },
  methods: {
    search(query) {
      return this.runAction(() => this.dossiersStore.fetchDossiers(query))
    },
    createDossier(title) {
      return this.runAction(() => this.dossiersStore.createDossier(title, this.query))
    },
  },
}
</script>
