<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <article class="mx-auto flex w-full max-w-200 flex-1 flex-col gap-12 px-6 pt-4 pb-16">
    <template v-if="post">
      <header class="flex flex-col gap-4">
        <h1 class="font-display text-5xl font-bold tracking-tighter text-wntrs-title">
          {{ post.title }}
        </h1>
        <p
          v-if="post.description"
          class="max-w-150 text-lg text-wntrs-slate"
          v-html="linkifyHtml(post.description)"
        ></p>
        <div class="flex items-center gap-3">
          <img class="size-10" :src="authorAvatarSrc" alt="" />
          <div>
            <p>{{ post.author }}</p>
            <p v-if="post.publishedAt" class="text-xs text-wntrs-muted">
              {{ publishedAtLabel }}
            </p>
          </div>
        </div>
      </header>

      <img
        v-if="post.thumbnail"
        :src="post.thumbnail"
        alt=""
        class="max-h-96 w-full rounded-box object-cover"
      />

      <section
        v-for="(section, index) in post.sections"
        :key="section.title ?? index"
        class="flex max-w-150 flex-col gap-4"
      >
        <h2 v-if="section.title" class="text-xl">{{ section.title }}</h2>
        <p v-if="section.subtitle" class="text-wntrs-slate">{{ section.subtitle }}</p>
        <p v-if="section.text" class="text-wntrs-muted" v-html="linkifyHtml(section.text)"></p>
      </section>
    </template>

    <div v-else class="flex flex-col gap-4">
      <div class="skeleton h-12 w-3/4"></div>
      <div class="skeleton h-4 w-full"></div>
      <div class="skeleton h-4 w-full"></div>
      <div class="skeleton h-64 w-full"></div>
    </div>
  </article>
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import { profiles } from '@core/assets/images.js'
import { icons } from '@core/assets/icons.js'
import { useContentStore } from '@core/stores/content.js'
import { linkifyHtml } from '@core/lib/linkify.js'

export default {
  name: 'ArticlePostView',
  components: { BaseBreadcrumbs },
  computed: {
    contentStore() {
      return useContentStore()
    },
    posts() {
      return this.contentStore.items.article?.data ?? []
    },
    post() {
      return this.posts.find((post) => post.slug === this.$route.params.slug) ?? null
    },
    breadcrumbs() {
      return [{ label: 'Artikel', to: '/article' }, { label: this.post?.title ?? '…' }]
    },
    authorAvatarSrc() {
      return profiles[this.post?.authorAvatar] ?? icons.user
    },
    publishedAtLabel() {
      return new Date(this.post.publishedAt).toLocaleDateString('de-CH', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    },
  },
  mounted() {
    this.contentStore.fetchContent('article')
  },
  methods: {
    linkifyHtml,
  },
}
</script>
