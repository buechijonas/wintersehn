<template>
  <BasePage active-navigation="media">
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto">
      <div class="mx-auto w-full max-w-150">
        <BaseCard v-for="group in visibleGroups" :key="group.title" tag="ul" class="list mt-4">
          <li class="p-4 pb-2 text-xs opacity-60 tracking-wide">{{ group.title }}</li>
          <li v-for="item in group.items" :key="item.url" class="list-row">
            <div>
              <img class="size-10" :alt="item.platform" :src="icons[item.icon]" />
            </div>
            <div class="flex">
              <div class="my-auto">{{ item.name }}</div>
            </div>
            <BaseButton variant="ghost" shape="square" :href="item.url">
              <img class="size-[1.2em]" alt="open" :src="icons['share-square']" />
            </BaseButton>
          </li>
        </BaseCard>
      </div>
    </div>
    <BaseFooter />
  </BasePage>
</template>

<script>
import BasePage from '@/components/layout/BasePage.vue'
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { icons } from '@/assets/icons.js'
import { useAuthStore } from '@/stores/auth.js'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'MediaView',
  components: { BasePage, BaseBreadcrumbs, BaseCard, BaseFooter, BaseButton },
  data() {
    return {
      icons,
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
