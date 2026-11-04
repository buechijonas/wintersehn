<template>
  <div ref="canvas" class="relative size-full overflow-hidden select-none">
    <svg
      v-if="nodes.length"
      :viewBox="`0 0 ${width} ${height}`"
      :data-frame="frame"
      class="size-full touch-none"
      :class="panning ? 'cursor-grabbing' : 'cursor-grab'"
      @pointerdown="startPan"
      @pointermove="pan"
      @pointerup="endPan"
      @pointercancel="endPan"
      @wheel.prevent="wheel"
    >
      <g ref="viewport" :transform="`translate(${view.x} ${view.y}) scale(${view.k})`">
        <line
          v-for="link in links"
          :key="`line-${link.source.uuid}-${link.target.uuid}`"
          :x1="link.source.x"
          :y1="link.source.y"
          :x2="link.target.x"
          :y2="link.target.y"
          class="stroke-primary/40 transition-opacity duration-300"
          :class="{ 'opacity-10': isDimmedLink(link) }"
          stroke-width="1.5"
        />
        <text
          v-for="label in links.flatMap(linkLabels)"
          :key="label.key"
          :x="label.x"
          :y="label.y"
          text-anchor="middle"
          dominant-baseline="middle"
          class="fill-wntrs-muted stroke-base-100 text-xs [paint-order:stroke] pointer-events-none transition-opacity duration-300"
          :class="{ 'opacity-10': isDimmedLink(label.link) }"
          stroke-width="4"
        >
          {{ label.text }}
        </text>
        <g
          v-for="node in nodes"
          :key="node.uuid"
          :transform="`translate(${node.x} ${node.y})`"
          class="transition-opacity duration-300"
          :class="[
            dragged === node.uuid ? 'cursor-grabbing' : 'cursor-pointer',
            { 'opacity-20': connected && !connected.has(node.uuid) },
          ]"
          role="link"
          :aria-label="node.title"
          @pointerdown.stop="startDrag($event, node)"
          @pointermove.stop="drag($event, node)"
          @pointerup.stop="endDrag($event, node)"
          @pointercancel.stop="endDrag($event, node)"
          @pointerenter="hoverStart(node)"
          @pointerleave="hoverEnd"
        >
          <circle
            :r="RADIUS"
            class="fill-primary"
            :class="{ 'stroke-base-content': [focus, highlighted].includes(node.uuid) }"
            stroke-width="3"
          />
          <circle
            v-if="node.fx != null && dragged !== node.uuid"
            :r="RADIUS + 4"
            class="fill-none stroke-primary/60"
            stroke-width="1.5"
            stroke-dasharray="3 3"
          />
          <image
            :href="folderIcon"
            x="-10"
            y="-10"
            width="20"
            height="20"
            class="invert pointer-events-none"
          />
          <text
            :y="RADIUS + 16"
            text-anchor="middle"
            class="fill-base-content stroke-base-100 text-sm font-bold [paint-order:stroke]"
            stroke-width="4"
          >
            {{ node.title }}
          </text>
        </g>
      </g>
    </svg>

    <div class="absolute top-4 right-4 flex flex-col items-end gap-2">
      <div class="flex gap-2">
        <BaseButton
          v-if="controls"
          variant="neutral"
          shape="square"
          size="sm"
          title="Kräfte"
          @click="showControls = !showControls"
        >
          <AppIcon name="settings" alt="Kräfte" />
        </BaseButton>
        <ZoomButtons @zoom="zoomBy" />
      </div>

      <BaseCard v-if="controls && showControls" class="w-64 p-4 flex flex-col gap-3 text-sm">
        <label v-for="slider in SLIDERS" :key="slider.key" class="flex flex-col gap-1">
          <span class="flex justify-between">
            {{ slider.label }}
            <span class="text-wntrs-muted">{{ forces[slider.key] }}</span>
          </span>
          <input
            v-model.number="forces[slider.key]"
            type="range"
            min="0"
            :max="slider.max"
            :step="slider.step"
            class="range range-xs range-primary"
          />
        </label>
        <div class="flex gap-2">
          <BaseButton size="sm" class="flex-1" @click="release">Positionen lösen</BaseButton>
          <BaseButton
            size="sm"
            variant="primary"
            class="flex-1"
            :disabled="!unsaved || saving"
            @click="saveForces"
          >
            <AppIcon name="disk" />
            Speichern
          </BaseButton>
        </div>
        <p v-if="error" class="text-error text-xs">{{ error }}</p>
      </BaseCard>
    </div>
  </div>
