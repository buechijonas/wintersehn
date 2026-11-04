<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div
    class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1"
  >
    <div class="mx-auto w-full max-w-150 pt-4">
      <div v-if="!document && !error" class="flex flex-col gap-4">
        <div class="skeleton h-12 w-full"></div>
        <div class="skeleton h-64 w-full"></div>
      </div>

      <SharedDocument v-else-if="document" :document="document" />

      <p v-if="error" class="text-error text-sm mt-4 text-center">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import SharedDocument from '@/components/SharedDocument.vue'
import { activeTab, sharedBreadcrumbs } from '@/data/sharing.js'
import { useDossiersStore } from '@/stores/dossiers.js'

export default {
  name: 'SharedDossierView',
  components: { BaseBreadcrumbs, SharedDocument },
  mixins: [asyncActionMixin],
  data() {
    return {
      document: null,
    }
  },
  computed: {
    breadcrumbs() {
      const root = { label: 'Mit mir geteilt', to: '/shared' }
      if (!this.document) return [root]
      return sharedBreadcrumbs(this.document, activeTab(this.$route), root)
    },
  },
  watch: {
    '$route.params.share': {
      immediate: true,
      handler(share) {
        this.document = null
        return this.runAction(async () => {
          this.document = await useDossiersStore().fetchSharedDossier(share)
        })
      },
    },
  },
}
</script>
