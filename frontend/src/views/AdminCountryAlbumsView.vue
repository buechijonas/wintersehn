<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-200">
      <h2 class="text-xl my-4">{{ country?.label }}</h2>

      <p v-if="error" class="text-error text-sm mb-4">{{ error }}</p>

      <p v-if="!albums.length" class="text-wntrs-muted mb-4">Noch keine Alben vorhanden.</p>
      <div v-else class="flex flex-wrap gap-2 mb-6">
        <div v-for="(album, albumIndex) in albums" :key="album.title + albumIndex" class="relative shrink-0">
          <AlbumCard
            :title="album.title"
            :thumbnail="album.thumbnail"
            :to="`/admin/countries/${sectionIndex}/${itemIndex}/albums/${albumIndex}`"
          />
          <DeleteButton
            v-if="canEdit"
            class="absolute top-2 right-2"
            :disabled="saving"
            @click="askRemoveAlbum(albumIndex)"
          />
        </div>
      </div>

      <div v-if="canEdit" class="flex gap-4">
        <input
          v-model="newAlbumTitle"
          type="text"
          placeholder="Neues Album"
          class="input flex-1"
          @keyup.enter="addAlbum"
        />
        <BaseButton variant="primary" @click="addAlbum">Album hinzufügen</BaseButton>
      </div>
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
import BaseButton from '@/components/common/BaseButton.vue'
import AlbumCard from '@/components/common/AlbumCard.vue'
import DeleteButton from '@/components/common/DeleteButton.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import { useAuthStore } from '@/stores/auth.js'
import countryAlbumRouteMixin from '@/mixins/countryAlbumRouteMixin.js'
import confirmDeleteMixin from '@/mixins/confirmDeleteMixin.js'
import asyncActionMixin from '@/mixins/asyncActionMixin.js'

export default {
  name: 'AdminCountryAlbumsView',
  components: { BaseBreadcrumbs, BaseButton, AlbumCard, DeleteButton, ConfirmDialog, BaseFooter },
  mixins: [countryAlbumRouteMixin, confirmDeleteMixin, asyncActionMixin],
  data() {
    return {
      newAlbumTitle: '',
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    albums() {
      return this.country?.albums ?? []
    },
    canEdit() {
      return !!this.authStore.user?.can_change_countries
    },
    breadcrumbs() {
      return [
        { label: 'Admin', to: '/admin' },
        { label: 'Länder', to: '/admin/countries' },
        { label: this.country?.label ?? '…' },
      ]
    },
  },
  methods: {
    persist(albums) {
      const data = this.sections.map((section, sIndex) =>
        sIndex === this.sectionIndex
          ? {
              ...section,
              items: section.items.map((item, iIndex) =>
                iIndex === this.itemIndex ? { ...item, albums } : item,
              ),
            }
          : section,
      )
      return this.runAction(() => this.contentStore.saveContent('countries', data))
    },
    addAlbum() {
      const title = this.newAlbumTitle.trim()
      if (!title) return
      this.newAlbumTitle = ''
      this.persist([...this.albums, { title, thumbnail: '', images: [] }])
    },
    askRemoveAlbum(albumIndex) {
      const { title } = this.albums[albumIndex]
      this.confirmRemoval('Album löschen', `Möchtest du "${title}" wirklich löschen?`, () =>
        this.persist(this.albums.filter((_, i) => i !== albumIndex)),
      )
    },
  },
}
</script>
