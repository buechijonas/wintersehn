<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="mx-auto flex w-full max-w-200 flex-1 flex-col gap-12 px-6 pt-4 pb-16">
    <header class="flex flex-col gap-4">
      <h1 class="font-display text-5xl font-bold tracking-tighter text-wntrs-title">
        {{ section?.label }}
      </h1>
      <p v-if="section?.description" class="max-w-150 text-lg text-wntrs-slate">
        {{ section.description }}
      </p>
    </header>

    <div v-if="loading" class="flex flex-col gap-4">
      <div class="skeleton h-6 w-32"></div>
      <div v-for="row in 3" :key="row" class="skeleton h-24 w-full"></div>
    </div>

    <template v-if="section">
      <section v-for="group in section.groups" :key="group.title" class="flex flex-col gap-4">
        <h2 class="text-xl">{{ group.title }}</h2>
        <div class="grid gap-4 sm:grid-cols-2">
          <RecommendationCard
            v-for="item in group.items"
            :key="`${item.name}-${item.description}`"
            :item="item"
            :flags="footprint?.flags"
            class="sm:last:odd:col-span-2"
          />
        </div>
      </section>

      <template v-if="section.privacy && footprint">
        <section class="flex flex-col gap-4">
          <h2 class="text-xl">{{ section.privacy.title }}</h2>
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

        <section class="flex flex-col gap-4">
          <h2 class="text-xl">Datenfluss nach Land</h2>
          <CountryMapPanel :tabs="mapTabs" :active="activeMapTab" :countries="mapCountries" />
          <BaseCard tag="ul" class="list">
            <li
              v-for="country in footprint[activeMapTab].regions"
              :key="country.icon"
              class="list-row items-center"
            >
              <img
                v-if="country.icon"
                class="size-5"
                :alt="country.icon"
                :src="countries[country.icon]"
              />
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
      </template>
    </template>
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
