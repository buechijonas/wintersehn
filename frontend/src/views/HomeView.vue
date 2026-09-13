<script setup>
import { computed } from 'vue'
import Page from '@/components/layout/Page.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import Footer from '@/components/common/Footer.vue'
import { icons } from '@/assets/icons.js'
import { profiles } from '@/assets/images.js'
import { useAuthStore } from '@/stores/auth.js'

const authStore = useAuthStore()

const breadcrumbs = [
  {
    label: 'Home',
    to: '/',
  },
]

const avatarSrc = computed(() => profiles[authStore.user?.avatar] ?? icons.user)
</script>

<template>
  <Page active-navigation="dashboard">
    <Breadcrumbs :items="breadcrumbs" />
    <div class="flex h-[calc(100vh-192px)]">
      <div class="flex flex-col mx-auto my-32">
        <h1 class="text-title my-8 font-light">Herzlich Willkommen</h1>
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
    <Footer />
  </Page>
</template>
