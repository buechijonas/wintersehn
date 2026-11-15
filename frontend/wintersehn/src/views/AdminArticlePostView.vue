<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 flex-1">
    <div class="mx-auto w-full max-w-200">
      <h2 class="text-xl my-4">{{ post?.title ?? '…' }}</h2>

      <p v-if="error" class="text-error text-sm mb-4">{{ error }}</p>

      <template v-if="post">
        <BaseCard class="p-6 mb-4">
          <div class="flex flex-col gap-2 mb-4">
            <input
              type="text"
              placeholder="Titel"
              class="input w-full"
              :value="post.title"
              :disabled="!canEdit"
              @change="updatePost('title', $event.target.value)"
            />
            <textarea
              rows="2"
              placeholder="Beschreibung"
              class="textarea w-full"
              :value="post.description"
              :disabled="!canEdit"
              @change="updatePost('description', $event.target.value)"
            ></textarea>
          </div>

          <img
            v-if="post.thumbnail"
            :src="post.thumbnail"
            alt=""
            class="size-24 rounded-box object-cover mb-2"
          />
          <ImageUploadField
            v-if="canEdit"
            label="Thumbnail ändern"
            @uploaded="onThumbnailUploaded"
          />
        </BaseCard>

        <form v-if="canEdit" class="flex flex-col gap-4" @submit.prevent="saveBody">
          <MarkdownEditor v-model="body" preview-url="/api/content/markdown/preview/" />
          <BaseButton
            type="submit"
            variant="primary"
            class="self-end"
            :disabled="saving || body === post.body"
          >
            <AppIcon name="disk" />
            Speichern
          </BaseButton>
        </form>
        <BaseCard v-else class="p-6">
          <MarkdownContent :html="html" placeholder="Noch kein Text." />
        </BaseCard>
      </template>
    </div>
  </div>
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import AppIcon from '@core/components/common/AppIcon.vue'
import ImageUploadField from '@core/components/common/ImageUploadField.vue'
import MarkdownContent from '@core/components/common/MarkdownContent.vue'
import MarkdownEditor from '@core/components/common/MarkdownEditor.vue'
import { useAuthStore } from '@core/stores/auth.js'
import { useContentStore } from '@core/stores/content.js'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'

export default {
  name: 'AdminArticlePostView',
  components: {
    BaseBreadcrumbs,
    BaseCard,
    BaseButton,
    AppIcon,
    ImageUploadField,
    MarkdownContent,
    MarkdownEditor,
  },
  mixins: [asyncActionMixin],
  data() {
    return {
      body: '',
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
    postIndex() {
      return this.posts.findIndex((post) => post.slug === this.$route.params.slug)
    },
    post() {
      return this.postIndex === -1 ? null : this.posts[this.postIndex]
    },
    html() {
      return this.contentStore.items.article?.html?.[this.post.slug] ?? ''
    },
    canEdit() {
      return !!this.authStore.user?.can_edit_content
    },
    breadcrumbs() {
      return [
        { label: 'Admin', to: '/admin' },
        { label: 'Artikeln', to: '/admin/article' },
        { label: this.post?.title ?? '…' },
      ]
    },
  },
  watch: {
    'post.body': {
      immediate: true,
      handler(body) {
        this.body = body ?? ''
      },
    },
  },
  mounted() {
    this.contentStore.fetchContent('article')
  },
  methods: {
    persistPost(patch) {
      const posts = this.posts.map((post, i) =>
        i === this.postIndex ? { ...post, ...patch } : post,
      )
      return this.runAction(() => this.contentStore.saveContent('article', posts))
    },
    updatePost(field, value) {
      const trimmed = value.trim()
      if (trimmed === (this.post[field] ?? '')) return
      this.persistPost({ [field]: trimmed })
    },
    onThumbnailUploaded(urls) {
      this.persistPost({ thumbnail: urls[0] })
    },
    saveBody() {
      this.persistPost({ body: this.body })
    },
  },
}
</script>
