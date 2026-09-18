<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col gap-4 pb-12 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <CardGridSkeleton v-if="loading" />
    <CardCategory
      v-for="category in ethosCategories"
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
  name: 'EthosView',
  components: { BaseBreadcrumbs, CardCategory, CardGridSkeleton, BaseFooter },
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
