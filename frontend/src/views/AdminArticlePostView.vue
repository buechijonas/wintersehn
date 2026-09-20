<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-200">
      <h2 class="text-xl my-4">{{ post?.title ?? '…' }}</h2>

      <p v-if="error" class="text-error text-sm mb-4">{{ error }}</p>

      <template v-if="post">
        <BaseCard class="p-6 mb-4">
          <div class="flex flex-col gap-2 mb-4">
            <input
              type="text"
              placeholder="Titel"
              class="input w-full"
              :value="post.title"
              :disabled="!canEdit"
              @change="updatePost('title', $event.target.value)"
            />
            <textarea
              rows="2"
              placeholder="Beschreibung"
              class="textarea w-full"
              :value="post.description"
              :disabled="!canEdit"
              @change="updatePost('description', $event.target.value)"
            ></textarea>
          </div>

          <img
            v-if="post.thumbnail"
            :src="post.thumbnail"
            alt=""
            class="size-24 rounded-box object-cover mb-2"
          />
          <ImageUploadField
            v-if="canEdit"
            label="Thumbnail ändern"
            @uploaded="onThumbnailUploaded"
          />
        </BaseCard>

        <SortableList
          :items="sections"
          :disabled="!canEdit"
          class="flex flex-col gap-4"
          @reorder="reorderSections"
        >
          <template #default="{ item: section, index: sectionIndex }">
            <BaseCard class="p-6">
              <div v-if="canEdit" class="flex items-center justify-between gap-2 mb-4">
                <div class="flex items-center gap-2">
                  <BaseButton
                    type="button"
                    shape="square"
                    size="sm"
                    title="Verlinken"
                    @click="addLink(sectionIndex)"
                  >
                    <AppIcon name="link-alt" class="size-4" alt="Verlinken" />
                  </BaseButton>
                  <BaseButton
                    type="button"
                    shape="square"
                    size="sm"
                    title="Entlinken"
                    @click="removeLink(sectionIndex)"
                  >
                    <AppIcon name="link-slash-alt" class="size-4" alt="Entlinken" />
                  </BaseButton>
                </div>
                <DeleteButton
                  shape="square"
                  :disabled="saving"
                  @click="askRemoveSection(sectionIndex)"
                />
              </div>

              <div class="flex flex-col gap-2 w-full max-w-120 mb-4">
                <input
                  type="text"
                  placeholder="Titel (optional)"
                  class="input input-sm w-full"
                  :value="section.title"
                  :disabled="!canEdit"
                  @change="updateSection(sectionIndex, 'title', $event.target.value)"
                />
                <input
                  type="text"
                  placeholder="Untertitel (optional)"
                  class="input input-sm w-full"
                  :value="section.subtitle"
                  :disabled="!canEdit"
                  @change="updateSection(sectionIndex, 'subtitle', $event.target.value)"
                />
              </div>
              <textarea
                :ref="(el) => setSectionTextarea(sectionIndex, el)"
                rows="4"
                placeholder="Text (optional)"
                class="textarea textarea-sm w-full"
                :value="section.text"
                :disabled="!canEdit"
                @change="updateSection(sectionIndex, 'text', $event.target.value)"
              ></textarea>
            </BaseCard>
          </template>
        </SortableList>

        <div v-if="canEdit" class="flex gap-4 mt-6">
          <input
            v-model="newSectionTitle"
            type="text"
            placeholder="Neuer Abschnitt"
            class="input flex-1"
            @keyup.enter="addSection"
          />
          <BaseButton variant="primary" @click="addSection">Abschnitt hinzufügen</BaseButton>
        </div>
      </template>
    </div>
  </div>

  <ConfirmDialog
    ref="confirmDialog"
    :title="dialogTitle"
    :message="dialogMessage"
    @confirm="onConfirmDelete"
  />

  <LinkDialog ref="linkDialog" @confirm="onLinkConfirm" />

  <BaseFooter />
</template>

