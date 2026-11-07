<template>
  <nav
    class="flex shrink-0 gap-1 overflow-x-auto [scrollbar-width:none]"
    :class="
      horizontal
        ? 'min-w-0'
        : 'border-b border-wntrs-border px-6 py-4 lg:w-64 lg:flex-col lg:overflow-y-auto lg:border-r lg:border-b-0 lg:pr-4'
    "
  >
    <template v-if="!authStore.ready">
      <div
        v-for="item in app.navigationItems"
        :key="item.key"
        class="skeleton h-10 w-32 shrink-0"
        :class="{ 'lg:w-full': !horizontal }"
      ></div>
    </template>
    <template v-else>
      <component
        :is="linkComponent(item)"
        v-for="item in items"
        :key="item.key"
        v-bind="linkAttributes(item)"
        class="flex h-10 shrink-0 items-center gap-3 rounded-box px-3 text-sm"
        :class="itemClass(item)"
      >
        <AppIcon v-if="!horizontal" :name="item.icon" />
        <CipherText v-if="item.cipher && isLocked(item)" :length="item.label.length" />
        <span v-else>{{ item.label }}</span>
        <AppIcon v-if="isLocked(item)" name="lock" class="ml-auto size-3!" />
        <AppIcon v-else-if="item.href" name="share-square" class="ml-auto size-3!" />
      </component>
      <div
        v-if="!horizontal"
        class="hidden lg:mt-auto lg:block lg:px-3 lg:pt-6 text-xs font-light text-wntrs-muted"
      >
        Version {{ app.version }}
      </div>
    </template>
  </nav>
</template>

<script>
import { RouterLink } from 'vue-router'
import AppIcon from '@core/components/common/AppIcon.vue'
import CipherText from '@core/components/common/CipherText.vue'
import { useAuthStore } from '@core/stores/auth.js'

const ADMIN_ITEM = { key: 'admin', label: 'Admin', icon: 'crown', to: '/admin' }

export default {
  name: 'SideNav',
  components: { AppIcon, CipherText },
  inject: ['app'],
  props: {
    activeNavigation: { type: String, default: null },
    horizontal: { type: Boolean, default: false },
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    items() {
      const items = this.app.navigationItems.filter(
        (item) => !item.requiresAuth || this.authStore.isAuthenticated,
      )
      const admin = this.app.hasAdmin && this.authStore.user?.can_view_admin
      return admin ? [...items, ADMIN_ITEM] : items
    },
  },
  methods: {
    isLocked(item) {
      if (!item.disabled) return false
      if (!this.authStore.isAuthenticated) return true
      return Boolean(item.permission && !this.authStore.user?.[item.permission])
    },
    linkComponent(item) {
      if (item.href) return 'a'
      return this.isLocked(item) ? 'span' : RouterLink
    },
    linkAttributes(item) {
      if (item.href) return { href: item.href, target: '_blank', rel: 'noopener' }
      if (this.isLocked(item)) return { 'aria-disabled': 'true' }
      return { to: item.to }
    },
    itemClass(item) {
      if (this.isLocked(item)) return 'cursor-not-allowed text-wntrs-muted opacity-60'
      if (this.horizontal) {
        return this.activeNavigation === item.key
          ? 'font-semibold text-base-content'
          : 'text-wntrs-muted hover:text-base-content'
      }
      if (this.activeNavigation === item.key) return 'bg-base-200 text-base-content'
      return 'text-wntrs-muted hover:bg-base-200 hover:text-base-content'
    },
  },
}
</script>
