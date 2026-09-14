<template>
  <BasePage active-navigation="countries">
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col gap-4 pt-12 pb-12 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto">
      <CardCategory
        v-for="category in countryCategories"
        :key="category.title"
        :title="category.title"
        :items="category.items"
      />
    </div>
    <BaseFooter />
  </BasePage>
</template>

<script>
import BasePage from '@/components/layout/BasePage.vue'
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import CardCategory from '@/components/common/CardCategory.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'CountriesView',
  components: { BasePage, BaseBreadcrumbs, CardCategory, BaseFooter },
  data() {
    return {
      breadcrumbs: [{ label: 'Länder', to: '/' }],
    }
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
    countryCategories() {
      return this.contentStore.items.countries?.data ?? []
    },
  },
  mounted() {
    this.contentStore.fetchContent('countries')
  },
}
</script>
