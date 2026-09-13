<script setup>
import { computed, onMounted } from 'vue'
import Page from '@/components/layout/Page.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import CardCategory from '@/components/common/CardCategory.vue'
import Footer from '@/components/common/Footer.vue'
import { useContentStore } from '@/stores/content.js'

const contentStore = useContentStore()
const breadcrumbs = [{ label: 'Lebenslauf', to: '/' }]

onMounted(() => contentStore.fetchContent('cv'))

const cvCategories = computed(() => contentStore.items.cv?.data ?? [])
</script>

<template>
  <Page active-navigation="cv">
    <Breadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col gap-4 mt-12 px-6">
      <CardCategory
        v-for="category in cvCategories"
        :key="category.title"
        :title="category.title"
        :items="category.items"
      />
    </div>
    <Footer />
  </Page>
</template>
