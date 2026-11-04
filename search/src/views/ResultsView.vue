<template>
  <div class="grid flex-1 content-start gap-x-6 px-6 pt-5 pb-16" :class="layout.grid">
    <RouterLink
      to="/"
      class="self-center font-display font-bold tracking-tighter text-3xl text-wntrs-title"
      :class="layout.logo"
    >
      Suche
    </RouterLink>
    <SearchHeader class="self-center px-0!" :class="layout.header" />
    <SearchField
      :model-value="searchStore.query"
      class="mt-2 sm:mt-0 sm:self-center"
      :class="layout.main"
      @submit="goTo"
    />
    <nav class="flex gap-6 overflow-x-auto px-7 mt-2 [scrollbar-width:none]" :class="layout.main">
      <RouterLink
        v-for="tab in categories"
        :key="tab.key"
        :to="{ query: { ...$route.query, tab: tab.key, page: undefined } }"
        replace
        class="h-10 shrink-0 border-b-2 flex items-center text-sm"
        :class="
          category === tab.key
            ? 'border-primary text-base-content'
            : 'border-transparent text-wntrs-muted hover:text-base-content'
        "
      >
        {{ tab.label }}
      </RouterLink>
    </nav>
    <div class="col-span-full -mx-6 border-b border-wntrs-border"></div>

    <div class="px-2" :class="category === 'images' ? layout.wide : layout.main">
      <p v-if="error" class="text-error text-sm mt-8">{{ error }}</p>

      <div v-else-if="saving" class="flex flex-col gap-8 mt-8">
        <div v-for="n in 5" :key="n" class="flex flex-col gap-2">
          <div class="skeleton h-3 w-28"></div>
          <div class="skeleton h-5 w-72"></div>
          <div class="skeleton h-3 w-full"></div>
        </div>
      </div>

      <template v-else-if="result">
        <p v-if="result.suggestions.length" class="text-sm text-wntrs-muted mt-6">
          Meintest du
          <button
            v-for="suggestion in result.suggestions.slice(0, 3)"
            :key="suggestion"
            type="button"
            class="link link-hover text-base-content ml-2"
            @click="goTo(suggestion)"
          >
            {{ suggestion }}
          </button>
        </p>

        <div v-if="result.results.length" class="mt-4 sm:mt-8">
          <ImageGrid v-if="category === 'images'" :results="result.results" />
          <ResultList v-else :results="result.results" :with-images="category !== 'general'" />
        </div>

        <p v-else class="text-wntrs-muted mt-8">Keine Treffer.</p>

        <template v-if="isInfinite">
          <InfiniteSentinel v-if="!result.done && !loadingMore" @visible="loadMore" />
          <div v-if="loadingMore" class="flex justify-center mt-8">
            <span class="loading loading-dots text-primary"></span>
          </div>
          <p v-if="moreError" class="text-error text-sm mt-6 text-center">{{ moreError }}</p>
        </template>

        <div v-else class="flex justify-between mt-12">
          <BaseButton
            v-if="result.page > 1"
            variant="ghost"
            size="sm"
            @click="goTo(result.query, result.page - 1)"
          >
            Zurück
          </BaseButton>
          <BaseButton
            v-if="result.results.length"
            variant="ghost"
            size="sm"
            class="ml-auto"
            @click="goTo(result.query, result.page + 1)"
          >
            Weiter
          </BaseButton>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'
import BaseButton from '@core/components/common/BaseButton.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import ImageGrid from '@/components/ImageGrid.vue'
import InfiniteSentinel from '@/components/InfiniteSentinel.vue'
import ResultList from '@/components/ResultList.vue'
import SearchField from '@/components/SearchField.vue'
import SearchHeader from '@/components/SearchHeader.vue'
import { handedness } from '@/lib/handedness.js'
import { categories } from '@/data/settings.js'
import { useSearchStore } from '@/stores/search.js'

const RIGHT_LAYOUT = {
  grid: 'grid-cols-[1fr_auto] sm:grid-cols-[auto_minmax(0,40rem)_1fr]',
  logo: 'col-start-1 row-start-1',
  header: 'col-start-2 row-start-1 sm:col-start-3 sm:justify-self-end',
  main: 'col-span-2 sm:col-span-1 sm:col-start-2',
  wide: 'col-span-2 sm:col-start-2 sm:col-span-2',
}

const LEFT_LAYOUT = {
  grid: 'grid-cols-[auto_1fr] sm:grid-cols-[auto_auto_minmax(0,40rem)_1fr]',
  logo: 'col-start-2 row-start-1 justify-self-end sm:justify-self-auto',
  header: 'col-start-1 row-start-1',
  main: 'col-span-2 sm:col-span-1 sm:col-start-3',
  wide: 'col-span-2 sm:col-start-3 sm:col-span-2',
}

export default {
  name: 'ResultsView',
  components: {
    RouterLink,
    BaseButton,
    ImageGrid,
    InfiniteSentinel,
    ResultList,
    SearchField,
    SearchHeader,
  },
  mixins: [asyncActionMixin],
  data() {
    return {
      categories,
      loadingMore: false,
      moreError: '',
    }
  },
  computed: {
    layout() {
      return handedness.value === 'left' ? LEFT_LAYOUT : RIGHT_LAYOUT
    },
    searchStore() {
      return useSearchStore()
    },
    result() {
      return this.searchStore.result
    },
    isGet() {
      return this.searchStore.settings.method === 'get'
    },
    category() {
      const tab = this.$route.query.tab
      return categories.some(({ key }) => key === tab) ? tab : 'general'
    },
    isInfinite() {
      return this.searchStore.settings.pagination === 'infinite'
    },
  },
  watch: {
    '$route.query': {
      immediate: true,
      handler({ q, page }) {
        const query = q ?? this.searchStore.query
        if (!query) return this.$router.replace({ name: 'search' })
        if (!q && this.result?.category === this.category) return
        return this.search(query, Number(page ?? 1))
      },
    },
  },
  methods: {
    search(query, page = 1) {
      return this.runAction(() => this.searchStore.search(query, page, this.category))
    },
    goTo(query, page = 1) {
      if (!this.isGet) return this.search(query, page)
      const tab = this.category === 'general' ? undefined : this.category
      this.$router.push({ query: { q: query, tab, page: page > 1 ? page : undefined } })
    },
    async loadMore() {
      this.loadingMore = true
      this.moreError = ''
      try {
        await this.searchStore.loadMore()
      } catch (e) {
        this.moreError = e.message
      } finally {
        this.loadingMore = false
      }
    },
  },
}
</script>
