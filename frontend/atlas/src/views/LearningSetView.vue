<template>
  <AtlasPage :breadcrumbs="breadcrumbs" :loading="!learningSet" :error="error">
    <template #actions>
      <LearningSetActions v-if="learningSet" :learning-set="learningSet" @error="error = $event" />
    </template>
    <div class="flex flex-wrap items-baseline justify-between gap-2">
      <h2 class="text-xl font-light">{{ learningSet.title }}</h2>
      <span class="text-sm text-wntrs-muted">{{ progress }}</span>
    </div>
    <BaseCard
      v-if="!learningSet.card_count"
      class="flex flex-col items-center gap-4 rounded-box p-8 text-center"
    >
      <p class="text-wntrs-muted">Dieses Lernset hat noch keine Karten.</p>
      <BaseButton variant="primary" :to="`/learning-sets/${learningSet.uuid}/cards`">
        <AppIcon name="plus" />
        Karten hinzufügen
      </BaseButton>
    </BaseCard>
    <ul v-else class="grid gap-4 sm:grid-cols-2">
      <li v-for="mode in modes" :key="mode.path">
        <BaseCard
          tag="RouterLink"
          :to="`/learning-sets/${learningSet.uuid}/${mode.path}`"
          class="flex h-full flex-col gap-3 rounded-box p-6 transition-colors hover:bg-base-200"
        >
          <AppIcon :name="mode.icon" class="size-8! text-primary" />
          <span class="text-lg text-wntrs-title">{{ mode.label }}</span>
          <span class="text-sm text-wntrs-muted">{{ mode.description }}</span>
        </BaseCard>
      </li>
    </ul>
  </AtlasPage>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import AtlasPage from '@/components/AtlasPage.vue'
import LearningSetActions from '@/components/LearningSetActions.vue'
import { learningSetBreadcrumbs } from '@/lib/breadcrumbs.js'
import { cardProgress } from '@/lib/progress.js'
import { useAtlasStore } from '@/stores/atlas.js'

export default {
  name: 'LearningSetView',
  components: { AppIcon, AtlasPage, BaseButton, BaseCard, LearningSetActions },
  mixins: [asyncActionMixin],
  data() {
    return {
      learningSet: null,
      modes: [
        {
          path: 'browse',
          label: 'Karten blättern',
          icon: 'cards-blank',
          description: 'Karten der Reihe nach anschauen und umdrehen, ohne Bewertung.',
        },
        {
          path: 'learn',
          label: 'Lernen',
          icon: 'brain',
          description: 'Zuerst aus vier Antworten wählen, dann die Rückseite selbst schreiben.',
        },
      ],
    }
  },
  computed: {
    breadcrumbs() {
      return learningSetBreadcrumbs(this.learningSet)
    },
    progress() {
      return cardProgress(this.learningSet)
    },
  },
  mounted() {
    this.runAction(async () => {
      this.learningSet = await useAtlasStore().load(
        `/learning-sets/${this.$route.params.uuid}/`,
        'Lernset konnte nicht geladen werden.',
      )
    })
  },
}
</script>
