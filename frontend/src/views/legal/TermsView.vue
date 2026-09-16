<template>
  <LegalContentLoader content-key="terms" />
</template>

<script>
import LegalContentLoader from '@/components/legal/LegalContentLoader.vue'

export default {
  name: 'TermsView',
  components: { LegalContentLoader },
}
</script>
