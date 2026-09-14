<template>
  <LegalContent v-if="page" :page="page" />
</template>

<script>
import LegalContent from '@/components/legal/LegalContent.vue'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'LegalContentLoader',
  components: { LegalContent },
  props: {
    contentKey: { type: String, required: true },
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
    page() {
      return this.contentStore.items[this.contentKey]?.data
    },
  },
  mounted() {
    this.contentStore.fetchContent(this.contentKey)
  },
}
</script>
