<template>
  <address class="text-wntrs-muted not-italic">
    <p v-for="line in lines" :key="line">{{ line }}</p>
  </address>
</template>

<script>
import { useContentStore } from '@core/stores/content.js'

export default {
  name: 'LegalAddress',
  computed: {
    contentStore() {
      return useContentStore()
    },
    lines() {
      return this.contentStore.items.address?.data?.lines ?? []
    },
  },
  mounted() {
    this.contentStore.fetchContent('address')
  },
}
</script>
