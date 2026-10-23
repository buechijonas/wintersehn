<template>
  <div ref="canvas" class="relative size-full overflow-hidden select-none">
    <svg
      :viewBox="`0 0 ${width} ${height}`"
      class="size-full touch-none"
      :class="panning ? 'cursor-grabbing' : 'cursor-grab'"
      @pointerdown="startPan"
      @pointermove="pan"
      @pointerup="endPan"
      @pointercancel="endPan"
      @wheel.prevent="wheel"
    >
      <g ref="viewport" :transform="`translate(${view.x} ${view.y}) scale(${view.k})`">
        <circle
          v-for="ring in rings"
          :key="`ring-${ring.level}`"
          :r="ring.radius"
          class="fill-primary stroke-primary/30"
          :fill-opacity="ring.opacity"
          stroke-width="1"
        />
        <circle
          :r="outerOrbit"
          class="fill-none stroke-wntrs-muted/50"
          stroke-width="1.5"
          stroke-dasharray="6 8"
        />
        <text
          v-for="ring in rings"
          :key="`label-${ring.level}`"
          :y="-ring.radius + 10"
          text-anchor="middle"
          dominant-baseline="middle"
          class="fill-wntrs-muted text-xs pointer-events-none"
        >
          {{ ring.level }}
        </text>
        <circle :r="CORE - 16" class="fill-primary" />
        <text
          text-anchor="middle"
          dominant-baseline="middle"
          class="fill-primary-content font-bold pointer-events-none"
        >
          Ich
        </text>

        <g
          v-for="node in nodes"
          :key="node.uuid"
          :transform="`translate(${node.x} ${node.y})`"
          :class="dragged?.uuid === node.uuid ? 'cursor-grabbing' : 'cursor-pointer'"
          role="link"
          :aria-label="`${node.title}: ${node.level ? `Kreis ${node.level}` : 'nicht zugeordnet'}`"
          @pointerdown.stop="startDrag($event, node)"
          @pointermove.stop="drag"
          @pointerup.stop="endDrag($event, node)"
          @pointercancel.stop="endDrag($event, node)"
        >
          <circle :r="NODE_RADIUS" class="fill-primary" />
          <image
            :href="folderIcon"
            x="-10"
            y="-10"
            width="20"
            height="20"
            class="invert pointer-events-none"
          />
          <text
            :y="NODE_RADIUS + 16"
            text-anchor="middle"
            class="fill-base-content stroke-base-100 text-sm font-bold [paint-order:stroke] pointer-events-none"
            stroke-width="10"
            stroke-linejoin="round"
          >
            {{ node.title }}
          </text>
        </g>
      </g>
    </svg>

    <div class="absolute top-4 right-4 flex gap-2">
      <ZoomButtons @zoom="zoomBy" />
    </div>
    <ul class="absolute bottom-4 left-4 text-xs text-wntrs-muted pointer-events-none">
      <li v-for="(label, level) in trustRingLabels" :key="level">{{ level }} · {{ label }}</li>
      <li>Ausserhalb · nicht zugeordnet</li>
    </ul>
  </div>
</template>

<script>
import { icons } from '@core/assets/icons.js'
import ZoomButtons from '@/components/ZoomButtons.vue'
import { trustRingLabels } from '@/data/trust.js'
import panZoomMixin from '@/mixins/panZoomMixin.js'

const CORE = 64
const BAND = 80
const NODE_RADIUS = 20
const OUTER_GAP = 48
const MARGIN = 48
const START_ZOOM_MIN = 0.75
const CLICK_DISTANCE = 4

export default {
  name: 'TrustCircles',
  components: { ZoomButtons },
  mixins: [panZoomMixin],
  props: {
    levels: { type: Number, required: true },
    dossiers: { type: Array, required: true },
  },
  emits: ['move'],
  data() {
    return {
      CORE,
      NODE_RADIUS,
      trustRingLabels,
      folderIcon: icons.folder,
      width: 0,
      height: 0,
      dragged: null,
    }
  },
  computed: {
    outerOrbit() {
      return CORE + this.levels * BAND + OUTER_GAP
    },
    rings() {
      return Array.from({ length: this.levels }, (_, index) => this.levels - index).map(
        (level) => ({
          level,
          radius: CORE + level * BAND,
          opacity: 0.03 + ((this.levels - level) / this.levels) * 0.12,
        }),
      )
    },
    nodes() {
      const groups = Object.groupBy(this.dossiers, (dossier) => dossier.level ?? 0)
      return Object.entries(groups).flatMap(([level, dossiers]) =>
        dossiers.map((dossier, index) => ({
          ...dossier,
          ...this.place(Number(level), index, dossiers.length),
          ...(this.dragged?.uuid === dossier.uuid && this.dragged.position),
        })),
      )
    },
  },
  mounted() {
    this.resizeObserver = new ResizeObserver(([entry]) => this.resize(entry.contentRect))
    this.resizeObserver.observe(this.$refs.canvas)
  },
  beforeUnmount() {
    this.resizeObserver.disconnect()
  },
  methods: {
    resize({ width, height }) {
      this.width = width
      this.height = height
      if (this.autoFit) this.center()
    },
    center() {
      const fit = Math.min(this.width, this.height) / (2 * (this.outerOrbit + MARGIN))
      const k = Math.min(1, Math.max(START_ZOOM_MIN, fit))
      this.view = { k, x: this.width / 2, y: this.height / 2 }
    },
    orbit(level) {
      return level ? CORE + (level - 0.5) * BAND : this.outerOrbit
    },
    place(level, index, count) {
      const angle = -Math.PI / 2 + ((index + 0.5) / count) * 2 * Math.PI
      const radius = this.orbit(level)
      return { x: radius * Math.cos(angle), y: radius * Math.sin(angle) }
    },
    levelAt({ x, y }) {
      const band = Math.ceil((Math.hypot(x, y) - CORE) / BAND)
      return band > this.levels ? null : Math.max(1, band)
    },
    startDrag(event, node) {
      event.currentTarget.setPointerCapture(event.pointerId)
      this.autoFit = false
      this.dragged = {
        uuid: node.uuid,
        start: { x: event.clientX, y: event.clientY },
        position: null,
      }
    },
    drag(event) {
      if (!this.dragged) return
      const { x, y } = this.point(event)
      this.dragged.position = { x, y }
    },
    endDrag(event, node) {
      if (this.dragged?.uuid !== node.uuid) return
      const { start, position } = this.dragged
      this.dragged = null
      const distance = Math.hypot(event.clientX - start.x, event.clientY - start.y)
      if (distance < CLICK_DISTANCE && event.type === 'pointerup') {
        this.$router.push({ name: 'dossier', params: { uuid: node.uuid } })
        return
      }
      const level = position && this.levelAt(position)
      if (position && level !== node.level) this.$emit('move', node, level)
    },
  },
}
</script>
