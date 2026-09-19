import { useContentStore } from '@/stores/content.js'
export default {
  computed: {
    contentStore() {
      return useContentStore()
    },
    loading() {
      return !this.contentStore.items.countries
    },
    sectionIndex() {
      return Number(this.$route.params.section)
    },
    itemIndex() {
      return Number(this.$route.params.item)
    },
    albumIndex() {
      return Number(this.$route.params.album)
    },
    sections() {
      return this.contentStore.items.countries?.data ?? []
    },
    country() {
      return this.sections[this.sectionIndex]?.items?.[this.itemIndex] ?? null
    },
    album() {
      return this.country?.albums?.[this.albumIndex] ?? null
    },
  },
  mounted() {
    this.contentStore.fetchContent('countries')
  },
}
