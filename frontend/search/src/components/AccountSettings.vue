<template>
  <div class="flex flex-col gap-6">
    <BaseCard v-if="!authStore.ready" class="p-6">
      <div class="skeleton h-5 w-48"></div>
    </BaseCard>

    <BaseCard
      v-else-if="authStore.isAuthenticated"
      class="p-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
    >
      <p class="text-wntrs-muted min-w-0">
        Angemeldet als {{ authStore.user.display_name }}. Profil, Passwort und Sicherheit verwaltest
        du im govex Account Center.
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
        Suchen geht auch ohne Konto. Angemeldet bleiben deine Einstellungen gespeichert.
      </p>
      <BaseButton variant="primary" class="shrink-0" to="/login">
        <AppIcon name="enter" />
        Anmelden
      </BaseButton>
    </BaseCard>

    <BaseCard v-if="authStore.ready" class="p-6 flex flex-col gap-4">
      <p class="text-wntrs-muted">
        Wo deine Sucheinstellungen gespeichert werden. Im Browser bleiben sie nur hier, «Nur diese
        Sitzung» vergisst sie beim Schliessen des Tabs, im Konto gelten sie auf allen Geräten.
      </p>
      <OptionButtons
        :model-value="searchStore.scope"
        :options="scopes"
        :labels="storageLabels"
        @update:model-value="searchStore.setScope($event)"
      />
    </BaseCard>
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import { useAuthStore } from '@core/stores/auth.js'
import OptionButtons from '@/components/OptionButtons.vue'
import { storageLabels } from '@/data/settings.js'
import { useSearchStore } from '@/stores/search.js'

export default {
  name: 'AccountSettings',
  components: { AppIcon, BaseButton, BaseCard, OptionButtons },
  data() {
    return {
      storageLabels,
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    searchStore() {
      return useSearchStore()
    },
    scopes() {
      return this.authStore.isAuthenticated
        ? ['browser', 'session', 'account']
        : ['browser', 'session']
    },
  },
}
</script>
