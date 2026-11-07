<template>
  <div
    tabindex="0"
    class="fixed inset-0 z-50 bg-black text-white outline-none select-none"
    :class="{ 'cursor-none': !controlsVisible }"
    @mousemove="wake"
    @keydown="shortcut"
    @fullscreenchange="fullscreen = !fullscreen"
  >
    <video
      v-if="media"
      class="absolute inset-0 size-full object-contain"
      :src="media.stream"
      autoplay
      playsinline
      @loadedmetadata="attach"
      @timeupdate="track"
      @play="playing = true"
      @pause="pause"
      @waiting="buffering = true"
      @playing="buffering = false"
      @volumechange="syncVolume"
      @ended="finish"
      @click="toggle"
      @dblclick="toggleFullscreen"
    ></video>

    <div v-if="!media || buffering" class="absolute inset-0 flex items-center justify-center">
      <span v-if="!error" class="loading loading-spinner loading-xl text-primary"></span>
      <p v-else class="text-error">{{ error }}</p>
    </div>

    <button
      v-else-if="!playing"
      type="button"
      aria-label="Abspielen"
      class="absolute top-1/2 left-1/2 flex size-20 -translate-1/2 items-center justify-center rounded-full bg-primary text-primary-content shadow-lg transition-transform hover:scale-110"
      @click="toggle"
    >
      <AppIcon name="play" class="size-8!" />
    </button>

    <div
      class="pointer-events-none absolute inset-0 flex flex-col justify-between transition-opacity duration-300"
      :class="controlsVisible ? 'opacity-100' : 'opacity-0'"
    >
      <div
        class="pointer-events-auto flex items-center gap-4 bg-gradient-to-b from-black/80 to-transparent px-6 pt-5 pb-16"
      >
        <button type="button" aria-label="Zurück" class="control" @click="$router.back()">
          <AppIcon name="angle-left" class="size-6!" />
        </button>
        <div v-if="media" class="min-w-0">
          <p class="truncate text-lg font-semibold">{{ media.title }}</p>
          <p v-if="media.subtitle" class="truncate text-sm text-white/70">{{ media.subtitle }}</p>
        </div>
      </div>

      <div
        class="pointer-events-auto flex flex-col gap-3 bg-gradient-to-t from-black/80 to-transparent px-6 pt-16 pb-5"
      >
        <div class="flex items-center gap-4">
          <input
            type="range"
            class="range range-primary range-xs flex-1 [--range-bg:rgb(255_255_255/0.25)]"
            min="0"
            :max="duration || 0"
            step="1"
            :value="position"
            aria-label="Position"
            @input="seek($event.target.value)"
          />
          <span class="w-16 text-right text-sm tabular-nums text-white/80">
            -{{ clock(Math.max(duration - position, 0)) }}
          </span>
        </div>
        <div class="flex items-center gap-2">
          <button
            type="button"
            class="control"
            :aria-label="playing ? 'Pause' : 'Abspielen'"
            @click="toggle"
          >
            <AppIcon :name="playing ? 'pause' : 'play'" class="size-6!" />
          </button>
          <button type="button" class="control" aria-label="10 Sekunden zurück" @click="skip(-10)">
            <AppIcon name="rotate-left" class="size-6!" />
          </button>
          <button type="button" class="control" aria-label="10 Sekunden vor" @click="skip(10)">
            <AppIcon name="rotate-right" class="size-6!" />
          </button>
          <div class="group flex items-center">
            <button
              type="button"
              class="control"
              :aria-label="muted ? 'Ton an' : 'Ton aus'"
              @click="toggleMute"
            >
              <AppIcon :name="muted || !volume ? 'volume-mute' : 'volume'" class="size-6!" />
            </button>
            <input
              type="range"
              class="range range-primary range-xs w-0 opacity-0 transition-all group-hover:w-24 group-hover:opacity-100 [--range-bg:rgb(255_255_255/0.25)]"
              min="0"
              max="1"
              step="0.05"
              :value="muted ? 0 : volume"
              aria-label="Lautstärke"
              @input="setVolume($event.target.value)"
            />
          </div>
          <span class="ml-2 text-sm tabular-nums text-white/80">
            {{ clock(position) }} / {{ clock(duration) }}
          </span>
          <div class="ml-auto flex items-center gap-2">
            <button
              v-if="media?.next"
              type="button"
              class="control gap-2 px-3"
              aria-label="Nächste Folge"
              @click="playNext"
            >
              <AppIcon name="step-forward" class="size-5!" />
              <span class="hidden text-sm sm:inline">Nächste Folge</span>
            </button>
            <button
              type="button"
              class="control"
              :aria-label="fullscreen ? 'Vollbild beenden' : 'Vollbild'"
              @click="toggleFullscreen"
            >
              <AppIcon :name="fullscreen ? 'compress' : 'expand'" class="size-5!" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="countdown !== null"
      class="absolute right-6 bottom-28 flex flex-col gap-3 rounded-box bg-black/80 p-4 shadow-lg"
    >
      <p class="text-sm text-white/70">Nächste Folge in {{ countdown }}</p>
      <div class="flex gap-2">
        <button type="button" class="btn btn-primary btn-sm" @click="playNext">
          <AppIcon name="play" />
          Jetzt abspielen
        </button>
        <button type="button" class="btn btn-ghost btn-sm text-white" @click="stopCountdown">
          <AppIcon name="cross" />
          Abbrechen
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { markRaw } from 'vue'
import AppIcon from '@core/components/common/AppIcon.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import { clock, resumable } from '@/lib/time.js'
import { useLumonStore } from '@/stores/lumon.js'

