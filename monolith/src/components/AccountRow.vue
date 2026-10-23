<template>
  <component :is="tag" class="flex items-center gap-4 py-4">
    <img
      :src="picture || fallback"
      alt=""
      class="size-12 shrink-0"
      :class="{ 'rounded-full object-cover': picture }"
      @error="picture = ''"
    />
    <div class="flex flex-col min-w-0 flex-1 text-sm">
      <span class="font-bold truncate">{{ name || username }}</span>
      <span class="text-wntrs-muted truncate">@{{ username }}</span>
      <slot />
    </div>
    <slot name="actions" />
  </component>
</template>

<script>
import { icons } from '@core/assets/icons.js'
import { profiles } from '@core/assets/profiles.js'

export default {
  name: 'AccountRow',
  props: {
    tag: { type: String, default: 'div' },
    name: { type: String, default: '' },
    username: { type: String, required: true },
    avatar: { type: String, default: '' },
    src: { type: String, default: '' },
  },
  data() {
    return {
      picture: this.src,
    }
  },
  computed: {
    fallback() {
      return profiles[this.avatar] ?? icons.user
    },
  },
  watch: {
    src(src) {
      this.picture = src
    },
  },
}
</script>
