<template>
  <div class="flex flex-col gap-6">
    <section>
      <h3 class="text-xl my-4">Zeichen hinter der Adresse</h3>
      <BaseCard tag="ul" class="p-6 flex flex-col gap-3 text-sm">
        <li v-for="entry in ratingLegend" :key="entry.rating" class="flex items-start gap-3">
          <AppIcon
            :name="ratingIcons[entry.rating].name"
            class="mt-0.5"
            :class="ratingIcons[entry.rating].class"
          />
          <span>{{ entry.text }}</span>
        </li>
        <li class="flex items-start gap-3">
          <span class="loading loading-spinner mt-0.5 size-4 text-wntrs-muted"></span>
          <span>Die Bewertung wird gerade geladen.</span>
        </li>
      </BaseCard>
      <p class="text-xs text-wntrs-muted mt-2">
        Ein Klick auf ein Zeichen zeigt, welche Schutzmassnahmen eine Seite hat und welche fehlen.
        Die Bewertungen holt der Server, dein Browser fragt Mozilla nie selbst an.
      </p>
    </section>
    <section>
      <h3 class="text-xl my-4">Unsichere Seiten</h3>
      <BaseCard class="p-6 flex flex-col gap-4">
        <p class="text-sm text-wntrs-muted">
          Gilt für unverschlüsselte Seiten (http) und Seiten, die laut Mozilla Observatory schlecht
          abgesichert sind. Warnen fragt vor dem Öffnen nach, Sperren macht den Link unanklickbar.
        </p>
        <OptionButtons
          v-model="settings.riskyLinks"
          :options="searchChoices.riskyLinks"
          :labels="riskyLinkLabels"
        />
      </BaseCard>
    </section>
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import OptionButtons from '@/components/OptionButtons.vue'
import { ratingIcons, ratingLegend } from '@/data/ratings.js'
import { riskyLinkLabels, searchChoices } from '@/data/settings.js'
import { useSearchStore } from '@/stores/search.js'

export default {
  name: 'SecuritySettings',
  components: { AppIcon, BaseCard, OptionButtons },
  data() {
    return {
      ratingIcons,
      ratingLegend,
      riskyLinkLabels,
      searchChoices,
    }
  },
  computed: {
    settings() {
      return useSearchStore().settings
    },
  },
}
</script>
