<template>
  <div v-if="html.trim()" class="markdown" v-html="html"></div>
  <p v-else-if="placeholder" class="text-sm text-wntrs-muted">{{ placeholder }}</p>
</template>

<script>
export default {
  name: 'MarkdownContent',
  props: {
    html: { type: String, default: '' },
    placeholder: { type: String, default: '' },
  },
}
</script>
