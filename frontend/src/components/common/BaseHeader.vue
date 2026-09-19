<template>
  <div class="relative z-20 h-12 w-full flex items-center bg-primary">
    <div
      class="lg:hidden flex items-center justify-center size-12 shrink-0 bg-base-100 text-base-content text-[1.2rem] font-normal"
    >
      {{ brandInitial }}
    </div>
    <div class="flex items-center gap-3 ml-auto px-6">
      <template v-if="authStore.isAuthenticated">
        <span class="text-white text-sm">{{ authStore.user.username }}</span>
        <BaseButton
          variant="ghost"
          shape="square"
          size="sm"
          popovertarget="user-menu"
          style="anchor-name: --user-menu-anchor"
        >
          <img
            :src="avatarSrc"
            alt=""
            class="size-5"
            :class="{ invert: !authStore.user?.avatar }"
          />
        </BaseButton>
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
      <BaseButton v-else variant="ghost" shape="square" size="sm" to="/settings">
        <img :src="icons.settings" alt="Einstellungen" class="size-5 invert" />
      </BaseButton>
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

<script>
import { RouterLink } from 'vue-router'
import BaseButton from '@/components/common/BaseButton.vue'
import { icons } from '@/assets/icons.js'
import { profiles } from '@/assets/images.js'
import { isNavDrawerOpen } from '@/lib/navDrawer.js'
import { useAuthStore } from '@/stores/auth.js'
import packageJson from '../../../package.json'

export default {
  name: 'BaseHeader',
  components: { RouterLink, BaseButton },
  data() {
    return { icons }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    avatarSrc() {
      return profiles[this.authStore.user?.avatar] ?? icons.user
    },
    drawerIcon() {
      return isNavDrawerOpen.value ? icons.cross : icons['menu-burger']
    },
    brandInitial() {
      return (this.authStore.user?.verified ? 'Jonas S. Büchi' : packageJson.name).charAt(0)
    },
  },
  methods: {
    closeMenu() {
      this.$refs.menu?.hidePopover()
    },
  },
}
</script>
