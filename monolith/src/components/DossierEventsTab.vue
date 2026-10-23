<template>
  <BaseCard class="border-t-0">
    <div class="flex justify-end px-6 pt-4">
      <BaseButton
        variant="neutral"
        shape="square"
        size="sm"
        title="Ereignis hinzufügen"
        @click="$refs.dialog.open()"
      >
        <AppIcon name="plus" alt="Ereignis hinzufügen" />
      </BaseButton>
    </div>

    <div v-if="!events && !error" class="flex flex-col gap-3 px-6 py-4">
      <div v-for="n in 3" :key="n" class="skeleton h-16 w-full"></div>
    </div>

    <ol v-else-if="events?.length" class="px-6 pb-4">
      <li v-for="(event, index) in events" :key="event.uuid" class="flex gap-3">
        <div class="flex w-3 shrink-0 flex-col items-center">
          <span class="h-3.5 w-1" :class="index > 0 ? 'bg-base-300' : 'invisible'"></span>
          <span class="size-3 shrink-0 rounded-full bg-primary"></span>
          <span
            class="w-1 flex-1"
            :class="index < events.length - 1 ? 'bg-base-300' : 'invisible'"
          ></span>
        </div>
        <RouterLink
          :to="{ name: 'event', params: { uuid, event: event.uuid } }"
          class="flex-1 min-w-0 my-0.5 rounded-box px-3 py-2 hover:bg-base-200"
        >
          <span class="block font-mono italic text-xs text-wntrs-muted">
            {{ formatDate(event.date) }}
          </span>
          <span class="block font-bold text-sm break-words">{{ event.title }}</span>
          <EventLinks :event="event" class="mt-1.5" />
        </RouterLink>
      </li>
    </ol>

    <p v-else-if="events" class="px-6 py-4 text-sm text-wntrs-muted">Noch keine Ereignisse.</p>

    <p v-if="error" class="text-error text-sm px-6 py-4">{{ error }}</p>
  </BaseCard>

  <EventDialog ref="dialog" @confirm="create" />
</template>

<script>
import { RouterLink } from 'vue-router'
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import EventDialog from '@/components/EventDialog.vue'
import EventLinks from '@/components/EventLinks.vue'
import { formatDate } from '@/data/dossierFields.js'
import { useDossiersStore } from '@/stores/dossiers.js'

export default {
  name: 'DossierEventsTab',
  components: { RouterLink, AppIcon, BaseButton, BaseCard, EventDialog, EventLinks },
  mixins: [asyncActionMixin],
  props: {
    uuid: { type: String, required: true },
  },
  data() {
    return {
      events: null,
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
        this.events = null
        return this.load()
      },
    },
  },
  methods: {
    formatDate,
    load() {
      return this.runAction(async () => {
        this.events = await this.dossiersStore.fetchEvents(this.uuid)
      })
    },
    create(data) {
      return this.runAction(async () => {
        const event = await this.dossiersStore.createEvent(this.uuid, data)
        this.$router.push({
          name: 'event',
          params: { uuid: this.uuid, event: event.uuid },
        })
      })
    },
  },
}
</script>
