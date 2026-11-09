<template>
  <p v-if="error" class="text-sm text-error">{{ error }}</p>
  <div v-else-if="!episodes" class="flex flex-col gap-3">
    <div v-for="n in 4" :key="n" class="skeleton h-24"></div>
  </div>
  <BaseCard v-else tag="ul" class="divide-y divide-wntrs-border">
    <li v-for="episode in episodes" :key="episode.number" class="flex gap-4 p-4">
      <div
        class="relative hidden aspect-video w-40 shrink-0 overflow-hidden rounded-box bg-base-200 sm:block"
      >
        <img
          v-if="episode.still"
          :src="episode.still"
          alt=""
          loading="lazy"
          class="size-full object-cover"
        />
        <span v-else class="flex size-full items-center justify-center text-2xl text-wntrs-muted">
          {{ episode.number }}
        </span>
        <progress
          v-if="resumable(episode.media)"
          class="progress progress-primary absolute right-0 bottom-0 left-0 h-1 rounded-none"
          :value="episode.media.position"
          :max="episode.media.duration"
        />
      </div>
      <div class="flex min-w-0 flex-1 flex-col gap-1">
        <p class="font-medium">{{ episode.number }}. {{ episode.title }}</p>
        <p class="text-xs text-wntrs-muted">{{ facts(episode) }}</p>
        <p class="line-clamp-2 text-sm text-wntrs-muted">{{ episode.overview }}</p>
        <div v-if="episode.media" class="mt-1 flex flex-wrap items-center gap-3">
          <PlayButton :media="episode.media" size="sm" :with-subtitle="false" />
          <label class="flex cursor-pointer items-center gap-2 text-sm">
            <input
              type="checkbox"
              class="checkbox checkbox-sm checkbox-primary"
              :checked="episode.media.played"
              :disabled="saving"
              @change="markPlayed(episode, $event.target.checked)"
            />
            Gesehen
          </label>
        </div>
        <UploadDrop
          v-else
          class="mt-1 max-w-100"
          compact
          :label="`${code(episode.number)} hochladen`"
          :target="{ media_type: 'tv', catalog_id: catalogId, season, episode: episode.number }"
          @uploaded="load"
        />
      </div>
    </li>
  </BaseCard>
</template>

<script>
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import PlayButton from '@/components/PlayButton.vue'
import UploadDrop from '@/components/UploadDrop.vue'
import { resumable } from '@/lib/time.js'
import { useLumonStore } from '@/stores/lumon.js'

export default {
  name: 'EpisodeList',
  components: { BaseCard, PlayButton, UploadDrop },
  mixins: [asyncActionMixin],
  props: {
    catalogId: { type: Number, required: true },
    season: { type: Number, required: true },
  },
  data() {
    return { episodes: null }
  },
  computed: {
    store() {
      return useLumonStore()
    },
  },
  watch: {
    season: { handler: 'load', immediate: true },
  },
  methods: {
    resumable,
    fetchEpisodes() {
      return this.store.load(
        `/catalog/tv/${this.catalogId}/seasons/${this.season}/`,
        'Folgen konnten nicht geladen werden.',
      )
    },
    load() {
      this.episodes = null
      this.runAction(async () => {
        this.episodes = await this.fetchEpisodes()
      })
    },
    code(number) {
      return `S${String(this.season).padStart(2, '0')}E${String(number).padStart(2, '0')}`
    },
    facts(episode) {
      return [episode.runtime && `${episode.runtime} Min.`, episode.air_date]
        .filter(Boolean)
        .join(' · ')
    },
    markPlayed(episode, played) {
      this.runAction(async () => {
        await this.store.progress(episode.media.id, { played, position: 0 })
        episode.media.played = played
        episode.media.position = 0
      })
    },
  },
}
</script>
