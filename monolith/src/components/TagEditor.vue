<template>
  <div class="flex flex-col gap-3 empty:hidden">
    <ul v-if="tags.length" class="flex flex-wrap gap-1.5">
      <li v-for="tag in tags" :key="tag" class="badge badge-soft gap-1">
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
      <form class="flex gap-2" @submit.prevent="add(draft)">
        <input
          v-model.trim="draft"
          type="text"
          maxlength="60"
          placeholder="Merkmal hinzufügen"
          :aria-label="`Merkmal zu ${label} hinzufügen`"
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

      <div v-for="[group, groupTags] in visibleSuggestions" :key="group">
        <span class="text-xs text-wntrs-muted">{{ groupLabels[group] }}</span>
        <ul class="flex flex-wrap gap-1.5 mt-1">
          <li v-for="tag in groupTags" :key="tag">
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
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'

export default {
  name: 'TagEditor',
  components: { AppIcon, BaseButton },
  props: {
    label: { type: String, required: true },
    tags: { type: Array, required: true },
    suggestions: { type: Object, required: true },
    groupLabels: { type: Object, required: true },
    editing: { type: Boolean, default: false },
    saving: { type: Boolean, default: false },
  },
  emits: ['save'],
  data() {
    return {
      draft: '',
    }
  },
  computed: {
    visibleSuggestions() {
      const query = this.draft.toLowerCase()
      const visible = (tag) => !this.tags.includes(tag) && tag.toLowerCase().includes(query)
      return Object.entries(this.suggestions)
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
      this.$emit(
        'save',
        this.tags.filter((t) => t !== tag),
      )
    },
    add(tag) {
      this.$emit('save', [...this.tags, tag])
      this.draft = ''
    },
  },
}
</script>
