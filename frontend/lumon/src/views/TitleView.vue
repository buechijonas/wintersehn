<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-1 flex-col gap-8 px-6 pt-4 pb-16">
    <p v-if="error && !title" class="text-sm text-error">{{ error }}</p>
    <div v-else-if="!title" class="flex flex-col gap-6 sm:flex-row">
      <div class="skeleton aspect-[2/3] w-48 shrink-0"></div>
      <div class="flex flex-1 flex-col gap-3">
        <div class="skeleton h-10 w-2/3"></div>
        <div class="skeleton h-4 w-1/3"></div>
        <div class="skeleton h-24 w-full"></div>
      </div>
    </div>

    <template v-else>
      <div class="flex flex-col gap-6 sm:flex-row">
        <div
          class="aspect-[2/3] w-40 shrink-0 overflow-hidden rounded-box border border-wntrs-border bg-base-200 sm:w-56"
        >
          <img
            v-if="title.poster"
            :src="title.poster"
            :alt="title.title"
            class="size-full object-cover"
          />
        </div>
        <div class="flex min-w-0 flex-1 flex-col gap-4">
          <div class="flex flex-col gap-1">
            <h1 class="font-display text-4xl font-bold tracking-tighter text-wntrs-title">
              {{ title.title }}
            </h1>
            <p class="text-sm text-wntrs-muted">{{ facts }}</p>
          </div>
          <div v-if="title.genres.length" class="flex flex-wrap gap-2">
            <span v-for="genre in title.genres" :key="genre" class="badge badge-ghost">
              {{ genre }}
            </span>
          </div>
          <p class="max-w-200">{{ title.overview || 'Keine Beschreibung vorhanden.' }}</p>
          <div class="flex flex-wrap items-center gap-3">
            <PlayButton v-if="title.media" :media="title.media" />
            <BaseButton
              :variant="title.saved || title.media ? 'neutral' : 'primary'"
              :disabled="saving"
              @click="toggle"
            >
              <AppIcon :name="title.saved ? 'cross' : 'bookmark'" />
              {{ title.saved ? 'Aus meiner Liste entfernen' : 'Zu meiner Liste' }}
            </BaseButton>
            <span v-if="error" class="text-sm text-error">{{ error }}</span>
          </div>
          <UploadDrop
            v-if="mediaType === 'movie' && !title.media"
            class="max-w-120"
            :target="{ media_type: 'movie', catalog_id: title.catalog_id }"
            @uploaded="reloadTitle"
          />
        </div>
      </div>

      <section v-if="title.seasons.length" class="flex flex-col gap-3">
        <h2 class="text-xs tracking-wide opacity-60">Staffeln</h2>
        <SeasonUpload
          :catalog-id="title.catalog_id"
          :seasons="title.seasons"
          :default-season="activeSeason"
          @uploaded="reloadEpisodes"
        />
        <BaseTabs :tabs="seasonTabs" :active="String(activeSeason)" />
        <EpisodeList :key="episodesKey" :catalog-id="title.catalog_id" :season="activeSeason" />
      </section>

      <section v-if="title.channel" class="flex flex-col gap-3">
        <h2 class="text-xs tracking-wide opacity-60">Läuft bei</h2>
        <BaseCard class="flex flex-wrap items-center justify-between gap-3 p-4">
          <span class="font-medium">{{ title.channel.name }}</span>
          <a
            v-if="title.channel.link"
            :href="title.channel.link"
            target="_blank"
            rel="noopener noreferrer"
            class="flex items-center gap-2 text-sm text-wntrs-muted hover:text-base-content"
          >
            <AppIcon name="share-square" />
            Zur Website
          </a>
        </BaseCard>
      </section>
      <SourceNotice />
    </template>
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import BaseTabs from '@core/components/common/BaseTabs.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import EpisodeList from '@/components/EpisodeList.vue'
import PlayButton from '@/components/PlayButton.vue'
import SeasonUpload from '@/components/SeasonUpload.vue'
import SourceNotice from '@/components/SourceNotice.vue'
import UploadDrop from '@/components/UploadDrop.vue'
import { useLumonStore } from '@/stores/lumon.js'

export default {
  name: 'TitleView',
  components: {
    AppIcon,
    BaseBreadcrumbs,
    BaseButton,
    BaseCard,
    BaseTabs,
    EpisodeList,
    PlayButton,
    SeasonUpload,
    SourceNotice,
    UploadDrop,
  },
  mixins: [asyncActionMixin],
  data() {
    return { title: null, episodesKey: 0 }
  },
  computed: {
    store() {
      return useLumonStore()
    },
    mediaType() {
      return this.$route.meta.mediaType
    },
    breadcrumbs() {
      const parent =
        this.mediaType === 'tv'
          ? { label: 'Serien', to: '/series' }
          : { label: 'Filme', to: '/movies' }
      return [parent, { label: this.title?.title ?? '' }]
    },
    facts() {
      const count = this.title.seasons.length
      const length = count
        ? `${count} ${count === 1 ? 'Staffel' : 'Staffeln'}`
        : this.title.runtime && `${this.title.runtime} Min.`
      const rating = this.title.rating && `★ ${this.title.rating}`
      return [this.title.year, length, rating].filter(Boolean).join(' · ')
    },
    seasonTabs() {
      return this.title.seasons.map((season) => ({
        key: String(season.number),
        label: season.name,
      }))
    },
    activeSeason() {
      const numbers = this.title.seasons.map((season) => season.number)
      const tab = Number(this.$route.query.tab)
      return numbers.includes(tab) ? tab : numbers[0]
    },
  },
  created() {
    this.runAction(async () => {
      this.title = await this.fetchTitle()
    })
  },
  methods: {
    fetchTitle() {
      return this.store.load(
        `/catalog/${this.mediaType}/${this.$route.params.id}/`,
        'Titel konnte nicht geladen werden.',
      )
    },
    reloadEpisodes() {
      this.episodesKey += 1
    },
    reloadTitle() {
      this.runAction(async () => {
        this.title = await this.fetchTitle()
      })
    },
    toggle() {
      this.runAction(async () => {
        if (this.title.saved) {
          await this.store.forget(this.title.saved)
          this.title.saved = null
        } else {
          this.title.saved = (await this.store.save(this.title)).uuid
        }
      })
    },
  },
}
</script>
