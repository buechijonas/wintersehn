<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-150">
      <template v-if="post">
        <h2 class="text-xl my-4">{{ post.title }}</h2>

        <BaseCard class="p-8">
          <p
            v-if="post.description"
            class="text-wntrs-slate"
            v-html="linkifyHtml(post.description)"
          ></p>

          <img
            v-if="post.thumbnail"
            :src="post.thumbnail"
            alt=""
            class="w-full max-h-80 object-cover mt-4"
          />

          <div class="divider"></div>

          <div class="flex items-center gap-3">
            <img class="size-10" :src="authorAvatarSrc" alt="" />
            <div>
              <p>{{ post.author }}</p>
              <p v-if="post.publishedAt" class="text-wntrs-muted text-xs">
                {{ publishedAtLabel }}
              </p>
            </div>
          </div>

          <div class="divider"></div>

          <LegalSection
            v-for="(section, index) in post.sections"
            :key="section.title ?? index"
            :title="section.title"
            :subtitle="section.subtitle"
          >
            <p v-if="section.text" class="font-light" v-html="linkifyHtml(section.text)"></p>
          </LegalSection>
        </BaseCard>
      </template>

      <div v-else class="flex flex-col gap-3">
        <div class="skeleton h-7 w-48"></div>
        <div class="skeleton h-4 w-full"></div>
        <div class="skeleton h-4 w-full"></div>
        <div class="skeleton h-4 w-3/4"></div>
      </div>
    </div>
  </div>
  <BaseFooter />
</template>

<script>
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import LegalSection from '@/components/legal/LegalSection.vue'
import { profiles } from '@/assets/images.js'
import { icons } from '@/assets/icons.js'
import { useContentStore } from '@/stores/content.js'
import { linkifyHtml } from '@/lib/linkify.js'

export default {
  name: 'ArticlePostView',
  components: { BaseBreadcrumbs, BaseCard, BaseFooter, LegalSection },
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
      return [
        { label: 'Artikel', to: '/article' },
        { label: this.post?.title ?? '…' },
      ]
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
