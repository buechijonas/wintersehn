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
      <li v-for="entry in ledger.entries" :key="entry.uuid" class="flex gap-4 px-6 py-4 text-sm">
        <div class="flex flex-col gap-0.5 flex-1 min-w-0">
          <span class="font-mono italic text-xs text-wntrs-muted">
            {{ formatDate(entry.date) }}
          </span>
          <span class="font-bold">{{ conductLabels[entry.conduct] }}</span>
          <span class="break-words whitespace-pre-line">{{ entry.text }}</span>
          <RouterLink
            v-if="entry.event"
            :to="{ name: 'event', params: { uuid, event: entry.event } }"
            class="text-xs text-primary truncate hover:underline"
          >
            {{ entry.event_title }}
          </RouterLink>
        </div>
        <div class="flex items-start gap-2 shrink-0">
          <TrustPoints :points="entry.points" />
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
        </div>
      </li>
    </ul>

    <p v-else-if="ledger" class="px-6 py-4 text-sm text-wntrs-muted">Noch keine Einträge.</p>

    <p v-if="error" class="text-error text-sm px-6 py-4">{{ error }}</p>
  </BaseCard>
</template>

<script>
import { RouterLink } from 'vue-router'
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import EditToggle from '@/components/EditToggle.vue'
import TrustPoints from '@/components/TrustPoints.vue'
import { formatDate } from '@/data/dossierFields.js'
import { conductLabels, formatPoints } from '@/data/trust.js'
import { useDossiersStore } from '@/stores/dossiers.js'

function emptyDraft() {
  return { conduct: '', date: new Date().toLocaleDateString('sv-SE'), text: '', event: null }
}

export default {
  name: 'DossierTrustTab',
  components: { RouterLink, AppIcon, BaseButton, BaseCard, EditToggle, TrustPoints },
  mixins: [asyncActionMixin],
  props: {
    uuid: { type: String, required: true },
  },
  data() {
    return {
      conductLabels,
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
  },
  watch: {
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
    remove(entry) {
      return this.runAction(async () => {
        this.ledger = await this.dossiersStore.removeTrustEntry(this.uuid, entry.uuid)
      })
    },
  },
}
</script>
