<template>
  <BaseCard class="border-t-0">
    <div class="flex justify-end px-6 pt-4">
      <EditToggle v-model="editing" />
    </div>

    <div v-if="!character && !error" class="px-6 py-4">
      <div class="skeleton h-12 w-full"></div>
    </div>

    <div v-else-if="character" class="px-6 py-4">
      <TagEditor
        label="Charakter"
        :tags="character.tags"
        :suggestions="character.suggestions"
        :group-labels="characterGroups"
        :editing="editing"
        :saving="saving"
        @save="save"
      />
      <p v-if="!character.tags.length && !editing" class="text-sm text-wntrs-muted">
        Noch keine Merkmale.
      </p>
    </div>

    <p v-if="error" class="text-error text-sm px-6 py-4">{{ error }}</p>
  </BaseCard>
</template>

<script>
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import EditToggle from '@/components/EditToggle.vue'
import TagEditor from '@/components/TagEditor.vue'
import { characterGroups } from '@/data/character.js'
import { useDossiersStore } from '@/stores/dossiers.js'

export default {
  name: 'DossierCharacterTab',
  components: { BaseCard, EditToggle, TagEditor },
  mixins: [asyncActionMixin],
  props: {
    uuid: { type: String, required: true },
  },
  data() {
    return {
      characterGroups,
      character: null,
      editing: false,
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
  },
  watch: {
    uuid: {
      immediate: true,
      handler() {
        this.character = null
        this.editing = false
        return this.runAction(async () => {
          this.character = await this.dossiersStore.fetchCharacter(this.uuid)
        })
      },
    },
  },
  methods: {
    save(tags) {
      return this.runAction(async () => {
        this.character = await this.dossiersStore.saveCharacter(this.uuid, tags)
      })
    },
  },
}
</script>
