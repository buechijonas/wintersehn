<template>
  <div
    class="flex min-h-[100dvh] flex-col bg-base-100 transition-[filter]"
    :class="{ 'blur-xl select-none': obscured }"
  >
    <SearchHeader v-if="$route.name !== 'results'" class="mt-5" />
    <RouterView />
  </div>
</template>

<script>
import { RouterView } from 'vue-router'
import SearchHeader from '@/components/SearchHeader.vue'
import { useAuthStore } from '@core/stores/auth.js'
import { useSearchStore } from '@/stores/search.js'
import { useSponsorsStore } from '@/stores/sponsors.js'
import { panicUrl } from '@/data/settings.js'

const PANIC_DELAY = 600

export default {
  name: 'App',
  components: { RouterView, SearchHeader },
  data() {
    return {
      hidden: false,
      lastEscape: 0,
    }
  },
  computed: {
    settings() {
      return useSearchStore().settings
    },
    obscured() {
      return this.settings.privacyScreen && this.hidden
    },
  },
  async mounted() {
    window.addEventListener('blur', this.hide)
    window.addEventListener('focus', this.show)
    window.addEventListener('keydown', this.onKeydown)
    await Promise.all([useAuthStore().fetchMe(), this.$router.isReady()])
    await useSearchStore().loadAccountSettings()
    await useSearchStore().fetchNetworks()
    await useSponsorsStore()
      .fetchSponsors()
      .catch(() => null)
    const { path, query, hash } = this.$route
    this.$router.replace({ path, query, hash, force: true })
  },
  beforeUnmount() {
    window.removeEventListener('blur', this.hide)
    window.removeEventListener('focus', this.show)
    window.removeEventListener('keydown', this.onKeydown)
  },
  methods: {
    hide() {
      this.hidden = true
    },
    show() {
      this.hidden = false
    },
    onKeydown(event) {
      if (event.key !== 'Escape' || !this.settings.panicKey) return
      if (event.timeStamp - this.lastEscape < PANIC_DELAY) window.location.replace(panicUrl)
      this.lastEscape = event.timeStamp
    },
  },
}
</script>
