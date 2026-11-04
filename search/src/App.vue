<template>
  <div class="flex min-h-[100dvh] flex-col bg-base-100">
    <SearchHeader v-if="$route.name !== 'results'" class="mt-5" />
    <RouterView />
  </div>
</template>

<script>
import { RouterView } from 'vue-router'
import SearchHeader from '@/components/SearchHeader.vue'
import { useAuthStore } from '@core/stores/auth.js'
import { useSearchStore } from '@/stores/search.js'

export default {
  name: 'App',
  components: { RouterView, SearchHeader },
  async mounted() {
    await Promise.all([useAuthStore().fetchMe(), this.$router.isReady()])
    await useSearchStore().loadAccountSettings()
    const { path, query, hash } = this.$route
    this.$router.replace({ path, query, hash, force: true })
  },
}
</script>
