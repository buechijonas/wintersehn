<template>
  <div class="w-full">
    <div v-if="!features.length" class="skeleton aspect-[2/1] w-full"></div>
    <svg v-else :viewBox="viewBox" class="size-full" role="img" aria-label="Weltkarte">
      <path
        v-for="shape in shapes"
        :key="shape.key"
        :d="shape.d"
        class="stroke-base-100 [stroke-width:0.4]"
        :class="
          shape.country ? 'fill-primary cursor-pointer hover:opacity-75' : 'fill-base-content/15'
        "
        @click="open(shape.country)"
      >
        <title v-if="shape.country">{{ shape.country.label }}</title>
      </path>
      <circle
        v-for="marker in markers"
        :key="marker.country.icon"
        :cx="marker.position[0]"
        :cy="marker.position[1]"
        r="3.5"
        class="fill-primary stroke-base-100 [stroke-width:1] cursor-pointer hover:opacity-75"
        @click="open(marker.country)"
      >
        <title>{{ marker.country.label }}</title>
      </circle>
    </svg>
  </div>
</template>

<script>
import { markRaw } from 'vue'
import { feature } from 'topojson-client'
import { geoCentroid, geoNaturalEarth1, geoPath } from 'd3-geo'

const WIDTH = 960
const ANTARCTICA = '010'
const MIN_VISIBLE_AREA = 8

export default {
  name: 'CountryMap',
  props: {
    countries: { type: Array, required: true },
  },
  data() {
    return { features: [] }
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
    open(country) {
      if (country) this.$router.push(country.to)
    },
  },
}
</script>
