<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col gap-4 pb-12 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-200 flex flex-col gap-4 pt-4">
      <p v-if="error" class="text-error text-sm">{{ error }}</p>
      <template v-if="loading">
        <div class="skeleton h-20 w-full"></div>
        <div class="skeleton h-12 w-full"></div>
        <div class="skeleton aspect-[2/1] w-full"></div>
      </template>
      <template v-else-if="map">
        <DestinationCard :destination="destination" />
        <CountryMapPanel
          :tabs="tabs"
          :active="activeTab"
          :countries="activeSection?.countries ?? []"
        />
      </template>
    </div>
    <CardCategory
      v-if="activeSection"
      :title="activeSection.title"
      :items="activeSection.countries"
    />
  </div>
  <BaseFooter />
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseFooter from '@core/components/common/BaseFooter.vue'
import CardCategory from '@/components/common/CardCategory.vue'
import CountryMapPanel from '@/components/common/CountryMapPanel.vue'
import DestinationCard from '@/components/common/DestinationCard.vue'
import { slugify } from '@core/lib/slug.js'
import { useCountriesStore } from '@/stores/countries.js'

export default {
  name: 'CountriesView',
  components: {
    BaseBreadcrumbs,
    BaseFooter,
    CardCategory,
    CountryMapPanel,
    DestinationCard,
  },
  data() {
    return {
      breadcrumbs: [{ label: 'Länder', to: '/' }],
      error: '',
    }
  },
  computed: {
    countriesStore() {
      return useCountriesStore()
    },
    map() {
      return this.countriesStore.map
    },
    loading() {
      return !this.map && !this.error
    },
    sections() {
      return (this.map?.sections ?? []).map((section, sectionIndex) => ({
        ...section,
        key: slugify(section.title),
        countries: section.countries.map((country, itemIndex) => ({
          ...country,
          iconSet: 'countries',
          to: `/countries/${sectionIndex}/${itemIndex}`,
        })),
      }))
    },
    tabs() {
      return this.sections.map(({ key, title }) => ({ key, label: title }))
    },
    activeTab() {
      return this.$route.query.tab ?? this.tabs[0]?.key ?? ''
    },
    activeSection() {
      return this.sections.find((section) => section.key === this.activeTab) ?? null
    },
    destination() {
      const destination = this.map?.destination
      return (
        destination && {
          ...destination,
          to: `/countries/${destination.section}/${destination.item}`,
        }
      )
    },
  },
  async mounted() {
    try {
      await this.countriesStore.fetchMap()
    } catch (e) {
      this.error = e.message
    }
  },
}
</script>
