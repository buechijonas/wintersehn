<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="mx-auto flex w-full max-w-200 flex-1 flex-col gap-12 px-6 pt-4 pb-16">
    <h1 class="font-display text-5xl font-bold tracking-tighter text-wntrs-title">Ethos</h1>
    <CardGridSkeleton v-if="loading" />
    <CardCategory
      v-for="category in ethosCategories"
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
  name: 'EthosView',
  components: { BaseBreadcrumbs, CardCategory, CardGridSkeleton },
  data() {
    return {
      breadcrumbs: [{ label: 'Ethos', to: '/' }],
    }
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
    loading() {
      return !this.contentStore.items.ethos
    },
    ethosCategories() {
      return this.contentStore.items.ethos?.data ?? []
    },
  },
  mounted() {
    this.contentStore.fetchContent('ethos')
  },
}
</script>
