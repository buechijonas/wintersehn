<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 flex-1">
    <div class="mx-auto w-full max-w-200">
      <h2 class="text-xl font-light mt-4 mb-1">{{ section?.label }}</h2>
      <p v-if="section?.description" class="text-wntrs-muted text-sm">{{ section.description }}</p>

      <div v-if="loading" class="mt-4 flex flex-col gap-4">
        <div v-for="row in 2" :key="row" class="flex flex-col gap-2">
          <div class="skeleton h-4 w-24"></div>
          <div v-for="item in 3" :key="item" class="skeleton h-14 w-full"></div>
        </div>
      </div>

      <template v-if="section">
        <section
          v-for="group in section.groups"
          :key="group.title"
          :class="group.separate ? 'mt-10' : 'mt-4'"
        >
          <div v-if="group.separate" class="divider text-xs opacity-60 tracking-wide mb-4">
            {{ group.title }}
          </div>
          <h3 v-else class="pb-2 text-xs opacity-60 tracking-wide">{{ group.title }}</h3>
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <RecommendationCard
              v-for="item in group.items"
              :key="`${item.name}-${item.description}`"
              :item="item"
              :flags="footprint?.flags"
            />
          </div>
        </section>

        <div v-if="section.privacy && footprint" class="mt-10 flex flex-col gap-6">
          <section class="flex flex-col gap-2">
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

          <section class="flex flex-col gap-2">
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
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import { countries } from '@core/assets/images.js'
import CountryMapPanel from '@/components/common/CountryMapPanel.vue'
import RecommendationCard from '@/components/common/RecommendationCard.vue'
import { useContentStore } from '@core/stores/content.js'
import { useFootprintStore } from '@/stores/footprint.js'

export default {
  name: 'NewsSectionView',
  components: { BaseBreadcrumbs, BaseCard, CountryMapPanel, RecommendationCard },
  data() {
    return { countries }
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
        .find((item) => item.key === this.$route.meta.section)
    },
    breadcrumbs() {
      const label = { label: this.section?.label ?? '' }
      return this.$route.meta.activeNavigation === 'dashboard'
        ? [{ label: 'Dashboard', to: '/' }, label]
        : [label]
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
}
</script>
