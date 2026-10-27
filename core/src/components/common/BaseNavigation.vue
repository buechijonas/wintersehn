<template>
  <div class="app-nav col-start-2 row-start-1 hidden h-12 w-80 items-center pl-8 lg:flex">
    <div v-if="!authStore.ready" class="skeleton h-5 w-40"></div>
    <h1 v-else class="text-[1.2rem]">{{ displayName }}</h1>
  </div>
  <div class="col-start-2 row-start-1 drawer drawer-end lg:drawer-open">
    <input id="my-drawer-3" v-model="isNavDrawerOpen" type="checkbox" class="drawer-toggle" />
    <div class="drawer-content"></div>
    <div
      class="app-nav drawer-side z-30 flex flex-col overflow-y-auto bg-base-100 top-12 h-[calc(100dvh-48px)]"
    >
      <label for="my-drawer-3" aria-label="close sidebar" class="drawer-overlay"></label>
      <ul v-if="!authStore.ready" class="menu w-full lg:w-80 p-4 gap-2">
        <li v-for="item in navigationItems" :key="item.key">
          <div class="flex items-center gap-3 p-4">
            <div class="skeleton size-6 lg:size-5 shrink-0"></div>
            <div class="skeleton h-4 w-28"></div>
          </div>
        </li>
      </ul>
      <ul v-else class="menu w-full lg:w-80 p-4 gap-2">
        <li v-for="item in navigationItems" :key="item.key">
          <component
            :is="linkComponent(item)"
            v-bind="linkAttributes(item)"
            class="nav-item flex items-center gap-3 p-4"
            :class="{
              'active bg-wntrs-highlight text-primary': activeNavigation === item.key,
              'disabled cursor-not-allowed': isLocked(item),
            }"
            @click="isNavDrawerOpen = false"
          >
            <img :src="icons[item.icon]" alt="" class="nav-icon size-6 lg:size-5 shrink-0" />
            <CipherText v-if="item.cipher && isLocked(item)" :length="item.label.length" />
            <span v-else>{{ item.label }}</span>
            <span v-if="item.href" class="ml-auto text-xs text-wntrs-muted">Externer Link</span>
            <img v-if="isLocked(item)" :src="icons.lock" alt="" class="lock-icon size-3 shrink-0" />
          </component>
        </li>
        <template v-if="app.hasAdmin && authStore.user?.can_view_admin">
          <div class="my-2 h-px bg-wntrs-border pointer-events-none"></div>
          <li>
            <RouterLink
              to="/admin"
              class="nav-item flex items-center gap-3 p-4"
              :class="{
                'active bg-wntrs-highlight text-primary': activeNavigation === 'admin',
              }"
              @click="isNavDrawerOpen = false"
            >
              <img :src="icons.crown" alt="" class="nav-icon size-6 lg:size-5 shrink-0" />
              <span>Admin</span>
            </RouterLink>
          </li>
        </template>
      </ul>
      <div v-if="!authStore.ready" class="mt-auto flex w-full flex-col gap-1 p-4">
        <div class="skeleton h-3 w-20"></div>
        <div class="skeleton mb-4 h-3 w-32"></div>
        <div class="skeleton h-10 w-full"></div>
      </div>
      <div v-else class="mt-auto p-4 w-full">
        <div class="mb-4 text-xs text-wntrs-muted font-light">
          <div>Version {{ app.version }}</div>
          <div>Created by Wintersehn</div>
        </div>
        <BaseButton
          v-if="!authStore.isAuthenticated"
          variant="primary"
          block
          to="/login"
          @click="isNavDrawerOpen = false"
        >
          <AppIcon name="enter" />Anmelden
        </BaseButton>
        <BaseButton v-else variant="primary" block to="/logout" @click="isNavDrawerOpen = false">
          <AppIcon name="exit" />Abmelden
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'
import BaseButton from '@core/components/common/BaseButton.vue'
import AppIcon from '@core/components/common/AppIcon.vue'
import CipherText from '@core/components/common/CipherText.vue'
import { icons } from '@core/assets/icons.js'
import { isNavDrawerOpen } from '@core/lib/navDrawer.js'
import { useAuthStore } from '@core/stores/auth.js'

export default {
  name: 'BaseNavigation',
  components: { RouterLink, BaseButton, AppIcon, CipherText },
  inject: ['app'],
  props: {
    activeNavigation: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      icons,
      RouterLink,
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    displayName() {
      return this.app.displayName(this.authStore.user)
    },
    navigationItems() {
      return this.app.navigationItems.filter(
        (item) => !item.requiresAuth || this.authStore.isAuthenticated,
      )
    },
    isNavDrawerOpen: {
      get() {
        return isNavDrawerOpen.value
      },
      set(value) {
        isNavDrawerOpen.value = value
      },
    },
  },
  methods: {
    isLocked(item) {
      if (!item.disabled) return false
      if (!this.authStore.isAuthenticated) return true
      if (item.permission) return !this.authStore.user?.[item.permission]
      return false
    },
    linkComponent(item) {
      if (item.href) return 'a'
      if (this.isLocked(item)) return 'span'
      return RouterLink
    },
    linkAttributes(item) {
      if (item.href) return { href: item.href, target: '_blank', rel: 'noopener' }
      if (this.isLocked(item)) return { 'aria-disabled': 'true' }
      return { to: item.to }
    },
  },
}
</script>

<style>
[data-theme='dark'] .nav-icon,
[data-theme='dark'] .lock-icon {
  filter: invert(1);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme]) .nav-icon,
  :root:not([data-theme]) .lock-icon {
    filter: invert(1);
  }
}

.nav-item.disabled .nav-icon,
.nav-item.disabled .lock-icon {
  filter: brightness(0) saturate(100%) invert(76%) sepia(15%) saturate(228%) hue-rotate(171deg)
    brightness(91%) contrast(90%);
}

.nav-item.active .nav-icon {
  filter: var(--icon-tint-primary);
}

/* drawer-end flips the grid columns; pin them so the open sidebar stays flush with the accent bar. */
@media (width >= 1024px) {
  .drawer.drawer-end.lg\:drawer-open {
    grid-template-columns: 0 max-content;
  }
}
</style>
