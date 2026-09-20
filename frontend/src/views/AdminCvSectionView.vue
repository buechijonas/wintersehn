<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-200">
      <h2 class="text-xl my-4">{{ section?.label }}</h2>

      <p v-if="error" class="text-error text-sm mb-4">{{ error }}</p>

      <SortableList
        v-if="section"
        :items="timeline"
        :disabled="!canEdit"
        class="flex flex-wrap gap-2"
        @reorder="reorderTimeline"
      >
        <template #default="{ item: entry, index: entryIndex }">
          <div class="relative shrink-0">
            <BaseCard class="size-40 flex items-center justify-center p-4">
              <div class="flex flex-col items-center text-center gap-2">
                <img
                  class="size-14"
                  :src="flatIcons[entry.icon ?? section.icon]"
                  :alt="entry.title"
                />
                <p class="font-mono italic text-wntrs-muted text-xs">{{ entry.year }}</p>
                <div>
                  <p class="text-wntrs-slate text-xs font-bold">{{ entry.title }}</p>
                  <p class="text-wntrs-slate font-light text-xs">{{ entry.description }}</p>
                </div>
              </div>
            </BaseCard>
            <DeleteButton
              v-if="canEdit"
              class="absolute top-2 right-2"
              :disabled="saving"
              @click="askRemoveEntry(entryIndex)"
            />
          </div>
        </template>

        <template #append>
          <BaseCard
            v-if="canEdit"
            tag="router-link"
            :to="`/admin/cv/${key}/create`"
            class="size-40 shrink-0 flex items-center justify-center p-4 hover:bg-base-200"
          >
            <span class="text-4xl text-wntrs-muted leading-none">+</span>
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

  <BaseFooter />
</template>

<script>
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import DeleteButton from '@/components/common/DeleteButton.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import SortableList from '@/components/common/SortableList.vue'
import { flats } from '@/assets/images.js'
import { useAuthStore } from '@/stores/auth.js'
import { useContentStore } from '@/stores/content.js'
import confirmDeleteMixin from '@/mixins/confirmDeleteMixin.js'
import asyncActionMixin from '@/mixins/asyncActionMixin.js'

export default {
  name: 'AdminCvSectionView',
  components: {
    BaseBreadcrumbs,
    BaseCard,
    DeleteButton,
    ConfirmDialog,
    BaseFooter,
    SortableList,
  },
  mixins: [confirmDeleteMixin, asyncActionMixin],
  computed: {
    authStore() {
      return useAuthStore()
    },
    contentStore() {
      return useContentStore()
    },
    flatIcons() {
      return flats
    },
    key() {
      return this.$route.params.key
    },
    categories() {
      return this.contentStore.items.cv?.data ?? []
    },
    location() {
      for (let categoryIndex = 0; categoryIndex < this.categories.length; categoryIndex++) {
        const itemIndex = this.categories[categoryIndex].items.findIndex(
          (item) => item.key === this.key,
        )
        if (itemIndex !== -1) return { categoryIndex, itemIndex }
      }
      return null
    },
    section() {
      if (!this.location) return null
      return this.categories[this.location.categoryIndex].items[this.location.itemIndex]
    },
    timeline() {
      return this.section?.timeline ?? []
    },
    canEdit() {
      return !!this.authStore.user?.can_change_cv
    },
    breadcrumbs() {
      return [
        { label: 'Admin', to: '/admin' },
        { label: 'Lebenslauf', to: '/admin/cv' },
        { label: this.section?.label ?? '…' },
      ]
    },
  },
  mounted() {
    this.contentStore.fetchContent('cv')
  },
  methods: {
    persistTimeline(newTimeline) {
      const { categoryIndex, itemIndex } = this.location
      const categories = this.categories.map((category, ci) =>
        ci !== categoryIndex
          ? category
          : {
              ...category,
              items: category.items.map((item, ii) =>
                ii !== itemIndex ? item : { ...item, timeline: newTimeline },
              ),
            },
      )
      return this.runAction(() => this.contentStore.saveContent('cv', categories))
    },
    reorderTimeline(entries) {
      this.persistTimeline(
        entries.map((entry, i) => ({ ...entry, side: i % 2 === 0 ? 'start' : 'end' })),
      )
    },
    askRemoveEntry(entryIndex) {
      const { title } = this.timeline[entryIndex]
      this.confirmRemoval('Eintrag löschen', `Möchtest du "${title}" wirklich löschen?`, () =>
        this.persistTimeline(this.timeline.filter((_, i) => i !== entryIndex)),
      )
    },
  },
}
</script>
