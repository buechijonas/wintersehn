<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-200">
      <h2 class="text-xl my-4">Artikeln</h2>

      <p v-if="error" class="text-error text-sm mb-4">{{ error }}</p>

      <SortableList
        :items="posts"
        :disabled="!canEdit"
        class="flex flex-wrap gap-2"
        @reorder="reorderPosts"
      >
        <template #default="{ item: post, index: postIndex }">
          <div class="relative shrink-0">
            <AlbumCard
              :title="post.title"
              :thumbnail="post.thumbnail"
              :to="`/admin/article/${post.slug}`"
            />
            <DeleteButton
              v-if="canEdit"
              class="absolute top-2 right-2"
              :disabled="saving"
              @click="askRemovePost(postIndex)"
            />
          </div>
        </template>

        <template #append>
          <BaseCard
            v-if="canEdit"
            tag="router-link"
            to="/admin/article/create"
            class="size-40 shrink-0 flex items-center justify-center p-4 hover:bg-base-200"
          >
            <span class="text-4xl text-wntrs-muted leading-none">+</span>
          </BaseCard>
        </template>
      </SortableList>
    </div>
  </div>

  <ConfirmDialog
    ref="confirmDialog"
    :title="dialogTitle"
    :message="dialogMessage"
    @confirm="onConfirmDelete"
  />

  <BaseFooter />
</template>

<script>
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import AlbumCard from '@/components/common/AlbumCard.vue'
import DeleteButton from '@/components/common/DeleteButton.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import SortableList from '@/components/common/SortableList.vue'
import { useAuthStore } from '@/stores/auth.js'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'AdminArticleView',
  components: {
    BaseBreadcrumbs,
    BaseCard,
    AlbumCard,
    DeleteButton,
    ConfirmDialog,
    BaseFooter,
    SortableList,
  },
  data() {
    return {
      breadcrumbs: [
        { label: 'Admin', to: '/admin' },
        { label: 'Artikeln' },
      ],
      error: '',
      saving: false,
      dialogTitle: '',
      dialogMessage: '',
      pendingAction: null,
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
    canEdit() {
      return !!this.authStore.user?.can_edit_content
    },
  },
  mounted() {
    this.contentStore.fetchContent('article')
  },
  methods: {
    async persist(posts) {
      this.error = ''
      this.saving = true
      try {
        await this.contentStore.saveContent('article', posts)
      } catch (e) {
        this.error = e.message
      } finally {
        this.saving = false
      }
    },
    reorderPosts(posts) {
      this.persist(posts)
    },
    confirmRemoval(title, message, action) {
      this.dialogTitle = title
      this.dialogMessage = message
      this.pendingAction = action
      this.$refs.confirmDialog?.open()
    },
    askRemovePost(postIndex) {
      const { title } = this.posts[postIndex]
      this.confirmRemoval('Artikel löschen', `Möchtest du "${title}" wirklich löschen?`, () =>
        this.persist(this.posts.filter((_, i) => i !== postIndex)),
      )
    },
    onConfirmDelete() {
      this.pendingAction?.()
    },
  },
}
</script>
