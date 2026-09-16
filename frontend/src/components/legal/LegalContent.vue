<template>
  <LegalPage :title="page.title" :breadcrumb-label="page.breadcrumbLabel">
    <p v-if="page.intro" class="mt-6 font-medium text-gray">{{ page.intro }}</p>
    <LegalSection
      v-for="(section, index) in page.sections"
      :key="section.title ?? index"
      :title="section.title"
      :subtitle="section.subtitle"
      :text="section.text"
      :items="section.items"
    >
      <template v-if="section.address">
        <LegalAddress />
      </template>
    </LegalSection>
    <LegalIllustration v-if="page.illustration" :src="undraws[page.illustration]" :alt="page.title" />
    <div
      v-if="
        page.consentField && authStore.isAuthenticated && !authStore.user.consent[page.consentField]
      "
      class="flex gap-4 mt-6"
    >
      <CancelButton class="flex-1" to="/logout" />
      <BaseButton variant="primary" class="flex-1" :disabled="accepting" @click="onAccept">
        Zustimmen
      </BaseButton>
    </div>
  </LegalPage>
</template>

<script>
import LegalPage from '@/components/layout/LegalPage.vue'
import LegalSection from '@/components/legal/LegalSection.vue'
import LegalAddress from '@/components/legal/LegalAddress.vue'
import LegalIllustration from '@/components/legal/LegalIllustration.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import CancelButton from '@/components/common/CancelButton.vue'
import { undraws } from '@/assets/images.js'
import { useAuthStore } from '@/stores/auth.js'

export default {
  name: 'LegalContent',
  components: { LegalPage, LegalSection, LegalAddress, LegalIllustration, BaseButton, CancelButton },
  props: {
    page: {
      type: Object,
      required: true,
    },
  },
  data() {
    return { undraws, accepting: false }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
  },
  methods: {
    async onAccept() {
      this.accepting = true
      try {
        await this.authStore.acceptConsent(this.page.consentField)
        this.$router.push('/')
      } finally {
        this.accepting = false
      }
    },
  },
}
</script>
