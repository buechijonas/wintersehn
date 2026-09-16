<template>
  <BasePage active-navigation="admin">
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto">
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
    <BaseFooter />
  </BasePage>
</template>

<script>
import BasePage from '@/components/layout/BasePage.vue'
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import { flats } from '@/assets/images.js'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'AdminCvView',
  components: { BasePage, BaseBreadcrumbs, BaseCard, BaseFooter },
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
