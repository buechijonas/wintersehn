<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="mx-auto flex w-full max-w-200 flex-1 flex-col gap-12 px-6 pt-4 pb-16">
    <h1 class="font-display text-5xl font-bold tracking-tighter text-wntrs-title">Projekte</h1>
    <CardCategory
      v-for="category in projectCategories"
      :key="category.title"
      :title="category.title"
      :items="category.items"
    />
  </div>
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import CardCategory from '@/components/common/CardCategory.vue'
import { projectCategories } from '@/data/projects.js'

export default {
  name: 'ProjectsView',
  components: { BaseBreadcrumbs, CardCategory },
  data() {
    return {
      breadcrumbs: [{ label: 'Projekte', to: '/' }],
      projectCategories,
    }
  },
}
</script>
