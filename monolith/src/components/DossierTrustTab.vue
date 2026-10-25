<template>
  <BaseCard class="border-t-0">
    <div class="flex items-start justify-between gap-4 px-6 pt-4">
      <div v-if="ledger" class="flex flex-col gap-1 text-sm">
        <TrustPoints :points="ledger.points" class="text-2xl!" />
        <span class="text-wntrs-muted">
          Kreis {{ ledger.level ?? '–' }} · Vorschlag {{ ledger.suggested_level ?? '–' }}
        </span>
      </div>
      <div v-else-if="!error" class="skeleton h-12 w-32"></div>
      <EditToggle v-model="editing" />
    </div>

    <form
      v-if="editing && ledger"
      class="flex flex-col gap-2 px-6 pt-4 pb-4 border-b border-wntrs-border"
      @submit.prevent="add"
    >
      <div class="flex gap-2">
        <select
          v-model="draft.conduct"
          aria-label="Verhalten"
          class="select flex-1 min-w-0"
          required
        >
          <option value="" disabled>Verhalten wählen</option>
          <option v-for="conduct in conducts" :key="conduct.value" :value="conduct.value">
            {{ conduct.label }} ({{ formatPoints(conduct.points) }})
          </option>
        </select>
        <input v-model="draft.date" type="date" aria-label="Datum" class="input w-40" required />
      </div>
      <textarea
        v-model="draft.text"
        aria-label="Begründung"
        placeholder="Begründung"
        class="textarea w-full"
        rows="2"
        required
      ></textarea>
      <div v-if="traitOptions.length" class="flex flex-col gap-1">
        <span class="text-xs text-wntrs-muted">Charakter</span>
        <ul class="flex flex-wrap gap-1.5">
          <li v-for="trait in traitOptions" :key="trait">
            <button
              type="button"
              class="badge badge-sm cursor-pointer"
              :class="
                draft.traits.includes(trait) ? 'badge-primary' : 'badge-ghost hover:badge-primary'
              "
              :aria-pressed="draft.traits.includes(trait)"
              @click="toggleTrait(trait)"
            >
              {{ trait }}
            </button>
          </li>
        </ul>
      </div>
      <div class="flex gap-2">
        <select v-model="draft.event" aria-label="Ereignis" class="select flex-1 min-w-0">
          <option :value="null">Kein Ereignis</option>
          <option v-for="event in events" :key="event.uuid" :value="event.uuid">
            {{ formatDate(event.date) }} · {{ event.title }}
          </option>
        </select>
        <BaseButton type="submit" shape="square" title="Hinzufügen" :disabled="saving">
          <AppIcon name="plus" alt="Hinzufügen" />
        </BaseButton>
      </div>
    </form>

    <div v-if="!ledger && !error" class="flex flex-col gap-3 px-6 py-4">
      <div v-for="n in 3" :key="n" class="skeleton h-14 w-full"></div>
    </div>

    <ul v-else-if="ledger?.entries.length" class="flex flex-col divide-y divide-wntrs-border">
      <TrustEntryRow v-for="entry in ledger.entries" :key="entry.uuid" :uuid="uuid" :entry="entry">
        <BaseButton
          v-if="editing"
          variant="neutral"
          shape="square"
          size="sm"
          title="Entfernen"
          :disabled="saving"
          @click="remove(entry)"
        >
          <AppIcon name="trash" alt="Entfernen" />
        </BaseButton>
      </TrustEntryRow>
    </ul>

    <p v-else-if="ledger" class="px-6 py-4 text-sm text-wntrs-muted">Noch keine Einträge.</p>

    <p v-if="error" class="text-error text-sm px-6 py-4">{{ error }}</p>
  </BaseCard>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import EditToggle from '@/components/EditToggle.vue'
import TrustEntryRow from '@/components/TrustEntryRow.vue'
import TrustPoints from '@/components/TrustPoints.vue'
import { formatDate } from '@/data/dossierFields.js'
import { conductLabels, formatPoints } from '@/data/trust.js'
import { useDossiersStore } from '@/stores/dossiers.js'

function emptyDraft() {
  return {
    conduct: '',
    date: new Date().toLocaleDateString('sv-SE'),
    text: '',
    event: null,
    traits: [],
  }
}

export default {
  name: 'DossierTrustTab',
  components: { AppIcon, BaseButton, BaseCard, EditToggle, TrustEntryRow, TrustPoints },
  mixins: [asyncActionMixin],
  props: {
    uuid: { type: String, required: true },
  },
  data() {
    return {
      ledger: null,
      events: [],
      editing: false,
      draft: emptyDraft(),
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
    conducts() {
      return Object.entries(this.ledger.conducts).map(([value, points]) => ({
        value,
        points,
        label: conductLabels[value],
      }))
    },
    traitOptions() {
      const suggested = this.ledger.conduct_traits[this.draft.conduct] ?? []
      return [...new Set([...this.ledger.traits, ...suggested])]
    },
  },
  watch: {
    'draft.conduct'(conduct) {
      this.draft.traits = [...(this.ledger.conduct_traits[conduct] ?? [])]
    },
    editing(editing) {
      this.draft = emptyDraft()
      if (editing) return this.loadEvents()
    },
    uuid: {
      immediate: true,
      handler() {
        this.ledger = null
        this.editing = false
        return this.runAction(async () => {
          this.ledger = await this.dossiersStore.fetchTrustEntries(this.uuid)
        })
      },
    },
  },
  methods: {
    formatDate,
    formatPoints,
    loadEvents() {
      return this.runAction(async () => {
        this.events = await this.dossiersStore.fetchEvents(this.uuid)
      })
    },
    add() {
      return this.runAction(async () => {
        this.ledger = await this.dossiersStore.addTrustEntry(this.uuid, this.draft)
        this.draft = emptyDraft()
      })
    },
    toggleTrait(trait) {
      const traits = this.draft.traits
      this.draft.traits = traits.includes(trait)
        ? traits.filter((t) => t !== trait)
        : [...traits, trait]
    },
    remove(entry) {
      return this.runAction(async () => {
        this.ledger = await this.dossiersStore.removeTrustEntry(this.uuid, entry.uuid)
      })
    },
  },
}
</script>
