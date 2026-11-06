<template>
  <div class="flex min-h-[100dvh] flex-col bg-base-100">
    <TitleHeader title="ATLAS" class="mt-5" />
    <div class="mt-3 border-b border-wntrs-border"></div>
    <div class="flex flex-1 flex-col lg:flex-row">
      <AtlasNav />
      <RouterView v-if="authStore.ready" class="min-w-0" />
    </div>
  </div>
</template>

<script>
import { RouterView } from 'vue-router'
import TitleHeader from '@core/components/layout/TitleHeader.vue'
import { useAuthStore } from '@core/stores/auth.js'
import AtlasNav from '@/components/AtlasNav.vue'

export default {
  name: 'App',
  components: { AtlasNav, RouterView, TitleHeader },
  computed: {
    authStore() {
      return useAuthStore()
    },
  },
  async mounted() {
    await Promise.all([this.authStore.fetchMe(), this.$router.isReady()])
    const { path, query, hash } = this.$route
    this.$router.replace({ path, query, hash, force: true })
  },
}
</script>
