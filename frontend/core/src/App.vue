<template>
  <v-app>
    <component :is="layout" :active-navigation="$route.meta.activeNavigation">
      <RouterView />
    </component>
  </v-app>
</template>

<script>
import { RouterView } from 'vue-router'
import BasePage from '@core/components/layout/BasePage.vue'
import SidebarLayout from '@core/components/layout/SidebarLayout.vue'
import { useAuthStore } from '@core/stores/auth.js'

export default {
  name: 'App',
  components: { RouterView, BasePage, SidebarLayout },
  inject: ['app'],
  computed: {
    layout() {
      return this.app.layout === 'sidebar' ? SidebarLayout : BasePage
    },
  },
  async mounted() {
    await Promise.all([useAuthStore().fetchMe(), this.$router.isReady()])
    const { path, query, hash } = this.$route
    this.$router.replace({ path, query, hash, force: true })
  },
}
</script>
