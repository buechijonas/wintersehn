<template>
  <div class="flex flex-col gap-10">
    <section>
      <h3 class="text-xl my-4">Schutz</h3>
      <BaseCard tag="ul" class="p-6 flex flex-col gap-3">
        <li class="flex items-start gap-3">
          <AppIcon name="check-circle" class="mt-0.5 text-primary" />
          <span>{{ networkStatus }}</span>
        </li>
        <li v-for="protection in protections" :key="protection" class="flex items-start gap-3">
          <AppIcon name="check-circle" class="mt-0.5 text-primary" />
          <span>{{ protection }}</span>
        </li>
      </BaseCard>
    </section>

    <section>
      <h3 class="text-xl my-4">So privat ist diese Suche</h3>
      <div class="flex flex-col gap-3 text-sm text-wntrs-slate leading-relaxed">
        <p>
          Diese Suche ist ein eigener Vermittler zwischen dir und den Suchmaschinen. Sie fragt
          Anbieter wie Brave, Mojeek oder Qwant in deinem Auftrag an. Die Anbieter erfahren dabei
          nie, wer du bist: Sie sehen weder deine IP-Adresse noch Cookies, Browserdaten oder einen
          Verlauf. Standardmässig gehen alle Anfragen zusätzlich über das Tor-Netzwerk, jeder
          Anbieter über einen eigenen, regelmässig wechselnden Weg. So sieht ein Anbieter nicht
          einmal den Server dieser Suche und kann deine Anfragen auch nicht mit denen bei anderen
          Anbietern verknüpfen. Unter «Netzwerk» kannst du stattdessen einen VPN-Anbieter, einen
          eigenen Proxy oder den direkten Weg wählen.
        </p>
        <p>
          Auch der Inhaber dieser Suche erhält deine Daten nicht. Suchbegriffe werden nicht
          gespeichert, nicht protokolliert und nicht ausgewertet; sie werden nur im Moment der Suche
          weitergereicht und danach verworfen. Es gibt kein Suchprofil, keine Werbung und keine
          Statistiken. Deine Einstellungen liegen in deinem Browser, ausser du speicherst sie
          bewusst in deinem Konto. Bilder werden über die Suche geladen, damit auch fremde
          Bildserver dich nicht sehen, und beim Öffnen eines Treffers erfährt die Zielseite nicht,
          woher du kommst.
        </p>
        <p>
          Eine Grenze bleibt: Den Suchbegriff selbst sehen die Anbieter, nur nicht, von wem er
          stammt. Wer Namen, Adressen oder andere persönliche Angaben eintippt, verrät diese also
          selbst. Sobald du einen Treffer öffnest, gelten die Regeln jener Seite.
        </p>
      </div>
    </section>

    <section>
      <h3 class="text-xl my-4">Netzwerk</h3>
      <BaseCard class="p-6 flex flex-col gap-4">
        <p class="text-sm text-wntrs-muted">{{ networkDescriptions[network] }}</p>
        <OptionButtons
          :model-value="network"
          :options="searchStore.networks"
          :labels="networkLabels"
          @update:model-value="save({ network: $event })"
        />
        <p
          v-if="searchStore.networks.length < searchChoices.network.length"
          class="text-sm text-wntrs-muted"
        >
          Nicht alle Netzwerke sind auf diesem Server eingerichtet.
        </p>
      </BaseCard>
    </section>

    <section>
      <h3 class="text-xl my-4">Suchanbieter</h3>
      <p class="text-sm text-wntrs-muted mb-4">
        Nur die gewählten Anbieter erhalten deine Suchanfrage. Weniger Anbieter heisst weniger
        Empfänger, mehr Anbieter heisst, dass keiner alle Treffer allein bestimmt.
      </p>
      <BaseCard tag="ul" class="divide-y divide-wntrs-border">
        <li v-for="engine in searchChoices.engines" :key="engine">
          <label class="flex cursor-pointer items-center justify-between gap-4 p-4">
            <span class="flex flex-col">
              <span>{{ engineLabels[engine].label }}</span>
              <span class="text-sm text-wntrs-muted">{{ engineLabels[engine].description }}</span>
            </span>
            <input
              type="checkbox"
              class="toggle toggle-primary"
              :checked="settings.engines.includes(engine)"
              :disabled="isLastEngine(engine)"
              @change="toggleEngine(engine)"
            />
          </label>
        </li>
      </BaseCard>
    </section>

    <section>
      <h3 class="text-xl my-4">Sprache an Anbieter</h3>
      <BaseCard class="p-6 flex flex-col gap-4">
        <p class="text-sm text-wntrs-muted">
          «Keine» verrät den Anbietern nichts über deine Sprache. Mit einer Sprache werden Treffer
          passender, die Anfrage aber leichter zuzuordnen.
        </p>
        <OptionButtons
          :model-value="settings.language"
          :options="searchChoices.language"
          :labels="languageLabels"
          @update:model-value="save({ language: $event })"
        />
      </BaseCard>
    </section>

    <section>
      <h3 class="text-xl my-4">Abfrage</h3>
      <BaseCard class="p-6 flex flex-col gap-4">
        <p class="text-sm text-wntrs-muted">
          POST hält den Suchbegriff aus Adresse, Browserverlauf und Logs heraus. GET schreibt ihn in
          die Adresse: Treffer lassen sich dann teilen und neu laden.
        </p>
        <OptionButtons
          :model-value="settings.method"
          :options="searchChoices.method"
          :labels="methodLabels"
          @update:model-value="save({ method: $event })"
        />
      </BaseCard>
    </section>

    <section>
      <h3 class="text-xl my-4">Treffer</h3>
      <BaseCard class="p-6 flex flex-col gap-6">
        <div class="flex flex-col gap-3">
          <p class="text-sm text-wntrs-muted">
            Weitere Treffer seitenweise oder beim Scrollen laden.
          </p>
          <OptionButtons
            :model-value="settings.pagination"
            :options="searchChoices.pagination"
            :labels="paginationLabels"
            @update:model-value="save({ pagination: $event })"
          />
        </div>
        <div class="flex flex-col gap-3">
          <p class="text-sm text-wntrs-muted">
            Länge einer Seite. Längere Seiten brauchen mehr Anfragen und laden langsamer.
          </p>
          <OptionButtons
            :model-value="settings.pageLength"
            :options="searchChoices.pageLength"
            :labels="pageLengthLabels"
            @update:model-value="save({ pageLength: $event })"
          />
        </div>
        <div class="flex flex-col gap-3">
          <p class="text-sm text-wntrs-muted">
            Wie lange auf langsame Anbieter gewartet wird. Schnell zeigt Treffer nach höchstens 3
            Sekunden, Gründlich wartet bis zu 10 Sekunden und bringt dafür mehr Anbieter.
          </p>
          <OptionButtons
            :model-value="settings.timeout"
            :options="searchChoices.timeout"
            :labels="timeoutLabels"
            @update:model-value="save({ timeout: $event })"
          />
        </div>
      </BaseCard>
    </section>
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import OptionButtons from '@/components/OptionButtons.vue'
import {
  engineLabels,
  languageLabels,
  methodLabels,
  pageLengthLabels,
  paginationLabels,
  networkDescriptions,
  networkLabels,
  protections,
  searchChoices,
  timeoutLabels,
} from '@/data/settings.js'
import { useSearchStore } from '@/stores/search.js'

