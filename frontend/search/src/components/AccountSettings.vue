<template>
  <div class="flex flex-col gap-6">
    <AccountCard />

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
import AccountCard from '@core/components/common/AccountCard.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import { useAuthStore } from '@core/stores/auth.js'
import OptionButtons from '@/components/OptionButtons.vue'
import { storageLabels } from '@/data/settings.js'
import { useSearchStore } from '@/stores/search.js'

export default {
  name: 'AccountSettings',
  components: { AccountCard, BaseCard, OptionButtons },
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
