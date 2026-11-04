<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col gap-4 pb-12 px-6 max-h-[calc(100dvh-101px-var(--footer-height))] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <CardGridSkeleton v-if="loading" />
    <CardCategory
      v-for="category in newsCategories"
      :key="category.title"
      :title="category.title"
      :items="category.items"
    />
  </div>
  <BaseFooter />
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import CardCategory from '@/components/common/CardCategory.vue'
import CardGridSkeleton from '@core/components/common/CardGridSkeleton.vue'
import BaseFooter from '@core/components/common/BaseFooter.vue'
import { useContentStore } from '@core/stores/content.js'

export default {
  name: 'NewsView',
  components: { BaseBreadcrumbs, CardCategory, CardGridSkeleton, BaseFooter },
  data() {
    return {
      breadcrumbs: [{ label: 'Medien', to: '/' }],
    }
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
    loading() {
      return !this.contentStore.items.news
    },
    newsCategories() {
      return this.contentStore.items.news?.data ?? []
    },
  },
  mounted() {
    this.contentStore.fetchContent('news')
  },
}
</script>
