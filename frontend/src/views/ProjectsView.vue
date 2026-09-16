<template>
  <BasePage active-navigation="projects">
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div class="flex h-[calc(100dvh-192px)] px-6">
      <div class="flex flex-col mx-auto my-32">
        <h1 class="text-title my-8 text-center font-light">Projekte</h1>
        <p class="subtitle mx-auto text-wntrs-muted font-light">Inhalt folgt in Kürze.</p>
      </div>
    </div>
    <BaseFooter />
  </BasePage>
</template>

<script>
import BasePage from '@/components/layout/BasePage.vue'
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'

export default {
  name: 'ProjectsView',
  components: { BasePage, BaseBreadcrumbs, BaseFooter },
  data() {
    return {
      breadcrumbs: [{ label: 'Projekte', to: '/' }],
    }
  },
}
</script>
