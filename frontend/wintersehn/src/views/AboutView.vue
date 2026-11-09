<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="mx-auto flex w-full max-w-200 flex-1 flex-col gap-12 px-6 pt-4 pb-16">
    <h1 class="font-display text-5xl font-bold tracking-tighter text-wntrs-title">Über mich</h1>
    <div v-if="loading" class="flex max-w-150 flex-col gap-4">
      <div v-for="row in 5" :key="row" class="skeleton h-6 w-full"></div>
    </div>
    <dl v-else class="grid max-w-150 grid-cols-[auto_1fr] gap-x-8 gap-y-4">
      <template v-for="row in aboutRows" :key="row.label">
        <dt class="text-wntrs-muted">{{ row.label }}</dt>
        <dd class="flex items-center gap-2">
          <img v-if="row.icon" class="size-5" :src="countries[row.icon]" alt="" />
          {{ row.value }}
        </dd>
      </template>
    </dl>
  </div>
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import { countries } from '@core/assets/images.js'
import { useContentStore } from '@core/stores/content.js'

export default {
  name: 'AboutView',
  components: { BaseBreadcrumbs },
  data() {
    return {
      countries,
      breadcrumbs: [{ label: 'Über mich', to: '/' }],
    }
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
    loading() {
      return !this.contentStore.items.about
    },
    aboutRows() {
      return this.contentStore.items.about?.data ?? []
    },
  },
  mounted() {
    this.contentStore.fetchContent('about')
  },
}
</script>
