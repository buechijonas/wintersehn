<template>
  <AtlasPage :breadcrumbs="breadcrumbs" :loading="!documentation" :error="error">
    <template #actions>
      <ActionsMenu
        v-if="documentation"
        :edit-to="editTo"
        :delete-message="`${documentation.title} löschen?`"
        @delete="destroy"
      />
    </template>
    <h2 class="text-xl font-light">{{ documentation.title }}</h2>
    <p v-if="!documentation.body" class="text-wntrs-muted">Diese Dokumentation ist noch leer.</p>
    <MarkdownContent :html="documentation.html" class="max-w-200" />
  </AtlasPage>
</template>

<script>
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import ActionsMenu from '@/components/ActionsMenu.vue'
import AtlasPage from '@/components/AtlasPage.vue'
import MarkdownContent from '@/components/MarkdownContent.vue'
import { subjectBreadcrumbs } from '@/lib/breadcrumbs.js'
import { useAtlasStore } from '@/stores/atlas.js'

export default {
  name: 'DocumentationView',
  components: { ActionsMenu, AtlasPage, MarkdownContent },
  mixins: [asyncActionMixin],
  data() {
    return {
      documentation: null,
    }
  },
  computed: {
    store() {
      return useAtlasStore()
    },
    path() {
      return `/documentations/${this.$route.params.uuid}/`
    },
    editTo() {
      return `/documentations/${this.$route.params.uuid}/edit`
    },
    breadcrumbs() {
      return [
        ...subjectBreadcrumbs(this.documentation?.subject),
        { label: this.documentation?.title ?? '' },
      ]
    },
  },
  mounted() {
    this.runAction(async () => {
      this.documentation = await this.store.load(
        this.path,
        'Dokumentation konnte nicht geladen werden.',
      )
    })
  },
  methods: {
    destroy() {
      return this.runAction(async () => {
        const target = `/subjects/${this.documentation.subject.uuid}`
        await this.store.remove(this.path, 'Löschen fehlgeschlagen.')
        this.$router.push(target)
      })
    },
  },
}
</script>
