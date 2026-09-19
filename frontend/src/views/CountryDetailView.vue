<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col gap-4 pb-12 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <CardGridSkeleton v-if="loading" :rows="1" />
    <div v-else class="mx-auto w-full max-w-200">
      <h2 class="text-xl my-4 text-center lg:text-left">{{ country?.label }}</h2>
      <p v-if="!albums.length" class="text-wntrs-muted">Noch keine Alben vorhanden.</p>
      <div v-else class="flex flex-wrap justify-center gap-2 lg:justify-start">
        <AlbumCard
          v-for="(album, albumIndex) in albums"
          :key="album.title + albumIndex"
          :title="album.title"
          :thumbnail="album.thumbnail"
          :to="`/countries/${sectionIndex}/${itemIndex}/${albumIndex}`"
        />
      </div>
    </div>
  </div>
  <BaseFooter />
</template>

<script>
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import AlbumCard from '@/components/common/AlbumCard.vue'
import CardGridSkeleton from '@/components/common/CardGridSkeleton.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import countryAlbumRouteMixin from '@/mixins/countryAlbumRouteMixin.js'

export default {
  name: 'CountryDetailView',
  components: { BaseBreadcrumbs, AlbumCard, CardGridSkeleton, BaseFooter },
  mixins: [countryAlbumRouteMixin],
  computed: {
    albums() {
      return this.country?.albums ?? []
    },
    breadcrumbs() {
      return [
        { label: 'Länder', to: '/countries' },
        { label: this.country?.label ?? '…' },
      ]
    },
  },
}
</script>
