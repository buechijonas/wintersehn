<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="relative h-[calc(100dvh-101px)]">
    <TrustCircles v-if="trust?.dossiers.length" v-bind="trust" @move="move" />
    <div v-else-if="!trust && !error" class="skeleton absolute inset-6"></div>
    <p v-else-if="trust" class="p-6 text-center text-wntrs-muted">Noch keine Akten.</p>
    <p v-if="error" class="absolute top-4 inset-x-0 text-error text-sm text-center">
      {{ error }}
    </p>
  </div>
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import TrustCircles from '@/components/TrustCircles.vue'
import { useDossiersStore } from '@/stores/dossiers.js'

export default {
  name: 'TrustView',
  components: { BaseBreadcrumbs, TrustCircles },
  mixins: [asyncActionMixin],
  data() {
    return {
      breadcrumbs: [{ label: 'Vertrauenskreise', to: '/trust' }],
      trust: null,
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
  },
  mounted() {
    return this.load()
  },
  methods: {
    load() {
      return this.runAction(async () => {
        this.trust = await this.dossiersStore.fetchTrust()
      })
    },
    async move(node, level) {
      const dossier = this.trust.dossiers.find((d) => d.uuid === node.uuid)
      const previous = dossier.level
      dossier.level = level
      await this.runAction(() =>
        level
          ? this.dossiersStore.setTrust(node.uuid, level)
          : this.dossiersStore.removeTrust(node.uuid),
      )
      if (this.error) dossier.level = previous
    },
  },
}
</script>
