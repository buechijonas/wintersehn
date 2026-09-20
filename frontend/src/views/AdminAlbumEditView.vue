<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-200">
      <input
        type="text"
        class="input w-full max-w-100 my-4"
        :value="album?.title"
        :disabled="!canEdit"
        @change="renameAlbum($event)"
      />

      <p v-if="error" class="text-error text-sm mb-4">{{ error }}</p>

      <ImageUploadField v-if="canEdit" class="mb-4" @uploaded="onImageUploaded" />

      <p v-if="!images.length" class="text-wntrs-muted">Noch keine Bilder in diesem Album.</p>
      <SortableList
        v-else
        :items="images"
        :disabled="!canEdit"
        class="flex flex-wrap gap-2"
        @reorder="reorderImages"
      >
        <template #default="{ item: image, index: imageIndex }">
          <div class="relative shrink-0">
            <BaseCard class="size-40 overflow-hidden">
              <img class="size-full object-cover" :src="image" alt="" />
            </BaseCard>
            <BaseButton
              v-if="canEdit"
              type="button"
              variant="neutral"
              shape="circle"
              size="sm"
              class="absolute bottom-2 left-2"
              :class="{ 'text-primary': album.thumbnail === image }"
              :disabled="saving"
              :title="
                album.thumbnail === image
                  ? 'Aktuelles Thumbnail'
                  : 'Als Thumbnail verwenden'
              "
              @click="setThumbnail(image)"
            >
              <AppIcon
                :name="album.thumbnail === image ? 'graphic-style' : 'picture'"
                class="size-4"
                :class="{ 'icon-tint-primary': album.thumbnail === image }"
                alt="Als Thumbnail verwenden"
              />
            </BaseButton>
            <DeleteButton
              v-if="canEdit"
              class="absolute top-2 right-2"
              :disabled="saving"
              @click="askRemoveImage(imageIndex)"
            />
          </div>
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
import BaseButton from '@/components/common/BaseButton.vue'
import AppIcon from '@/components/common/AppIcon.vue'
import ImageUploadField from '@/components/common/ImageUploadField.vue'
import DeleteButton from '@/components/common/DeleteButton.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import SortableList from '@/components/common/SortableList.vue'
import { useAuthStore } from '@/stores/auth.js'
import countryAlbumRouteMixin from '@/mixins/countryAlbumRouteMixin.js'
import confirmDeleteMixin from '@/mixins/confirmDeleteMixin.js'
import asyncActionMixin from '@/mixins/asyncActionMixin.js'

export default {
  name: 'AdminAlbumEditView',
  components: {
    BaseBreadcrumbs,
    BaseCard,
    BaseButton,
    AppIcon,
    ImageUploadField,
    DeleteButton,
    ConfirmDialog,
    BaseFooter,
    SortableList,
  },
  mixins: [countryAlbumRouteMixin, confirmDeleteMixin, asyncActionMixin],
  computed: {
    authStore() {
      return useAuthStore()
    },
    images() {
      return this.album?.images ?? []
    },
    canEdit() {
      return !!this.authStore.user?.can_change_countries
    },
    breadcrumbs() {
      return [
        { label: 'Admin', to: '/admin' },
        { label: 'Länder', to: '/admin/countries' },
        {
          label: this.country?.label ?? '…',
          to: `/admin/countries/${this.sectionIndex}/${this.itemIndex}/albums`,
        },
        { label: this.album?.title ?? '…' },
      ]
    },
  },
  methods: {
    persistAlbum(patch) {
      const data = this.sections.map((section, sIndex) =>
        sIndex !== this.sectionIndex
          ? section
          : {
              ...section,
              items: section.items.map((item, iIndex) =>
                iIndex !== this.itemIndex
                  ? item
                  : {
                      ...item,
                      albums: item.albums.map((album, aIndex) =>
                        aIndex === this.albumIndex ? { ...album, ...patch } : album,
                      ),
                    },
              ),
            },
      )
      return this.runAction(() => this.contentStore.saveContent('countries', data))
    },
    renameAlbum(event) {
      const title = event.target.value.trim()
      event.target.value = title
      if (!title || title === this.album.title) return
      this.persistAlbum({ title })
    },
    onImageUploaded(urls) {
      const images = [...this.images, ...urls]
      const thumbnail = this.album.thumbnail || urls[0]
      this.persistAlbum({ images, thumbnail })
    },
    reorderImages(images) {
      this.persistAlbum({ images })
    },
    setThumbnail(image) {
      this.persistAlbum({ thumbnail: image })
    },
    askRemoveImage(imageIndex) {
      const removed = this.images[imageIndex]
      this.confirmRemoval('Bild löschen', 'Möchtest du dieses Bild wirklich löschen?', () => {
        const images = this.images.filter((_, i) => i !== imageIndex)
        const thumbnail = this.album.thumbnail === removed ? '' : this.album.thumbnail
        this.persistAlbum({ images, thumbnail })
      })
    },
  },
}
</script>
