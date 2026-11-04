<template>
  <div class="relative w-full">
    <div v-if="!features.length" class="skeleton aspect-[2/1] w-full"></div>
    <svg v-else :viewBox="viewBox" class="size-full" role="img" aria-label="Weltkarte">
      <path
        v-for="shape in shapes"
        :key="shape.key"
        :d="shape.d"
        class="stroke-base-100 [stroke-width:0.4]"
        :class="shape.country ? countryClass(shape.country) : 'fill-base-content/15'"
        :style="{ fillOpacity: shape.country?.weight }"
        @mouseenter="hovered = shape.country"
        @mouseleave="hovered = null"
        @click="open(shape.country)"
      >
      </path>
      <circle
        v-for="marker in markers"
        :key="marker.country.icon"
        :cx="marker.position[0]"
        :cy="marker.position[1]"
        r="3.5"
        class="stroke-base-100 [stroke-width:1]"
        :class="countryClass(marker.country)"
        :style="{ fillOpacity: marker.country.weight }"
        @mouseenter="hovered = marker.country"
        @mouseleave="hovered = null"
        @click="open(marker.country)"
      >
      </circle>
    </svg>
    <BaseCard
      v-if="hovered"
      class="absolute top-0 left-0 flex items-center gap-2 px-2 py-1 text-xs rounded-box max-w-4/5 pointer-events-none"
    >
      <img class="size-4 shrink-0" :alt="hovered.icon" :src="flags[hovered.icon]" />
      <span>{{ hovered.label }}</span>
    </BaseCard>
  </div>
</template>

<script>
import { markRaw } from 'vue'
import { feature } from 'topojson-client'
import { geoCentroid, geoNaturalEarth1, geoPath } from 'd3-geo'
import BaseCard from '@core/components/common/BaseCard.vue'
import { countries as flags } from '@core/assets/images.js'

const WIDTH = 960
const ANTARCTICA = '010'
const MIN_VISIBLE_AREA = 8

export default {
  name: 'CountryMap',
  components: { BaseCard },
  props: {
    countries: { type: Array, required: true },
  },
  data() {
    return { features: [], flags, hovered: null }
  },
  computed: {
    projection() {
      return geoNaturalEarth1().fitWidth(WIDTH, {
        type: 'FeatureCollection',
        features: this.features,
      })
    },
    path() {
      return geoPath(this.projection)
    },
    viewBox() {
      const [[x, y], [right, bottom]] = this.path.bounds({
        type: 'FeatureCollection',
        features: this.features,
      })
      return `${x} ${y} ${right - x} ${bottom - y}`
    },
    countriesByCode() {
      return Object.fromEntries(
        this.countries.filter((country) => country.code).map((country) => [country.code, country]),
      )
    },
    shapes() {
      return this.features.map((shape) => ({
        key: shape.properties.name,
        d: this.path(shape),
        area: this.path.area(shape),
        centroid: this.projection(geoCentroid(shape)),
        country: this.countriesByCode[shape.id] ?? null,
      }))
    },
    markers() {
      const tiny = this.shapes
        .filter((shape) => shape.country && shape.area < MIN_VISIBLE_AREA)
        .map((shape) => ({ country: shape.country, position: shape.centroid }))
      const points = this.countries
        .filter((country) => country.point)
        .map((country) => ({ country, position: this.projection(country.point) }))
      return [...tiny, ...points]
    },
  },
  async mounted() {
    const { default: topology } = await import('world-atlas/countries-50m.json')
    this.features = markRaw(
      feature(topology, topology.objects.countries).features.filter(
        (shape) => shape.id !== ANTARCTICA,
      ),
    )
  },
  methods: {
    countryClass(country) {
      return country.to ? 'fill-primary cursor-pointer hover:opacity-75' : 'fill-primary'
    },
    open(country) {
      if (country?.to) this.$router.push(country.to)
    },
  },
}
</script>
