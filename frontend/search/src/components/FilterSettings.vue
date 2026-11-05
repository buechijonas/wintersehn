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
    <section>
      <h3 class="text-xl my-4">Vorlagen</h3>
      <BaseCard class="p-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <p class="text-wntrs-muted min-w-0">
          Setzt Google, Meta, Amazon, Apple, Microsoft, TikTok und X auf die Blacklist.
        </p>
        <BaseButton class="shrink-0" @click="blockBigTech">
          <AppIcon name="link-slash-alt" />
          Big Tech ausblenden
        </BaseButton>
      </BaseCard>
    </section>
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import DomainListSettings from '@/components/DomainListSettings.vue'
import { bigTechDomains } from '@/data/settings.js'
import { useSearchStore } from '@/stores/search.js'

export default {
  name: 'FilterSettings',
  components: { AppIcon, BaseButton, BaseCard, DomainListSettings },
  computed: {
    settings() {
      return useSearchStore().settings
    },
  },
  methods: {
    blockBigTech() {
      this.settings.blocklist = [...new Set([...this.settings.blocklist, ...bigTechDomains])]
      this.settings.blocklistEnabled = true
    },
  },
}
</script>
