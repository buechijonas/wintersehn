<template>
  <LegalContentLoader content-key="cookies" label="Cookierichtlinie" />
</template>

<script>
import LegalContentLoader from '@/components/legal/LegalContentLoader.vue'

export default {
  name: 'CookieView',
  components: { LegalContentLoader },
}
</script>
