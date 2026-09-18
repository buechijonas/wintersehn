<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <LegalContent v-if="page" :page="page" />
  <div v-else class="flex flex-col overflow-y-auto lg:flex-1">
    <div class="mx-auto w-full max-w-150 px-6">
      <div class="skeleton mt-4 mb-4 h-7 w-48"></div>
      <div
        class="list bg-base-100 rounded-box shadow-none border-wntrs-border border-solid border-1 p-8"
      >
        <div class="flex flex-col gap-3">
          <div class="skeleton h-4 w-full"></div>
          <div class="skeleton h-4 w-full"></div>
          <div class="skeleton h-4 w-3/4"></div>
          <div class="skeleton mt-4 h-4 w-1/3"></div>
          <div class="skeleton h-4 w-full"></div>
          <div class="skeleton h-4 w-5/6"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import LegalContent from '@/components/legal/LegalContent.vue'
import { useContentStore } from '@/stores/content.js'

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
