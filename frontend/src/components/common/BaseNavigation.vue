<template>
  <div class="hidden h-12 w-[330px] items-center pl-8 lg:flex">
    <h1 class="text-[1.2rem]">{{ displayName }}</h1>
  </div>
  <div class="drawer drawer-end lg:drawer-open lg:top-16 lg:h-[calc(100dvh-64px)]">
    <input id="my-drawer-3" v-model="isNavDrawerOpen" type="checkbox" class="drawer-toggle" />
    <div class="drawer-content"></div>
    <div
      class="drawer-side flex flex-col overflow-y-auto bg-base-100 max-lg:top-12 max-lg:h-[calc(100dvh-48px)] lg:top-16 lg:h-[calc(100dvh-64px)]"
    >
      <label for="my-drawer-3" aria-label="close sidebar" class="drawer-overlay"></label>
      <ul class="menu w-full lg:w-80 p-4 gap-2">
        <li v-for="item in navigationItems" :key="item.key">
          <component
            :is="isLocked(item) ? 'span' : RouterLink"
            v-bind="isLocked(item) ? { 'aria-disabled': 'true' } : { to: item.to }"
            class="nav-item flex items-center gap-3 p-4"
            :class="{
              'active bg-wntrs-highlight text-primary': activeNavigation === item.key,
              'disabled cursor-not-allowed': isLocked(item),
            }"
            @click="isNavDrawerOpen = false"
          >
            <img :src="icons[item.icon]" alt="" class="nav-icon size-5 shrink-0" />
            <span>{{ item.label }}</span>
            <img v-if="isLocked(item)" :src="icons.lock" alt="" class="lock-icon size-3 shrink-0" />
          </component>
        </li>
        <template v-if="authStore.user?.can_view_admin">
          <li><hr class="my-2 border-wntrs-border" /></li>
          <li>
            <RouterLink
              to="/admin"
              class="nav-item flex items-center gap-3 p-4"
              :class="{ 'active bg-wntrs-highlight text-primary': activeNavigation === 'admin' }"
              @click="isNavDrawerOpen = false"
            >
              <img :src="icons.crown" alt="" class="nav-icon size-5 shrink-0" />
              <span>Admin</span>
            </RouterLink>
          </li>
        </template>
      </ul>
      <div class="mt-auto p-4 w-full">
        <div class="mb-4 text-xs text-wntrs-muted font-light">
          <div>Version {{ version }}</div>
          <div>Created by Wintersehn</div>
        </div>
        <RouterLink
          v-if="!authStore.isAuthenticated"
          to="/login"
          class="btn btn-primary w-full shadow-none"
          @click="isNavDrawerOpen = false"
        >
          <img :src="icons.enter" alt="" class="nav-icon mr-2 size-5 shrink-0 invert" />Anmelden
        </RouterLink>
        <RouterLink
          v-else
          to="/logout"
          class="btn btn-primary w-full shadow-none"
          @click="isNavDrawerOpen = false"
        >
          <img :src="icons.exit" alt="" class="nav-icon mr-2 size-5 shrink-0 invert" />Abmelden
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'
import { icons } from '@/assets/icons.js'
import { navigationItems } from '@/data/navigation.js'
import { isNavDrawerOpen } from '@/lib/navDrawer.js'
import { useAuthStore } from '@/stores/auth.js'
import packageJson from '../../../package.json'

export default {
  name: 'BaseNavigation',
  components: { RouterLink },
  props: {
    activeNavigation: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      icons,
      navigationItems,
      version: packageJson.version,
      RouterLink,
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    displayName() {
      return this.authStore.user?.verified ? 'Jonas S. Büchi' : packageJson.name
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
  },
}
</script>

<style>
.nav-item.disabled .nav-icon,
.nav-item.disabled .lock-icon {
  filter: brightness(0) saturate(100%) invert(76%) sepia(15%) saturate(228%) hue-rotate(171deg)
    brightness(91%) contrast(90%);
}
.nav-item.active .nav-icon {
  filter: brightness(0) saturate(100%) invert(24%) sepia(55%) saturate(2090%) hue-rotate(303deg)
    brightness(86%) contrast(85%);
}
</style>
