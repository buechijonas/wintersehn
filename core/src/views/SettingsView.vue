<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-150">
      <h2 class="text-xl font-light my-4">Einstellungen</h2>

      <div v-if="!authStore.ready" class="mb-10">
        <div class="skeleton my-5 h-5 w-24"></div>
        <div class="skeleton h-24 w-full rounded-box"></div>
      </div>
      <div v-else-if="authStore.isAuthenticated" class="mb-10">
        <h3 class="text-xl my-4">Konto</h3>
        <BaseCard class="p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <p class="text-wntrs-muted min-w-0">
            Profil, Profilbild, Passwort und Sicherheit verwaltest du im govex Account Center.
          </p>
          <BaseButton class="shrink-0" @click="authStore.openGovexAccount()">
            <AppIcon name="share-square" />
            Zum Account Center
          </BaseButton>
        </BaseCard>
      </div>

      <AppearanceSettings />
    </div>
  </div>
  <BaseFooter />
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import BaseFooter from '@core/components/common/BaseFooter.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import AppIcon from '@core/components/common/AppIcon.vue'
import AppearanceSettings from '@core/components/common/AppearanceSettings.vue'
import { useAuthStore } from '@core/stores/auth.js'

export default {
  name: 'SettingsView',
  components: { BaseBreadcrumbs, BaseCard, BaseFooter, BaseButton, AppIcon, AppearanceSettings },
  data() {
    return {
      breadcrumbs: [{ label: 'Einstellungen', to: '/' }],
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
  },
}
</script>
