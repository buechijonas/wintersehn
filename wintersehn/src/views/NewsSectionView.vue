<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div
    class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px-var(--footer-height))] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1"
  >
    <div class="mx-auto w-full max-w-200" :class="{ 'lg:max-w-300': section?.privacy }">
      <h2 class="text-xl font-light mt-4 mb-1">{{ section?.label }}</h2>
      <p v-if="section?.description" class="text-wntrs-muted text-sm">{{ section.description }}</p>

      <div v-if="loading" class="mt-4 flex flex-col gap-4">
        <div v-for="row in 2" :key="row" class="flex flex-col gap-2">
          <div class="skeleton h-4 w-24"></div>
          <div v-for="item in 3" :key="item" class="skeleton h-14 w-full"></div>
        </div>
      </div>

      <div v-if="section" :class="{ 'lg:grid lg:grid-cols-5 lg:gap-x-16 lg:items-start': section.privacy }">
        <div :class="{ 'lg:col-span-3': section.privacy }">
          <section
            v-for="group in section.groups"
            :key="group.title"
            :class="group.separate ? 'mt-10' : 'mt-4'"
          >
            <div v-if="group.separate" class="divider text-xs opacity-60 tracking-wide mb-4">
              {{ group.title }}
            </div>
            <h3 v-else class="pb-2 text-xs opacity-60 tracking-wide">{{ group.title }}</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <BaseCard
                v-for="item in group.items"
                :key="`${item.name}-${item.description}`"
                :tag="item.url ? 'a' : 'div'"
                :href="item.url"
                :target="item.url && '_blank'"
                :rel="item.url && 'noopener noreferrer'"
                class="flex flex-col gap-2 p-3 min-w-0 rounded-box"
                :class="{ 'hover:bg-base-200': item.url, 'border-dashed!': item.planned }"
              >
                <div class="flex items-center justify-between gap-2 text-xs">
                  <span class="text-wntrs-muted truncate">
                    {{ item.category }}<template v-if="item.description"> · {{ item.description }}</template>
                  </span>
                  <span v-if="item.footprint" class="shrink-0 font-medium">
                    <template v-for="(step, index) in footprintSteps(item)" :key="index">
                      <span v-if="index" class="text-wntrs-muted"> → </span>
                      <span :class="footprintClass(step)">{{ step }}</span>
                    </template>
                  </span>
                </div>
                <div
                  v-for="replaced in item.replaces ?? []"
                  :key="replaced.name"
                  class="flex items-center gap-2 min-w-0 text-xs text-wntrs-muted"
                >
                  <img class="size-4 shrink-0 grayscale opacity-40" :alt="replaced.name" :src="brands[replaced.icon]" />
                  <span class="line-through truncate">{{ replaced.name }}</span>
                  <img
                    v-if="replaced.country"
                    class="size-3 shrink-0 opacity-60"
                    :alt="replaced.country"
                    :src="countries[flag(replaced.country)]"
                  />
                </div>
                <div class="flex items-center gap-2 min-w-0">
                  <img
                    v-if="item.icon"
                    class="size-6 shrink-0 rounded-sm"
                    :class="{ 'grayscale opacity-40': item.dropped }"
                    :alt="item.name"
                    :src="brands[item.icon]"
                  />
                  <span class="text-sm truncate" :class="{ 'line-through text-wntrs-muted': item.dropped }">
                    {{ item.name }}
                  </span>
                  <img
                    v-if="item.country"
                    class="size-3 shrink-0"
                    :class="{ 'opacity-60': item.dropped }"
                    :alt="item.country"
                    :src="countries[flag(item.country)]"
                  />
                </div>
                <p v-if="item.reason" class="text-wntrs-muted text-xs">{{ item.reason }}</p>
              </BaseCard>
            </div>
          </section>
        </div>

        <aside v-if="section.privacy" class="lg:col-span-2 lg:sticky lg:top-0">
          <section v-if="section.privacy && footprint" class="mt-4 flex flex-col gap-2">
            <h3 class="pb-2 text-xs opacity-60 tracking-wide">{{ section.privacy.title }}</h3>
            <BaseCard class="flex flex-col gap-4 p-4">
              <p class="text-wntrs-muted text-xs">{{ section.privacy.description }}</p>
              <div v-for="bar in footprintBars" :key="bar.label" class="flex flex-col gap-1">
                <div class="flex justify-between text-sm">
                  <span>{{ bar.label }}</span>
                  <span class="font-medium">{{ bar.total.value }}/{{ bar.total.max }}</span>
                </div>
                <progress
                  class="progress w-full opacity-50"
                  :class="bar.class"
                  :value="bar.total.value"
                  :max="bar.total.max"
                />
              </div>
              <p class="text-sm">
                <span class="font-medium">−{{ footprint.reduction }} %</span> Datenabdruck
              </p>
            </BaseCard>
          </section>

          <section v-if="footprint" class="mt-4 flex flex-col gap-2">
            <h3 class="pb-2 text-xs opacity-60 tracking-wide">Datenfluss nach Land</h3>
            <CountryMapPanel :tabs="mapTabs" :active="activeMapTab" :countries="mapCountries" />
            <BaseCard tag="ul" class="list">
              <li
                v-for="country in footprint[activeMapTab].regions"
                :key="country.icon"
                class="list-row items-center"
              >
                <img v-if="country.icon" class="size-5" :alt="country.icon" :src="countries[country.icon]" />
                <span v-else class="size-5"></span>
                <div class="list-col-grow min-w-0 text-xs text-wntrs-muted">
                  {{ country.icon ? country.label : `Ohne Firmensitz · ${country.label}` }}
                </div>
                <span class="text-sm font-medium whitespace-nowrap">
                  {{ country.value }} · {{ country.share }} %
                </span>
              </li>
            </BaseCard>
          </section>
        </aside>
      </div>

    </div>
  </div>
  <BaseFooter />
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import BaseFooter from '@core/components/common/BaseFooter.vue'
import { countries, logos, social } from '@core/assets/images.js'
import CountryMapPanel from '@/components/common/CountryMapPanel.vue'
import { useContentStore } from '@core/stores/content.js'
import { useFootprintStore } from '@/stores/footprint.js'

