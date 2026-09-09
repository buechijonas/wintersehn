<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import Page from '@/components/layout/Page.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import Card from '@/components/common/Card.vue'
import { profiles } from '@/assets/images.js'
import { icons } from '@/assets/icons.js'
import { useAuthStore } from '@/stores/auth.js'

const authStore = useAuthStore()
const breadcrumbs = [{ label: 'Einstellungen', to: '/' }]

const avatarSrc = computed(() => profiles[authStore.user.avatar] ?? icons.user)
</script>

<template>
  <Page active-navigation="dashboard">
    <Breadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 pb-8 max-h-[calc(100vh-101px)] overflow-y-auto">
      <div class="mx-auto w-150">
        <h2 class="text-xl font-light my-4">Einstellungen</h2>

        <div class="flex gap-4 mb-10 items-stretch">
          <div class="flex flex-col">
            <h3 class="title-category my-4">Profilbild</h3>
            <Card class="w-24 flex-1 shrink-0 flex items-center justify-center p-2">
              <img class="size-14" :src="avatarSrc" alt="" />
            </Card>
          </div>

          <div class="flex-1 flex flex-col">
            <h3 class="title-category my-4">Konto</h3>
            <Card class="p-6 flex items-center justify-between gap-4">
              <div class="flex flex-col gap-1">
                <p><span class="color-gray">Benutzername:</span> {{ authStore.user.username }}</p>
                <p><span class="color-gray">E-Mail:</span> {{ authStore.user.email }}</p>
              </div>
              <RouterLink to="/settings/account" class="btn shadow-none">Bearbeiten</RouterLink>
            </Card>
          </div>
        </div>

        <div class="mb-10">
          <h3 class="title-category my-4">Passwort</h3>
          <Card class="p-6 flex items-center justify-between gap-4">
            <p class="color-gray">Passwort ändern oder zurücksetzen.</p>
            <RouterLink to="/settings/password" class="btn shadow-none">Ändern</RouterLink>
          </Card>
        </div>
      </div>
    </div>
  </Page>
</template>
