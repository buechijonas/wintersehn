<template>
  <div class="app-topbar relative z-20 h-12 w-full flex items-center bg-primary">
    <div
      class="lg:hidden flex items-center justify-center size-12 shrink-0 bg-base-100 text-base-content text-[1.2rem] font-normal"
    >
      <div v-if="!authStore.ready" class="skeleton size-5"></div>
      <template v-else>{{ brandInitial }}</template>
    </div>
    <div class="flex h-full items-center gap-3 ml-auto px-4">
      <span v-if="!authStore.ready" class="skeleton h-4 w-24"></span>
      <span v-else-if="authStore.isAuthenticated" class="text-primary-content text-sm">
        {{ authStore.user.display_name }}
      </span>
      <RouterLink to="/settings" title="Einstellungen" :class="iconLinkClass">
        <AppIcon name="settings" alt="Einstellungen" class="size-6!" />
      </RouterLink>
      <label for="my-drawer-3" aria-label="Navigation öffnen" :class="[iconLinkClass, 'lg:hidden']">
        <AppIcon :name="drawerIcon" class="size-6!" />
      </label>
    </div>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'
import AppIcon from '@core/components/common/AppIcon.vue'
import { isNavDrawerOpen } from '@core/lib/navDrawer.js'
import { useAuthStore } from '@core/stores/auth.js'

export default {
  name: 'BaseHeader',
  components: { RouterLink, AppIcon },
  inject: ['app'],
  data() {
    return {
      iconLinkClass: 'flex h-full cursor-pointer items-center px-2 text-primary-content',
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    drawerIcon() {
      return isNavDrawerOpen.value ? 'cross' : 'menu-burger'
    },
    brandInitial() {
      return this.app.displayName(this.authStore.user).charAt(0)
    },
  },
}
</script>
