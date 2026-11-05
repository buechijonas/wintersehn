<template>
  <aside
    class="fixed inset-0 z-50 flex flex-col gap-4 overflow-y-auto bg-base-100 p-4 lg:sticky lg:inset-auto lg:top-40 lg:z-10 lg:max-h-[calc(100dvh-11rem)] lg:rounded-box lg:border lg:border-wntrs-border"
  >
    <div class="flex items-center justify-between gap-2">
      <BaseButton v-if="canGoBack" variant="ghost" size="sm" @click="$emit('back')">
        <AppIcon name="angle-left" />
        Zurück
      </BaseButton>
      <span v-else class="text-sm text-wntrs-muted">Vorschau</span>
      <BaseButton variant="ghost" size="sm" shape="circle" @click="$emit('close')">
        <AppIcon name="cross" alt="Vorschau schliessen" />
      </BaseButton>
    </div>

    <img
      :src="fullLoaded ? item.full : item.image"
      :alt="item.title"
      class="max-h-[60dvh] w-full rounded-box bg-base-200 object-contain"
    />
    <img
      v-if="item.full && !fullLoaded"
      :src="item.full"
      alt=""
      class="hidden"
      @load="fullLoaded = true"
    />
    <p v-if="item.resolution" class="-mt-2 text-xs text-wntrs-muted">{{ item.resolution }}</p>

    <ResultList
      :results="[item]"
      :host-ratings="searchStore.hostRatings"
      :pending-hosts="searchStore.pendingHosts"
      :risky-links="searchStore.settings.riskyLinks"
      :confirm-links="searchStore.settings.confirmLinks"
    />

    <section class="flex flex-col gap-3">
      <h3 class="text-sm text-wntrs-muted">Ähnliche Bilder</h3>
      <ImageGrid
        v-if="similar.length"
        :results="similar"
        :host-ratings="searchStore.hostRatings"
        :pending-hosts="searchStore.pendingHosts"
        :columns="columns"
        @select="$emit('select', $event)"
      />
      <p v-else-if="!loading && !error" class="text-sm text-wntrs-muted">
        Keine ähnlichen Bilder gefunden.
      </p>
      <p v-if="error" class="text-sm text-error">{{ error }}</p>
      <div v-if="loading" class="flex justify-center">
        <span class="loading loading-dots text-primary"></span>
      </div>
      <BaseButton v-else-if="similar.length && !done" size="sm" class="self-center" @click="load">
        <AppIcon name="plus" />
        Mehr laden
      </BaseButton>
    </section>
  </aside>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import ImageGrid from '@/components/ImageGrid.vue'
import ResultList from '@/components/ResultList.vue'
import { useSearchStore } from '@/stores/search.js'

export default {
  name: 'ImagePreview',
  components: { AppIcon, BaseButton, ImageGrid, ResultList },
  props: {
    item: { type: Object, required: true },
    canGoBack: { type: Boolean, default: false },
    columns: { type: Number, default: 2 },
  },
  emits: ['back', 'close', 'select'],
  data() {
    return {
      similar: [],
      page: 0,
      loading: false,
      error: '',
      done: false,
      fullLoaded: false,
      trail: new Map(),
    }
  },
  computed: {
    searchStore() {
      return useSearchStore()
    },
  },
  watch: {
    item: {
      immediate: true,
      handler(item, previous) {
        if (previous) this.trail.set(previous.key, this.snapshot())
        const saved = this.trail.get(item.key)
        this.similar = saved?.similar ?? []
        this.page = saved?.page ?? 0
        this.done = saved?.done ?? false
        this.error = ''
        this.fullLoaded = false
        if (this.$el) this.$el.scrollTop = saved?.scroll ?? 0
        if (!saved) this.load()
      },
    },
  },
  mounted() {
    window.addEventListener('keydown', this.onKeydown)
  },
  beforeUnmount() {
    window.removeEventListener('keydown', this.onKeydown)
  },
  methods: {
    snapshot() {
      return {
        similar: this.similar,
        page: this.page,
        done: this.done,
        scroll: this.$el?.scrollTop ?? 0,
      }
    },
    async load() {
      const item = this.item
      this.loading = true
      this.error = ''
      try {
        const results = await this.searchStore.similarImages(item, this.page + 1)
        if (item !== this.item) return
        const keys = new Set(this.similar.map(({ key }) => key))
        const fresh = results.filter(({ key }) => !keys.has(key))
        this.similar = [...this.similar, ...fresh]
        this.page += 1
        this.done = !fresh.length
      } catch (e) {
        if (item === this.item) this.error = e.message
      } finally {
        if (item === this.item) this.loading = false
      }
    },
    onKeydown(event) {
      if (event.key === 'Escape') this.$emit('close')
    },
  },
}
</script>
