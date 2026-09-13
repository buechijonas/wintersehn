<script setup>
import { computed, onMounted } from 'vue'
import Page from '@/components/layout/Page.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import Card from '@/components/common/Card.vue'
import { icons } from '@/assets/icons.js'
import { useAuthStore } from '@/stores/auth.js'
import { useContentStore } from '@/stores/content.js'

const authStore = useAuthStore()
const contentStore = useContentStore()
const breadcrumbs = [{ label: 'Medien', to: '/' }]

onMounted(() => contentStore.fetchContent('media'))

const visibleGroups = computed(() =>
  (contentStore.items.media?.data ?? []).filter(
    (group) => !group.requiresAuth || authStore.user?.can_view_media,
  ),
)
</script>

<template>
  <Page active-navigation="media">
    <Breadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 pb-8 px-6 max-h-[calc(100vh-101px)] overflow-y-auto">
      <div class="mx-auto w-full max-w-150">
        <Card v-for="group in visibleGroups" :key="group.title" tag="ul" class="list mt-4">
          <li class="p-4 pb-2 text-xs opacity-60 tracking-wide">{{ group.title }}</li>
          <li v-for="item in group.items" :key="item.url" class="list-row">
            <div>
              <img class="size-10" :alt="item.platform" :src="icons[item.icon]" />
            </div>
            <div class="flex">
              <div class="my-auto">{{ item.name }}</div>
            </div>
            <a :href="item.url" class="btn btn-square btn-ghost">
              <img class="size-[1.2em]" alt="open" :src="icons['share-square']" />
            </a>
          </li>
        </Card>
      </div>
    </div>
  </Page>
</template>
