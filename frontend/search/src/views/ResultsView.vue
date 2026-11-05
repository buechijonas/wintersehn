<template>
  <div class="grid flex-1 content-start gap-x-6 px-6 pb-16" :class="layout.grid">
    <header
      class="col-span-full grid sm:sticky sm:top-0 sm:z-20 grid-cols-subgrid bg-base-100 pt-5 shadow-[-1.5rem_0_0_var(--color-base-100),1.5rem_0_0_var(--color-base-100)]"
    >
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
      <div class="mt-2 flex items-center gap-4" :class="layout.main">
        <nav class="flex min-w-0 flex-1 gap-6 overflow-x-auto px-7 [scrollbar-width:none]">
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
          <a
            :href="donateUrl"
            target="_blank"
            rel="noopener noreferrer"
            class="h-10 shrink-0 border-b-2 border-transparent flex items-center text-sm text-wntrs-muted hover:text-primary"
          >
            Spenden
          </a>
        </nav>
        <SecureBadge class="shrink-0" />
      </div>
      <div class="col-span-full -mx-6 border-b border-wntrs-border"></div>
    </header>

    <div class="px-2" :class="category === 'images' ? layout.wide : layout.main">
      <p v-if="error" class="text-error text-sm mt-8">{{ error }}</p>

      <div v-else-if="saving" class="flex flex-col gap-8 mt-8">
        <div v-for="n in 5" :key="n" class="flex flex-col gap-2">
          <div class="skeleton h-3 w-28"></div>
          <div class="skeleton h-5 w-72"></div>
          <div class="skeleton h-3 w-full"></div>
        </div>
      </div>

      <div v-else-if="result?.blocked" class="mt-8 flex max-w-160 flex-col gap-6">
        <div role="alert" class="alert alert-error alert-soft items-start">
          <AppIcon name="octagon-xmark" class="mt-0.5" />
          <span>{{ result.blocked.message }}</span>
        </div>
        <ResultList
          v-if="result.blocked.link"
          :results="[result.blocked.link]"
          :host-ratings="searchStore.hostRatings"
          :pending-hosts="searchStore.pendingHosts"
        />
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
          <template v-if="category === 'images'">
            <ResultList
              v-if="sponsorsStore.current"
              :results="[]"
              :sponsor="sponsorsStore.current"
              class="mb-6 max-w-160"
            />
            <div ref="imageLayout" class="lg:grid lg:grid-cols-5 lg:gap-4">
              <ImageGrid
                :results="result.results"
                :host-ratings="searchStore.hostRatings"
                :pending-hosts="searchStore.pendingHosts"
                :selected="selectedImage?.key"
                :columns="gridColumns - (selectedImage ? previewColumns : 0)"
                :class="spanClasses[gridColumns - (selectedImage ? previewColumns : 0)]"
                @select="imageTrail = [$event]"
              />
              <div v-if="selectedImage" class="relative" :class="spanClasses[previewColumns]">
                <div
                  role="separator"
                  aria-orientation="vertical"
                  aria-label="Breite der Vorschau"
                  :aria-valuenow="previewColumns"
                  tabindex="0"
                  class="group absolute inset-y-0 -left-4 hidden w-4 cursor-col-resize touch-none focus:outline-none lg:block"
                  @pointerdown="startResize"
                  @pointermove="resize"
                  @pointerup="stopResize"
                  @pointercancel="stopResize"
                  @dblclick="previewColumns = defaultPreviewColumns"
                  @keydown.left.prevent="previewColumns = clampPreviewColumns(previewColumns + 1)"
                  @keydown.right.prevent="previewColumns = clampPreviewColumns(previewColumns - 1)"
                >
                  <div
                    class="sticky top-40 flex h-[calc(100dvh-11rem)] items-center justify-center"
                  >
                    <span
                      class="h-12 w-1 rounded-full transition-colors group-hover:bg-primary group-focus-visible:bg-primary"
                      :class="resizing ? 'bg-primary' : 'bg-wntrs-border'"
                    ></span>
                  </div>
                </div>
                <ImagePreview
                  :item="selectedImage"
                  :columns="Math.max(previewColumns, 2)"
                  :can-go-back="imageTrail.length > 1"
                  @select="imageTrail = [...imageTrail, $event]"
                  @back="imageTrail = imageTrail.slice(0, -1)"
                  @close="imageTrail = []"
                />
              </div>
            </div>
          </template>
          <ResultList
            v-else
            :results="result.results"
            :with-images="category !== 'general'"
            :sponsor="sponsorsStore.current"
            :host-ratings="searchStore.hostRatings"
            :pending-hosts="searchStore.pendingHosts"
            :risky-links="searchStore.settings.riskyLinks"
            :confirm-links="searchStore.settings.confirmLinks"
          />
        </div>

        <div v-else-if="result.failures.length" class="mt-8 flex flex-col gap-2 text-sm">
          <p class="text-wntrs-title">Die Suchanbieter haben gerade nicht geantwortet.</p>
          <ul class="text-wntrs-muted">
            <li v-for="failure in result.failures" :key="failure.provider">
              {{ engineLabels[failure.provider]?.label ?? failure.provider }}:
              {{ failureLabels[failure.reason] ?? failure.reason }}
            </li>
          </ul>
          <p class="text-wntrs-muted">
            Versuche es in ein paar Minuten nochmals oder wähle unter Einstellungen → Datenschutz
            ein anderes Netzwerk.
          </p>
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
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import ImageGrid from '@/components/ImageGrid.vue'
import ImagePreview from '@/components/ImagePreview.vue'
import InfiniteSentinel from '@/components/InfiniteSentinel.vue'
import ResultList from '@/components/ResultList.vue'
import SearchField from '@/components/SearchField.vue'
import SecureBadge from '@/components/SecureBadge.vue'
import SearchHeader from '@/components/SearchHeader.vue'
import { handedness } from '@/lib/handedness.js'
import {
  DEFAULT_PREVIEW_COLUMNS,
  GRID_COLUMNS,
  clampPreviewColumns,
  previewColumns,
} from '@/lib/previewColumns.js'
import { categories, donateUrl, engineLabels, failureLabels } from '@/data/settings.js'
import { useSearchStore } from '@/stores/search.js'
import { useSponsorsStore } from '@/stores/sponsors.js'

