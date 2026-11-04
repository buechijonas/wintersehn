<template>
  <BaseCard class="border-t-0">
    <div class="flex justify-end px-6 pt-4">
      <EditToggle v-model="editing" />
    </div>

    <form
      v-if="editing"
      class="flex gap-2 px-6 pt-4 pb-4 border-b border-wntrs-border"
      @submit.prevent="add"
    >
      <select v-model="draft.kind" aria-label="Sucht" class="select flex-1 min-w-0" required>
        <option value="" disabled>Sucht wählen</option>
        <optgroup v-for="group in available" :key="group.label" :label="group.label">
          <option v-for="kind in group.kinds" :key="kind.value" :value="kind.value">
            {{ kind.label }}
          </option>
        </optgroup>
      </select>
      <select v-model="draft.frequency" aria-label="Konsum" class="select w-36">
        <option v-for="frequency in frequencies" :key="frequency.value" :value="frequency.value">
          {{ frequency.label }}
        </option>
      </select>
      <BaseButton type="submit" shape="square" title="Hinzufügen" :disabled="saving">
        <AppIcon name="plus" alt="Hinzufügen" />
      </BaseButton>
    </form>

    <div v-if="!addictions && !error" class="flex items-center justify-between px-6 py-4">
      <div class="skeleton h-4 w-32"></div>
      <div class="skeleton h-4 w-20"></div>
    </div>

    <ul v-else-if="addictions?.length" class="flex flex-col divide-y divide-wntrs-border">
      <li
        v-for="addiction in addictions"
        :key="addiction.kind"
        class="flex items-center justify-between gap-4 px-6 py-4 text-sm"
      >
        <span class="font-bold truncate">{{ addictionLabels[addiction.kind] }}</span>
        <div v-if="editing" class="flex items-center gap-2">
          <select
            :value="addiction.frequency"
            :aria-label="`Konsum von ${addictionLabels[addiction.kind]}`"
            class="select select-sm w-36"
            :disabled="saving"
            @change="setFrequency(addiction, $event.target.value)"
          >
            <option
              v-for="frequency in frequencies"
              :key="frequency.value"
              :value="frequency.value"
            >
              {{ frequency.label }}
            </option>
          </select>
          <BaseButton
            variant="neutral"
            shape="square"
            size="sm"
            title="Entfernen"
            :disabled="saving"
            @click="remove(addiction)"
          >
            <AppIcon name="trash" alt="Entfernen" />
          </BaseButton>
        </div>
        <span v-else class="shrink-0 text-wntrs-muted">
          {{ frequencyLabels[addiction.frequency] }}
        </span>
      </li>
    </ul>

    <p v-else-if="addictions" class="px-6 py-4 text-sm text-wntrs-muted">Keine Süchte erfasst.</p>

    <p v-if="error" class="text-error text-sm px-6 py-4">{{ error }}</p>
  </BaseCard>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import EditToggle from '@/components/EditToggle.vue'
import {
  addictionGroups,
  addictionLabels,
  frequencies,
  frequencyLabels,
} from '@/data/addictions.js'
import { useDossiersStore } from '@/stores/dossiers.js'

const EMPTY_DRAFT = { kind: '', frequency: 'daily' }

export default {
  name: 'DossierAddictionsTab',
  components: { AppIcon, BaseButton, BaseCard, EditToggle },
  mixins: [asyncActionMixin],
  props: {
    uuid: { type: String, required: true },
  },
  data() {
    return {
      addictionLabels,
      frequencies,
      frequencyLabels,
      addictions: null,
      editing: false,
      draft: { ...EMPTY_DRAFT },
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
    available() {
      const taken = new Set((this.addictions ?? []).map((addiction) => addiction.kind))
      return addictionGroups
        .map((group) => ({ ...group, kinds: group.kinds.filter((kind) => !taken.has(kind.value)) }))
        .filter((group) => group.kinds.length)
    },
  },
  watch: {
    editing() {
      this.draft = { ...EMPTY_DRAFT }
    },
    uuid: {
      immediate: true,
      handler() {
        this.addictions = null
        this.editing = false
        return this.runAction(async () => {
          this.addictions = await this.dossiersStore.fetchAddictions(this.uuid)
        })
      },
    },
  },
  methods: {
    add() {
      return this.runAction(async () => {
        const addiction = await this.dossiersStore.addAddiction(this.uuid, this.draft)
        this.addictions = [...this.addictions, addiction]
        this.draft = { ...EMPTY_DRAFT }
      })
    },
    setFrequency(addiction, frequency) {
      return this.runAction(async () => {
        Object.assign(
          addiction,
          await this.dossiersStore.updateAddiction(this.uuid, addiction.kind, frequency),
        )
      })
    },
    remove(addiction) {
      return this.runAction(async () => {
        await this.dossiersStore.removeAddiction(this.uuid, addiction.kind)
        this.addictions = this.addictions.filter((a) => a !== addiction)
      })
    },
  },
}
</script>
