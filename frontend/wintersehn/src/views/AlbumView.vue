<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col gap-4 pb-12 px-6 flex-1">
    <CardGridSkeleton v-if="loading" :rows="1" />
    <div v-else class="mx-auto w-full max-w-200">
      <h2 class="text-xl my-4 text-center lg:text-left">{{ album?.title }}</h2>
      <p v-if="!images.length" class="text-wntrs-muted">Noch keine Bilder in diesem Album.</p>
      <div v-else class="columns-2 sm:columns-3 lg:columns-4 gap-2">
        <img
          v-for="(image, imageIndex) in images"
          :key="image"
          :src="image"
          alt=""
          class="w-full mb-2 rounded-box cursor-pointer break-inside-avoid"
          @click="openLightbox(imageIndex)"
        />
      </div>
    </div>
  </div>

  <ImageLightbox ref="lightbox" :images="images" />
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import CardGridSkeleton from '@core/components/common/CardGridSkeleton.vue'
import ImageLightbox from '@core/components/common/ImageLightbox.vue'
import countryAlbumRouteMixin from '@/mixins/countryAlbumRouteMixin.js'

export default {
  name: 'AlbumView',
  components: { BaseBreadcrumbs, CardGridSkeleton, ImageLightbox },
  mixins: [countryAlbumRouteMixin],
  computed: {
    images() {
      return this.album?.images ?? []
    },
    breadcrumbs() {
      return [
        { label: 'Länder', to: '/countries' },
        { label: this.country?.label ?? '…', to: `/countries/${this.sectionIndex}/${this.itemIndex}` },
        { label: this.album?.title ?? '…' },
      ]
    },
  },
  methods: {
    openLightbox(index) {
      this.$refs.lightbox?.open(index)
    },
  },
}
</script>
