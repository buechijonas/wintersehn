<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { icons } from '@/assets/icons.js'
import { profiles } from '@/assets/images.js'
import { useAuthStore } from '@/stores/auth.js'

const authStore = useAuthStore()
const menu = ref(null)

const avatarSrc = computed(() => profiles[authStore.user?.avatar] ?? icons.user)

function closeMenu() {
  menu.value?.hidePopover()
}
</script>

<template>
  <div class="header flex items-center justify-end gap-3 px-6">
    <template v-if="authStore.isAuthenticated">
      <span class="text-white text-sm">{{ authStore.user.username }}</span>
      <button
        type="button"
        class="btn btn-square btn-ghost btn-sm"
        popovertarget="user-menu"
        style="anchor-name: --user-menu-anchor"
      >
        <img :src="avatarSrc" alt="" class="size-5" :class="{ invert: !authStore.user?.avatar }" />
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
  </div>
</template>

<style>
.header {
  height: 48px;
  width: 100%;
  background-color: #b42b5f;
}
</style>
