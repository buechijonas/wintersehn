<template>
  <div class="flex flex-col gap-3 text-sm">
    <div class="flex flex-col gap-0.5">
      <p class="font-medium">Mozilla Observatory: Note {{ report.grade }}</p>
      <p class="text-xs text-wntrs-muted">
        {{ report.score }} Punkte · ab 85 grünes Schild, unter 45 rotes Zeichen
      </p>
    </div>
    <div v-for="group in groups" :key="group.label" class="flex flex-col gap-1.5">
      <p class="text-xs font-medium text-wntrs-muted">{{ group.label }}</p>
      <ul class="flex flex-col gap-1.5">
        <li v-for="test in group.tests" :key="test.name" class="flex items-center gap-2">
          <AppIcon :name="group.icon" :class="group.class" />
          <span>{{ testLabels[test.name] ?? test.name }}</span>
        </li>
      </ul>
    </div>
    <a
      :href="report.url"
      target="_blank"
      rel="noopener noreferrer"
      class="link link-hover text-xs text-wntrs-muted"
    >
      Vollständiger Bericht bei Mozilla
    </a>
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import { testLabels } from '@/data/ratings.js'

export default {
  name: 'RatingReport',
  components: { AppIcon },
  props: {
    report: { type: Object, required: true },
  },
  data() {
    return {
      testLabels,
    }
  },
  computed: {
    groups() {
      const groups = [
        {
          label: 'Vorhanden',
          icon: 'shield-check',
          class: 'text-wntrs-secure',
          tests: this.report.tests.filter(({ passed }) => passed),
        },
        {
          label: 'Fehlt',
          icon: 'octagon-xmark',
          class: 'text-error',
          tests: this.report.tests.filter(({ passed }) => !passed),
        },
      ]
      return groups.filter(({ tests }) => tests.length)
    },
  },
}
</script>
