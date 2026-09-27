<template>
  <v-app>
    <BasePage :active-navigation="$route.meta.activeNavigation">
      <RouterView />
    </BasePage>
  </v-app>
</template>

<script>
import { RouterView } from 'vue-router'
import BasePage from '@/components/layout/BasePage.vue'
import { useAuthStore } from '@/stores/auth.js'

export default {
  name: 'App',
  components: { RouterView, BasePage },
  async mounted() {
    await Promise.all([useAuthStore().fetchMe(), this.$router.isReady()])
    const { path, query, hash } = this.$route
    this.$router.replace({ path, query, hash, force: true })
  },
}
</script>
