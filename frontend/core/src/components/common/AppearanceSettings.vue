<template>
  <div class="mb-10">
    <h3 class="text-xl my-4">Darstellung</h3>
    <BaseCard
      class="p-6 flex flex-col items-center text-center gap-4"
      :class="{ 'sm:flex-row sm:items-center sm:text-left sm:justify-between': !dyslexiaFont }"
    >
      <p class="text-wntrs-muted min-w-0">Erscheinungsbild der Oberfläche.</p>
      <div class="flex flex-wrap justify-center gap-2">
        <BaseButton
          v-for="option in themeOptions"
          :key="option.value"
          type="button"
          size="sm"
          :variant="themeMode === option.value ? 'primary' : 'neutral'"
          @click="themeMode = option.value"
        >
          <AppIcon :name="option.icon" />
          {{ option.label }}
        </BaseButton>
      </div>
    </BaseCard>
  </div>

  <div class="mb-10">
    <h3 class="text-xl my-4">Barrierefreiheit</h3>
    <BaseCard class="p-6 flex flex-col items-center text-center gap-4 mb-4 sm:flex-row sm:items-center sm:text-left sm:justify-between">
      <p class="text-wntrs-muted min-w-0">Legasthenie</p>
      <div class="flex flex-wrap justify-center gap-2">
        <BaseButton
          v-for="option in dyslexiaOptions"
          :key="option.value"
          type="button"
          size="sm"
          :variant="dyslexiaFont === option.value ? 'primary' : 'neutral'"
          @click="dyslexiaFont = option.value"
        >
          {{ option.label }}
        </BaseButton>
      </div>
    </BaseCard>
    <BaseCard class="p-6 flex flex-col items-center text-center gap-4 sm:flex-row sm:items-center sm:text-left sm:justify-between">
      <p class="text-wntrs-muted min-w-0">Kontrastmodus</p>
      <div class="flex flex-wrap justify-center gap-2">
        <BaseButton
          v-for="option in contrastOptions"
          :key="option.value"
          type="button"
          size="sm"
          :variant="contrastMode === option.value ? 'primary' : 'neutral'"
          @click="contrastMode = option.value"
        >
          {{ option.label }}
        </BaseButton>
      </div>
    </BaseCard>
  </div>
</template>

<script>
import BaseCard from '@core/components/common/BaseCard.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import AppIcon from '@core/components/common/AppIcon.vue'
import { themeMode } from '@core/lib/theme.js'
import { dyslexiaFont } from '@core/lib/dyslexia.js'
import { contrastMode } from '@core/lib/contrast.js'

export default {
  name: 'AppearanceSettings',
  components: { BaseCard, BaseButton, AppIcon },
  data() {
    return {
      themeOptions: [
        { value: 'auto', icon: 'laptop', label: 'Auto' },
        { value: 'light', icon: 'brightness', label: 'Hell' },
        { value: 'dark', icon: 'moon-stars', label: 'Dunkel' },
      ],
      dyslexiaOptions: [
        { value: true, label: 'An' },
        { value: false, label: 'Aus' },
      ],
      contrastOptions: [
        { value: true, label: 'An' },
        { value: false, label: 'Aus' },
      ],
    }
  },
  computed: {
    themeMode: {
      get() {
        return themeMode.value
      },
      set(value) {
        themeMode.value = value
      },
    },
    dyslexiaFont: {
      get() {
        return dyslexiaFont.value
      },
      set(value) {
        dyslexiaFont.value = value
      },
    },
    contrastMode: {
      get() {
        return contrastMode.value
      },
      set(value) {
        contrastMode.value = value
      },
    },
  },
}
</script>
