<template>
  <li class="px-6 py-4">
    <SpectrumBar :label="topic.label" :poles="topic.poles" :value="stance.value" />

    <ul v-if="stance.tags.length" class="flex flex-wrap gap-1.5 mt-3">
      <li v-for="tag in stance.tags" :key="tag" class="badge badge-soft gap-1">
        {{ tag }}
        <button
          v-if="editing"
          type="button"
          class="cursor-pointer"
          :title="`${tag} entfernen`"
          :disabled="saving"
          @click="remove(tag)"
        >
          <AppIcon name="cross" :alt="`${tag} entfernen`" class="size-2.5!" />
        </button>
      </li>
    </ul>

    <template v-if="editing">
      <form class="flex gap-2 mt-3" @submit.prevent="add(draft)">
        <input
          v-model.trim="draft"
          type="text"
          maxlength="60"
          placeholder="Merkmal hinzufügen"
          :aria-label="`Merkmal zu ${topic.label} hinzufügen`"
          class="input input-sm flex-1"
        />
        <BaseButton
          type="submit"
          size="sm"
          shape="square"
          title="Hinzufügen"
          :disabled="saving || !draft"
        >
          <AppIcon name="plus" alt="Hinzufügen" />
        </BaseButton>
      </form>

      <div v-for="[group, tags] in suggestions" :key="group" class="mt-3">
        <span class="text-xs text-wntrs-muted">{{ suggestionGroups[group] }}</span>
        <ul class="flex flex-wrap gap-1.5 mt-1">
          <li v-for="tag in tags" :key="tag">
            <button
              type="button"
              class="badge badge-sm badge-ghost cursor-pointer hover:badge-primary"
              :disabled="saving"
              @click="add(tag)"
            >
              + {{ tag }}
            </button>
          </li>
        </ul>
      </div>
    </template>
  </li>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import SpectrumBar from '@/components/SpectrumBar.vue'
import { suggestionGroups } from '@/data/topics.js'

export default {
  name: 'StanceRow',
  components: { AppIcon, BaseButton, SpectrumBar },
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
      draft: '',
    }
  },
  computed: {
    suggestions() {
      const query = this.draft.toLowerCase()
      const visible = (tag) => !this.stance.tags.includes(tag) && tag.toLowerCase().includes(query)
      return Object.entries(this.stance.suggestions)
        .map(([group, tags]) => [group, tags.filter(visible)])
        .filter(([, tags]) => tags.length)
    },
  },
  watch: {
    editing() {
      this.draft = ''
    },
  },
  methods: {
    remove(tag) {
      const tags = this.stance.tags.filter((t) => t !== tag)
      this.$emit('save', tags)
    },
    add(tag) {
      this.$emit('save', [...this.stance.tags, tag])
      this.draft = ''
    },
  },
}
</script>