</template>

<script>
import { markRaw } from 'vue'
import { forceCollide, forceLink, forceSimulation, forceX, forceY } from 'd3-force'
import { icons } from '@core/assets/icons.js'
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import ZoomButtons from '@/components/ZoomButtons.vue'
import panZoomMixin, { ZOOM_MIN } from '@/mixins/panZoomMixin.js'
import { inverseStatus, statusLabels } from '@/data/statuses.js'
import { useDossiersStore } from '@/stores/dossiers.js'

const RADIUS = 22
const CLICK_DISTANCE = 4
const FIT_MAX = 1.2
const FIT_PADDING = RADIUS + 40
const HOVER_DELAY = 500

const SLIDERS = [
  { key: 'attraction', label: 'Anziehung (verbunden)', max: 100, step: 1 },
  { key: 'distance', label: 'Abstand (verbunden)', max: 1000, step: 10 },
  { key: 'repulsion', label: 'Abstossung (nicht verbunden)', max: 20000, step: 100 },
  { key: 'gravity', label: 'Gravitation', max: 100, step: 1 },
  { key: 'untangling', label: 'Linien entflechten', max: 100, step: 1 },
]

const DEFAULT_FORCES = {
  attraction: 20,
  distance: 180,
  repulsion: 800,
  gravity: 12,
  untangling: 30,
}

const UNTANGLE_SPEED = 10
const LINE_CLEARANCE = RADIUS * 2

function side(p, q, r) {
  return Math.sign((q.x - p.x) * (r.y - p.y) - (q.y - p.y) * (r.x - p.x))
}

function crosses({ source: a, target: b }, { source: c, target: d }) {
  if (new Set([a, b, c, d]).size < 4) return false
  return side(a, b, c) !== side(a, b, d) && side(c, d, a) !== side(c, d, b)
}

function nudge(nodes, dx, dy) {
  nodes.forEach((node) => {
    node.vx += dx
    node.vy += dy
  })
}

function separateCrossing(first, second, speed) {
  const dx = (first.source.x + first.target.x - second.source.x - second.target.x) / 2
  const dy = (first.source.y + first.target.y - second.source.y - second.target.y) / 2
  const length = Math.hypot(dx, dy) || 1
  nudge([first.source, first.target], (dx / length) * speed, (dy / length) * speed)
  nudge([second.source, second.target], (-dx / length) * speed, (-dy / length) * speed)
}

function clearLine(node, { source, target }, speed) {
  if (node === source || node === target) return
  const lx = target.x - source.x
  const ly = target.y - source.y
  const t = Math.max(
    0,
    Math.min(1, ((node.x - source.x) * lx + (node.y - source.y) * ly) / (lx * lx + ly * ly || 1)),
  )
  const dx = node.x - (source.x + lx * t)
  const dy = node.y - (source.y + ly * t)
  const distance = Math.hypot(dx, dy) || 1
  if (distance >= LINE_CLEARANCE) return
  const push = ((LINE_CLEARANCE - distance) / LINE_CLEARANCE) * speed
  nudge([node], (dx / distance) * push, (dy / distance) * push)
  nudge([source, target], (-dx / distance) * push * 0.5, (-dy / distance) * push * 0.5)
}

function forceUntangle(links) {
  let nodes = []
  let strength = 0

  function force(alpha) {
    const speed = strength * alpha * UNTANGLE_SPEED
    if (!speed) return
    links.forEach((first, i) => {
      links
        .slice(i + 1)
        .filter((second) => crosses(first, second))
        .forEach((second) => separateCrossing(first, second, speed))
    })
    nodes.forEach((node) => links.forEach((link) => clearLine(node, link, speed)))
  }

  force.initialize = (initialNodes) => {
    nodes = initialNodes
  }
  force.strength = (value) => {
    strength = value
    return force
  }
  return force
}

const LABEL_CLEARANCE = RADIUS + 14
const TITLE_CLEARANCE = 26

function pointNear(node, other) {
  const dx = other.x - node.x
  const dy = other.y - node.y
  const length = Math.hypot(dx, dy) || 1
  const clearance = LABEL_CLEARANCE + TITLE_CLEARANCE * Math.max(0, dy / length)
  const ratio = Math.min(0.5, clearance / length)
  return { x: node.x + dx * ratio, y: node.y + dy * ratio }
}

const LABEL_SPACE = 40
const TITLE_CHAR_WIDTH = 8

