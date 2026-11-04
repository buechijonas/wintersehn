<template>
  <BaseBreadcrumbs :items="breadcrumbs">
    <template v-if="event" #actions>
      <EditButton :to="{ name: 'event-edit', params: $route.params }" />
    </template>
  </BaseBreadcrumbs>
  <div
    class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1"
  >
    <div class="mx-auto w-full max-w-150 pt-4">
      <div v-if="!event && !error" class="flex flex-col gap-4">
        <div class="skeleton h-12 w-full"></div>
        <div class="skeleton h-96 w-full"></div>
      </div>

      <BaseCard v-else-if="event" class="p-6">
        <span class="block font-mono italic text-xs text-wntrs-muted">
          {{ formatDate(event.date) }}
        </span>
        <h2 class="text-xl font-bold mt-1 break-words">{{ event.title }}</h2>
        <div class="flex flex-wrap items-center gap-1.5 mt-3">
          <span class="text-xs text-wntrs-muted">Beteiligt:</span>
          <RouterLink
            v-for="dossier in event.dossiers"
            :key="dossier.uuid"
            :to="{ name: 'dossier', params: { uuid: dossier.uuid } }"
            class="badge badge-sm hover:badge-primary"
            :class="dossier.uuid === uuid ? 'badge-primary' : 'badge-soft'"
          >
            {{ dossier.title }}
          </RouterLink>
          <BaseButton
            variant="ghost"
            shape="square"
            size="xs"
            title="Beteiligte Akten bearbeiten"
            :disabled="saving"
            @click="$refs.dossiersDialog.open(event.dossiers)"
          >
            <AppIcon name="pencil" alt="Beteiligte Akten bearbeiten" />
          </BaseButton>
        </div>
        <p v-if="event.text" class="mt-4 whitespace-pre-wrap break-words leading-relaxed">
          {{ event.text }}
        </p>
        <p v-else class="mt-4 text-sm text-wntrs-muted">Noch kein Text.</p>
      </BaseCard>

      <template v-if="event">
        <div class="flex items-center justify-between gap-4 my-4">
          <h3 class="text-xl font-light">Vertrauen</h3>
          <TrustPoints v-if="event.trust.entries.length" :points="event.trust.points" />
        </div>
        <BaseCard>
          <ul v-if="event.trust.entries.length" class="flex flex-col divide-y divide-wntrs-border">
            <TrustEntryRow
              v-for="entry in event.trust.entries"
              :key="entry.uuid"
              :uuid="uuid"
              :entry="entry"
              :show-event="false"
            />
          </ul>
          <p v-else class="px-6 py-4 text-sm text-wntrs-muted">
            Keine Vertrauenspunkte zu diesem Ereignis.
          </p>
        </BaseCard>
      </template>

      <EventLinksCard v-if="event" :uuid="uuid" :event="event" @update="event = $event" />

      <EventReferencesSection v-if="event" :uuid="uuid" :event="event.uuid" />

      <p v-if="error" class="text-error text-sm mt-4 text-center">{{ error }}</p>
    </div>
  </div>

  <EventDossiersDialog ref="dossiersDialog" @confirm="saveDossiers" />
</template>

<script>
import { RouterLink } from 'vue-router'
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import EditButton from '@core/components/common/EditButton.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import EventDossiersDialog from '@/components/EventDossiersDialog.vue'
import EventLinksCard from '@/components/EventLinksCard.vue'
import EventReferencesSection from '@/components/EventReferencesSection.vue'
import TrustEntryRow from '@/components/TrustEntryRow.vue'
import TrustPoints from '@/components/TrustPoints.vue'
import eventMixin from '@/mixins/eventMixin.js'
import { formatDate } from '@/data/dossierFields.js'

export default {
  name: 'EventView',
  components: {
    RouterLink,
    AppIcon,
    BaseBreadcrumbs,
    BaseButton,
    BaseCard,
    EditButton,
    EventDossiersDialog,
    EventLinksCard,
    EventReferencesSection,
    TrustEntryRow,
    TrustPoints,
  },
  mixins: [asyncActionMixin, eventMixin],
  computed: {
    breadcrumbs() {
      return [...this.baseBreadcrumbs, { label: this.event?.title ?? '…' }]
    },
  },
  methods: {
    formatDate,
    saveDossiers(dossiers) {
      return this.runAction(async () => {
        const event = await this.dossiersStore.updateEvent(this.uuid, this.event.uuid, {
          dossiers,
        })
        if (dossiers.includes(this.uuid)) {
          this.event = event
          return
        }
        this.$router.replace({
          name: 'event',
          params: { uuid: dossiers[0], event: event.uuid },
        })
      })
    },
  },
}
</script>
