<template>
  <BaseCard class="overflow-hidden">
    <div
      class="flex items-center gap-2 border-b border-wntrs-border px-4 py-2 text-xs text-wntrs-muted"
    >
      <AppIcon name="code-simple" />
      <a
        v-if="url"
        :href="url"
        target="_blank"
        rel="noopener noreferrer"
        class="link truncate font-mono link-hover hover:text-primary"
      >
        {{ file }}
      </a>
      <span v-else class="truncate font-mono">{{ file }}</span>
      <a
        v-if="url"
        :href="url"
        target="_blank"
        rel="noopener noreferrer"
        class="ml-auto flex shrink-0 items-center gap-1 hover:text-primary"
      >
        <AppIcon name="share-square" />
        GitHub
      </a>
    </div>
    <pre
      class="overflow-x-auto bg-base-200 p-4 text-sm leading-relaxed"
    ><code>{{ code }}</code></pre>
  </BaseCard>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseCard from '@core/components/common/BaseCard.vue'

export default {
  name: 'CodeSnippet',
  components: { AppIcon, BaseCard },
  props: {
    file: { type: String, required: true },
    code: { type: String, required: true },
    url: { type: String, default: '' },
  },
}
</script>
