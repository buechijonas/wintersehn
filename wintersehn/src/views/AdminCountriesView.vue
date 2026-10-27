<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-200">
      <div class="flex items-center justify-between gap-4 my-4">
        <h2 class="text-xl">Länder</h2>
        <AddButton
          v-if="canEdit"
          label="Abschnitt hinzufügen"
          @click="$refs.sectionDialog.open()"
        />
      </div>

      <p v-if="error" class="text-error text-sm mb-4">{{ error }}</p>

      <BaseCard class="p-6 mb-4">
        <h3 class="mb-4">Nächstes Ziel</h3>
        <form class="flex flex-wrap items-center gap-4" @submit.prevent="saveDestination">
          <select
            v-model="destinationIcon"
            class="select select-sm w-full max-w-60"
            :disabled="!canEdit"
            aria-label="Land"
          >
            <option value="">Kein Ziel</option>
            <option v-for="country in countryOptions" :key="country.icon" :value="country.icon">
              {{ country.label }}
            </option>
          </select>
          <input
            v-model="destinationDate"
            type="date"
            class="input input-sm w-full max-w-44"
            :disabled="!canEdit || !destinationIcon"
            aria-label="Reisedatum"
          />
          <SaveButton v-if="canEdit" type="submit" :disabled="saving" />
        </form>
      </BaseCard>

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
              />
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
    </div>
  </div>

  <ConfirmDialog
    ref="confirmDialog"
    :title="dialogTitle"
    :message="dialogMessage"
    @confirm="onConfirmDelete"
  />

  <SectionDialog ref="sectionDialog" @confirm="addSection" />

  <BaseFooter />
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import DeleteButton from '@core/components/common/DeleteButton.vue'
import ConfirmDialog from '@core/components/common/ConfirmDialog.vue'
import BaseFooter from '@core/components/common/BaseFooter.vue'
import AddButton from '@core/components/common/AddButton.vue'
import SectionDialog from '@core/components/common/SectionDialog.vue'
import SortableList from '@core/components/common/SortableList.vue'
import SaveButton from '@core/components/common/SaveButton.vue'
import { countries } from '@core/assets/images.js'
import { useAuthStore } from '@core/stores/auth.js'
import { useContentStore } from '@core/stores/content.js'
import { useCountriesStore } from '@/stores/countries.js'
import confirmDeleteMixin from '@core/mixins/confirmDeleteMixin.js'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'

export default {
  name: 'AdminCountriesView',
  components: {
    BaseBreadcrumbs,
    BaseCard,
    DeleteButton,
    ConfirmDialog,
    BaseFooter,
    SortableList,
    AddButton,
    SectionDialog,
    SaveButton,
  },
  mixins: [confirmDeleteMixin, asyncActionMixin],
  data() {
    return {
      breadcrumbs: [
        { label: 'Admin', to: '/admin' },
        { label: 'Länder' },
      ],
      destinationIcon: '',
      destinationDate: '',
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    contentStore() {
      return useContentStore()
    },
    countriesStore() {
      return useCountriesStore()
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
    countryOptions() {
      const items = this.sections.flatMap((section) => section.items)
      return [...new Map(items.map((item) => [item.icon, item])).values()]
    },
  },
  async mounted() {
    this.contentStore.fetchContent('countries')
    const { destination } = await this.countriesStore.fetchMap()
    this.destinationIcon = destination?.icon ?? ''
    this.destinationDate = destination?.date ?? ''
  },
  methods: {
    saveDestination() {
      this.runAction(() =>
        this.destinationIcon
          ? this.countriesStore.saveDestination({
              icon: this.destinationIcon,
              date: this.destinationDate || null,
            })
          : this.countriesStore.clearDestination(),
      )
    },
    persist(data) {
      return this.runAction(() => this.contentStore.saveContent('countries', data))
    },
    addSection(title) {
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
