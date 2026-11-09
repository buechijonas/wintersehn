<template>
  <div class="flex flex-1 flex-col gap-6 px-6 pt-6 pb-16">
    <label class="input input-lg w-full max-w-200">
      <AppIcon name="search" />
      <input
        :value="query"
        type="search"
        placeholder="Filme und Serien suchen"
        autofocus
        @input="search($event.target.value)"
      />
    </label>

    <div class="flex flex-wrap gap-2">
      <BaseButton
        v-for="category in categories"
        :key="category.key"
        size="sm"
        :variant="category.key === activeCategory ? 'primary' : 'neutral'"
        @click="toggleCategory(category.key)"
      >
        {{ category.label }}
      </BaseButton>
    </div>

    <p v-if="error" class="text-sm text-error">{{ error }}</p>
    <p v-else-if="!saving && !results.length" class="text-wntrs-muted">Nichts gefunden.</p>
    <PosterGrid :items="results" :loading="saving" />

    <SourceNotice class="mt-auto" />
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import PosterGrid from '@/components/PosterGrid.vue'
import SourceNotice from '@/components/SourceNotice.vue'
import { useLumonStore } from '@/stores/lumon.js'

const DELAY = 300

export default {
  name: 'SearchView',
  components: { AppIcon, BaseButton, PosterGrid, SourceNotice },
  mixins: [asyncActionMixin],
  data() {
    return { categories: [], results: [], timer: null }
  },
  computed: {
    store() {
      return useLumonStore()
    },
    query() {
      return this.$route.query.q ?? ''
    },
    activeCategory() {
      return this.$route.query.category ?? null
    },
  },
  watch: {
    '$route.query': { handler: 'load', immediate: true },
  },
  async created() {
    this.categories = await this.store.load('/catalog/categories/', 'Kategorien fehlen.')
  },
  beforeUnmount() {
    clearTimeout(this.timer)
  },
  methods: {
    load() {
      const params = new URLSearchParams()
      if (this.query) params.set('q', this.query)
      if (this.activeCategory) params.set('category', this.activeCategory)
      this.runAction(async () => {
        this.results = await this.store.load(`/catalog/search/?${params}`, 'Suche fehlgeschlagen.')
      })
    },
    update(changes) {
      const query = { ...this.$route.query, ...changes }
      Object.keys(query).forEach((key) => !query[key] && delete query[key])
      this.$router.replace({ query })
    },
    search(value) {
      clearTimeout(this.timer)
      this.timer = setTimeout(() => this.update({ q: value.trim() }), DELAY)
    },
    toggleCategory(key) {
      this.update({ category: key === this.activeCategory ? null : key })
    },
  },
}
</script>
