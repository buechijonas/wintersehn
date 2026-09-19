<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-150">
      <div v-if="loading" class="mt-4 flex flex-col gap-4">
        <div v-for="row in 2" :key="row" class="flex flex-col gap-2">
          <div class="skeleton h-4 w-24"></div>
          <div v-for="item in 3" :key="item" class="skeleton h-14 w-full"></div>
        </div>
      </div>
      <BaseCard v-for="group in visibleGroups" :key="group.title" tag="ul" class="list mt-4">
        <li class="p-4 pb-2 text-xs opacity-60 tracking-wide">{{ group.title }}</li>
        <li v-for="item in group.items" :key="item.url" class="list-row">
          <div>
            <img class="size-10" :alt="item.platform" :src="social[item.icon]" />
          </div>
          <div class="flex">
            <div class="my-auto">{{ item.name }}</div>
          </div>
          <BaseButton variant="ghost" shape="square" :href="item.url">
            <AppIcon class="size-[1.2em]" alt="open" name="share-square" />
          </BaseButton>
        </li>
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
import AppIcon from '@/components/common/AppIcon.vue'
import { social } from '@/assets/images.js'
import { useAuthStore } from '@/stores/auth.js'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'MediaView',
  components: { BaseBreadcrumbs, BaseCard, BaseFooter, BaseButton, AppIcon },
  data() {
    return {
      social,
      breadcrumbs: [{ label: 'Medien', to: '/' }],
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
