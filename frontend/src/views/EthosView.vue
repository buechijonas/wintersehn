<script setup>
import { computed, onMounted } from 'vue'
import Page from '@/components/layout/Page.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import CardCategory from '@/components/common/CardCategory.vue'
import { useContentStore } from '@/stores/content.js'

const contentStore = useContentStore()
const breadcrumbs = [{ label: 'Ethos', to: '/' }]

onMounted(() => contentStore.fetchContent('ethos'))

const ethosCategories = computed(() => contentStore.items.ethos?.data ?? [])
</script>

<template>
  <Page active-navigation="ethos">
    <Breadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col gap-4 pt-12 pb-12 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto">
      <CardCategory
        v-for="category in ethosCategories"
        :key="category.title"
        :title="category.title"
        :items="category.items"
      />
    </div>
  </Page>
</template>
