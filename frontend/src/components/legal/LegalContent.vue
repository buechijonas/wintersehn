<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import LegalPage from '@/components/layout/LegalPage.vue'
import LegalSection from '@/components/legal/LegalSection.vue'
import LegalAddress from '@/components/legal/LegalAddress.vue'
import LegalIllustration from '@/components/legal/LegalIllustration.vue'
import { undraws } from '@/assets/images.js'
import { useAuthStore } from '@/stores/auth.js'

const props = defineProps({
  page: {
    type: Object,
    required: true,
  },
})

const authStore = useAuthStore()
const router = useRouter()
const accepting = ref(false)

function onCancel() {
  router.push('/logout')
}

async function onAccept() {
  accepting.value = true
  try {
    await authStore.acceptConsent(props.page.consentField)
    router.push('/')
  } finally {
    accepting.value = false
  }
}
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
    <LegalIllustration v-if="page.illustration" :src="undraws[page.illustration]" :alt="page.title" />
    <div
      v-if="
        page.consentField && authStore.isAuthenticated && !authStore.user.consent[page.consentField]
      "
      class="flex gap-4 mt-6"
    >
      <button type="button" class="btn flex-1 shadow-none" @click="onCancel">Abbrechen</button>
      <button
        type="button"
        class="btn btn-primary flex-1 shadow-none"
        :disabled="accepting"
        @click="onAccept"
      >
        Zustimmen
      </button>
    </div>
  </LegalPage>
</template>
