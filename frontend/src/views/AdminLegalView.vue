<template>
  <BasePage active-navigation="admin">
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
      <div class="mx-auto w-full max-w-200">
        <h2 class="text-xl my-4">{{ label }}</h2>

        <p v-if="error" class="text-error text-sm mb-4">{{ error }}</p>

        <SortableList
          :items="sections"
          :disabled="!canEdit"
          class="flex flex-col gap-4"
          @reorder="reorderSections"
        >
          <template #default="{ item: section, index: sectionIndex }">
            <BaseCard class="p-6">
              <button
                v-if="canEdit"
                type="button"
                class="badge badge-sm mb-2"
                :class="section.address ? 'badge-primary' : 'badge-outline'"
                :disabled="saving"
                :title="
                  section.address
                    ? 'Enthält den Adressblock – klicken zum Entfernen'
                    : 'Adressblock zu diesem Abschnitt hinzufügen'
                "
                @click="toggleAddress(sectionIndex)"
              >
                Adressblock
              </button>
              <span v-else-if="section.address" class="badge badge-primary badge-sm mb-2">
                Adressblock
              </span>
              <div class="flex items-start justify-between gap-4 mb-4">
                <div class="flex flex-col gap-2 w-full max-w-120">
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
                <DeleteButton
                  v-if="canEdit"
                  class="shrink-0"
                  :disabled="saving"
                  @click="askRemoveSection(sectionIndex)"
                >
                  Abschnitt löschen
                </DeleteButton>
              </div>

              <textarea
                rows="4"
                placeholder="Text (optional)"
                class="textarea textarea-sm w-full"
                :value="section.text"
                :disabled="!canEdit"
                @change="updateSection(sectionIndex, 'text', $event.target.value)"
              ></textarea>

              <div class="mt-4 flex flex-col gap-2">
                <SortableList
                  :items="section.items ?? []"
                  :disabled="!canEdit"
                  class="flex flex-col gap-2"
                  @reorder="(items) => reorderItems(sectionIndex, items)"
                >
                  <template #default="{ item, index: itemIndex }">
                    <div class="flex items-center gap-2 bg-base-200 rounded-box p-3">
                      <div class="flex-1">
                        <p class="font-medium text-sm">{{ item.listtitle }}</p>
                        <p v-if="item.texttitle" class="text-sm text-wntrs-slate">{{ item.texttitle }}</p>
                      </div>
                      <DeleteButton
                        v-if="canEdit"
                        :disabled="saving"
                        @click="askRemoveItem(sectionIndex, itemIndex)"
                      />
                    </div>
                  </template>
                </SortableList>

                <div v-if="canEdit" class="flex flex-col gap-2 sm:flex-row">
                  <input
                    v-model="itemDrafts[sectionIndex].listtitle"
                    type="text"
                    placeholder="Listentitel"
                    class="input input-sm flex-1"
                  />
                  <input
                    v-model="itemDrafts[sectionIndex].texttitle"
                    type="text"
                    placeholder="Text"
                    class="input input-sm flex-1"
                  />
                  <BaseButton size="sm" @click="addItem(sectionIndex)">Eintrag hinzufügen</BaseButton>
                </div>
              </div>
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
      </div>
    </div>

    <ConfirmDialog
      ref="confirmDialog"
      :title="dialogTitle"
      :message="dialogMessage"
      @confirm="onConfirmDelete"
    />

    <BaseFooter />
  </BasePage>
</template>

