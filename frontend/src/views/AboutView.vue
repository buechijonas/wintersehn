<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-12 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-150">
      <h2 class="text-xl my-4">Über mich</h2>
      <div v-if="loading" class="flex flex-col gap-3">
        <div v-for="row in 5" :key="row" class="skeleton h-10 w-full"></div>
      </div>
      <BaseCard v-else class="overflow-x-auto">
        <table class="table">
          <tbody>
            <tr v-for="row in aboutRows" :key="row.label">
              <td class="text-wntrs-muted font-medium">{{ row.label }}</td>
              <td>
                <span class="flex items-center gap-2">
                  <img v-if="row.icon" class="size-5" :src="countries[row.icon]" alt="" />
                  {{ row.value }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </BaseCard>
    </div>
  </div>
  <BaseFooter />
</template>

<script>
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import { countries } from '@/assets/images.js'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'AboutView',
  components: { BaseBreadcrumbs, BaseCard, BaseFooter },
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
