<template>
  <svg
    :viewBox="`0 0 ${layout.width} ${layout.height}`"
    class="w-full"
    role="img"
    :aria-label="title"
  >
    <defs>
      <marker
        :id="arrowId"
        viewBox="0 0 10 10"
        refX="9"
        refY="5"
        markerWidth="7"
        markerHeight="7"
        orient="auto-start-reverse"
      >
        <path d="M0 0L10 5L0 10z" class="fill-wntrs-muted" />
      </marker>
    </defs>
    <g v-for="group in layout.groups" :key="group.label">
      <rect
        :x="group.x"
        :y="group.y"
        :width="group.width"
        :height="group.height"
        rx="16"
        stroke-dasharray="6 4"
        class="fill-base-200 stroke-wntrs-border"
      />
      <text :x="group.x + 14" :y="group.y + 22" class="fill-primary text-xs font-semibold">
        {{ group.label }}
      </text>
    </g>
    <text
      v-for="column in layout.columns"
      :key="column.title"
      :x="column.x + COLUMN_WIDTH / 2"
      :y="layout.titleY"
      text-anchor="middle"
      class="fill-wntrs-muted text-xs font-medium"
    >
      {{ column.title }}
    </text>
    <path
      v-for="edge in layout.edges"
      :key="edge.key"
      :d="edge.path"
      fill="none"
      class="stroke-wntrs-muted"
      stroke-width="1.5"
      :marker-end="`url(#${arrowId})`"
    />
    <g v-for="node in layout.nodes" :key="node.id">
      <rect
        :x="node.x"
        :y="node.y"
        :width="COLUMN_WIDTH"
        :height="NODE_HEIGHT"
        rx="10"
        class="fill-base-100 stroke-wntrs-border"
      />
      <text
        :x="node.x + COLUMN_WIDTH / 2"
        :y="node.y + (node.note ? 22 : 30)"
        text-anchor="middle"
        class="fill-base-content text-sm font-medium"
      >
        {{ node.label }}
      </text>
      <text
        v-if="node.note"
        :x="node.x + COLUMN_WIDTH / 2"
        :y="node.y + 40"
        text-anchor="middle"
        class="fill-wntrs-muted text-xs"
      >
        {{ node.note }}
      </text>
    </g>
  </svg>
</template>

<script>
const COLUMN_WIDTH = 160
const COLUMN_GAP = 56
const NODE_HEIGHT = 52
const ROW_GAP = 18
const GROUP_PAD = 16
const GROUP_LABEL = 26

function groupsOf(columns) {
  return columns.reduce((groups, column, index) => {
    const last = groups.at(-1)
    if (!column.group) return groups
    if (last && last.label === column.group && last.end === index - 1) {
      last.end = index
      return groups
    }
    return [...groups, { label: column.group, start: index, end: index }]
  }, [])
}

export default {
  name: 'DiagramCanvas',
  props: {
    title: { type: String, required: true },
    columns: { type: Array, required: true },
    edges: { type: Array, default: () => [] },
    variant: { type: String, default: 'inline' },
  },
  data() {
    return { COLUMN_WIDTH, NODE_HEIGHT }
  },
  computed: {
    arrowId() {
      return `arrow-${this.variant}-${this.title.toLowerCase().replace(/\W+/g, '-')}`
    },
    layout() {
      const grouped = groupsOf(this.columns)
      const pad = grouped.length ? GROUP_PAD : 0
      const titleY = pad + (grouped.length ? GROUP_LABEL : 0) + 14
      const top = titleY + 16
      const rows = Math.max(...this.columns.map((column) => column.nodes.length))
      const step = NODE_HEIGHT + ROW_GAP
      const bottom = top + rows * step - ROW_GAP
      const columns = this.columns.map((column, index) => ({
        title: column.title,
        x: pad + index * (COLUMN_WIDTH + COLUMN_GAP),
        offset: ((rows - column.nodes.length) * step) / 2,
        nodes: column.nodes,
      }))
      const nodes = columns.flatMap((column) =>
        column.nodes.map((node, row) => ({
          ...node,
          x: column.x,
          y: top + column.offset + row * step,
        })),
      )
      const groups = grouped.map((group) => ({
        label: group.label,
        x: columns[group.start].x - pad,
        y: 0,
        width: columns[group.end].x + COLUMN_WIDTH - columns[group.start].x + 2 * pad,
        height: bottom + pad,
      }))
      const byId = Object.fromEntries(nodes.map((node) => [node.id, node]))
      const edges = this.edges
        .filter(([from, to]) => byId[from] && byId[to])
        .map(([from, to]) => {
          const start = { x: byId[from].x + COLUMN_WIDTH, y: byId[from].y + NODE_HEIGHT / 2 }
          const end = { x: byId[to].x - 2, y: byId[to].y + NODE_HEIGHT / 2 }
          const bend = (end.x - start.x) / 2
          return {
            key: `${from}-${to}`,
            path: `M${start.x} ${start.y}C${start.x + bend} ${start.y} ${end.x - bend} ${end.y} ${end.x} ${end.y}`,
          }
        })
      const width = columns.at(-1).x + COLUMN_WIDTH + pad
      return { columns, nodes, edges, groups, titleY, width, height: bottom + 2 * pad }
    },
  },
}
</script>
