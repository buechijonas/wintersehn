<template>
  <div class="flex flex-col gap-3">
    <label
      v-if="!rows.length"
      class="flex cursor-pointer flex-col items-center gap-1 rounded-box border border-dashed p-5 text-center text-sm transition-colors"
      :class="dragging ? 'border-primary bg-primary/5' : 'border-wntrs-border hover:bg-base-200'"
      @dragover.prevent="dragging = true"
      @dragleave="dragging = false"
      @drop.prevent="drop"
    >
      <input type="file" :accept="accept" multiple class="hidden" @change="pick" />
      <span class="flex items-center gap-2">
        <AppIcon name="upload" />
        Folgen hierher ziehen oder auswählen
      </span>
      <span class="text-xs text-wntrs-muted">
        Staffel und Folge werden aus dem Dateinamen erkannt, etwa «S01E03» oder «Folge 3».
      </span>
    </label>

    <BaseCard v-else tag="ul" class="divide-y divide-wntrs-border">
      <li
        v-for="row in rows"
        :key="row.filename"
        class="flex flex-col gap-2 p-3 sm:flex-row sm:items-center"
      >
        <div class="min-w-0 flex-1">
          <p class="truncate text-sm">{{ row.filename }}</p>
          <p class="text-xs" :class="hint(row).tone">{{ hint(row).text }}</p>
          <progress
            v-if="row.progress !== null"
            class="progress progress-primary mt-1 h-1 w-full"
            :value="row.progress"
            max="1"
          ></progress>
        </div>
        <div class="flex shrink-0 gap-2">
          <select
            v-model.number="row.season"
            class="select select-sm w-32"
            :disabled="uploading"
            aria-label="Staffel"
          >
            <option :value="null" disabled>Staffel</option>
            <option v-for="season in seasons" :key="season.number" :value="season.number">
              {{ season.name }}
            </option>
          </select>
          <select
            v-model.number="row.episode"
            class="select select-sm w-28"
            :disabled="uploading || !row.season"
            aria-label="Folge"
          >
            <option :value="null" disabled>Folge</option>
            <option v-for="number in episodeNumbers(row.season)" :key="number" :value="number">
              Folge {{ number }}
            </option>
          </select>
        </div>
      </li>
    </BaseCard>

    <div v-if="rows.length" class="flex flex-wrap items-center gap-2">
      <BaseButton variant="primary" :disabled="!ready || uploading" @click="start">
        <AppIcon name="upload" />
        {{ rows.length === 1 ? 'Folge hochladen' : `${rows.length} Folgen hochladen` }}
      </BaseButton>
      <BaseButton :disabled="uploading" @click="rows = []">
        <AppIcon name="cross" />
        Abbrechen
      </BaseButton>
    </div>
    <p v-if="error" class="text-sm text-error">{{ error }}</p>
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import { useLumonStore } from '@/stores/lumon.js'

export default {
  name: 'SeasonUpload',
  components: { AppIcon, BaseButton, BaseCard },
  mixins: [asyncActionMixin],
  props: {
    tmdbId: { type: Number, required: true },
    seasons: { type: Array, required: true },
    defaultSeason: { type: Number, required: true },
  },
  emits: ['uploaded'],
  data() {
    return {
      accept: '.mp4,.m4v,.webm,.mkv,.mov,video/*',
      dragging: false,
      uploading: false,
      rows: [],
    }
  },
  computed: {
    store() {
      return useLumonStore()
    },
    ready() {
      return this.rows.every((row) => row.season && row.episode)
    },
  },
  methods: {
    drop(event) {
      this.dragging = false
      this.prepare([...event.dataTransfer.files])
    },
    pick(event) {
      this.prepare([...event.target.files])
      event.target.value = ''
    },
    prepare(files) {
      if (!files.length) return
      this.runAction(async () => {
        const detections = await this.store.detect(
          this.tmdbId,
          files.map((file) => file.name),
          this.defaultSeason,
        )
        this.rows = detections.map((detection, index) => ({
          ...detection,
          file: files[index],
          detected: detection,
          progress: null,
          done: false,
        }))
      })
    },
    episodeNumbers(number) {
      const season = this.seasons.find((item) => item.number === number)
      return season ? Array.from({ length: season.episodes }, (_, index) => index + 1) : []
    },
    hint(row) {
      if (row.done) return { text: 'Hochgeladen', tone: 'text-success' }
      if (!row.season || !row.episode)
        return { text: 'Staffel und Folge bitte wählen', tone: 'text-warning' }
      const detected = row.season === row.detected.season && row.episode === row.detected.episode
      const title = detected && row.detected.title ? ` · ${row.detected.title}` : ''
      if (detected && row.detected.exists)
        return { text: `Ersetzt die vorhandene Folge${title}`, tone: 'text-warning' }
      return {
        text: `S${String(row.season).padStart(2, '0')}E${String(row.episode).padStart(2, '0')}${title}`,
        tone: 'text-wntrs-muted',
      }
    },
    start() {
      this.uploading = true
      this.runAction(async () => {
        try {
          for (const row of this.rows.filter((item) => !item.done)) {
            row.progress = 0
            await this.store.upload(
              {
                media_type: 'tv',
                tmdb_id: this.tmdbId,
                season: row.season,
                episode: row.episode,
              },
              row.file,
              (progress) => {
                row.progress = progress
              },
            )
            row.done = true
          }
          this.$emit(
            'uploaded',
            this.rows.map(({ season, episode }) => ({ season, episode })),
          )
          this.rows = []
        } finally {
          this.uploading = false
        }
      })
    },
  },
}
</script>
