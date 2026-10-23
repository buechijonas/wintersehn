<template>
  <svg
    viewBox="-1.8 -1.8 3.6 3.6"
    class="w-full max-w-96 mx-auto aspect-square touch-none select-none"
    :class="dragging ? 'cursor-grabbing' : 'cursor-grab'"
    role="img"
    :aria-label="description"
    @pointerdown="startRotate"
    @pointermove="rotate"
    @pointerup="endRotate"
    @pointercancel="endRotate"
  >
    <line
      v-for="(edge, index) in edges"
      :key="`edge-${index}`"
      v-bind="edge"
      class="stroke-base-300"
      stroke-width="0.012"
    />
    <line
      v-for="axis in axes"
      :key="`axis-${axis.key}`"
      v-bind="axis.line"
      class="stroke-wntrs-muted"
      stroke-width="0.008"
      stroke-dasharray="0.04 0.04"
    />
    <text
      v-for="label in labels"
      :key="label.key"
      :x="label.x"
      :y="label.y"
      font-size="0.11"
      text-anchor="middle"
      dominant-baseline="middle"
      class="fill-wntrs-muted stroke-base-100 [paint-order:stroke]"
      stroke-width="0.03"
    >
      {{ label.text }}
    </text>
    <template v-if="point">
      <line v-bind="point.drop" class="stroke-primary/50" stroke-width="0.01" />
      <circle :cx="point.floor.x" :cy="point.floor.y" r="0.035" class="fill-primary/30" />
      <circle :cx="point.position.x" :cy="point.position.y" r="0.07" class="fill-primary" />
    </template>
  </svg>
</template>

<script>
const CORNERS = [-1, 1]
const VERTICES = CORNERS.flatMap((x) => CORNERS.flatMap((y) => CORNERS.map((z) => [x, y, z])))
const EDGES = VERTICES.flatMap((a, i) =>
  VERTICES.slice(i + 1)
    .filter((b) => a.filter((value, k) => value !== b[k]).length === 1)
    .map((b) => [a, b]),
)
const AXIS_KEYS = ['economy', 'freedom', 'society']
const LABEL_DISTANCE = 1.35
const CAMERA_DISTANCE = 5
const ROTATE_SPEED = 0.01
const PITCH_LIMIT = 1.3

function unit(index, length) {
  return AXIS_KEYS.map((key, k) => (k === index ? length : 0))
}

export default {
  name: 'StanceCompass',
  props: {
    compass: { type: Object, required: true },
    axisLabels: { type: Object, required: true },
  },
  data() {
    return {
      yaw: -0.6,
      pitch: 0.35,
      dragging: null,
    }
  },
  computed: {
    edges() {
      return EDGES.map(([a, b]) => this.segment(a, b))
    },
    axes() {
      return AXIS_KEYS.map((key, index) => ({
        key,
        line: this.segment(unit(index, -1), unit(index, 1)),
      }))
    },
    labels() {
      return AXIS_KEYS.flatMap((key, index) =>
        this.axisLabels[key].poles.map((text, side) => ({
          key: `${key}-${side}`,
          text,
          ...this.project(unit(index, side ? LABEL_DISTANCE : -LABEL_DISTANCE)),
        })),
      )
    },
    point() {
      const values = AXIS_KEYS.map((key) => this.compass[key])
      if (values.every((value) => value === null)) return null
      const [x, y, z] = values.map((value) => (value ?? 0) / 100)
      return {
        position: this.project([x, y, z]),
        floor: this.project([x, -1, z]),
        drop: this.segment([x, y, z], [x, -1, z]),
      }
    },
    description() {
      return AXIS_KEYS.map((key) => {
        const value = this.compass[key]
        return `${this.axisLabels[key].label}: ${value ?? 'nicht einstufbar'}`
      }).join(', ')
    },
  },
  methods: {
    project([x, y, z]) {
      const [cosYaw, sinYaw] = [Math.cos(this.yaw), Math.sin(this.yaw)]
      const [cosPitch, sinPitch] = [Math.cos(this.pitch), Math.sin(this.pitch)]
      const turnedX = x * cosYaw + z * sinYaw
      const turnedZ = z * cosYaw - x * sinYaw
      const tiltedY = y * cosPitch - turnedZ * sinPitch
      const depth = y * sinPitch + turnedZ * cosPitch
      const scale = CAMERA_DISTANCE / (CAMERA_DISTANCE + depth)
      return { x: turnedX * scale, y: -tiltedY * scale }
    },
    segment(a, b) {
      const [start, end] = [this.project(a), this.project(b)]
      return { x1: start.x, y1: start.y, x2: end.x, y2: end.y }
    },
    startRotate(event) {
      event.currentTarget.setPointerCapture(event.pointerId)
      this.dragging = { x: event.clientX, y: event.clientY }
    },
    rotate(event) {
      if (!this.dragging) return
      this.yaw += (event.clientX - this.dragging.x) * ROTATE_SPEED
      this.pitch = Math.min(
        PITCH_LIMIT,
        Math.max(-PITCH_LIMIT, this.pitch + (event.clientY - this.dragging.y) * ROTATE_SPEED),
      )
      this.dragging = { x: event.clientX, y: event.clientY }
    },
    endRotate() {
      this.dragging = null
    },
  },
}
</script>
