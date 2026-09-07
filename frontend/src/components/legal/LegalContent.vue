<script setup>
import LegalPage from '@/components/layout/LegalPage.vue'
import LegalSection from '@/components/legal/LegalSection.vue'
import LegalAddress from '@/components/legal/LegalAddress.vue'
import LegalIllustration from '@/components/legal/LegalIllustration.vue'
import { undraws } from '@/assets/images.js'

defineProps({
  page: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <LegalPage :title="page.title" :breadcrumb-label="page.breadcrumbLabel">
    <p v-if="page.intro" class="mt-6 font-medium text-gray">{{ page.intro }}</p>
    <LegalSection
      v-for="(section, index) in page.sections"
      :key="section.title ?? index"
      :title="section.title"
      :text="section.text"
      :items="section.items"
    >
      <template v-if="section.address">
        <LegalAddress />
      </template>
    </LegalSection>
    <LegalIllustration :src="undraws[page.illustration]" :alt="page.title" />
  </LegalPage>
</template>
