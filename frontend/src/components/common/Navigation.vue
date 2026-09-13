<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { icons } from '@/assets/icons.js'
import { navigationItems } from '@/data/navigation.js'
import { isNavDrawerOpen } from '@/lib/navDrawer.js'
import { useAuthStore } from '@/stores/auth.js'
import packageJson from '../../../package.json'

const version = packageJson.version
const authStore = useAuthStore()
const displayName = computed(() =>
  authStore.user?.verified ? 'Jonas S. Büchi' : packageJson.name,
)

defineProps({
  activeNavigation: {
    type: String,
    default: null,
  },
})

function isLocked(item) {
  if (!item.disabled) return false
  if (!authStore.isAuthenticated) return true
  if (item.permission) return !authStore.user?.[item.permission]
  return false
}
</script>

<template>
  <div class="appinfo hidden lg:flex items-center pl-8">
    <h1>{{ displayName }}</h1>
  </div>
  <div class="drawer drawer-end lg:drawer-open">
    <input id="my-drawer-3" v-model="isNavDrawerOpen" type="checkbox" class="drawer-toggle" />
    <div class="drawer-content"></div>
    <div class="drawer-side flex flex-col bg-base-100">
      <label for="my-drawer-3" aria-label="close sidebar" class="drawer-overlay"></label>
      <ul class="menu w-full lg:w-80 p-4 gap-2">
        <li v-for="item in navigationItems" :key="item.key">
          <component
            :is="isLocked(item) ? 'span' : RouterLink"
            v-bind="isLocked(item) ? { 'aria-disabled': 'true' } : { to: item.to }"
            class="nav-item flex items-center gap-3 p-4"
            :class="{ active: activeNavigation === item.key, disabled: isLocked(item) }"
          >
            <img :src="icons[item.icon]" alt="" class="nav-icon" />
            <span>{{ item.label }}</span>
            <img v-if="isLocked(item)" :src="icons.lock" alt="" class="lock-icon" />
          </component>
        </li>
        <template v-if="authStore.user?.can_view_admin">
          <li><hr class="my-2 border-wntrs-gray" /></li>
          <li>
            <RouterLink
              to="/admin"
              class="nav-item flex items-center gap-3 p-4"
              :class="{ active: activeNavigation === 'admin' }"
            >
              <img :src="icons.crown" alt="" class="nav-icon" />
              <span>Admin</span>
            </RouterLink>
          </li>
        </template>
      </ul>
      <div class="mt-auto p-4 w-full">
        <div class="mb-4 text-xs color-gray font-light">
          <div>Version {{ version }}</div>
          <div>Created by Wintersehn</div>
        </div>
        <RouterLink
          v-if="!authStore.isAuthenticated"
          to="/login"
          class="btn btn-primary w-full shadow-none"
        >
          <img :src="icons.enter" alt="" class="nav-icon mr-2 invert" />Anmelden
        </RouterLink>
        <RouterLink v-else to="/logout" class="btn btn-primary w-full shadow-none">
          <img :src="icons.exit" alt="" class="nav-icon mr-2 invert" />Abmelden
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style>
.appinfo {
  height: 48px;
  width: 330px;
  h1 {
    font-size: 1.2rem;
  }
}
.drawer-side {
  top: 48px;
  height: calc(100vh - 48px);
}
@media (min-width: 1024px) {
  .drawer {
    top: 64px;
    height: calc(100vh - 64px);
  }
  .drawer-side {
    top: 64px;
    height: calc(100vh - 64px);
  }
}
.lock-icon {
  width: 12px;
  height: 12px;
  flex-shrink: 0;
}
.nav-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}
.nav-item.disabled {
  cursor: not-allowed;
}
.nav-item.disabled .nav-icon,
.nav-item.disabled .lock-icon {
  filter: brightness(0) saturate(100%) invert(76%) sepia(15%) saturate(228%) hue-rotate(171deg)
    brightness(91%) contrast(90%);
}
.nav-item.active {
  background: #f0dbe3;
  color: #b42b5f;
}
.nav-item.active .nav-icon {
  filter: brightness(0) saturate(100%) invert(24%) sepia(55%) saturate(2090%) hue-rotate(303deg)
    brightness(86%) contrast(85%);
}
</style>
