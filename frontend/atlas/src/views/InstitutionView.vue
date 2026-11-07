<template>
  <AtlasPage :breadcrumbs="breadcrumbs" :loading="!institution" :error="error">
    <template #actions>
      <AddButton label="Hinzufügen" :to="`/institutions/${$route.params.uuid}/subjects/new`" />
      <ActionsMenu
        v-if="institution"
        :edit-to="editTo"
        :delete-message="`${institution.name} mit allen Fächern, Dokumentationen und Lernsets löschen?`"
        @delete="destroy"
      />
    </template>
    <div class="flex items-start justify-between gap-4">
      <h2 class="text-xl font-light">{{ institution.name }}</h2>
      <div v-if="institution.rounded" class="flex flex-col items-end gap-1">
        <GradeBadge :value="institution.rounded" :tone="institution.tone" size="lg" />
        <span class="text-xs text-wntrs-muted">{{ institution.average }}</span>
      </div>
    </div>
    <p v-if="!institution.subjects.length" class="text-wntrs-muted">Noch keine Fächer.</p>
    <ul class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <li v-for="subject in institution.subjects" :key="subject.uuid">
        <ItemCard
          :title="subject.name"
          :to="`/subjects/${subject.uuid}`"
          :meta="`${subject.documentation_count} Dokumentationen · ${subject.learning_set_count} Lernsets`"
        >
          <template #aside>
            <GradeBadge :value="subject.rounded" :tone="subject.tone" />
          </template>
        </ItemCard>
      </li>
    </ul>
  </AtlasPage>
</template>

<script>
import AddButton from '@core/components/common/AddButton.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import ActionsMenu from '@/components/ActionsMenu.vue'
import AtlasPage from '@/components/AtlasPage.vue'
import GradeBadge from '@/components/GradeBadge.vue'
import ItemCard from '@/components/ItemCard.vue'
import { useAtlasStore } from '@/stores/atlas.js'

export default {
  name: 'InstitutionView',
  components: { ActionsMenu, AddButton, AtlasPage, GradeBadge, ItemCard },
  mixins: [asyncActionMixin],
  data() {
    return {
      institution: null,
    }
  },
  computed: {
    store() {
      return useAtlasStore()
    },
    path() {
      return `/institutions/${this.$route.params.uuid}/`
    },
    editTo() {
      return `/institutions/${this.$route.params.uuid}/edit`
    },
    breadcrumbs() {
      return [{ label: 'Institutionen', to: '/' }, { label: this.institution?.name ?? '' }]
    },
  },
  mounted() {
    this.runAction(async () => {
      this.institution = await this.store.load(
        this.path,
        'Institution konnte nicht geladen werden.',
      )
    })
  },
  methods: {
    destroy() {
      return this.runAction(async () => {
        const target = '/'
        await this.store.remove(this.path, 'Löschen fehlgeschlagen.')
        this.$router.push(target)
      })
    },
  },
}
</script>
