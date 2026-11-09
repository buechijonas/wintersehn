<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="mx-auto flex w-full max-w-200 flex-1 flex-col gap-12 px-6 pt-4 pb-16">
    <h1 class="font-display text-5xl font-bold tracking-tighter text-wntrs-title">Kanäle</h1>

    <div v-if="loading" class="flex flex-col gap-4">
      <div class="skeleton h-6 w-32"></div>
      <div v-for="row in 3" :key="row" class="skeleton h-10 w-full"></div>
    </div>

    <section v-for="group in visibleGroups" :key="group.title" class="flex flex-col gap-4">
      <h2 class="text-xl">{{ group.title }}</h2>
      <div class="grid gap-4 sm:grid-cols-2">
        <BaseCard
          v-for="item in group.items"
          :key="item.url"
          tag="a"
          :href="item.url"
          class="group flex items-center gap-4 p-4 hover:bg-base-200 sm:last:odd:col-span-2"
        >
          <img class="size-10" :alt="item.platform" :src="social[item.icon]" />
          <span class="min-w-0 flex-1 truncate group-hover:text-primary">{{ item.name }}</span>
          <AppIcon name="share-square" class="text-wntrs-muted group-hover:text-primary" />
        </BaseCard>
      </div>
    </section>
  </div>
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import AppIcon from '@core/components/common/AppIcon.vue'
import { social } from '@core/assets/images.js'
import { useAuthStore } from '@core/stores/auth.js'
import { useContentStore } from '@core/stores/content.js'

export default {
  name: 'MediaView',
  components: { BaseBreadcrumbs, BaseCard, AppIcon },
  data() {
    return {
      social,
      breadcrumbs: [{ label: 'Kanäle', to: '/' }],
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    contentStore() {
      return useContentStore()
    },
    loading() {
      return !this.contentStore.items.media
    },
    visibleGroups() {
      return (this.contentStore.items.media?.data ?? []).filter(
        (group) => !group.requiresAuth || this.authStore.user?.can_view_media,
      )
    },
  },
  mounted() {
    this.contentStore.fetchContent('media')
  },
}
</script>
