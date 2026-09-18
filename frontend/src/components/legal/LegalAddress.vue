<template>
  <p v-for="line in lines" :key="line" class="font-light">{{ line }}</p>
</template>

<script>
import { useContentStore } from '@/stores/content.js'

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
