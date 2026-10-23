<template>
  <BaseCard class="border-t-0">
    <div class="flex justify-end gap-2 px-6 pt-4">
      <BaseButton
        variant="neutral"
        shape="square"
        size="sm"
        :title="showCompass ? 'Liste' : '3D-Modell'"
        @click="showCompass = !showCompass"
      >
        <AppIcon
          :name="showCompass ? 'menu-burger' : 'compass-alt'"
          :alt="showCompass ? 'Liste' : '3D-Modell'"
        />
      </BaseButton>
      <EditToggle v-model="editing" />
    </div>

    <div v-if="!stances && !error" class="flex flex-col gap-3 px-6 py-4">
      <div v-for="n in 4" :key="n" class="skeleton h-12 w-full"></div>
    </div>

    <template v-else-if="stances">
      <SpectrumBar
        v-if="summary"
        class="px-6 py-4 border-b border-wntrs-border"
        :label="spectrum.label"
        :poles="spectrum.poles"
        :value="summary.spectrum"
      />

      <div v-if="showCompass" class="px-6 py-4">
        <template v-if="summary">
          <StanceCompass :compass="summary.compass" :axis-labels="compassAxes" />
          <SpectrumBar
            v-for="(axis, key) in compassAxes"
            :key="key"
            class="mt-4"
            :label="axis.label"
            :poles="axis.poles"
            :value="summary.compass[key]"
          />
        </template>
        <div v-else class="skeleton aspect-square w-full max-w-96 mx-auto"></div>
      </div>

      <template v-else>
        <section v-for="group in groups" :key="group.label">
          <h3 class="px-6 pt-4 text-xs font-bold uppercase tracking-wide text-wntrs-muted">
            {{ group.label }}
          </h3>
          <ul class="flex flex-col divide-y divide-wntrs-border">
            <StanceRow
              v-for="topic in group.topics"
              :key="topic"
              :topic="topics[topic]"
              :stance="stances[topic]"
              :editing="editing"
              :saving="saving"
              @save="save(topic, $event)"
            />
          </ul>
        </section>
      </template>
    </template>

    <p v-if="error" class="text-error text-sm px-6 py-4">{{ error }}</p>
  </BaseCard>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import EditToggle from '@/components/EditToggle.vue'
import SpectrumBar from '@/components/SpectrumBar.vue'
import StanceCompass from '@/components/StanceCompass.vue'
import StanceRow from '@/components/StanceRow.vue'
import { compassAxes, spectrum, topicGroups, topics } from '@/data/topics.js'
import { useDossiersStore } from '@/stores/dossiers.js'

export default {
  name: 'DossierStancesTab',
  components: { AppIcon, BaseButton, BaseCard, EditToggle, SpectrumBar, StanceCompass, StanceRow },
  mixins: [asyncActionMixin],
  props: {
    uuid: { type: String, required: true },
  },
  data() {
    return {
      compassAxes,
      spectrum,
      groups: topicGroups,
      topics,
      stances: null,
      summary: null,
      editing: false,
      showCompass: true,
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
  },
  watch: {
    editing(editing) {
      if (editing) this.showCompass = false
    },
    showCompass(show) {
      if (show) this.editing = false
    },
    uuid: {
      immediate: true,
      handler() {
        this.stances = null
        this.editing = false
        this.showCompass = true
        return this.runAction(async () => {
          const [stances] = await Promise.all([
            this.dossiersStore.fetchStances(this.uuid),
            this.loadSummary(),
          ])
          this.stances = Object.fromEntries(stances.map((stance) => [stance.topic, stance]))
        })
      },
    },
  },
  methods: {
    async loadSummary() {
      this.summary = await this.dossiersStore.fetchStanceSummary(this.uuid)
    },
    save(topic, tags) {
      return this.runAction(async () => {
        this.stances[topic] = await this.dossiersStore.saveStance(this.uuid, topic, { tags })
        await this.loadSummary()
      })
    },
  },
}
</script>
