<template>
  <BaseCard
    :tag="repository ? 'div' : tag"
    v-bind="repository ? {} : linkAttributes"
    class="relative size-40 shrink-0 flex items-center justify-center p-4"
    :class="{ 'hover:bg-base-200': tag !== 'div' }"
  >
    <a
      v-if="repository"
      :href="repository"
      target="_blank"
      rel="noopener noreferrer"
      title="Auf GitHub ansehen"
      class="absolute top-3 right-3 z-10 flex text-wntrs-slate hover:text-primary"
    >
      <AppIcon name="github" alt="GitHub" />
    </a>
    <div class="flex flex-col items-center text-center gap-4 w-full">
      <div class="relative size-16 shrink-0">
        <div v-if="!imgLoaded" class="skeleton absolute inset-0 rounded-full"></div>
        <img
          class="size-16"
          :class="{ invisible: !imgLoaded }"
          :alt="label"
          :src="sources[iconSet][icon]"
          @load="imgLoaded = true"
        />
      </div>
      <p class="text-wntrs-slate text-sm line-clamp-2 text-ellipsis w-full">
        <component
          :is="tag"
          v-if="repository"
          v-bind="linkAttributes"
          class="after:absolute after:inset-0"
        >
          {{ label }}
        </component>
        <template v-else>{{ label }}</template>
      </p>
    </div>
  </BaseCard>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import { flats, countries, logos } from '@core/assets/images.js'
import { icons } from '@core/assets/icons.js'
import { path, url } from '@core/lib/link.js'

export default {
  name: 'IconLabelCard',
  components: { AppIcon, BaseCard },
  props: {
    icon: { type: String, required: true },
    label: { type: String, required: true },
    to: { type: String, default: null },
    iconSet: { type: String, default: 'flats' },
    repository: { type: String, default: '' },
  },
  data() {
    return { sources: { flats, icons, countries, logos }, imgLoaded: false }
  },
  computed: {
    linkAttributes() {
      return {
        to: path(this.to),
        href: url(this.to),
        target: url(this.to) && '_blank',
        rel: url(this.to) && 'noopener noreferrer',
      }
    },
    tag() {
      if (path(this.to)) return 'router-link'
      if (url(this.to)) return 'a'
      return 'div'
    },
  },
}
</script>
