<template>
  <BasePage>
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div
      class="flex flex-col pt-8 lg:pb-8 lg:gap-8 overflow-y-auto max-lg:h-[calc(100dvh-101px)] lg:max-h-[calc(100dvh-101px)]"
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
      <BaseFooter />
    </div>
  </BasePage>
</template>

<script>
import BasePage from '@/components/layout/BasePage.vue'
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'

export default {
  name: 'LegalPage',
  components: { BasePage, BaseBreadcrumbs, BaseFooter },
  props: {
    title: { type: String, required: true },
    breadcrumbLabel: { type: String, default: null },
  },
  computed: {
    breadcrumbs() {
      return [{ label: this.breadcrumbLabel ?? this.title, to: '/' }]
    },
  },
}
</script>
