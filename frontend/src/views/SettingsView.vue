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
  <Page>
    <Breadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto">
      <div class="mx-auto w-full max-w-150">
        <h2 class="text-xl font-light my-4">Einstellungen</h2>

        <div class="flex gap-4 mb-10 items-stretch">
          <div class="flex flex-col">
            <h3 class="text-xl my-4">Profilbild</h3>
            <Card class="size-24 shrink-0 flex items-center justify-center p-2">
              <img class="size-14" :src="avatarSrc" alt="" />
            </Card>
          </div>

          <div class="flex-1 flex flex-col min-w-0">
            <h3 class="text-xl my-4">Konto</h3>
            <Card class="p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div class="flex flex-col gap-1 min-w-0">
                <p>
                  <span class="text-wntrs-muted block sm:inline">Benutzername:</span>
                  {{ authStore.user.username }}
                </p>
                <p class="break-all">
                  <span class="text-wntrs-muted block sm:inline">E-Mail:</span>
                  {{ authStore.user.email }}
                </p>
              </div>
              <RouterLink to="/settings/account" class="btn shadow-none shrink-0">Bearbeiten</RouterLink>
            </Card>
          </div>
        </div>

        <div class="mb-10">
          <h3 class="text-xl my-4">Passwort</h3>
          <Card class="p-6 flex items-center justify-between gap-4">
            <p class="text-wntrs-muted">Passwort ändern oder zurücksetzen.</p>
            <RouterLink to="/settings/password" class="btn shadow-none">Ändern</RouterLink>
          </Card>
        </div>
      </div>
    </div>
  </Page>
</template>
