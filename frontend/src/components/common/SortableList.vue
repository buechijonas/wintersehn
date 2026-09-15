<template>
  <div v-bind="$attrs">
    <div
      v-for="(item, index) in displayItems"
      :key="index"
      draggable="true"
      class="cursor-move"
      :class="{ 'opacity-40': draggedItem === item }"
      @dragstart="onDragStart(item, $event)"
      @dragenter.prevent="onDragEnter(item)"
      @dragover.prevent
      @drop.prevent="onDrop"
      @dragend="onDragEnd"
    >
      <slot :item="item" :index="index" />
    </div>
    <slot name="append" />
  </div>
</template>

<script>
export default {
  name: 'SortableList',
  inheritAttrs: false,
  props: {
    items: { type: Array, required: true },
    disabled: { type: Boolean, default: false },
  },
  emits: ['reorder'],
  data() {
    return {
      draggedItem: null,
      workingItems: null,
      changed: false,
    }
  },
  computed: {
    displayItems() {
      return this.workingItems ?? this.items
    },
  },
  methods: {
    onDragStart(item, event) {
      if (this.disabled || event.target.closest('button')) {
        event.preventDefault()
        return
      }
      this.draggedItem = item
      this.workingItems = [...this.items]
      this.changed = false
      event.dataTransfer.effectAllowed = 'move'
      event.dataTransfer.setData('text/plain', '')
    },
    onDragEnter(targetItem) {
      if (!this.draggedItem || targetItem === this.draggedItem) return
      const from = this.workingItems.indexOf(this.draggedItem)
      const to = this.workingItems.indexOf(targetItem)
      if (from === -1 || to === -1) return
      const reordered = [...this.workingItems]
      reordered.splice(from, 1)
      reordered.splice(to, 0, this.draggedItem)
      this.workingItems = reordered
      this.changed = true
    },
    onDrop() {
      this.finishDrag()
    },
    onDragEnd() {
      this.finishDrag()
    },
    finishDrag() {
      if (this.changed && this.workingItems) {
        this.$emit('reorder', this.workingItems)
      }
      this.draggedItem = null
      this.workingItems = null
      this.changed = false
    },
  },
}
</script>
