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
        <p v-if="event.text" class="mt-4 whitespace-pre-wrap break-words leading-relaxed">
          {{ event.text }}
        </p>
        <p v-else class="mt-4 text-sm text-wntrs-muted">Noch kein Text.</p>
      </BaseCard>

      <EventLinksCard v-if="event" :uuid="uuid" :event="event" @update="event = $event" />

      <p v-if="error" class="text-error text-sm mt-4 text-center">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import EditButton from '@core/components/common/EditButton.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import EventLinksCard from '@/components/EventLinksCard.vue'
import eventMixin from '@/mixins/eventMixin.js'
import { formatDate } from '@/data/dossierFields.js'

export default {
  name: 'EventView',
  components: { BaseBreadcrumbs, BaseCard, EditButton, EventLinksCard },
  mixins: [asyncActionMixin, eventMixin],
  computed: {
    breadcrumbs() {
      return [...this.baseBreadcrumbs, { label: this.event?.title ?? '…' }]
    },
  },
  methods: {
    formatDate,
  },
}
</script>
