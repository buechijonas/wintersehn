<template>
  <AtlasPage :breadcrumbs="breadcrumbs" :loading="!subject" :error="error">
    <template #actions>
      <AddButton label="Hinzufügen" @click="$refs.addDialog.open()" />
      <ActionsMenu
        v-if="subject"
        :edit-to="editTo"
        :delete-message="`${subject.name} mit allen Dokumentationen und Lernsets löschen?`"
        @delete="destroy"
      />
    </template>
    <h2 class="text-xl font-light">{{ subject.name }}</h2>
    <div class="grid items-start gap-8 lg:grid-cols-2">
      <section v-for="section in sections" :key="section.key" class="flex flex-col gap-4">
        <h3 class="text-sm text-wntrs-muted">{{ section.label }}</h3>
        <p v-if="!subject[section.key].length" class="text-sm text-wntrs-muted">
          {{ section.empty }}
        </p>
        <ul class="grid gap-4 sm:grid-cols-2 lg:grid-cols-1 xl:grid-cols-2">
          <li v-for="item in subject[section.key]" :key="item.uuid">
            <ItemCard
              :title="item.title"
              :to="`${section.base}/${item.uuid}`"
              :icon="section.icon"
              :meta="section.meta(item)"
            />
          </li>
        </ul>
      </section>
    </div>
    <BaseDialog
      ref="addDialog"
      title="Hinzufügen"
      description="Was möchtest du zu diesem Fach hinzufügen?"
      :buttons="addOptions"
      @action="add"
    />
  </AtlasPage>
</template>

<script>
import AddButton from '@core/components/common/AddButton.vue'
import BaseDialog from '@core/components/common/BaseDialog.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import ActionsMenu from '@/components/ActionsMenu.vue'
import AtlasPage from '@/components/AtlasPage.vue'
import ItemCard from '@/components/ItemCard.vue'
import { subjectBreadcrumbs } from '@/lib/breadcrumbs.js'
import { cardProgress } from '@/lib/progress.js'
import { useAtlasStore } from '@/stores/atlas.js'

export default {
  name: 'SubjectView',
  components: { ActionsMenu, AddButton, AtlasPage, BaseDialog, ItemCard },
  mixins: [asyncActionMixin],
  data() {
    return {
      subject: null,
      addOptions: [
        { value: 'documentations', label: 'Dokumentation', icon: 'poll-h' },
        { value: 'learning-sets', label: 'Lernset', icon: 'cards-blank', variant: 'primary' },
      ],
      sections: [
        {
          key: 'documentations',
          label: 'Dokumentationen',
          empty: 'Noch keine Dokumentationen.',
          base: '/documentations',
          icon: 'poll-h',
          meta: () => '',
        },
        {
          key: 'learning_sets',
          label: 'Lernsets',
          empty: 'Noch keine Lernsets.',
          base: '/learning-sets',
          icon: 'cards-blank',
          meta: cardProgress,
        },
      ],
    }
  },
  computed: {
    store() {
      return useAtlasStore()
    },
    path() {
      return `/subjects/${this.$route.params.uuid}/`
    },
    editTo() {
      return `/subjects/${this.$route.params.uuid}/edit`
    },
    breadcrumbs() {
      return [...subjectBreadcrumbs(this.subject).slice(0, -1), { label: this.subject?.name ?? '' }]
    },
  },
  mounted() {
    this.runAction(async () => {
      this.subject = await this.store.load(this.path, 'Fach konnte nicht geladen werden.')
    })
  },
  methods: {
    destroy() {
      return this.runAction(async () => {
        const target = `/institutions/${this.subject.institution.uuid}`
        await this.store.remove(this.path, 'Löschen fehlgeschlagen.')
        this.$router.push(target)
      })
    },
    add(type) {
      this.$router.push(`/subjects/${this.$route.params.uuid}/${type}/new`)
    },
  },
}
</script>
