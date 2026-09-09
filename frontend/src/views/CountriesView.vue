<script setup>
import { computed, onMounted } from 'vue'
import Page from '@/components/layout/Page.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import CardCategory from '@/components/common/CardCategory.vue'
import { useContentStore } from '@/stores/content.js'

const contentStore = useContentStore()
const breadcrumbs = [{ label: 'Länder', to: '/' }]

onMounted(() => contentStore.fetchContent('countries'))

const countryCategories = computed(() => contentStore.items.countries?.data ?? [])
</script>

<template>
  <Page active-navigation="countries">
    <Breadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col gap-4 pt-12 pb-12 max-h-[calc(100vh-101px)] overflow-y-auto">
      <CardCategory
        v-for="category in countryCategories"
        :key="category.title"
        :title="category.title"
        :items="category.items"
      />
    </div>
  </Page>
</template>
