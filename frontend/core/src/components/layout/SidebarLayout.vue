<template>
  <div class="flex min-h-[100dvh] flex-col bg-base-100 lg:h-[100dvh] lg:overflow-hidden">
    <TitleHeader :title="app.title" :switches="appSwitches" class="mt-5">
      <SideNav
        v-if="hasNavigation && topNavigation"
        horizontal
        class="hidden lg:flex"
        :active-navigation="activeNavigation"
      />
    </TitleHeader>
    <div v-if="!isSettings && !topNavigation" class="mt-3 border-b border-wntrs-border"></div>
    <SideNav
      v-if="hasNavigation && topNavigation"
      horizontal
      class="px-6 pt-2 lg:hidden"
      :active-navigation="activeNavigation"
    />
    <div class="flex flex-1 flex-col lg:min-h-0 lg:flex-row" :class="{ 'mt-3': topNavigation }">
      <SideNav v-if="hasNavigation && !topNavigation" :active-navigation="activeNavigation" />
      <main :key="$route.path" class="flex min-w-0 flex-1 flex-col lg:overflow-y-auto">
        <slot v-if="authStore.ready" />
      </main>
    </div>
  </div>
</template>

<script>
import { unref } from 'vue'
import SideNav from '@core/components/layout/SideNav.vue'
import TitleHeader from '@core/components/layout/TitleHeader.vue'
import { appSwitchTargets } from '@core/lib/appSwitch.js'
import { useAuthStore } from '@core/stores/auth.js'

export default {
  name: 'SidebarLayout',
  components: { SideNav, TitleHeader },
  inject: ['app'],
  props: {
    activeNavigation: { type: String, default: null },
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    appSwitches() {
      return appSwitchTargets(this.app, this.authStore.user)
    },
    isSettings() {
      return this.$route.name === 'settings'
    },
    topNavigation() {
      return Boolean(unref(this.app.topNavigation))
    },
    hasNavigation() {
      return !this.isSettings && this.app.navigationItems.length > 0
    },
  },
  watch: {
    '$route.path'() {
      window.scrollTo(0, 0)
    },
  },
}
</script>