const SPAN_CLASSES = {
  1: 'lg:col-span-1',
  2: 'lg:col-span-2',
  3: 'lg:col-span-3',
  4: 'lg:col-span-4',
  5: 'lg:col-span-5',
}

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
    AppIcon,
    BaseButton,
    ImageGrid,
    ImagePreview,
    InfiniteSentinel,
    ResultList,
    SearchField,
    SecureBadge,
    SearchHeader,
  },
  mixins: [asyncActionMixin],
  data() {
    return {
      categories,
      donateUrl,
      engineLabels,
      failureLabels,
      loadingMore: false,
      moreError: '',
      imageTrail: [],
      resizing: null,
      gridColumns: GRID_COLUMNS,
      spanClasses: SPAN_CLASSES,
      defaultPreviewColumns: DEFAULT_PREVIEW_COLUMNS,
    }
  },
  computed: {
    layout() {
      return handedness.value === 'left' ? LEFT_LAYOUT : RIGHT_LAYOUT
    },
    searchStore() {
      return useSearchStore()
    },
    sponsorsStore() {
      return useSponsorsStore()
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
    previewColumns: {
      get() {
        return previewColumns.value
      },
      set(columns) {
        previewColumns.value = columns
      },
    },
    selectedImage() {
      return this.imageTrail.at(-1) ?? null
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
    clampPreviewColumns,
    startResize(event) {
      event.currentTarget.setPointerCapture(event.pointerId)
      const { width } = this.$refs.imageLayout.getBoundingClientRect()
      this.resizing = {
        x: event.clientX,
        columns: this.previewColumns,
        columnWidth: width / GRID_COLUMNS,
      }
    },
    resize(event) {
      if (!this.resizing) return
      const { x, columns, columnWidth } = this.resizing
      this.previewColumns = clampPreviewColumns(columns + (x - event.clientX) / columnWidth)
    },
    stopResize() {
      this.resizing = null
    },
    search(query, page = 1) {
      this.imageTrail = []
      this.sponsorsStore.rotate()
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
