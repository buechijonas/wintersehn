<template>
  <ul v-if="links.length" class="flex flex-wrap gap-1.5">
    <li v-for="item in links" :key="item.key" class="badge badge-sm badge-soft">
      {{ item.text }}
    </li>
  </ul>
</template>

<script>
import { eventLinks } from '@/data/links.js'

export default {
  name: 'EventLinks',
  props: {
    event: { type: Object, required: true },
  },
  computed: {
    links() {
      return eventLinks(this.event)
    },
  },
}
</script>
