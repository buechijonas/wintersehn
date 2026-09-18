<template>
  <BasePage active-navigation="admin">
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
      <div class="mx-auto w-full max-w-200">
        <h2 class="text-xl my-4">Länder</h2>

        <p v-if="error" class="text-error text-sm mb-4">{{ error }}</p>

        <div class="flex flex-col gap-4">
          <BaseCard v-for="(section, sectionIndex) in sections" :key="sectionIndex" class="p-6">
            <div class="flex items-center justify-between gap-4 mb-4">
              <input
                type="text"
                class="input input-sm w-full max-w-60"
                :value="section.title"
                :disabled="!canEdit"
                @change="renameSection(sectionIndex, $event)"
              />
              <DeleteButton
                v-if="canEdit"
                class="shrink-0"
                :disabled="saving"
                @click="askRemoveSection(sectionIndex)"
              >
                Abschnitt löschen
              </DeleteButton>
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
                    <div class="flex flex-col items-center text-center gap-4">
                      <img class="size-16" :src="countryIcons[item.icon]" :alt="item.label" />
                      <p class="text-wntrs-slate text-sm">{{ item.label }}</p>
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
                  :to="`/admin/countries/${sectionIndex}/create`"
                  class="size-40 shrink-0 flex items-center justify-center p-4 hover:bg-base-200"
                >
                  <span class="text-4xl text-wntrs-muted leading-none">+</span>
                </BaseCard>
              </template>
            </SortableList>
          </BaseCard>
        </div>

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
import { countries } from '@/assets/images.js'
import { useAuthStore } from '@/stores/auth.js'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'AdminCountriesView',
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
  data() {
    return {
      breadcrumbs: [
        { label: 'Admin', to: '/admin' },
        { label: 'Länder' },
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
    countryIcons() {
      return countries
    },
    sections() {
      return this.contentStore.items.countries?.data ?? []
    },
    canEdit() {
      return !!this.authStore.user?.can_edit_content
    },
  },
  mounted() {
    this.contentStore.fetchContent('countries')
  },
  methods: {
    async persist(data) {
      this.error = ''
      this.saving = true
      try {
        await this.contentStore.saveContent('countries', data)
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
    confirmRemoval(title, message, action) {
      this.dialogTitle = title
      this.dialogMessage = message
      this.pendingAction = action
      this.$refs.confirmDialog?.open()
    },
    reorderItems(sectionIndex, items) {
      this.persist(
        this.sections.map((section, i) => (i === sectionIndex ? { ...section, items } : section)),
      )
    },
    askRemoveSection(sectionIndex) {
      const { title } = this.sections[sectionIndex]
      this.confirmRemoval('Abschnitt löschen', `Möchtest du "${title}" wirklich löschen?`, () =>
        this.persist(this.sections.filter((_, i) => i !== sectionIndex)),
      )
    },
    askRemoveItem(sectionIndex, itemIndex) {
      const { label } = this.sections[sectionIndex].items[itemIndex]
      this.confirmRemoval('Eintrag löschen', `Möchtest du "${label}" wirklich löschen?`, () =>
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
