<template>
  <AtlasPage :breadcrumbs="breadcrumbs" :loading="!learningSet" :error="error">
    <template #actions>
      <LearningSetActions v-if="learningSet" :learning-set="learningSet" @error="error = $event" />
    </template>
    <div class="flex flex-wrap items-baseline justify-between gap-2">
      <h2 class="text-xl font-light">Karten</h2>
      <span class="text-sm text-wntrs-muted">{{ progress }}</span>
    </div>
    <FlashcardForm @submit="create" />
    <ul class="flex flex-col gap-4">
      <li v-for="card in learningSet.cards" :key="card.uuid">
        <FlashcardForm
          v-if="editing === card.uuid"
          :card="card"
          @submit="update(card, $event)"
          @cancel="editing = null"
        />
        <BaseCard v-else class="flex flex-col gap-4 rounded-box p-4 sm:flex-row sm:items-start">
          <FlashcardView :card="card" class="flex-1" />
          <div class="flex shrink-0 gap-2">
            <EditButton size="md" @click="editing = card.uuid" />
            <DeleteButton size="md" @click="remove(card)" />
          </div>
        </BaseCard>
      </li>
    </ul>
  </AtlasPage>
</template>

<script>
import BaseCard from '@core/components/common/BaseCard.vue'
import DeleteButton from '@core/components/common/DeleteButton.vue'
import EditButton from '@core/components/common/EditButton.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import AtlasPage from '@/components/AtlasPage.vue'
import LearningSetActions from '@/components/LearningSetActions.vue'
import FlashcardForm from '@/components/FlashcardForm.vue'
import FlashcardView from '@/components/FlashcardView.vue'
import { learningSetBreadcrumbs } from '@/lib/breadcrumbs.js'
import { cardProgress } from '@/lib/progress.js'
import { useAtlasStore } from '@/stores/atlas.js'

export default {
  name: 'CardsView',
  components: {
    AtlasPage,
    BaseCard,
    DeleteButton,
    EditButton,
    FlashcardForm,
    FlashcardView,
    LearningSetActions,
  },
  mixins: [asyncActionMixin],
  data() {
    return {
      learningSet: null,
      editing: null,
    }
  },
  computed: {
    store() {
      return useAtlasStore()
    },
    path() {
      return `/learning-sets/${this.$route.params.uuid}/`
    },
    breadcrumbs() {
      return learningSetBreadcrumbs(this.learningSet, 'Karten')
    },
    progress() {
      return cardProgress(this.learningSet)
    },
  },
  mounted() {
    this.fetch()
  },
  methods: {
    fetch() {
      return this.runAction(async () => {
        this.learningSet = await this.store.load(this.path, 'Lernset konnte nicht geladen werden.')
      })
    },
    create(card) {
      return this.runAction(async () => {
        await this.store.send(
          `${this.path}cards/`,
          'POST',
          card,
          'Karte konnte nicht erstellt werden.',
        )
        await this.fetch()
      })
    },
    update(card, data) {
      return this.runAction(async () => {
        await this.store.send(`/cards/${card.uuid}/`, 'PATCH', data, 'Speichern fehlgeschlagen.')
        this.editing = null
        await this.fetch()
      })
    },
    remove(card) {
      return this.runAction(async () => {
        await this.store.remove(`/cards/${card.uuid}/`, 'Löschen fehlgeschlagen.')
        await this.fetch()
      })
    },
  },
}
</script>
