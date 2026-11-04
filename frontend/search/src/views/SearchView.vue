<template>
  <div class="mx-auto flex w-full max-w-160 flex-1 flex-col justify-center px-6 pb-[42vh]">
    <div class="mb-10 flex flex-col items-center">
      <h1 class="font-display font-bold tracking-tighter text-6xl text-wntrs-title -translate-x-6">
        Suche
      </h1>
      <span class="font-display font-bold tracking-tight text-lg text-primary translate-x-12">
        Wintersehn
      </span>
    </div>
    <SearchField :model-value="searchStore.query" @submit="search" />
  </div>
</template>

<script>
import SearchField from '@/components/SearchField.vue'
import { useSearchStore } from '@/stores/search.js'

export default {
  name: 'SearchView',
  components: { SearchField },
  computed: {
    searchStore() {
      return useSearchStore()
    },
  },
  methods: {
    search(query) {
      this.searchStore.query = query
      this.searchStore.result = null
      const isGet = this.searchStore.settings.method === 'get'
      this.$router.push({ name: 'results', query: isGet ? { q: query } : {} })
    },
  },
}
</script>
