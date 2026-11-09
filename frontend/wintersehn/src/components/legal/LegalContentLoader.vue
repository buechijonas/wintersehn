<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <LegalContent v-if="page" :page="page" />
  <div v-else class="mx-auto flex w-full max-w-200 flex-1 flex-col gap-12 px-6 pt-4 pb-16">
    <div class="skeleton h-12 w-64"></div>
    <div class="flex max-w-150 flex-col gap-3">
      <div class="skeleton h-6 w-48"></div>
      <div class="skeleton h-4 w-full"></div>
      <div class="skeleton h-4 w-full"></div>
      <div class="skeleton h-4 w-3/4"></div>
    </div>
  </div>
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import LegalContent from '@/components/legal/LegalContent.vue'
import { useContentStore } from '@core/stores/content.js'

export default {
  name: 'LegalContentLoader',
  components: { BaseBreadcrumbs, LegalContent },
  props: {
    contentKey: { type: String, required: true },
    label: { type: String, required: true },
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
    breadcrumbs() {
      return [{ label: this.label, to: '/' }]
    },
    page() {
      return this.contentStore.items[this.contentKey]?.data
    },
  },
  mounted() {
    this.contentStore.fetchContent(this.contentKey)
  },
}
</script>
