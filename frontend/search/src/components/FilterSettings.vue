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
      :locked="childProtection.required"
      title="Whitelist"
      description="Es werden nur Treffer von diesen Seiten angezeigt. Subdomains sind eingeschlossen."
    >
      <template #notice>
        <p v-if="childProtection.required" class="flex items-start gap-2 text-sm">
          <AppIcon name="shield-check" class="mt-0.5 text-wntrs-secure" />
          Kinderschutz ist aktiv, weil dein Konto jünger als 18 Jahre ist. Ab 18 kannst du die Liste
          ändern, ausschalten oder leeren.
        </p>
      </template>
    </DomainListSettings>
    <section>
      <h3 class="text-xl my-4">Vorlagen</h3>
      <BaseCard tag="ul" class="divide-y divide-wntrs-border">
        <li
          v-for="template in templates"
          :key="template.key"
          class="flex flex-col gap-4 p-6 sm:flex-row sm:items-center sm:justify-between"
        >
          <span class="flex min-w-0 flex-col">
            <span>{{ template.label }}</span>
            <span class="text-sm text-wntrs-muted">{{ template.description }}</span>
          </span>
          <BaseButton
            class="shrink-0"
            :disabled="template.list === 'allowlist' && childProtection.required"
            @click="apply(template)"
          >
            <AppIcon :name="template.icon" />
            Übernehmen
          </BaseButton>
        </li>
      </BaseCard>
    </section>
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import DomainListSettings from '@/components/DomainListSettings.vue'
import { filterTemplates } from '@/data/settings.js'
import { useSearchStore } from '@/stores/search.js'

export default {
  name: 'FilterSettings',
  components: { AppIcon, BaseButton, BaseCard, DomainListSettings },
  computed: {
    searchStore() {
      return useSearchStore()
    },
    settings() {
      return this.searchStore.settings
    },
    childProtection() {
      return this.searchStore.childProtection
    },
    templates() {
      return filterTemplates.map((template) => ({
        ...template,
        domains: template.domains ?? this.childProtection.domains,
      }))
    },
  },
  methods: {
    apply({ list, domains }) {
      this.settings[list] = [...new Set([...this.settings[list], ...domains])]
      this.settings[`${list}Enabled`] = true
    },
  },
}
</script>
