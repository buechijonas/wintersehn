<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="mx-auto flex w-full max-w-200 flex-1 flex-col gap-12 px-6 pt-4 pb-16">
    <h1 class="font-display text-5xl font-bold tracking-tighter text-wntrs-title">Artikel</h1>

    <div v-if="loading" class="flex flex-col gap-10">
      <div v-for="row in 3" :key="row" class="skeleton h-24 w-full"></div>
    </div>

    <p v-else-if="!posts.length" class="text-wntrs-muted">Noch keine Artikel vorhanden.</p>

    <ul v-else class="flex flex-col gap-10">
      <li v-for="post in posts" :key="post.slug">
        <RouterLink :to="`/article/${post.slug}`" class="group flex items-start gap-6">
          <img
            v-if="post.thumbnail"
            v-bind="squareImage(post.thumbnail, 64)"
            alt=""
            class="size-16 shrink-0 rounded-box object-cover"
          />
          <div class="flex min-w-0 flex-col gap-2">
            <h2 class="text-xl group-hover:text-primary">{{ post.title }}</h2>
            <p class="line-clamp-3 max-w-150 text-wntrs-muted">{{ post.description }}</p>
          </div>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import { useContentStore } from '@core/stores/content.js'
import { squareImage } from '@core/lib/image.js'

export default {
  name: 'ArticleView',
  components: { RouterLink, BaseBreadcrumbs },
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
  methods: {
    squareImage,
  },
}
</script>
