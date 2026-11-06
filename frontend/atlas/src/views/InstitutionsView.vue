<template>
  <AtlasPage :breadcrumbs="breadcrumbs" :loading="!institutions" :error="error">
    <template #actions>
      <AddButton label="Hinzufügen" to="/institutions/new" />
    </template>
    <p v-if="!institutions.length" class="text-wntrs-muted">Noch keine Institutionen.</p>
    <ul class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <li v-for="institution in institutions" :key="institution.uuid">
        <ItemCard
          :title="institution.name"
          :to="`/institutions/${institution.uuid}`"
          icon="building"
          :meta="`${institution.subject_count} Fächer`"
        />
      </li>
    </ul>
  </AtlasPage>
</template>

<script>
import AddButton from '@core/components/common/AddButton.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import AtlasPage from '@/components/AtlasPage.vue'
import ItemCard from '@/components/ItemCard.vue'
import { useAtlasStore } from '@/stores/atlas.js'

export default {
  name: 'InstitutionsView',
  components: { AddButton, AtlasPage, ItemCard },
  mixins: [asyncActionMixin],
  data() {
    return {
      institutions: null,
      breadcrumbs: [{ label: 'Institutionen' }],
    }
  },
  mounted() {
    this.runAction(async () => {
      this.institutions = await useAtlasStore().load(
        '/institutions/',
        'Institutionen konnten nicht geladen werden.',
      )
    })
  },
}
</script>
