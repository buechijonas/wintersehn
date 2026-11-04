<template>
  <BaseCard class="border-t-0">
    <div class="flex justify-end gap-2 px-6 pt-4">
      <BaseButton
        variant="neutral"
        shape="square"
        size="sm"
        :title="showNetwork ? 'Liste' : 'Netzwerk'"
        @click="showNetwork = !showNetwork"
      >
        <AppIcon
          :name="showNetwork ? 'menu-burger' : 'network-analytic'"
          :alt="showNetwork ? 'Liste' : 'Netzwerk'"
        />
      </BaseButton>
      <EditToggle v-model="editing" />
    </div>

    <div v-if="showNetwork" class="h-96 mt-4 border-t border-wntrs-border">
      <NetworkGraph v-if="neighborhood" v-bind="neighborhood" :focus="uuid" controls />
      <div v-else-if="!error" class="skeleton size-full"></div>
    </div>

    <template v-else>
      <div v-if="editing" class="px-6 pt-4 pb-4 border-b border-wntrs-border">
        <input
          v-model.trim="query"
          type="search"
          placeholder="Personalakte suchen"
          aria-label="Personalakte suchen"
          class="input w-full"
        />
        <ul v-if="query" class="flex flex-col divide-y divide-wntrs-border mt-2">
          <li
            v-for="dossier in candidates"
            :key="dossier.uuid"
            class="flex items-center gap-3 py-3"
          >
            <DossierLabel :dossier="dossier" />
            <BaseButton size="sm" :disabled="saving" @click="add(dossier)">
              <AppIcon name="plus" />
              Hinzufügen
            </BaseButton>
          </li>
          <li v-if="!candidates.length" class="py-3 text-sm text-wntrs-muted">
            Keine Personalakten gefunden.
          </li>
        </ul>
      </div>

      <div v-if="!relationships && !error" class="flex items-center gap-3 px-6 py-4">
        <div class="skeleton size-6 lg:size-5 shrink-0"></div>
        <div class="skeleton h-4 w-40"></div>
      </div>

      <ul v-else-if="relationships?.length" class="flex flex-col divide-y divide-wntrs-border">
        <li
          v-for="relationship in relationships"
          :key="relationship.person.uuid"
          class="flex items-center"
        >
          <RouterLink
            :to="{ name: 'dossier', params: { uuid: relationship.person.uuid } }"
            class="flex flex-1 min-w-0 px-6 py-4 hover:bg-base-200"
          >
            <DossierLabel :dossier="relationship.person" />
            <span v-if="!editing" class="shrink-0 self-center pl-3 text-sm text-wntrs-muted">
              {{ statusLabel(relationship.status) }}
            </span>
          </RouterLink>
          <div v-if="editing" class="flex items-center gap-2 pr-6">
            <select
              :value="relationship.status"
              :aria-label="`Status von ${relationship.person.title}`"
              class="select select-sm w-32"
              :disabled="saving"
              @change="setStatus(relationship, $event.target.value)"
            >
              <option value="">Status</option>
              <option v-if="relationship.status === 'child'" value="child" disabled>Kind</option>
              <option v-for="status in statuses" :key="status.value" :value="status.value">
                {{ status.label }}
              </option>
            </select>
            <BaseButton
              variant="neutral"
              shape="square"
              size="sm"
              title="Beziehung entfernen"
              :disabled="saving"
              @click="remove(relationship)"
            >
              <AppIcon name="link-slash-alt" alt="Beziehung entfernen" />
            </BaseButton>
          </div>
        </li>
      </ul>

      <p v-else-if="relationships" class="px-6 py-4 text-sm text-wntrs-muted">
        Noch keine Beziehungen.
      </p>
    </template>

    <p v-if="error" class="text-error text-sm px-6 py-4">{{ error }}</p>
  </BaseCard>
</template>

<script>
import { RouterLink } from 'vue-router'
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import DossierLabel from '@/components/DossierLabel.vue'
import EditToggle from '@/components/EditToggle.vue'
import NetworkGraph from '@/components/NetworkGraph.vue'
import { statusLabels, statuses } from '@/data/statuses.js'
import { useDossiersStore } from '@/stores/dossiers.js'

export default {
  name: 'DossierRelationshipsTab',
  components: { RouterLink, DossierLabel, AppIcon, BaseButton, BaseCard, EditToggle, NetworkGraph },
  mixins: [asyncActionMixin],
  props: {
    uuid: { type: String, required: true },
  },
  data() {
    return {
      statuses,
      relationships: null,
      editing: false,
      showNetwork: true,
      network: null,
      query: '',
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
    candidates() {
      const taken = new Set([this.uuid, ...(this.relationships ?? []).map((r) => r.person.uuid)])
      const query = this.query.toLowerCase()
      return (this.dossiersStore.items ?? [])
        .filter((dossier) => !taken.has(dossier.uuid))
        .filter((dossier) => `${dossier.title} ${dossier.uuid}`.toLowerCase().includes(query))
        .slice(0, 10)
    },
    neighborhood() {
      if (!this.network) return null
      const relationships = this.network.relationships.filter((relationship) =>
        [relationship.dossier, relationship.person].includes(this.uuid),
      )
      const uuids = new Set([this.uuid, ...relationships.flatMap((r) => [r.dossier, r.person])])
      return {
        dossiers: this.network.dossiers.filter((dossier) => uuids.has(dossier.uuid)),
        relationships,
      }
    },
  },
  watch: {
    editing(editing) {
      this.query = ''
      this.showNetwork = !editing
    },
    showNetwork(show) {
      if (!show) return
      this.editing = false
      return this.loadNetwork()
    },
    uuid: {
      immediate: true,
      handler() {
        this.relationships = null
        this.editing = false
        this.query = ''
        if (this.showNetwork) this.loadNetwork()
        this.showNetwork = true
        return this.runAction(async () => {
          this.relationships = await this.dossiersStore.fetchRelationships(this.uuid)
        })
      },
    },
  },
  mounted() {
    return this.runAction(() => this.dossiersStore.fetchDossiers())
  },
  methods: {
    loadNetwork() {
      this.network = null
      return this.runAction(async () => {
        this.network = await this.dossiersStore.fetchNetwork()
      })
    },
    statusLabel(value) {
      return statusLabels[value] ?? ''
    },
    add(dossier) {
      return this.runAction(async () => {
        await this.dossiersStore.addRelationship(this.uuid, dossier.uuid)
        this.relationships = await this.dossiersStore.fetchRelationships(this.uuid)
        this.query = ''
      })
    },
    setStatus(relationship, status) {
      return this.runAction(async () => {
        Object.assign(
          relationship,
          await this.dossiersStore.updateRelationship(this.uuid, relationship.person.uuid, status),
        )
      })
    },
    remove(relationship) {
      return this.runAction(async () => {
        await this.dossiersStore.removeRelationship(this.uuid, relationship.person.uuid)
        this.relationships = this.relationships.filter((r) => r !== relationship)
      })
    },
  },
}
</script>
