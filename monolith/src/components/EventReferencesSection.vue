<template>
  <div class="flex items-center justify-between gap-4 my-4">
    <h3 class="text-xl font-light">Referenzen</h3>
    <BaseButton
      variant="neutral"
      shape="square"
      size="sm"
      title="Referenz hinzufügen"
      :disabled="saving"
      @click="$refs.dialog.open()"
    >
      <AppIcon name="plus" alt="Referenz hinzufügen" />
    </BaseButton>
  </div>

  <BaseCard>
    <div v-if="!references && !error" class="flex flex-col gap-3 px-6 py-4">
      <div v-for="n in 2" :key="n" class="skeleton h-10 w-full"></div>
    </div>

    <ul v-else-if="references?.length" class="flex flex-col divide-y divide-wntrs-border">
      <li v-for="reference in references" :key="reference.uuid">
        <RouterLink
          :to="{ name: 'event-reference', params: { uuid, event, reference: reference.uuid } }"
          class="flex items-center gap-4 px-6 py-3 hover:bg-base-200"
        >
          <img class="size-8 shrink-0" :src="referenceIcon(reference)" alt="" />
          <span class="flex flex-col min-w-0 flex-1">
            <span class="text-sm font-bold truncate">{{ reference.title }}</span>
            <span class="text-xs text-wntrs-muted truncate">
              {{ referenceSummary(reference) }}
            </span>
          </span>
        </RouterLink>
      </li>
    </ul>

    <p v-else-if="references" class="px-6 py-4 text-sm text-wntrs-muted">Noch keine Referenzen.</p>

    <p v-if="error" class="text-error text-sm px-6 py-4">{{ error }}</p>
  </BaseCard>

  <EventReferenceDialog ref="dialog" @confirm="create" />
</template>

<script>
import { RouterLink } from 'vue-router'
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import EventReferenceDialog from '@/components/EventReferenceDialog.vue'
import { referenceIcon, referenceSummary } from '@/data/eventReferences.js'
import { useDossiersStore } from '@/stores/dossiers.js'

export default {
  name: 'EventReferencesSection',
  components: { RouterLink, AppIcon, BaseButton, BaseCard, EventReferenceDialog },
  mixins: [asyncActionMixin],
  props: {
    uuid: { type: String, required: true },
    event: { type: String, required: true },
  },
  data() {
    return {
      references: null,
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
  },
  watch: {
    event: {
      immediate: true,
      handler() {
        this.references = null
        return this.runAction(async () => {
          this.references = await this.dossiersStore.fetchEventReferences(this.uuid, this.event)
        })
      },
    },
  },
  methods: {
    referenceIcon,
    referenceSummary,
    create(data) {
      return this.runAction(async () => {
        const reference = await this.dossiersStore.createEventReference(this.uuid, this.event, data)
        this.$router.push({
          name: 'event-reference',
          params: { uuid: this.uuid, event: this.event, reference: reference.uuid },
        })
      })
    },
  },
}
</script>
