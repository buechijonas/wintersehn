<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col gap-4 pb-12 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <CardGridSkeleton v-if="loading" />
    <CardCategory
      v-for="category in countryCategories"
      :key="category.title"
      :title="category.title"
      :items="category.items"
    />
  </div>
  <BaseFooter />
</template>

<script>
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import CardCategory from '@/components/common/CardCategory.vue'
import CardGridSkeleton from '@/components/common/CardGridSkeleton.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'CountriesView',
  components: { BaseBreadcrumbs, CardCategory, CardGridSkeleton, BaseFooter },
  data() {
    return {
      breadcrumbs: [{ label: 'Länder', to: '/' }],
    }
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
    loading() {
      return !this.contentStore.items.countries
    },
    countryCategories() {
      const sections = this.contentStore.items.countries?.data ?? []
      return sections.map((section, sectionIndex) => ({
        ...section,
        items: section.items.map((item, itemIndex) => ({
          ...item,
          to: `/countries/${sectionIndex}/${itemIndex}`,
        })),
      }))
    },
  },
  mounted() {
    this.contentStore.fetchContent('countries')
  },
}
</script>
