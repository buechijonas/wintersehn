<template>
  <BaseCard v-if="!authStore.ready" class="p-6">
    <div class="skeleton h-5 w-48"></div>
  </BaseCard>

  <BaseCard
    v-else-if="authStore.isAuthenticated"
    class="p-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
  >
    <p class="text-wntrs-muted min-w-0">
      Angemeldet als {{ authStore.user.display_name }}. Profil, Profilbild, Passwort und Sicherheit
      verwaltest du im govex Account Center.
    </p>
    <div class="flex shrink-0 flex-wrap gap-2">
      <BaseButton @click="authStore.openGovexAccount()">
        <AppIcon name="share-square" />
        Zum Account Center
      </BaseButton>
      <BaseButton variant="primary" to="/logout">
        <AppIcon name="exit" />
        Abmelden
      </BaseButton>
    </div>
  </BaseCard>

  <BaseCard v-else class="p-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
    <p class="text-wntrs-muted min-w-0">
      Mit deinem govex Konto meldest du dich bei allen Apps an. Deine Einstellungen bleiben dann
      gespeichert.
    </p>
    <BaseButton variant="primary" class="shrink-0" to="/login">
      <AppIcon name="enter" />
      Anmelden
    </BaseButton>
  </BaseCard>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import { useAuthStore } from '@core/stores/auth.js'

export default {
  name: 'AccountCard',
  components: { AppIcon, BaseButton, BaseCard },
  computed: {
    authStore() {
      return useAuthStore()
    },
  },
}
</script>
