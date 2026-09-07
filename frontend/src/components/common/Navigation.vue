<script setup>
import { RouterLink } from 'vue-router'
import { icons } from '@/assets/icons.js'
import { navigationItems } from '@/data/navigation.js'
import { useAuthStore } from '@/stores/auth.js'
import packageJson from '../../../package.json'

const version = packageJson.version
const name = packageJson.name
const authStore = useAuthStore()

defineProps({
  activeNavigation: {
    type: String,
    default: null,
  },
})
</script>

<template>
  <div class="appinfo flex items-center pl-8">
    <h1>{{ name }}</h1>
  </div>
  <div class="drawer lg:drawer-open">
    <input id="my-drawer-3" type="checkbox" class="drawer-toggle" />
    <div class="drawer-content flex flex-col items-center justify-center">
      <label for="my-drawer-3" class="btn drawer-button lg:hidden"> Open drawer </label>
    </div>
    <div class="drawer-side flex flex-col">
      <label for="my-drawer-3" aria-label="close sidebar" class="drawer-overlay"></label>
      <ul class="menu w-80 p-4 gap-2">
        <li v-for="item in navigationItems" :key="item.key">
          <component
            :is="item.disabled ? 'span' : RouterLink"
            v-bind="item.disabled ? { 'aria-disabled': 'true' } : { to: item.to }"
            class="nav-item flex items-center gap-3 p-4"
            :class="{ active: activeNavigation === item.key, disabled: item.disabled }"
          >
            <img :src="icons[item.icon]" alt="" class="nav-icon" />
            <span>{{ item.label }}</span>
            <img v-if="item.disabled" :src="icons.lock" alt="" class="lock-icon" />
          </component>
        </li>
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
.drawer {
  top: 64px;
  height: calc(100vh - 64px);
}
.drawer-side {
  top: 64px;
  height: calc(100vh - 64px);
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