function minimumLength({ status }) {
  const ends = 2 * LABEL_CLEARANCE + TITLE_CLEARANCE
  if (!status) return ends
  return ends + LABEL_SPACE * (inverseStatus[status] ? 2 : 1)
}

function forceMinimumLength(links) {
  function force() {
    links.forEach((link) => {
      const { source, target } = link
      const dx = target.x - source.x || Math.random() - 0.5
      const dy = target.y - source.y || Math.random() - 0.5
      const length = Math.hypot(dx, dy)
      const missing = minimumLength(link) - length
      if (missing <= 0) return
      const shift = missing / length / 2
      source.x -= dx * shift
      source.y -= dy * shift
      target.x += dx * shift
      target.y += dy * shift
    })
  }
  force.initialize = () => {}
  return force
}

function collideRadius(node) {
  return Math.max(RADIUS * 2.5, (node.title.length * TITLE_CHAR_WIDTH) / 2 + 12)
}

function pairKey(a, b) {
  return [a, b].sort().join(':')
}

function forceUnlinkedRepulsion(pairs) {
  let nodes = []
  let strength = 0
  const linked = new Set(pairs.map(([a, b]) => pairKey(a, b)))

  function force(alpha) {
    nodes.forEach((a, i) => {
      nodes.slice(i + 1).forEach((b) => {
        if (linked.has(pairKey(a.uuid, b.uuid))) return
        const dx = b.x - a.x || Math.random() - 0.5
        const dy = b.y - a.y || Math.random() - 0.5
        const push = (strength * alpha) / Math.max(dx * dx + dy * dy, 100)
        a.vx -= dx * push
        a.vy -= dy * push
        b.vx += dx * push
        b.vy += dy * push
      })
    })
  }

  force.initialize = (initialNodes) => {
    nodes = initialNodes
  }
  force.strength = (value) => {
    strength = value
    return force
  }
  return force
}

