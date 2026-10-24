<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col gap-4 pb-12 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <CardCategory
      v-for="category in projectCategories"
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
import BaseFooter from '@core/components/common/BaseFooter.vue'
import { projectCategories } from '@/data/projects.js'

export default {
  name: 'ProjectsView',
  components: { BaseBreadcrumbs, CardCategory, BaseFooter },
  data() {
    return {
      breadcrumbs: [{ label: 'Projekte', to: '/' }],
      projectCategories,
    }
  },
}
</script>
