<template>
  <LegalPage :title="page.title">
    <MarkdownContent :html="html" />
    <LegalIllustration
      v-if="page.illustration"
      :src="undraws[page.illustration]"
      :alt="page.title"
    />
    <div
      v-if="
        page.consentField && authStore.isAuthenticated && !authStore.user.consent[page.consentField]
      "
      class="flex gap-4"
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
import LegalIllustration from '@/components/legal/LegalIllustration.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import CancelButton from '@core/components/common/CancelButton.vue'
import MarkdownContent from '@core/components/common/MarkdownContent.vue'
import { undraws } from '@core/assets/images.js'
import { useAuthStore } from '@core/stores/auth.js'

export default {
  name: 'LegalContent',
  components: {
    LegalPage,
    LegalIllustration,
    BaseButton,
    CancelButton,
    MarkdownContent,
  },
  props: {
    page: {
      type: Object,
      required: true,
    },
    html: { type: String, default: '' },
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
