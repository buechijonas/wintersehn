<template>
  <div class="mb-10">
    <h3 class="text-xl my-4">Stil</h3>
    <BaseCard
      class="p-6 flex flex-col items-center text-center gap-4 sm:flex-row sm:items-center sm:text-left sm:justify-between"
    >
      <p class="text-wntrs-muted min-w-0">
        Netflix ist immer dunkel, unabhängig von Hell und Dunkel.
      </p>
      <div class="flex shrink-0 flex-wrap justify-center gap-2">
        <BaseButton
          v-for="option in options"
          :key="option.value"
          type="button"
          size="sm"
          :variant="style === option.value ? 'primary' : 'neutral'"
          @click="style = option.value"
        >
          <AppIcon :name="option.icon" />
          {{ option.label }}
        </BaseButton>
      </div>
    </BaseCard>
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import { lumonStyle } from '@/lib/style.js'

export default {
  name: 'StyleSettings',
  components: { AppIcon, BaseButton, BaseCard },
  data() {
    return {
      options: [
        { value: 'standard', icon: 'apps', label: 'Standard' },
        { value: 'netflix', icon: 'film', label: 'Netflix' },
      ],
    }
  },
  computed: {
    style: {
      get() {
        return lumonStyle.value
      },
      set(value) {
        lumonStyle.value = value
      },
    },
  },
}
</script>
