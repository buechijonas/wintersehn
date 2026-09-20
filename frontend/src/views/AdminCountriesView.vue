<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-200">
      <h2 class="text-xl my-4">Länder</h2>

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
                  <BaseCard
                    tag="router-link"
                    :to="`/admin/countries/${sectionIndex}/${itemIndex}/albums`"
                    class="size-40 flex items-center justify-center p-4 hover:bg-base-200"
                  >
                    <div class="flex flex-col items-center text-center gap-4 w-full">
                      <img class="size-16" :src="countryIcons[item.icon]" :alt="item.label" />
                      <p class="text-wntrs-slate text-sm line-clamp-2 text-ellipsis w-full">
                        {{ item.label }}
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
                  :to="`/admin/countries/${sectionIndex}/create`"
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
import { countries } from '@/assets/images.js'
import { useAuthStore } from '@/stores/auth.js'
import { useContentStore } from '@/stores/content.js'
import confirmDeleteMixin from '@/mixins/confirmDeleteMixin.js'
import asyncActionMixin from '@/mixins/asyncActionMixin.js'

export default {
  name: 'AdminCountriesView',
  components: {
    BaseBreadcrumbs,
    BaseCard,
    BaseButton,
    DeleteButton,
    ConfirmDialog,
    BaseFooter,
    SortableList,
  },
  mixins: [confirmDeleteMixin, asyncActionMixin],
  data() {
    return {
      breadcrumbs: [
        { label: 'Admin', to: '/admin' },
        { label: 'Länder' },
      ],
      newSectionTitle: '',
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
      return !!this.authStore.user?.can_change_countries
    },
  },
  mounted() {
    this.contentStore.fetchContent('countries')
  },
  methods: {
    persist(data) {
      return this.runAction(() => this.contentStore.saveContent('countries', data))
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
    reorderSections(sections) {
      this.persist(sections)
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
  },
}
</script>
