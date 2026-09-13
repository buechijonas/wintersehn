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
    <div class="flex flex-col pb-16 px-6 max-h-[calc(100vh-101px)] overflow-y-auto">
      <div class="mx-auto w-full max-w-100">
        <div
          class="list bg-base-100 rounded-box shadow-none border-wntrs-border border-solid border-1 mt-16 p-8"
        >
          <h2 class="text-xl font-light mb-6">{{ title }}</h2>
          <div class="text-wntrs-slate">
            <slot />
          </div>
        </div>
      </div>
    </div>
  </Page>
</template>