export default {
  name: 'PrivacySettings',
  components: { AppIcon, BaseCard, OptionButtons },
  data() {
    return {
      engineLabels,
      languageLabels,
      methodLabels,
      pageLengthLabels,
      paginationLabels,
      protections,
      searchChoices,
      timeoutLabels,
      networkDescriptions,
      networkLabels,
    }
  },
  computed: {
    searchStore() {
      return useSearchStore()
    },
    settings() {
      return this.searchStore.settings
    },
    network() {
      return this.searchStore.activeNetwork()
    },
    networkStatus() {
      if (this.network !== 'tor') return `Anfragen laufen über: ${networkLabels[this.network]}.`
      if (import.meta.env.PROD) return 'Alle Anfragen laufen über Tor.'
      return 'Tor ist in dieser Entwicklungsumgebung nicht aktiv.'
    },
  },
  methods: {
    isLastEngine(engine) {
      return this.settings.engines.length === 1 && this.settings.engines.includes(engine)
    },
    toggleEngine(engine) {
      const engines = this.settings.engines.includes(engine)
        ? this.settings.engines.filter((item) => item !== engine)
        : [...this.settings.engines, engine]
      return this.save({ engines })
    },
    save(changes) {
      Object.assign(this.settings, changes)
    },
  },
}
</script>