export default {
  name: 'NewsSectionView',
  components: { BaseBreadcrumbs, BaseCard, BaseFooter, CountryMapPanel },
  data() {
    return { countries, brands: { ...logos, ...social } }
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
    loading() {
      return !this.contentStore.items.news
    },
    section() {
      return (this.contentStore.items.news?.data ?? [])
        .flatMap((category) => category.items)
        .find((item) => item.key === this.$route.params.key)
    },
    breadcrumbs() {
      return [
        { label: 'Medien', to: '/news' },
        { label: this.section?.label ?? '' },
      ]
    },
    footprintStore() {
      return useFootprintStore()
    },
    footprint() {
      return this.footprintStore.footprint
    },
    mapTabs() {
      return [
        { key: 'before', label: 'Vorher' },
        { key: 'after', label: 'Nachher' },
      ]
    },
    mapCountries() {
      return this.footprint[this.activeMapTab].countries.map((country) => ({
        ...country,
        label: `${country.value} · ${country.share} % · ${country.label}`,
      }))
    },
    activeMapTab() {
      return this.$route.query.tab === 'after' ? 'after' : 'before'
    },
    footprintBars() {
      return [
        { label: 'Vorher', total: this.footprint.before, class: 'progress-error' },
        { label: 'Nachher', total: this.footprint.after, class: 'progress-success' },
      ]
    },
  },
  mounted() {
    this.contentStore.fetchContent('news')
    this.footprintStore.fetchFootprint()
  },
  methods: {
    flag(country) {
      return this.footprint?.flags[country] ?? country
    },
    footprintSteps(item) {
      if (item.dropped) return [item.footprint, 0]
      return [...(item.replaces ?? []).map((replaced) => replaced.footprint), item.footprint]
    },
    footprintClass(footprint) {
      if (footprint <= 3) return 'text-success/70'
      if (footprint <= 6) return 'text-warning/70'
      return 'text-error/70'
    },
  },
}
</script>
