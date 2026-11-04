<template>
  <BaseBreadcrumbs :items="[{ label: 'Bilder' }]" />
  <div
    class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1"
  >
    <div class="mx-auto w-full max-w-250 pt-4">
      <BaseCard class="p-4">
        <ImageLibrary />
      </BaseCard>
    </div>
  </div>
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import ImageLibrary from '@/components/ImageLibrary.vue'

export default {
  name: 'ImagesView',
  components: { BaseBreadcrumbs, BaseCard, ImageLibrary },
}
</script>