const REPORT_SECONDS = 30
const SKIP_SECONDS = 10
const HIDE_DELAY = 3000
const NEXT_COUNTDOWN = 5
const SHORTCUTS = {
  ' ': 'toggle',
  k: 'toggle',
  f: 'toggleFullscreen',
  m: 'toggleMute',
  ArrowLeft: 'skipBack',
  ArrowRight: 'skipForward',
}

export default {
  name: 'PlayerView',
  components: { AppIcon },
  mixins: [asyncActionMixin],
  data() {
    return {
      media: null,
      video: null,
      playing: false,
      buffering: false,
      fullscreen: false,
      controlsVisible: true,
      position: 0,
      duration: 0,
      volume: 1,
      muted: false,
      reported: 0,
      countdown: null,
      hideTimer: null,
      countdownTimer: null,
    }
  },
  computed: {
    store() {
      return useLumonStore()
    },
  },
  created() {
    this.runAction(async () => {
      this.media = await this.store.load(
        `/media/${this.$route.params.id}/`,
        'Video konnte nicht geladen werden.',
      )
    })
  },
  beforeUnmount() {
    clearTimeout(this.hideTimer)
    clearInterval(this.countdownTimer)
    this.report()
  },
  methods: {
    clock,
    attach(event) {
      this.video = markRaw(event.target)
      this.video.parentElement.focus()
      this.duration = Math.floor(this.video.duration)
      if (this.media.duration !== this.duration)
        this.store.progress(this.media.id, { duration: this.duration }).catch(() => null)
      if (resumable(this.media)) this.video.currentTime = this.media.position
      this.wake()
    },
    track() {
      this.position = Math.floor(this.video.currentTime)
      if (Math.abs(this.position - this.reported) >= REPORT_SECONDS) this.report()
    },
    report() {
      if (!this.media || this.position === this.reported) return
      this.reported = this.position
      this.store.progress(this.media.id, { position: this.position }).catch(() => null)
    },
    pause() {
      this.playing = false
      this.controlsVisible = true
      this.report()
    },
    finish() {
      this.playing = false
      this.reported = this.position
      this.store.progress(this.media.id, { played: true, position: 0 }).catch(() => null)
      if (this.media.next) this.startCountdown()
    },
    toggle() {
      if (!this.video) return
      if (this.video.paused) this.video.play()
      else this.video.pause()
    },
    skip(seconds) {
      if (!this.video) return
      this.video.currentTime = Math.min(
        Math.max(this.video.currentTime + seconds, 0),
        this.duration,
      )
      this.wake()
    },
    skipBack() {
      this.skip(-SKIP_SECONDS)
    },
    skipForward() {
      this.skip(SKIP_SECONDS)
    },
    seek(value) {
      if (this.video) this.video.currentTime = Number(value)
    },
    setVolume(value) {
      if (!this.video) return
      this.video.volume = Number(value)
      this.video.muted = Number(value) === 0
    },
    toggleMute() {
      if (this.video) this.video.muted = !this.video.muted
    },
    syncVolume() {
      this.volume = this.video.volume
      this.muted = this.video.muted
    },
    toggleFullscreen() {
      if (!this.video) return
      if (this.fullscreen) this.video.ownerDocument.exitFullscreen()
      else this.video.parentElement.requestFullscreen()
    },
    shortcut(event) {
      const method = SHORTCUTS[event.key]
      if (!method) return
      event.preventDefault()
      this[method]()
      this.wake()
    },
    wake() {
      this.controlsVisible = true
      clearTimeout(this.hideTimer)
      this.hideTimer = setTimeout(() => {
        if (this.playing) this.controlsVisible = false
      }, HIDE_DELAY)
    },
    startCountdown() {
      this.countdown = NEXT_COUNTDOWN
      this.countdownTimer = setInterval(() => {
        this.countdown -= 1
        if (this.countdown <= 0) this.playNext()
      }, 1000)
    },
    stopCountdown() {
      clearInterval(this.countdownTimer)
      this.countdown = null
    },
    playNext() {
      this.stopCountdown()
      this.report()
      this.$router.replace(`/play/${this.media.next}`)
    },
  },
}
</script>

<style scoped>
.control {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 2.5rem;
  height: 2.5rem;
  border-radius: 9999px;
  transition: background-color 150ms;
}

.control:hover {
  background-color: rgb(255 255 255 / 0.15);
}
</style>
