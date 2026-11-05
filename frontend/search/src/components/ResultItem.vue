<template>
  <div class="relative flex gap-4">
    <component
      :is="linkTag"
      v-if="withImage && item.image"
      v-bind="linkAttrs"
      class="shrink-0"
      @click="openLink"
    >
      <ResultImage
        :src="item.image"
        class="aspect-video w-36 rounded-box object-cover bg-base-200"
      />
    </component>
    <div class="flex min-w-0 flex-1 flex-col gap-1">
      <div class="flex min-h-5 items-center gap-2">
        <span class="flex min-w-0 items-center gap-2 text-xs">
          <slot name="prefix" />
          <span class="truncate" :class="hostClass">{{ item.host }}</span>
        </span>
        <RatingMarker
          v-if="rating"
          :rating="rating"
          :report="report"
          :host="item.host"
          class="max-sm:ml-auto"
        />
        <span
          v-else-if="pending"
          class="loading loading-spinner size-3.5 text-wntrs-muted max-sm:ml-auto"
          aria-label="Sicherheit wird geprüft"
        ></span>
        <span class="ml-auto flex shrink-0 empty:hidden max-sm:ml-0">
          <slot name="badge" />
        </span>
      </div>
      <component
        :is="linkTag"
        v-bind="linkAttrs"
        class="group flex flex-col gap-1 after:absolute after:inset-0"
        @click="openLink"
        @keydown.enter="openLink"
      >
        <span class="text-lg text-wntrs-title" :class="{ 'group-hover:underline': !isBlocked }">
          {{ item.title }}
        </span>
        <span v-if="item.content" class="text-sm text-wntrs-slate line-clamp-2">
          {{ item.content }}
        </span>
      </component>
    </div>
  </div>
</template>

<script>
import RatingMarker from '@/components/RatingMarker.vue'
import ResultImage from '@/components/ResultImage.vue'

const hostClasses = { secure: 'text-wntrs-secure', insecure: 'text-error' }
const RISKY_RATINGS = ['insecure', 'http', 'lookalike']
const linkAttributes = {
  warn: {
    role: 'button',
    tabindex: '0',
    title: 'Unsichere Seite: vor dem Öffnen wird nachgefragt',
    class: 'cursor-pointer',
  },
  confirm: {
    role: 'button',
    tabindex: '0',
    title: 'Vor dem Öffnen wird die Adresse angezeigt',
    class: 'cursor-pointer',
  },
  block: {
    'aria-disabled': 'true',
    title: 'Gesperrt: unsichere Seite',
    class: 'cursor-not-allowed opacity-60',
  },
}

export default {
  name: 'ResultItem',
  components: { RatingMarker, ResultImage },
  props: {
    item: { type: Object, required: true },
    withImage: { type: Boolean, default: false },
    rel: { type: String, default: 'noopener noreferrer' },
    rating: { type: String, default: null },
    report: { type: Object, default: null },
    pending: { type: Boolean, default: false },
    riskyLinks: { type: String, default: 'warn' },
    confirmLinks: { type: Boolean, default: false },
  },
  emits: ['warn'],
  computed: {
    hostClass() {
      return hostClasses[this.rating] ?? 'text-wntrs-muted'
    },
    linkMode() {
      const mode = RISKY_RATINGS.includes(this.rating) ? this.riskyLinks : 'allow'
      return mode === 'allow' && this.confirmLinks ? 'confirm' : mode
    },
    isBlocked() {
      return this.linkMode === 'block'
    },
    linkTag() {
      return this.linkMode === 'allow' ? 'a' : 'span'
    },
    linkAttrs() {
      return linkAttributes[this.linkMode] ?? { href: this.item.url, rel: this.rel }
    },
  },
  methods: {
    openLink() {
      if (!['warn', 'confirm'].includes(this.linkMode)) return
      this.$emit('warn', {
        ...this.item,
        rating: this.linkMode === 'confirm' ? 'confirm' : this.rating,
        grade: this.report?.grade,
        unicode: this.report?.unicode,
      })
    },
  },
}
</script>
