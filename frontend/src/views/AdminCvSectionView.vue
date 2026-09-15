<template>
  <BasePage active-navigation="admin">
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto">
      <div class="mx-auto w-full max-w-200">
        <h2 class="text-xl my-4">{{ section?.label }}</h2>

        <p v-if="error" class="text-error text-sm mb-4">{{ error }}</p>

        <div v-if="section" class="flex flex-wrap gap-2">
          <div v-for="(entry, entryIndex) in timeline" :key="entryIndex" class="relative shrink-0">
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

          <BaseCard
            v-if="canEdit"
            tag="router-link"
            :to="`/admin/cv/${key}/create`"
            class="size-40 shrink-0 flex items-center justify-center p-4 hover:bg-base-200"
          >
            <span class="text-4xl text-wntrs-muted leading-none">+</span>
          </BaseCard>
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
import DeleteButton from '@/components/common/DeleteButton.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import { flats } from '@/assets/images.js'
import { useAuthStore } from '@/stores/auth.js'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'AdminCvSectionView',
  components: { BasePage, BaseBreadcrumbs, BaseCard, DeleteButton, ConfirmDialog, BaseFooter },
  data() {
    return {
      error: '',
      saving: false,
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
      return !!this.authStore.user?.can_edit_content
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
    async persistTimeline(newTimeline) {
      this.error = ''
      this.saving = true
      try {
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
        await this.contentStore.saveContent('cv', categories)
      } catch (e) {
        this.error = e.message
      } finally {
        this.saving = false
      }
    },
    askRemoveEntry(entryIndex) {
      const { title } = this.timeline[entryIndex]
      this.dialogTitle = 'Eintrag löschen'
      this.dialogMessage = `Möchtest du "${title}" wirklich löschen?`
      this.pendingAction = () =>
        this.persistTimeline(this.timeline.filter((_, i) => i !== entryIndex))
      this.$refs.confirmDialog?.open()
    },
    onConfirmDelete() {
      this.pendingAction?.()
    },
  },
}
</script>
