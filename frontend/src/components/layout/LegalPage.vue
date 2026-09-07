<script setup>
import { computed } from 'vue'
import Page from '@/components/layout/Page.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import Footer from '@/components/common/Footer.vue'

const props = defineProps({
  title: { type: String, required: true },
  breadcrumbLabel: { type: String, default: null },
})

const breadcrumbs = computed(() => [{ label: props.breadcrumbLabel ?? props.title, to: '/' }])
</script>
<template>
  <Page active-navigation="dashboard">
    <Breadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 max-h-[calc(100vh-101px)] overflow-y-auto">
      <div class="mx-auto w-150">
        <h2 class="text-xl font-light my-4">{{ title }}</h2>
        <div
          class="list bg-base-100 rounded-box shadow-none border-wntrs-gray border-solid border-1 p-8"
        >
          <div class="color-dark-gray">
            <slot />
          </div>
        </div>
      </div>
      <Footer class="my-4" />
    </div>
  </Page>
</template>
