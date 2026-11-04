<template>
  <li class="px-6 py-4">
    <SpectrumBar :label="topic.label" :poles="topic.poles" :value="stance.value" />
    <TagEditor
      class="mt-3"
      :label="topic.label"
      :tags="stance.tags"
      :suggestions="stance.suggestions"
      :group-labels="suggestionGroups"
      :editing="editing"
      :saving="saving"
      @save="$emit('save', $event)"
    />
  </li>
</template>

<script>
import SpectrumBar from '@/components/SpectrumBar.vue'
import TagEditor from '@/components/TagEditor.vue'
import { suggestionGroups } from '@/data/topics.js'

export default {
  name: 'StanceRow',
  components: { SpectrumBar, TagEditor },
  props: {
    topic: { type: Object, required: true },
    stance: { type: Object, required: true },
    editing: { type: Boolean, default: false },
    saving: { type: Boolean, default: false },
  },
  emits: ['save'],
  data() {
    return {
      suggestionGroups,
    }
  },
}
</script>
