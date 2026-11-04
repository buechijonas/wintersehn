<template>
  <LegalContentLoader content-key="privacy" label="Datenschutzerklärung" />
</template>

<script>
import LegalContentLoader from '@/components/legal/LegalContentLoader.vue'

export default {
  name: 'PrivacyView',
  components: { LegalContentLoader },
}
</script>
