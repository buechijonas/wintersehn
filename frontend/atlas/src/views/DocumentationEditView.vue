<template>
  <AtlasPage :breadcrumbs="breadcrumbs" :loading="!draft" :error="error">
    <template v-if="documentation" #actions>
      <DeleteAction :message="`${documentation.title} löschen?`" @confirm="destroy" />
    </template>
    <form class="flex flex-col gap-4" @submit.prevent="save">
      <input
        v-model="draft.title"
        type="text"
        aria-label="Titel"
        placeholder="Titel, z.B. Ableitungen"
        class="input w-full max-w-160 border-wntrs-border text-lg focus:border-primary focus:outline-none"
      />
      <div class="flex flex-wrap items-center gap-2">
        <ImageUploadButton @uploaded="insertImage" @error="error = $event" />
        <span class="text-xs text-wntrs-muted">
          Markdown, zum Beispiel # Titel, **fett**, - Liste oder ``` für Code.
        </span>
      </div>
      <div class="grid gap-4 lg:grid-cols-2">
        <textarea
          v-model="draft.body"
          aria-label="Inhalt in Markdown"
          class="textarea min-h-[60dvh] w-full border-wntrs-border font-mono text-sm focus:border-primary focus:outline-none"
        ></textarea>
        <BaseCard class="min-h-[60dvh] overflow-y-auto rounded-box p-4">
          <MarkdownContent :html="preview" />
        </BaseCard>
      </div>
      <div class="grid grid-cols-2 gap-2 sm:flex sm:justify-end">
        <CancelButton :to="cancelTarget" />
        <BaseButton type="submit" variant="primary" :disabled="saving || !draft.title.trim()">
          <AppIcon :name="editing ? 'disk' : 'plus'" />
          {{ editing ? 'Speichern' : 'Erstellen' }}
        </BaseButton>
      </div>
    </form>
  </AtlasPage>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import CancelButton from '@core/components/common/CancelButton.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import AtlasPage from '@/components/AtlasPage.vue'
import DeleteAction from '@/components/DeleteAction.vue'
import ImageUploadButton from '@/components/ImageUploadButton.vue'
import MarkdownContent from '@core/components/common/MarkdownContent.vue'
import { subjectBreadcrumbs } from '@/lib/breadcrumbs.js'
import { useAtlasStore } from '@/stores/atlas.js'

const PREVIEW_DELAY = 300

export default {
  name: 'DocumentationEditView',
  components: {
    AppIcon,
    AtlasPage,
    BaseButton,
    BaseCard,
    CancelButton,
    DeleteAction,
    ImageUploadButton,
    MarkdownContent,
  },
  mixins: [asyncActionMixin],
  data() {
    return {
      documentation: null,
      subject: null,
      draft: null,
      preview: '',
      previewTimer: null,
    }
  },
  computed: {
    store() {
      return useAtlasStore()
    },
    editing() {
      return this.$route.meta.mode === 'edit'
    },
    uuid() {
      return this.$route.params.uuid
    },
    path() {
      return `/documentations/${this.uuid}/`
    },
    cancelTarget() {
      return this.editing ? `/documentations/${this.uuid}` : `/subjects/${this.uuid}`
    },
    breadcrumbs() {
      if (!this.editing) {
        return [...subjectBreadcrumbs(this.subject), { label: 'Neue Dokumentation' }]
      }
      const documentation = this.documentation
      return [
        ...subjectBreadcrumbs(documentation?.subject),
        {
          label: documentation?.title ?? '',
          to: documentation && `/documentations/${documentation.uuid}`,
        },
        { label: 'Bearbeiten' },
      ]
    },
  },
  watch: {
    'draft.body'(body) {
      clearTimeout(this.previewTimer)
      this.previewTimer = setTimeout(() => this.renderPreview(body), PREVIEW_DELAY)
    },
  },
  mounted() {
    this.runAction(async () => {
      if (!this.editing) {
        this.subject = await this.store.load(
          `/subjects/${this.uuid}/`,
          'Fach konnte nicht geladen werden.',
        )
        this.draft = { title: '', body: '' }
        return
      }
      this.documentation = await this.store.load(
        this.path,
        'Dokumentation konnte nicht geladen werden.',
      )
      this.draft = { title: this.documentation.title, body: this.documentation.body }
      this.preview = this.documentation.html
    })
  },
  beforeUnmount() {
    clearTimeout(this.previewTimer)
  },
  methods: {
    async renderPreview(body) {
      const { html } = await this.store.send(
        '/documentations/preview/',
        'POST',
        { body },
        'Vorschau fehlgeschlagen.',
      )
      this.preview = html
    },
    insertImage(image) {
      const separator = this.draft.body && !this.draft.body.endsWith('\n') ? '\n\n' : ''
      this.draft.body = `${this.draft.body}${separator}![${image.name}](${image.url})\n`
    },
    save() {
      return this.runAction(async () => {
        const documentation = this.editing
          ? await this.store.send(this.path, 'PATCH', this.draft, 'Speichern fehlgeschlagen.')
          : await this.store.send(
              `/subjects/${this.uuid}/documentations/`,
              'POST',
              this.draft,
              'Erstellen fehlgeschlagen.',
            )
        this.$router.push(`/documentations/${documentation.uuid}`)
      })
    },
    destroy() {
      return this.runAction(async () => {
        await this.store.remove(this.path, 'Löschen fehlgeschlagen.')
        this.$router.push(`/subjects/${this.documentation.subject.uuid}`)
      })
    },
  },
}
</script>