<script>
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import AppIcon from '@/components/common/AppIcon.vue'
import DeleteButton from '@/components/common/DeleteButton.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import LinkDialog from '@/components/common/LinkDialog.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import SortableList from '@/components/common/SortableList.vue'
import ImageUploadField from '@/components/common/ImageUploadField.vue'
import { useAuthStore } from '@/stores/auth.js'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'AdminArticlePostView',
  components: {
    BaseBreadcrumbs,
    BaseCard,
    BaseButton,
    AppIcon,
    DeleteButton,
    ConfirmDialog,
    LinkDialog,
    BaseFooter,
    SortableList,
    ImageUploadField,
  },
  data() {
    return {
      error: '',
      saving: false,
      newSectionTitle: '',
      dialogTitle: '',
      dialogMessage: '',
      pendingAction: null,
      sectionTextareas: {},
      linkDialogSectionIndex: null,
      linkDialogSelection: null,
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    contentStore() {
      return useContentStore()
    },
    posts() {
      return this.contentStore.items.article?.data ?? []
    },
    postIndex() {
      return this.posts.findIndex((post) => post.slug === this.$route.params.slug)
    },
    post() {
      return this.postIndex === -1 ? null : this.posts[this.postIndex]
    },
    sections() {
      return this.post?.sections ?? []
    },
    canEdit() {
      return !!this.authStore.user?.can_edit_content
    },
    breadcrumbs() {
      return [
        { label: 'Admin', to: '/admin' },
        { label: 'Artikeln', to: '/admin/article' },
        { label: this.post?.title ?? '…' },
      ]
    },
  },
  mounted() {
    this.contentStore.fetchContent('article')
  },
  methods: {
    async persist(posts) {
      this.error = ''
      this.saving = true
      try {
        await this.contentStore.saveContent('article', posts)
      } catch (e) {
        this.error = e.message
      } finally {
        this.saving = false
      }
    },
    persistPost(patch) {
      return this.persist(
        this.posts.map((post, i) => (i === this.postIndex ? { ...post, ...patch } : post)),
      )
    },
    updatePost(field, value) {
      const trimmed = value.trim()
      if (trimmed === (this.post[field] ?? '')) return
      this.persistPost({ [field]: trimmed })
    },
    onThumbnailUploaded(urls) {
      this.persistPost({ thumbnail: urls[0] })
    },
    persistSections(sections) {
      return this.persistPost({ sections })
    },
    addSection() {
      const title = this.newSectionTitle.trim()
      if (!title) return
      this.newSectionTitle = ''
      this.persistSections([...this.sections, { title, subtitle: '', text: '' }])
    },
    updateSection(sectionIndex, field, value) {
      const trimmed = value.trim()
      if (trimmed === (this.sections[sectionIndex][field] ?? '')) return
      this.persistSections(
        this.sections.map((section, i) =>
          i === sectionIndex ? { ...section, [field]: trimmed } : section,
        ),
      )
    },
    reorderSections(sections) {
      this.persistSections(sections)
    },
    setSectionTextarea(sectionIndex, el) {
      this.sectionTextareas[sectionIndex] = el
    },
    addLink(sectionIndex) {
      const textarea = this.sectionTextareas[sectionIndex]
      if (!textarea) return

      const { selectionStart, selectionEnd, value } = textarea
      const selected = value.slice(selectionStart, selectionEnd)
      if (!selected) {
        this.error = 'Bitte zuerst den zu verlinkenden Text markieren.'
        return
      }

      this.error = ''
      this.linkDialogSectionIndex = sectionIndex
      this.linkDialogSelection = { start: selectionStart, end: selectionEnd, selected }
      this.$refs.linkDialog?.open()
    },
    onLinkConfirm(input) {
      const sectionIndex = this.linkDialogSectionIndex
      const { start, end, selected } = this.linkDialogSelection ?? {}
      if (sectionIndex === null || !this.sectionTextareas[sectionIndex]) return

      const url = /^https?:\/\//.test(input) ? input : `https://${input}`
      const value = this.sectionTextareas[sectionIndex].value
      const newValue = value.slice(0, start) + `[${selected}](${url})` + value.slice(end)
      this.updateSection(sectionIndex, 'text', newValue)
    },
    removeLink(sectionIndex) {
      const textarea = this.sectionTextareas[sectionIndex]
      if (!textarea) return

      const { selectionStart, selectionEnd, value } = textarea
      const pattern = /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g
      let match
      while ((match = pattern.exec(value))) {
        const start = match.index
        const end = start + match[0].length
        if (selectionStart >= start && selectionEnd <= end) {
          this.error = ''
          this.updateSection(sectionIndex, 'text', value.slice(0, start) + match[1] + value.slice(end))
          return
        }
      }
      this.error = 'Bitte einen bestehenden Link markieren oder den Cursor hineinsetzen.'
    },
    confirmRemoval(title, message, action) {
      this.dialogTitle = title
      this.dialogMessage = message
      this.pendingAction = action
      this.$refs.confirmDialog?.open()
    },
    askRemoveSection(sectionIndex) {
      const { title } = this.sections[sectionIndex]
      this.confirmRemoval(
        'Abschnitt löschen',
        `Möchtest du "${title || 'diesen Abschnitt'}" wirklich löschen?`,
        () => this.persistSections(this.sections.filter((_, i) => i !== sectionIndex)),
      )
    },
    onConfirmDelete() {
      this.pendingAction?.()
    },
  },
}
</script>
