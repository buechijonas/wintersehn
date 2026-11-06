<template>
  <div class="atlas-markdown" v-html="html"></div>
</template>

<script>
export default {
  name: 'MarkdownContent',
  props: {
    html: { type: String, required: true },
  },
}
</script>
