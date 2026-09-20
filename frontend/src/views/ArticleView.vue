<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-150">
      <h2 class="text-xl font-light my-4">Artikel</h2>

      <div v-if="loading" class="flex flex-col gap-3">
        <div v-for="row in 3" :key="row" class="skeleton h-20 w-full"></div>
      </div>

      <p v-else-if="!posts.length" class="text-wntrs-muted">Noch keine Artikel vorhanden.</p>

      <BaseCard v-else tag="ul" class="divide-y divide-wntrs-border">
        <li v-for="post in posts" :key="post.slug">
          <RouterLink :to="`/article/${post.slug}`" class="flex items-center gap-4 p-4 hover:bg-base-200">
            <img
              v-if="post.thumbnail"
              :src="post.thumbnail"
              alt=""
              class="size-16 rounded-box object-cover shrink-0"
            />
            <div class="min-w-0">
              <p class="font-medium truncate">{{ post.title }}</p>
              <p class="text-wntrs-muted text-sm line-clamp-2">{{ post.description }}</p>
            </div>
          </RouterLink>
        </li>
      </BaseCard>
    </div>
  </div>
  <BaseFooter />
</template>

<script>
import { RouterLink } from 'vue-router'
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'ArticleView',
  components: { RouterLink, BaseBreadcrumbs, BaseCard, BaseFooter },
  data() {
    return {
      breadcrumbs: [{ label: 'Artikel', to: '/' }],
    }
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
    loading() {
      return !this.contentStore.items.article
    },
    posts() {
      return this.contentStore.items.article?.data ?? []
    },
  },
  mounted() {
    this.contentStore.fetchContent('article')
  },
}
</script>
