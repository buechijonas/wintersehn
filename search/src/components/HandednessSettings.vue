<template>
  <div class="mb-10">
    <h3 class="text-xl my-4">Bedienung</h3>
    <BaseCard
      class="p-6 flex flex-col items-center text-center gap-4 sm:flex-row sm:items-center sm:text-left sm:justify-between"
    >
      <p class="text-wntrs-muted min-w-0">Menü auf der Seite deiner Hand.</p>
      <OptionButtons v-model="handedness" :options="options" :labels="labels" />
    </BaseCard>
  </div>
</template>

<script>
import BaseCard from '@core/components/common/BaseCard.vue'
import OptionButtons from '@/components/OptionButtons.vue'
import { handedness } from '@/lib/handedness.js'

export default {
  name: 'HandednessSettings',
  components: { BaseCard, OptionButtons },
  data() {
    return {
      options: ['right', 'left'],
      labels: { right: 'Rechtshänder', left: 'Linkshänder' },
    }
  },
  computed: {
    handedness: {
      get() {
        return handedness.value
      },
      set(value) {
        handedness.value = value
      },
    },
  },
}
</script>
