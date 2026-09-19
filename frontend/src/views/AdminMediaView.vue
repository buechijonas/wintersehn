<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-200">
      <h2 class="text-xl my-4">Medien</h2>

      <p v-if="error" class="text-error text-sm mb-4">{{ error }}</p>

      <SortableList
        :items="sections"
        :disabled="!canEdit"
        class="flex flex-col gap-4"
        @reorder="reorderSections"
      >
        <template #default="{ item: section, index: sectionIndex }">
          <BaseCard class="p-6">
            <div class="flex items-center justify-between gap-4 mb-4">
              <input
                type="text"
                class="input input-sm w-full max-w-60"
                :value="section.title"
                :disabled="!canEdit"
                @change="renameSection(sectionIndex, $event)"
              />
              <div v-if="canEdit" class="flex items-center gap-1 shrink-0">
                <BaseButton
                  type="button"
                  variant="neutral"
                  shape="circle"
                  size="sm"
                  :class="{ 'text-success': !section.requiresAuth }"
                  :disabled="saving"
                  :title="
                    section.requiresAuth
                      ? 'Nur für angemeldete Nutzer mit Berechtigung sichtbar – klicken um öffentlich zu machen'
                      : 'Öffentlich sichtbar – klicken um einzuschränken'
                  "
                  @click="toggleRequiresAuth(sectionIndex)"
                >
                  <AppIcon
                    :name="section.requiresAuth ? 'lock' : 'earth-europa'"
                    class="size-4"
                    :class="{ 'icon-success': !section.requiresAuth }"
                    alt="Sichtbarkeit umschalten"
                  />
                </BaseButton>
                <DeleteButton :disabled="saving" @click="askRemoveSection(sectionIndex)">
                  Abschnitt löschen
                </DeleteButton>
              </div>
            </div>

            <SortableList
              :items="section.items"
              :disabled="!canEdit"
              class="flex flex-wrap gap-2"
              @reorder="(items) => reorderItems(sectionIndex, items)"
            >
              <template #default="{ item, index: itemIndex }">
                <div class="relative shrink-0">
                  <BaseCard class="size-40 flex items-center justify-center p-4">
                    <div class="flex flex-col items-center text-center gap-4 w-full">
                      <img class="size-16" :src="mediaIcons[item.icon]" :alt="item.platform" />
                      <p class="text-wntrs-slate text-sm line-clamp-2 text-ellipsis w-full">
                        {{ item.name }}
                      </p>
                    </div>
                  </BaseCard>
                  <DeleteButton
                    v-if="canEdit"
                    class="absolute top-2 right-2"
                    :disabled="saving"
                    @click="askRemoveItem(sectionIndex, itemIndex)"
                  />
                </div>
              </template>

              <template #append>
                <BaseCard
                  v-if="canEdit"
                  tag="router-link"
                  :to="`/admin/media/${sectionIndex}/create`"
                  class="size-40 shrink-0 flex items-center justify-center p-4 hover:bg-base-200"
                >
                  <span class="text-4xl text-wntrs-muted leading-none">+</span>
                </BaseCard>
              </template>
            </SortableList>
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
</template>

<script>
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import DeleteButton from '@/components/common/DeleteButton.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import SortableList from '@/components/common/SortableList.vue'
import AppIcon from '@/components/common/AppIcon.vue'
import { social } from '@/assets/images.js'
import { useAuthStore } from '@/stores/auth.js'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'AdminMediaView',
  components: {
    BaseBreadcrumbs,
    BaseCard,
    BaseButton,
    DeleteButton,
    ConfirmDialog,
    BaseFooter,
    SortableList,
    AppIcon,
  },
  data() {
    return {
      breadcrumbs: [
        { label: 'Admin', to: '/admin' },
        { label: 'Medien' },
      ],
      error: '',
      saving: false,
      newSectionTitle: '',
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
    mediaIcons() {
      return social
    },
    sections() {
      return this.contentStore.items.media?.data ?? []
    },
    canEdit() {
      return !!this.authStore.user?.can_edit_content
    },
  },
  mounted() {
    this.contentStore.fetchContent('media')
  },
  methods: {
    async persist(data) {
      this.error = ''
      this.saving = true
      try {
        await this.contentStore.saveContent('media', data)
      } catch (e) {
        this.error = e.message
      } finally {
        this.saving = false
      }
    },
    addSection() {
      const title = this.newSectionTitle.trim()
      if (!title) return
      this.newSectionTitle = ''
      this.persist([...this.sections, { title, items: [] }])
    },
    renameSection(sectionIndex, event) {
      const title = event.target.value.trim()
      event.target.value = title
      if (!title || title === this.sections[sectionIndex].title) return
      this.persist(
        this.sections.map((section, i) => (i === sectionIndex ? { ...section, title } : section)),
      )
    },
    toggleRequiresAuth(sectionIndex) {
      this.persist(
        this.sections.map((section, i) =>
          i === sectionIndex ? { ...section, requiresAuth: !section.requiresAuth } : section,
        ),
      )
    },
    reorderSections(sections) {
      this.persist(sections)
    },
    reorderItems(sectionIndex, items) {
      this.persist(
        this.sections.map((section, i) => (i === sectionIndex ? { ...section, items } : section)),
      )
    },
    confirmRemoval(title, message, action) {
      this.dialogTitle = title
      this.dialogMessage = message
      this.pendingAction = action
      this.$refs.confirmDialog?.open()
    },
    askRemoveSection(sectionIndex) {
      const { title } = this.sections[sectionIndex]
      this.confirmRemoval('Abschnitt löschen', `Möchtest du "${title}" wirklich löschen?`, () =>
        this.persist(this.sections.filter((_, i) => i !== sectionIndex)),
      )
    },
    askRemoveItem(sectionIndex, itemIndex) {
      const { name } = this.sections[sectionIndex].items[itemIndex]
      this.confirmRemoval('Eintrag löschen', `Möchtest du "${name}" wirklich löschen?`, () =>
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

<style scoped>
.icon-success {
  filter: brightness(0) saturate(100%) invert(64%) sepia(29%) saturate(500%) hue-rotate(80deg)
    brightness(92%) contrast(86%);
}
</style>
