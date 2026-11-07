<template>
  <section
    class="relative -mx-6 -mt-6 flex min-h-[28rem] items-end overflow-hidden lg:min-h-[34rem]"
  >
    <img
      v-if="title.backdrop"
      :src="title.backdrop"
      alt=""
      class="absolute inset-0 size-full object-cover"
    />
    <div
      class="absolute inset-0 bg-gradient-to-r from-base-100 via-base-100/70 to-transparent"
    ></div>
    <div
      class="absolute inset-0 bg-gradient-to-t from-base-100 via-transparent to-transparent"
    ></div>
    <div class="relative flex max-w-2xl flex-col gap-4 px-6 pb-12">
      <h1 class="font-display text-6xl leading-none text-base-content lg:text-7xl">
        {{ title.title }}
      </h1>
      <p class="text-sm text-wntrs-slate">{{ facts }}</p>
      <p class="line-clamp-3 text-base text-base-content/90">{{ title.overview }}</p>
      <div class="flex flex-wrap gap-3">
        <PlayButton v-if="title.media" :media="title.media" />
        <BaseButton :to="`/${title.media_type}/${title.tmdb_id}`">
          <AppIcon name="info" />
          Mehr Infos
        </BaseButton>
      </div>
    </div>
  </section>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import PlayButton from '@/components/PlayButton.vue'

export default {
  name: 'FeaturedHero',
  components: { AppIcon, BaseButton, PlayButton },
  props: {
    title: { type: Object, required: true },
  },
  computed: {
    facts() {
      return [this.title.year, ...this.title.genres.slice(0, 3)].filter(Boolean).join(' · ')
    },
  },
}
</script>
