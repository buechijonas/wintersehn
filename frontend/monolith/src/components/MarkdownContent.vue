<template>
  <div v-if="text.trim()" class="markdown" v-html="html"></div>
  <p v-else class="text-sm text-wntrs-muted">{{ placeholder }}</p>
</template>

<script>
import { renderMarkdown } from '@/lib/markdown.js'

export default {
  name: 'MarkdownContent',
  props: {
    text: { type: String, default: '' },
    placeholder: { type: String, default: 'Noch kein Text.' },
  },
  computed: {
    html() {
      return renderMarkdown(this.text)
    },
  },
}
</script>