export default {
  name: 'NetworkGraph',
  components: { AppIcon, BaseButton, BaseCard, ZoomButtons },
  mixins: [asyncActionMixin, panZoomMixin],
  props: {
    dossiers: { type: Array, required: true },
    relationships: { type: Array, required: true },
    focus: { type: String, default: '' },
    controls: { type: Boolean, default: false },
  },
  data() {
    return {
      RADIUS,
      SLIDERS,
      folderIcon: icons.folder,
      nodes: [],
      links: [],
      width: 0,
      height: 0,
      frame: 0,
      dragged: null,
      forces: { ...DEFAULT_FORCES },
      showControls: false,
      highlighted: '',
      connected: null,
    }
  },
  watch: {
    dossiers: 'start',
    relationships: 'start',
    forces: {
      deep: true,
      handler() {
        this.applyForces()
        this.simulation?.alpha(0.5).restart()
      },
    },
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
    unsaved() {
      const saved = this.dossiersStore.networkSettings
      return Boolean(saved) && SLIDERS.some(({ key }) => saved[key] !== this.forces[key])
    },
  },
  async created() {
    this.forces = { ...(await this.dossiersStore.fetchNetworkSettings()) }
  },
  mounted() {
    this.resizeObserver = new ResizeObserver(([entry]) => this.resize(entry.contentRect))
    this.resizeObserver.observe(this.$refs.canvas)
    this.width = this.$refs.canvas.clientWidth
    this.height = this.$refs.canvas.clientHeight
    this.start()
  },
  beforeUnmount() {
    clearTimeout(this.hoverTimer)
    this.resizeObserver?.disconnect()
    this.simulation?.stop()
  },
  methods: {
    linkLabels(link) {
      const { source, target, status } = link
      const key = `label-${source.uuid}-${target.uuid}`
      if (!status) return []
      if (!inverseStatus[status]) {
        const text = statusLabels[status]
        return [{ key, link, text, x: (source.x + target.x) / 2, y: (source.y + target.y) / 2 }]
      }
      return [
        { key: `${key}-target`, link, text: statusLabels[status], ...pointNear(target, source) },
        {
          key: `${key}-source`,
          link,
          text: statusLabels[inverseStatus[status]],
          ...pointNear(source, target),
        },
      ]
    },
    start() {
      this.simulation?.stop()
      this.autoFit = true
      const nodes = this.dossiers.map((dossier) => ({
        ...dossier,
        x: this.width / 2 + (Math.random() - 0.5) * 100,
        y: this.height / 2 + (Math.random() - 0.5) * 100,
      }))
      const links = this.relationships.map((relationship) => ({
        source: relationship.dossier,
        target: relationship.person,
        status: relationship.status,
      }))
      this.simulation = markRaw(
        forceSimulation(nodes)
          .force(
            'link',
            forceLink(links).id((node) => node.uuid),
          )
          .force(
            'repulsion',
            forceUnlinkedRepulsion(this.relationships.map((r) => [r.dossier, r.person])),
          )
          .force('untangle', forceUntangle(links))
          .force('collide', forceCollide(collideRadius))
          .force('minimumLength', forceMinimumLength(links))
          .force('x', forceX())
          .force('y', forceY())
          .on('tick', () => this.tick()),
      )
      this.nodes = markRaw(nodes)
      this.links = markRaw(links)
      this.applyForces()
      this.resize({ width: this.width, height: this.height })
    },
    applyForces() {
      if (!this.simulation) return
      const { attraction, distance, repulsion, gravity, untangling } = this.forces
      this.simulation
        .force('link')
        .strength(attraction / 50)
        .distance(distance)
      this.simulation.force('repulsion').strength(repulsion)
      this.simulation.force('x').strength(gravity / 200)
      this.simulation.force('y').strength(gravity / 200)
      this.simulation.force('untangle').strength(untangling / 100)
    },
    resize({ width, height }) {
      this.width = width
      this.height = height
      if (!this.simulation) return
      this.simulation.force('x').x(width / 2)
      this.simulation.force('y').y(height / 2)
      this.simulation.alpha(0.3).restart()
    },
    hoverStart(node) {
      clearTimeout(this.hoverTimer)
      this.hoverTimer = setTimeout(() => this.highlight(node.uuid), HOVER_DELAY)
    },
    hoverEnd() {
      clearTimeout(this.hoverTimer)
      this.highlighted = ''
      this.connected = null
    },
    highlight(uuid) {
      const neighbours = this.links
        .filter((link) => [link.source.uuid, link.target.uuid].includes(uuid))
        .flatMap((link) => [link.source.uuid, link.target.uuid])
      this.highlighted = uuid
      this.connected = new Set([uuid, ...neighbours])
    },
    isDimmedLink(link) {
      return (
        Boolean(this.highlighted) &&
        ![link.source.uuid, link.target.uuid].includes(this.highlighted)
      )
    },
    tick() {
      if (this.autoFit) this.fitView()
      this.frame++
    },
    fitView() {
      const xs = this.nodes.map((node) => node.x)
      const ys = this.nodes.map((node) => node.y)
      const [left, right] = [Math.min(...xs) - FIT_PADDING, Math.max(...xs) + FIT_PADDING]
      const [top, bottom] = [Math.min(...ys) - FIT_PADDING, Math.max(...ys) + FIT_PADDING]
      const k = Math.max(
        ZOOM_MIN,
        Math.min(FIT_MAX, this.width / (right - left), this.height / (bottom - top)),
      )
      this.view = {
        k,
        x: this.width / 2 - ((left + right) / 2) * k,
        y: this.height / 2 - ((top + bottom) / 2) * k,
      }
    },
    saveForces() {
      return this.runAction(() => this.dossiersStore.saveNetworkSettings(this.forces))
    },
    release() {
      this.nodes.forEach((node) => {
        node.fx = null
        node.fy = null
      })
      this.autoFit = true
      this.simulation.alpha(0.8).restart()
    },
    startDrag(event, node) {
      event.currentTarget.setPointerCapture(event.pointerId)
      this.dragged = node.uuid
      this.autoFit = false
      this.dragStart = { x: event.clientX, y: event.clientY, fx: node.fx, fy: node.fy }
      node.fx = node.x
      node.fy = node.y
      this.simulation.alphaTarget(0.3).restart()
    },
    drag(event, node) {
      if (this.dragged !== node.uuid) return
      const { x, y } = this.point(event)
      node.fx = x
      node.fy = y
    },
    endDrag(event, node) {
      if (this.dragged !== node.uuid) return
      const distance = Math.hypot(
        event.clientX - this.dragStart.x,
        event.clientY - this.dragStart.y,
      )
      this.dragged = null
      this.simulation.alphaTarget(0)
      if (distance >= CLICK_DISTANCE) return
      node.fx = this.dragStart.fx
      node.fy = this.dragStart.fy
      if (event.type === 'pointerup') {
        this.$router.push({
          name: 'dossier',
          params: { uuid: node.uuid },
          query: { tab: 'relationships' },
        })
      }
    },
  },
}
</script>
