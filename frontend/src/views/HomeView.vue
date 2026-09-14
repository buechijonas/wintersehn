<template>
  <BasePage active-navigation="dashboard">
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div class="flex h-[calc(100dvh-192px)] px-6">
      <div class="flex flex-col mx-auto my-32">
        <h1 class="text-title my-8 text-center font-light">Herzlich Willkommen</h1>
        <div v-if="authStore.isAuthenticated" class="flex items-center gap-4 mx-auto mb-8">
          <img class="size-16" :src="avatarSrc" alt="" />
          <div class="flex flex-col gap-1 items-start">
            <span class="badge badge-primary badge-sm">{{ authStore.user.role ?? 'Keine Rolle' }}</span>
            <span class="font-medium">{{ authStore.user.username }}</span>
          </div>
        </div>
        <p class="subtitle mx-auto text-wntrs-muted font-light">wintersehn.ch</p>
      </div>
    </div>
    <BaseFooter />
  </BasePage>
</template>

<script>
import BasePage from '@/components/layout/BasePage.vue'
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import { icons } from '@/assets/icons.js'
import { profiles } from '@/assets/images.js'
import { useAuthStore } from '@/stores/auth.js'

export default {
  name: 'HomeView',
  components: { BasePage, BaseBreadcrumbs, BaseFooter },
  data() {
    return {
      breadcrumbs: [{ label: 'Home', to: '/' }],
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    avatarSrc() {
      return profiles[this.authStore.user?.avatar] ?? icons.user
    },
  },
}
</script>
