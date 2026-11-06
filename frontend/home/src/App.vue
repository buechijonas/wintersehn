<template>
  <div class="flex min-h-[100dvh] flex-col bg-base-100">
    <HomeHeader class="mt-5" />
    <div class="mt-3 border-b border-wntrs-border"></div>
    <RouterView v-if="authStore.ready" />
  </div>
</template>

<script>
import { RouterView } from 'vue-router'
import HomeHeader from '@/components/HomeHeader.vue'
import { useAuthStore } from '@core/stores/auth.js'

export default {
  name: 'App',
  components: { RouterView, HomeHeader },
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
