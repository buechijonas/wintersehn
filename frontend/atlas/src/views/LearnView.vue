<template>
  <AtlasPage :breadcrumbs="breadcrumbs" :loading="!learningSet || !queue" :error="error">
    <template #actions>
      <LearningSetActions v-if="learningSet" :learning-set="learningSet" @error="error = $event" />
    </template>
    <div class="mx-auto flex w-full max-w-160 flex-col gap-6">
      <template v-if="current">
        <div class="flex flex-col gap-2">
          <div class="flex justify-between text-sm text-wntrs-muted">
            <span>{{ stageLabels[current.stage] }}</span>
            <span>{{ done }} / {{ total }} gelernt</span>
          </div>
          <progress class="progress progress-primary w-full" :value="done" :max="total"></progress>
        </div>

        <BaseCard class="flex min-h-48 items-center justify-center rounded-box p-8">
          <CardFace
            label="Vorderseite"
            :text="current.card.front"
            :image="current.card.front_image_url"
          />
        </BaseCard>

        <ul v-if="current.stage === 'choice'" class="grid gap-2 sm:grid-cols-2">
          <li v-for="option in current.card.options" :key="option.uuid">
            <BaseCard
              tag="button"
              type="button"
              :disabled="Boolean(result) || saving"
              class="flex h-full w-full cursor-pointer flex-col items-center gap-2 rounded-box p-4 text-center transition-colors hover:bg-base-200 disabled:cursor-default"
              :class="optionClass(option)"
              @click="answer(option.uuid)"
            >
              <img
                v-if="option.image_url"
                :src="option.image_url"
                alt=""
                class="max-h-24 rounded-box object-contain"
              />
              <span class="whitespace-pre-line">{{ option.back }}</span>
            </BaseCard>
          </li>
        </ul>

        <form v-else class="flex gap-2" @submit.prevent="result ? next() : answer(typed)">
          <input
            v-model="typed"
            type="text"
            aria-label="Rückseite schreiben"
            placeholder="Rückseite schreiben"
            :readonly="Boolean(result)"
            class="input w-full border-wntrs-border focus:border-primary focus:outline-none"
          />
          <BaseButton
            v-if="!result"
            type="submit"
            variant="primary"
            :disabled="saving || !typed.trim()"
          >
            <AppIcon name="check-circle" />
            Prüfen
          </BaseButton>
        </form>

        <div v-if="result" class="flex flex-col gap-4">
          <div
            role="status"
            class="alert alert-soft"
            :class="result.correct ? 'alert-success' : 'alert-error'"
          >
            <AppIcon :name="result.correct ? 'check-circle' : 'octagon-xmark'" />
            <span v-if="result.correct">Richtig.</span>
            <span v-else>Richtig wäre: {{ result.back }}</span>
          </div>
          <BaseButton variant="primary" class="self-end" @click="next">
            Weiter
            <AppIcon name="angle-left" class="rotate-180" />
          </BaseButton>
        </div>
      </template>

      <BaseCard v-else class="flex flex-col items-center gap-4 rounded-box p-8 text-center">
        <AppIcon name="check-circle" class="size-10! text-primary" />
        <p class="text-xl text-wntrs-title">Runde geschafft</p>
        <p class="text-wntrs-muted">{{ total }} Karten gelernt, {{ mistakes }} Fehler unterwegs.</p>
        <div class="grid w-full grid-cols-2 gap-2 sm:flex sm:w-auto">
          <BaseButton :to="`/learning-sets/${$route.params.uuid}`">
            <AppIcon name="angle-left" />
            Lernmodus
          </BaseButton>
          <BaseButton variant="primary" @click="start">
            <AppIcon name="brain" />
            Nochmals
          </BaseButton>
        </div>
      </BaseCard>
    </div>
  </AtlasPage>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import AtlasPage from '@/components/AtlasPage.vue'
import CardFace from '@/components/CardFace.vue'
import LearningSetActions from '@/components/LearningSetActions.vue'
import { learningSetBreadcrumbs } from '@/lib/breadcrumbs.js'
import { useAtlasStore } from '@/stores/atlas.js'

function firstStage(card) {
  if (card.options.length > 1) return 'choice'
  return card.writable ? 'write' : null
}

export default {
  name: 'LearnView',
  components: { AppIcon, AtlasPage, BaseButton, BaseCard, CardFace, LearningSetActions },
  mixins: [asyncActionMixin],
  data() {
    return {
      learningSet: null,
      queue: null,
      result: null,
      chosen: null,
      typed: '',
      total: 0,
      done: 0,
      mistakes: 0,
      stageLabels: { choice: 'Antwort wählen', write: 'Rückseite schreiben' },
    }
  },
  computed: {
    store() {
      return useAtlasStore()
    },
    path() {
      return `/learning-sets/${this.$route.params.uuid}/`
    },
    current() {
      return this.queue?.[0] ?? null
    },
    breadcrumbs() {
      return learningSetBreadcrumbs(this.learningSet, 'Lernen')
    },
  },
  mounted() {
    this.runAction(async () => {
      this.learningSet = await this.store.load(this.path, 'Lernset konnte nicht geladen werden.')
    })
    this.start()
  },
  methods: {
    start() {
      return this.runAction(async () => {
        const cards = await this.store.load(
          `${this.path}quiz/`,
          'Karten konnten nicht geladen werden.',
        )
        this.queue = cards
          .map((card) => ({ card, stage: firstStage(card) }))
          .filter(({ stage }) => stage)
        this.total = this.queue.length
        this.done = 0
        this.mistakes = 0
        this.result = null
        this.typed = ''
      })
    },
    answer(value) {
      return this.runAction(async () => {
        const { card, stage } = this.current
        this.chosen = value
        this.result = await this.store.send(
          `/cards/${card.uuid}/answer/`,
          'POST',
          { mode: stage, answer: value },
          'Antwort konnte nicht geprüft werden.',
        )
      })
    },
    next() {
      const [item, ...rest] = this.queue
      if (!this.result.correct) {
        this.mistakes += 1
        this.queue = [...rest, item]
      } else if (item.stage === 'choice' && item.card.writable) {
        this.queue = [...rest, { ...item, stage: 'write' }]
      } else {
        this.done += 1
        this.queue = rest
      }
      this.result = null
      this.typed = ''
    },
    optionClass(option) {
      if (!this.result) return ''
      if (option.uuid === this.current.card.uuid) return 'border-success! bg-success/10'
      return option.uuid === this.chosen ? 'border-error! bg-error/10' : 'opacity-60'
    },
  },
}
</script>
