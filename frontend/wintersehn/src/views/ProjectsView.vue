<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col gap-4 pb-12 px-6 flex-1">
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
