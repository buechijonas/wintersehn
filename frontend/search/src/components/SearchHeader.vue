<template>
  <div
    class="flex h-14 w-full items-center gap-3 px-6"
    :class="isLeft ? 'flex-row-reverse justify-end' : 'justify-end'"
  >
    <span v-if="!authStore.ready" class="skeleton h-4 w-24"></span>
    <span v-else-if="authStore.isAuthenticated" class="text-sm">
      {{ authStore.user.display_name }}
    </span>
    <div class="dropdown" :class="isLeft ? 'dropdown-start' : 'dropdown-end'">
      <div
        tabindex="0"
        role="button"
        aria-label="Menü"
        class="flex size-10 cursor-pointer items-center justify-center"
      >
        <AppIcon name="menu-burger" class="size-6!" />
      </div>
      <ul
        tabindex="0"
        class="dropdown-content menu z-40 w-56 rounded-box border border-wntrs-border bg-base-100 p-1"
      >
        <li>
          <RouterLink
            v-if="$route.name === 'settings'"
            to="/"
            class="flex h-12 items-center gap-3"
            @click="closeMenu"
          >
            <AppIcon name="search" class="size-6!" />
            <span>Suche</span>
          </RouterLink>
          <RouterLink v-else to="/settings" class="flex h-12 items-center gap-3" @click="closeMenu">
            <AppIcon name="settings" class="size-6!" />
            <span>Einstellungen</span>
          </RouterLink>
        </li>
        <li
          v-for="(target, index) in appSwitches"
          :key="target.url"
          :class="{ 'mt-1 border-t border-wntrs-border pt-1': index === 0 }"
        >
          <a :href="target.url" class="flex h-12 items-center gap-3">
            <img
              :src="target.icon ?? `${target.url}/icons/maskable-512.png`"
              alt=""
              class="size-6"
            />
            <span>{{ target.label }}</span>
          </a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'
import AppIcon from '@core/components/common/AppIcon.vue'
import { useAuthStore } from '@core/stores/auth.js'
import { handedness } from '@/lib/handedness.js'

export default {
  name: 'SearchHeader',
  components: { RouterLink, AppIcon },
  inject: ['app'],
  computed: {
    isLeft() {
      return handedness.value === 'left'
    },
    authStore() {
      return useAuthStore()
    },
    appSwitches() {
      const user = this.authStore.user
      return this.app.appSwitches.filter(
        (target) => !target.permission || user?.[target.permission],
      )
    },
  },
  methods: {
    closeMenu() {
      document.activeElement.blur()
    },
  },
}
</script>
