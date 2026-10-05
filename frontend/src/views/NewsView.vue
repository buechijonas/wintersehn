<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div
    class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1"
  >
    <div class="mx-auto w-full max-w-150">
      <h2 class="text-xl font-light mt-4 mb-1">Medien</h2>
      <p class="text-wntrs-muted text-sm">
        Die Medien, denen ich vertraue und die ich regelmässig konsumiere.
      </p>

      <div v-if="loading" class="mt-4 flex flex-col gap-4">
        <div v-for="row in 2" :key="row" class="flex flex-col gap-2">
          <div class="skeleton h-4 w-24"></div>
          <div v-for="item in 3" :key="item" class="skeleton h-14 w-full"></div>
        </div>
      </div>
      <BaseCard v-for="group in groups" :key="group.title" tag="ul" class="list mt-4">
        <li class="p-4 pb-2 text-xs opacity-60 tracking-wide">{{ group.title }}</li>
        <li v-for="item in group.items" :key="item.url" class="list-row">
          <div class="list-col-grow min-w-0">
            <div>{{ item.name }}</div>
            <div class="text-wntrs-muted text-sm">
              <span class="font-medium">{{ item.category }}:</span> {{ item.description }}
            </div>
          </div>
          <BaseButton variant="ghost" shape="square" :href="item.url">
            <AppIcon name="share-square" alt="open" />
          </BaseButton>
        </li>
      </BaseCard>
    </div>
  </div>
  <BaseFooter />
</template>

<script>
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import AppIcon from '@/components/common/AppIcon.vue'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'NewsView',
  components: { BaseBreadcrumbs, BaseCard, BaseFooter, BaseButton, AppIcon },
  data() {
    return {
      breadcrumbs: [{ label: 'Medien', to: '/' }],
    }
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
    loading() {
      return !this.contentStore.items.news
    },
    groups() {
      return this.contentStore.items.news?.data ?? []
    },
  },
  mounted() {
    this.contentStore.fetchContent('news')
  },
}
</script>
