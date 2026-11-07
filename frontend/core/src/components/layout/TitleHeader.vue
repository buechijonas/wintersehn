<template>
  <div
    class="flex h-14 w-full items-center gap-3 px-6"
    :class="reverse ? 'flex-row-reverse justify-end' : 'justify-end'"
  >
    <div class="mr-auto flex min-w-0 items-center gap-8">
      <RouterLink
        v-if="!hideTitle && $route.name !== 'settings'"
        to="/"
        class="shrink-0 font-display font-bold tracking-tighter text-3xl text-wntrs-logo"
      >
        {{ title }}
      </RouterLink>
      <slot />
    </div>
    <span v-if="!authStore.ready" class="skeleton h-4 w-24"></span>
    <span v-else-if="authStore.isAuthenticated" class="text-sm">
      {{ authStore.user.display_name }}
    </span>
    <div
      class="group dropdown"
      :class="reverse ? 'dropdown-start' : 'dropdown-end'"
      @keydown.esc="closeMenu"
    >
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
        class="dropdown-content menu invisible group-focus-within:visible z-40 w-56 rounded-box border border-wntrs-border bg-base-100 p-1"
      >
        <li>
          <RouterLink
            v-if="$route.name !== 'settings'"
            to="/settings"
            class="flex h-12 items-center gap-3"
            @click="closeMenu"
          >
            <AppIcon name="settings" class="size-6!" />
            <span>Einstellungen</span>
          </RouterLink>
          <RouterLink v-else to="/" class="flex h-12 items-center gap-3" @click="closeMenu">
            <AppIcon :name="homeIcon" class="size-6!" />
            <span>{{ title }}</span>
          </RouterLink>
        </li>
        <li
          v-for="(target, index) in switches"
          :key="target.url"
          :class="{ 'mt-1 border-t border-wntrs-border pt-1': index === 0 }"
        >
          <a :href="target.url" class="flex h-12 items-center gap-3">
            <img :src="target.icon" alt="" class="size-6" />
            <span>{{ target.label }}</span>
          </a>
        </li>
        <li v-if="authStore.ready" class="mt-1 border-t border-wntrs-border pt-1">
          <RouterLink
            :to="authStore.isAuthenticated ? '/logout' : '/login'"
            class="flex h-12 items-center gap-3"
            @click="closeMenu"
          >
            <AppIcon :name="authStore.isAuthenticated ? 'exit' : 'enter'" class="size-6!" />
            <span>{{ authStore.isAuthenticated ? 'Abmelden' : 'Anmelden' }}</span>
          </RouterLink>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'
import AppIcon from '@core/components/common/AppIcon.vue'
import { useAuthStore } from '@core/stores/auth.js'
import { closeMenu } from '@core/lib/menu.js'

export default {
  name: 'TitleHeader',
  components: { RouterLink, AppIcon },
  props: {
    title: { type: String, required: true },
    switches: { type: Array, default: () => [] },
    homeIcon: { type: String, default: 'apps' },
    hideTitle: { type: Boolean, default: false },
    reverse: { type: Boolean, default: false },
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
  },
  methods: {
    closeMenu,
  },
}
</script>
