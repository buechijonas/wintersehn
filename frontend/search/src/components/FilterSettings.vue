<template>
  <div class="flex flex-col gap-6">
    <DomainListSettings
      v-model:enabled="settings.blocklistEnabled"
      v-model:domains="settings.blocklist"
      title="Blacklist"
      description="Treffer von diesen Seiten werden nie angezeigt. Subdomains sind eingeschlossen."
    />
    <DomainListSettings
      v-model:enabled="settings.allowlistEnabled"
      v-model:domains="settings.allowlist"
      title="Whitelist"
      description="Es werden nur Treffer von diesen Seiten angezeigt. Subdomains sind eingeschlossen."
    />
  </div>
</template>

<script>
import DomainListSettings from '@/components/DomainListSettings.vue'
import { useSearchStore } from '@/stores/search.js'

export default {
  name: 'FilterSettings',
  components: { DomainListSettings },
  computed: {
    settings() {
      return useSearchStore().settings
    },
  },
}
</script>
