<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { icons } from '@/assets/icons.js'
import { profiles } from '@/assets/images.js'
import { isNavDrawerOpen } from '@/lib/navDrawer.js'
import { useAuthStore } from '@/stores/auth.js'
import packageJson from '../../../package.json'

const authStore = useAuthStore()
const menu = ref(null)

const avatarSrc = computed(() => profiles[authStore.user?.avatar] ?? icons.user)
const drawerIcon = computed(() => (isNavDrawerOpen.value ? icons.cross : icons['menu-burger']))
const brandInitial = computed(() =>
  (authStore.user?.verified ? 'Jonas S. Büchi' : packageJson.name).charAt(0),
)

function closeMenu() {
  menu.value?.hidePopover()
}
</script>

<template>
  <div class="header relative w-full flex items-center">
    <div
      class="lg:hidden flex items-center justify-center size-12 shrink-0 bg-white text-base-content text-[1.2rem] font-normal"
    >
      {{ brandInitial }}
    </div>
    <div class="flex items-center gap-3 ml-auto px-6">
      <template v-if="authStore.isAuthenticated">
        <span class="text-white text-sm">{{ authStore.user.username }}</span>
        <button
          type="button"
          class="btn btn-square btn-ghost btn-sm"
          popovertarget="user-menu"
          style="anchor-name: --user-menu-anchor"
        >
          <img
            :src="avatarSrc"
            alt=""
            class="size-5"
            :class="{ invert: !authStore.user?.avatar }"
          />
        </button>
        <ul
          id="user-menu"
          ref="menu"
          popover
          class="dropdown menu w-52 rounded-box bg-base-100 shadow-sm"
          style="position-anchor: --user-menu-anchor; margin-right: 8px"
        >
          <li>
            <RouterLink to="/settings" @click="closeMenu">Einstellungen</RouterLink>
          </li>
          <li v-if="authStore.user?.can_view_admin">
            <RouterLink to="/admin" @click="closeMenu">Admin</RouterLink>
          </li>
        </ul>
      </template>
      <label
        for="my-drawer-3"
        aria-label="Navigation öffnen"
        class="btn btn-square btn-ghost btn-sm lg:hidden"
      >
        <img :src="drawerIcon" alt="" class="size-5 invert" />
      </label>
    </div>
  </div>
</template>

<style>
.header {
  z-index: 20;
  height: 48px;
  background-color: #b42b5f;
}
</style>
