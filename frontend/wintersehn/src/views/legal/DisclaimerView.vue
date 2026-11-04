<template>
  <LegalContentLoader content-key="disclaimer" label="Haftungsausschluss" />
</template>

<script>
import LegalContentLoader from '@/components/legal/LegalContentLoader.vue'

export default {
  name: 'DisclaimerView',
  components: { LegalContentLoader },
}
</script>
