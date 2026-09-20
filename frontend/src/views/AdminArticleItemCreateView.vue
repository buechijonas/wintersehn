<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-150">
      <h2 class="text-xl font-light my-4">Neuer Artikel</h2>

      <BaseCard class="p-6">
        <form class="fieldset" @submit.prevent="save">
          <label class="label" for="article-item-title">Titel</label>
          <input id="article-item-title" v-model="title" type="text" class="input w-full" required />

          <label class="label mt-4" for="article-item-description">Beschreibung</label>
          <textarea
            id="article-item-description"
            v-model="description"
            rows="3"
            class="textarea w-full"
          ></textarea>

          <label class="label mt-4">Thumbnail</label>
          <img v-if="thumbnail" :src="thumbnail" alt="" class="size-24 rounded-box object-cover mb-2" />
          <ImageUploadField label="Thumbnail hochladen" @uploaded="onThumbnailUploaded" />

          <p v-if="error" class="text-error text-sm mt-3">{{ error }}</p>

          <div class="flex gap-4 mt-4">
            <CancelButton to="/admin/article" />
            <BaseButton type="submit" variant="primary" :disabled="saving">Speichern</BaseButton>
          </div>
        </form>
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
import CancelButton from '@/components/common/CancelButton.vue'
import ImageUploadField from '@/components/common/ImageUploadField.vue'
import { useAuthStore } from '@/stores/auth.js'
import { useContentStore } from '@/stores/content.js'
import { uniqueSlug } from '@/lib/slug.js'

export default {
  name: 'AdminArticleItemCreateView',
  components: {
    BaseBreadcrumbs,
    BaseCard,
    BaseFooter,
    BaseButton,
    CancelButton,
    ImageUploadField,
  },
  data() {
    return {
      title: '',
      description: '',
      thumbnail: '',
      error: '',
      saving: false,
      breadcrumbs: [
        { label: 'Admin', to: '/admin' },
        { label: 'Artikeln', to: '/admin/article' },
        { label: 'Neuer Artikel' },
      ],
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    contentStore() {
      return useContentStore()
    },
    posts() {
      return this.contentStore.items.article?.data ?? []
    },
  },
  mounted() {
    this.contentStore.fetchContent('article')
  },
  methods: {
    onThumbnailUploaded(urls) {
      this.thumbnail = urls[0]
    },
    async save() {
      this.error = ''
      if (!this.title.trim()) {
        this.error = 'Titel ist erforderlich.'
        return
      }

      this.saving = true
      try {
        const existingSlugs = new Set(this.posts.map((post) => post.slug))
        const slug = uniqueSlug(this.title.trim(), existingSlugs)
        const post = {
          slug,
          title: this.title.trim(),
          description: this.description.trim(),
          thumbnail: this.thumbnail,
          author: this.authStore.user?.username ?? '',
          authorAvatar: this.authStore.user?.avatar ?? '',
          publishedAt: new Date().toISOString(),
          sections: [],
        }
        await this.contentStore.saveContent('article', [...this.posts, post])
        this.$router.push(`/admin/article/${slug}`)
      } catch (e) {
        this.error = e.message
      } finally {
        this.saving = false
      }
    },
  },
}
</script>
