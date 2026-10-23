<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="relative h-[calc(100dvh-101px)]">
    <NetworkGraph v-if="network?.dossiers.length" v-bind="network" controls />
    <div v-else-if="!network && !error" class="skeleton absolute inset-6"></div>
    <p v-else-if="network" class="p-6 text-center text-wntrs-muted">Noch keine Akten.</p>
    <p v-if="error" class="text-error text-sm p-6 text-center">{{ error }}</p>
  </div>
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import NetworkGraph from '@/components/NetworkGraph.vue'
import { useDossiersStore } from '@/stores/dossiers.js'

export default {
  name: 'NetworkView',
  components: { BaseBreadcrumbs, NetworkGraph },
  mixins: [asyncActionMixin],
  data() {
    return {
      breadcrumbs: [{ label: 'Netzwerk', to: '/network' }],
      network: null,
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
  },
  mounted() {
    return this.runAction(async () => {
      this.network = await this.dossiersStore.fetchNetwork()
    })
  },
}
</script>
