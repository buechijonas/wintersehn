<template>
  <h3 class="text-xl font-light my-4">Erkenntnisse</h3>
  <BaseCard class="px-6 pb-4">
    <div class="flex justify-end pt-4">
      <EditToggle v-model="editing" />
    </div>

    <template v-if="!editing">
      <EventLinks v-if="selected.size" :event="event" />
      <p v-else class="text-sm text-wntrs-muted">Noch nichts verknüpft.</p>
    </template>

    <div v-else-if="!options && !error" class="skeleton h-24 w-full"></div>

    <template v-else-if="options">
      <div v-for="group in options" :key="group.label" class="not-first:mt-3">
        <span class="text-xs text-wntrs-muted">{{ group.label }}</span>
        <p v-if="!group.links.length" class="mt-1 text-sm text-wntrs-muted">
          Im Tab «{{ group.label }}» ist noch nichts erfasst.
        </p>
        <ul v-else class="flex flex-wrap gap-1.5 mt-1">
          <li v-for="item in group.links" :key="item.key">
            <button
              type="button"
              class="badge badge-sm cursor-pointer"
              :class="selected.has(item.key) ? 'badge-primary' : 'badge-ghost hover:badge-primary'"
              :aria-pressed="selected.has(item.key)"
              :disabled="saving"
              @click="toggle(item.key)"
            >
              {{ item.text }}
            </button>
          </li>
        </ul>
      </div>
    </template>

    <p v-if="error" class="text-error text-sm mt-3">{{ error }}</p>
  </BaseCard>
</template>

<script>
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import EditToggle from '@/components/EditToggle.vue'
import EventLinks from '@/components/EventLinks.vue'
import {
  addictionLink,
  eventLinks,
  linkTypes,
  referenceLink,
  relationshipLink,
  stanceLink,
  traitLink,
} from '@/data/links.js'
import { useDossiersStore } from '@/stores/dossiers.js'

export default {
  name: 'EventLinksCard',
  components: { BaseCard, EditToggle, EventLinks },
  mixins: [asyncActionMixin],
  props: {
    uuid: { type: String, required: true },
    event: { type: Object, required: true },
  },
  emits: ['update'],
  data() {
    return {
      editing: false,
      options: null,
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
    selected() {
      return new Set(eventLinks(this.event).map((item) => item.key))
    },
  },
  watch: {
    editing(editing) {
      if (editing && !this.options) this.loadOptions()
    },
  },
  methods: {
    loadOptions() {
      return this.runAction(async () => {
        const [stances, character, addictions, references, relationships] = await Promise.all([
          this.dossiersStore.fetchStances(this.uuid),
          this.dossiersStore.fetchCharacter(this.uuid),
          this.dossiersStore.fetchAddictions(this.uuid),
          this.dossiersStore.fetchReferences(this.uuid),
          this.dossiersStore.fetchRelationships(this.uuid),
        ])
        this.options = [
          {
            label: 'Ideologie',
            links: stances.flatMap(({ topic, tags }) =>
              tags.map((tag) => stanceLink({ topic, tag })),
            ),
          },
          { label: 'Charakter', links: character.tags.map(traitLink) },
          { label: 'Sucht', links: addictions.map(addictionLink) },
          { label: 'Beziehungen', links: relationships.map(relationshipLink) },
          { label: 'Referenzen', links: references.map(referenceLink) },
        ]
      })
    },
    toggle(key) {
      const keys = new Set(this.selected)
      if (!keys.delete(key)) keys.add(key)
      const chosen = this.options
        .flatMap((group) => group.links)
        .filter((item) => keys.has(item.key))
      const links = Object.fromEntries(
        linkTypes.map((type) => [
          type,
          chosen.filter((item) => item.type === type).map((item) => item.ref),
        ]),
      )
      return this.runAction(async () => {
        this.$emit('update', await this.dossiersStore.linkEvent(this.uuid, this.event.uuid, links))
      })
    },
  },
}
</script>
