<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col gap-4 pb-12 px-6 flex-1">
    <CardGridSkeleton v-if="loading" />
    <CardCategory
      v-for="category in cvCategories"
      :key="category.title"
      :title="category.title"
      :items="category.items"
    />
  </div>
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import CardCategory from '@/components/common/CardCategory.vue'
import CardGridSkeleton from '@core/components/common/CardGridSkeleton.vue'
import { useContentStore } from '@core/stores/content.js'

export default {
  name: 'CvView',
  components: { BaseBreadcrumbs, CardCategory, CardGridSkeleton },
  data() {
    return {
      breadcrumbs: [{ label: 'Lebenslauf', to: '/' }],
    }
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
    loading() {
      return !this.contentStore.items.cv
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
