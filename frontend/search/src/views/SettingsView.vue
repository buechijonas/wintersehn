<template>
  <div class="mx-auto flex w-full max-w-160 flex-1 flex-col px-6 pb-16">
    <h2 class="text-xl font-light my-6">Einstellungen</h2>
    <BaseTabs :tabs="settingsTabs" :active="activeTab" />
    <div class="mt-6">
      <AccountSettings v-if="activeTab === 'account'" />
      <template v-else-if="activeTab === 'appearance'">
        <AppearanceSettings />
        <HandednessSettings />
      </template>
      <PrivacySettings v-else-if="activeTab === 'privacy'" />
      <FilterSettings v-else-if="activeTab === 'filter'" />
      <DonateSettings v-else />
    </div>
  </div>
</template>

<script>
import AppearanceSettings from '@core/components/common/AppearanceSettings.vue'
import BaseTabs from '@core/components/common/BaseTabs.vue'
import AccountSettings from '@/components/AccountSettings.vue'
import DonateSettings from '@/components/DonateSettings.vue'
import FilterSettings from '@/components/FilterSettings.vue'
import HandednessSettings from '@/components/HandednessSettings.vue'
import PrivacySettings from '@/components/PrivacySettings.vue'
import { settingsTabs } from '@/data/settings.js'

export default {
  name: 'SettingsView',
  components: {
    AppearanceSettings,
    BaseTabs,
    AccountSettings,
    DonateSettings,
    FilterSettings,
    HandednessSettings,
    PrivacySettings,
  },
  data() {
    return {
      settingsTabs,
    }
  },
  computed: {
    activeTab() {
      const tab = this.$route.query.tab
      return settingsTabs.some(({ key }) => key === tab) ? tab : 'account'
    },
  },
}
</script>
