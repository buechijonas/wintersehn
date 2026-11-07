<template>
  <div class="mx-auto flex w-full max-w-160 flex-1 flex-col px-6 pb-16">
    <h2 class="text-xl font-light my-6">Einstellungen</h2>
    <BaseTabs :tabs="tabs" :active="activeTab" />
    <div class="mt-6">
      <AccountCard v-if="activeTab === 'account'" />
      <AppearanceSettings v-else-if="activeTab === 'appearance'" />
      <LegalSettings v-else />
    </div>
  </div>
</template>

<script>
import AccountCard from '@core/components/common/AccountCard.vue'
import AppearanceSettings from '@core/components/common/AppearanceSettings.vue'
import BaseTabs from '@core/components/common/BaseTabs.vue'
import LegalSettings from '@core/components/common/LegalSettings.vue'

export default {
  name: 'SettingsView',
  components: { AccountCard, AppearanceSettings, BaseTabs, LegalSettings },
  inject: ['app'],
  computed: {
    tabs() {
      return [
        { key: 'account', label: 'Konto' },
        { key: 'appearance', label: 'Darstellung' },
        ...(this.app.legalLinks.length ? [{ key: 'legal', label: 'Rechtliches' }] : []),
      ]
    },
    activeTab() {
      const tab = this.$route.query.tab
      return this.tabs.some(({ key }) => key === tab) ? tab : 'account'
    },
  },
}
</script>