<script>
import BasePage from '@/components/layout/BasePage.vue'
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import DeleteButton from '@/components/common/DeleteButton.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import SortableList from '@/components/common/SortableList.vue'
import { useAuthStore } from '@/stores/auth.js'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'AdminLegalView',
  components: {
    BasePage,
    BaseBreadcrumbs,
    BaseCard,
    BaseButton,
    DeleteButton,
    ConfirmDialog,
    BaseFooter,
    SortableList,
  },
  props: {
    contentKey: { type: String, required: true },
    label: { type: String, required: true },
  },
  data() {
    return {
      error: '',
      saving: false,
      newSectionTitle: '',
      itemDrafts: {},
      dialogTitle: '',
      dialogMessage: '',
      pendingAction: null,
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    contentStore() {
      return useContentStore()
    },
    contentData() {
      return this.contentStore.items[this.contentKey]?.data ?? null
    },
    sections() {
      return this.contentData?.sections ?? []
    },
    canEdit() {
      return !!this.authStore.user?.can_edit_content
    },
    breadcrumbs() {
      return [{ label: 'Admin', to: '/admin' }, { label: this.label }]
    },
  },
  watch: {
    contentKey: {
      immediate: true,
      handler() {
        this.contentStore.fetchContent(this.contentKey)
      },
    },
    sections: {
      immediate: true,
      handler(newSections) {
        newSections.forEach((_, index) => {
          if (!this.itemDrafts[index]) {
            this.itemDrafts[index] = { listtitle: '', texttitle: '' }
          }
        })
      },
    },
  },
  methods: {
    async persistData(patch) {
      this.error = ''
      this.saving = true
      try {
        await this.contentStore.saveContent(this.contentKey, { ...this.contentData, ...patch })
      } catch (e) {
        this.error = e.message
      } finally {
        this.saving = false
      }
    },
    persist(sections) {
      return this.persistData({ sections })
    },
    addSection() {
      const title = this.newSectionTitle.trim()
      if (!title) return
      this.newSectionTitle = ''
      this.persist([...this.sections, { title, subtitle: '', text: '', items: [] }])
    },
    updateSection(sectionIndex, field, value) {
      const trimmed = value.trim()
      if (trimmed === (this.sections[sectionIndex][field] ?? '')) return
      this.persist(
        this.sections.map((section, i) =>
          i === sectionIndex ? { ...section, [field]: trimmed } : section,
        ),
      )
    },
    toggleAddress(sectionIndex) {
      this.persist(
        this.sections.map((section, i) =>
          i === sectionIndex ? { ...section, address: !section.address } : section,
        ),
      )
    },
    confirmRemoval(title, message, action) {
      this.dialogTitle = title
      this.dialogMessage = message
      this.pendingAction = action
      this.$refs.confirmDialog?.open()
    },
    reorderSections(sections) {
      this.persist(sections)
    },
    reorderItems(sectionIndex, items) {
      this.persist(
        this.sections.map((section, i) => (i === sectionIndex ? { ...section, items } : section)),
      )
    },
    addItem(sectionIndex) {
      const draft = this.itemDrafts[sectionIndex]
      const listtitle = draft.listtitle.trim()
      const texttitle = draft.texttitle.trim()
      if (!listtitle) return
      const items = [...(this.sections[sectionIndex].items ?? []), { listtitle, texttitle }]
      this.itemDrafts[sectionIndex] = { listtitle: '', texttitle: '' }
      this.persist(
        this.sections.map((section, i) => (i === sectionIndex ? { ...section, items } : section)),
      )
    },
    askRemoveSection(sectionIndex) {
      const { title } = this.sections[sectionIndex]
      this.confirmRemoval(
        'Abschnitt löschen',
        `Möchtest du "${title || 'diesen Abschnitt'}" wirklich löschen?`,
        () => this.persist(this.sections.filter((_, i) => i !== sectionIndex)),
      )
    },
    askRemoveItem(sectionIndex, itemIndex) {
      const { listtitle } = this.sections[sectionIndex].items[itemIndex]
      this.confirmRemoval(
        'Eintrag löschen',
        `Möchtest du "${listtitle}" wirklich löschen?`,
        () =>
          this.persist(
            this.sections.map((section, i) =>
              i === sectionIndex
                ? { ...section, items: section.items.filter((_, j) => j !== itemIndex) }
                : section,
            ),
          ),
      )
    },
    onConfirmDelete() {
      this.pendingAction?.()
    },
  },
}
</script>
