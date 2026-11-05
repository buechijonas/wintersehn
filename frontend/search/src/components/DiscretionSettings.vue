<template>
  <section>
    <h3 class="text-xl my-4">Sichtschutz</h3>
    <BaseCard tag="ul" class="divide-y divide-wntrs-border">
      <li v-for="option in options" :key="option.key">
        <label class="flex cursor-pointer items-center justify-between gap-4 p-4">
          <span class="flex flex-col">
            <span>{{ option.label }}</span>
            <span class="text-sm text-wntrs-muted">{{ option.description }}</span>
          </span>
          <input v-model="settings[option.key]" type="checkbox" class="toggle toggle-primary" />
        </label>
      </li>
    </BaseCard>
  </section>

  <section v-if="onion">
    <h3 class="text-xl my-4">Onion-Adresse</h3>
    <BaseCard class="p-6 flex flex-col gap-4">
      <p class="text-sm text-wntrs-muted">
        Im Tor Browser erreichst du diese Suche auch als Onion-Dienst. Dann sieht nicht einmal der
        Server deine IP-Adresse.
      </p>
      <a :href="onion" rel="noopener noreferrer" class="link link-hover break-all text-sm">
        {{ onion }}
      </a>
    </BaseCard>
  </section>

  <section>
    <h3 class="text-xl my-4">Lokale Daten</h3>
    <BaseCard class="p-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <p class="text-sm text-wntrs-muted min-w-0">
        Löscht alle Einstellungen, die diese Suche in deinem Browser gespeichert hat, auch
        Darstellung und Händigkeit. Einstellungen im Konto bleiben erhalten.
      </p>
      <BaseButton variant="error" outline class="shrink-0" @click="searchStore.clearLocalData()">
        <AppIcon name="trash" />
        Alles löschen
      </BaseButton>
    </BaseCard>
  </section>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import { useSearchStore } from '@/stores/search.js'

export default {
  name: 'DiscretionSettings',
  components: { AppIcon, BaseButton, BaseCard },
  data() {
    return {
      options: [
        {
          key: 'privacyScreen',
          label: 'Unscharf im Hintergrund',
          description:
            'Die Suche wird unscharf, sobald du in ein anderes Fenster oder einen anderen Tab wechselst.',
        },
        {
          key: 'panicKey',
          label: 'Schnell verlassen',
          description:
            'Zweimal Esc wechselt sofort zu Wikipedia. Die Suche bleibt nicht als letzte Seite zurück.',
        },
      ],
    }
  },
  computed: {
    searchStore() {
      return useSearchStore()
    },
    settings() {
      return this.searchStore.settings
    },
    onion() {
      if (window.location.hostname.endsWith('.onion')) return null
      return this.searchStore.onion
    },
  },
}
</script>
