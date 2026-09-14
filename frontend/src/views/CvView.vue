<template>
  <BasePage active-navigation="cv">
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col gap-4 mt-12 px-6">
      <CardCategory
        v-for="category in cvCategories"
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
  name: 'CvView',
  components: { BasePage, BaseBreadcrumbs, CardCategory, BaseFooter },
  data() {
    return {
      breadcrumbs: [{ label: 'Lebenslauf', to: '/' }],
    }
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
    cvCategories() {
      return this.contentStore.items.cv?.data ?? []
    },
  },
  mounted() {
    this.contentStore.fetchContent('cv')
  },
}
</script>
