export const ZOOM_MIN = 0.2
const ZOOM_MAX = 4

export default {
  data() {
    return {
      view: { x: 0, y: 0, k: 1 },
      panning: false,
      autoFit: true,
    }
  },
  created() {
    this.pointers = new Map()
  },
  methods: {
    point(event) {
      const matrix = this.$refs.viewport.getScreenCTM().inverse()
      return new DOMPoint(event.clientX, event.clientY).matrixTransform(matrix)
    },
    zoomAt(factor, clientX, clientY) {
      const k = Math.min(ZOOM_MAX, Math.max(ZOOM_MIN, this.view.k * factor))
      const svg = this.$refs.viewport.ownerSVGElement
      const origin = new DOMPoint(clientX, clientY).matrixTransform(svg.getScreenCTM().inverse())
      const ratio = k / this.view.k
      this.view = {
        k,
        x: origin.x - (origin.x - this.view.x) * ratio,
        y: origin.y - (origin.y - this.view.y) * ratio,
      }
    },
    zoomBy(factor) {
      this.autoFit = false
      const rect = this.$refs.canvas.getBoundingClientRect()
      this.zoomAt(factor, rect.left + rect.width / 2, rect.top + rect.height / 2)
    },
    wheel(event) {
      this.autoFit = false
      this.zoomAt(Math.exp(-event.deltaY / 500), event.clientX, event.clientY)
    },
    startPan(event) {
      event.currentTarget.setPointerCapture(event.pointerId)
      this.pointers.set(event.pointerId, { x: event.clientX, y: event.clientY })
      this.panning = true
      this.autoFit = false
    },
    pan(event) {
      const previous = this.pointers.get(event.pointerId)
      if (!previous) return
      const [other] = [...this.pointers].filter(([id]) => id !== event.pointerId)
      const current = { x: event.clientX, y: event.clientY }
      this.pointers.set(event.pointerId, current)
      if (other) {
        const [, fixed] = other
        const factor =
          Math.hypot(current.x - fixed.x, current.y - fixed.y) /
          Math.hypot(previous.x - fixed.x, previous.y - fixed.y)
        this.zoomAt(factor, (current.x + fixed.x) / 2, (current.y + fixed.y) / 2)
        return
      }
      const scale = this.$refs.viewport.ownerSVGElement.getScreenCTM().a
      this.view = {
        ...this.view,
        x: this.view.x + (current.x - previous.x) / scale,
        y: this.view.y + (current.y - previous.y) / scale,
      }
    },
    endPan(event) {
      this.pointers.delete(event.pointerId)
      this.panning = this.pointers.size > 0
    },
  },
}
