<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 flex-1">
    <div class="mx-auto w-full max-w-200">
      <h2 class="text-xl my-4">Lebenslauf</h2>

      <div class="flex flex-wrap gap-2">
        <BaseCard
          v-for="section in sections"
          :key="section.key"
          tag="router-link"
          :to="`/admin/cv/${section.key}`"
          class="size-40 flex items-center justify-center p-4 hover:bg-base-200"
        >
          <div class="flex flex-col items-center text-center gap-4">
            <img class="size-16" :src="flatIcons[section.icon]" :alt="section.label" />
            <p class="text-wntrs-slate text-sm">{{ section.label }}</p>
          </div>
        </BaseCard>
      </div>
    </div>
  </div>
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import { flats } from '@core/assets/images.js'
import { useContentStore } from '@core/stores/content.js'

export default {
  name: 'AdminCvView',
  components: { BaseBreadcrumbs, BaseCard },
  data() {
    return {
      breadcrumbs: [
        { label: 'Admin', to: '/admin' },
        { label: 'Lebenslauf' },
      ],
    }
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
    flatIcons() {
      return flats
    },
    categories() {
      return this.contentStore.items.cv?.data ?? []
    },
    sections() {
      return this.categories.flatMap((category) => category.items)
    },
  },
  mounted() {
    this.contentStore.fetchContent('cv')
  },
}
</script>
