<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="mx-auto flex w-full max-w-200 flex-1 flex-col gap-12 px-6 pt-4 pb-16">
    <h1 class="font-display text-5xl font-bold tracking-tighter text-wntrs-title">
      {{ section?.label }}
    </h1>

    <p v-if="!section?.timeline?.length" class="text-wntrs-muted">Inhalt folgt in Kürze.</p>

    <ol v-else class="-my-8 flex flex-col">
      <li
        v-for="entry in section.timeline"
        :key="`${entry.year}-${entry.title}`"
        class="group grid grid-cols-[0.625rem_minmax(0,1fr)] gap-4"
      >
        <div class="flex flex-col items-center">
          <span class="h-11.75 w-px shrink-0 bg-wntrs-border group-first:invisible"></span>
          <span class="size-2.5 shrink-0 rounded-full bg-primary"></span>
          <span class="w-px flex-1 bg-wntrs-border group-last:invisible"></span>
        </div>
        <div class="py-8">
          <div class="flex flex-wrap items-start gap-x-4 gap-y-3">
            <img
              class="size-10 shrink-0"
              :alt="entry.title"
              :src="flats[entry.icon ?? section.icon]"
            />
            <div class="flex min-w-0 flex-1 flex-col wrap-break-word">
              <span class="text-xs font-medium tracking-wide text-primary">{{ entry.year }}</span>
              <h2 class="font-medium">{{ entry.title }}</h2>
              <p v-if="entry.description" class="text-sm text-wntrs-muted">
                {{ entry.description }}
              </p>
            </div>
            <div
              v-if="entry.links?.length"
              class="grid w-full grid-cols-2 gap-2 pl-14 sm:grid-flow-col sm:grid-cols-none sm:auto-cols-[8rem]"
            >
              <BaseButton
                v-for="link in entry.links"
                :key="link.url"
                variant="primary"
                outline
                size="sm"
                class="min-w-0 flex-nowrap"
                :href="link.url"
                target="_blank"
                rel="noopener noreferrer"
                :title="link.label"
              >
                <span class="truncate">{{ link.label }}</span>
                <AppIcon name="share-square" class="shrink-0" />
              </BaseButton>
            </div>
          </div>
        </div>
      </li>
    </ol>
  </div>
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import AppIcon from '@core/components/common/AppIcon.vue'
import { flats } from '@core/assets/images.js'
import { useContentStore } from '@core/stores/content.js'

export default {
  name: 'CvSectionView',
  components: { BaseBreadcrumbs, BaseButton, AppIcon },
  data() {
    return { flats }
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
    cvCategories() {
      return this.contentStore.items.cv?.data ?? []
    },
    section() {
      return this.cvCategories
        .flatMap((category) => category.items)
        .find((item) => item.key === this.$route.params.key)
    },
    breadcrumbs() {
      return [{ label: 'Lebenslauf', to: '/cv' }, { label: this.section?.label ?? '' }]
    },
  },
  mounted() {
    this.contentStore.fetchContent('cv')
  },
}
</script>
