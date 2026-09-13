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
  <Page>
    <Breadcrumbs :items="breadcrumbs" />
    <div
      class="flex flex-col pt-8 lg:pb-8 lg:gap-8 overflow-y-auto max-lg:h-[calc(100vh-101px)] lg:max-h-[calc(100vh-101px)]"
    >
      <div class="mx-auto w-full max-w-150 px-6">
        <h2 class="text-xl font-light my-4">{{ title }}</h2>
        <div
          class="list bg-base-100 rounded-box shadow-none border-wntrs-border border-solid border-1 p-8"
        >
          <div class="text-wntrs-slate">
            <slot />
          </div>
        </div>
      </div>
      <Footer />
    </div>
  </Page>
</template>
