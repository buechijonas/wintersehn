<template>
  <div class="mx-auto flex w-full max-w-240 flex-1 flex-col gap-10 px-6 pt-10 pb-16">
    <section class="flex flex-col gap-3">
      <p class="text-sm font-medium text-primary">Portfolio</p>
      <h1 class="font-display text-5xl font-bold tracking-tighter text-wntrs-title">
        {{ app.displayName(authStore.user) }}
      </h1>
      <p class="max-w-150 text-lg text-wntrs-slate">{{ intro }}</p>
    </section>

    <p v-if="error" class="text-sm text-error">{{ error }}</p>

    <div v-else-if="!dashboard" class="grid gap-4 lg:grid-cols-2">
      <div v-for="n in 4" :key="n" class="skeleton h-40"></div>
    </div>

    <template v-else>
      <section class="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <BaseCard v-for="stat in dashboard.stats" :key="stat.label" class="flex flex-col gap-1 p-4">
          <span class="font-display text-3xl font-bold text-wntrs-title">
            {{ stat.value ?? '–' }}{{ stat.value === null ? '' : stat.unit }}
          </span>
          <span class="text-sm text-wntrs-muted">{{ stat.label }}</span>
        </BaseCard>
      </section>

      <div class="grid gap-4 lg:grid-cols-2">
        <section v-if="dashboard.now.length" class="flex flex-col gap-2">
          <SectionTitle title="Jetzt" />
          <BaseCard tag="ul" class="flex flex-1 flex-col divide-y divide-wntrs-border">
            <li v-for="entry in dashboard.now" :key="entry.label" class="flex flex-col gap-0.5 p-4">
              <span class="text-xs text-wntrs-muted">{{ entry.label }}</span>
              <span>{{ entry.value }}</span>
            </li>
          </BaseCard>
        </section>

        <section v-if="dashboard.alternative" class="flex flex-col gap-2">
          <SectionTitle title="Alternative" to="/apps" />
          <RecommendationCard :item="dashboard.alternative" class="flex-1" />
        </section>

        <section v-if="dashboard.medium" class="flex flex-col gap-2">
          <SectionTitle title="Medium" to="/news" />
          <RecommendationCard :item="dashboard.medium" class="flex-1" />
        </section>

        <section v-if="dashboard.retrospect" class="flex flex-col gap-2">
          <SectionTitle title="Rückblick" to="/cv" />
          <BaseCard class="flex flex-1 flex-col gap-1 p-4">
            <span class="text-xs text-wntrs-muted">
              {{ retrospectLabel }} · {{ dashboard.retrospect.year }} ·
              {{ dashboard.retrospect.section }}
            </span>
            <span class="font-medium">{{ dashboard.retrospect.title }}</span>
            <span class="text-sm text-wntrs-muted">{{ dashboard.retrospect.description }}</span>
          </BaseCard>
        </section>
      </div>
    </template>
  </div>
</template>

<script>
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import { useAuthStore } from '@core/stores/auth.js'
import RecommendationCard from '@/components/common/RecommendationCard.vue'
import SectionTitle from '@/components/common/SectionTitle.vue'
import { useDashboardStore } from '@/stores/dashboard.js'

export default {
  name: 'HomeView',
  components: { BaseCard, RecommendationCard, SectionTitle },
  mixins: [asyncActionMixin],
  inject: ['app'],
  computed: {
    authStore() {
      return useAuthStore()
    },
    dashboard() {
      return useDashboardStore().dashboard
    },
    intro() {
      return this.authStore.user?.verified
        ? 'Persönliches Portfolio mit Lebenslauf, Projekten, Reisen und Medien.'
        : 'Artikel, Projekte und Kanäle an einem Ort.'
    },
    retrospectLabel() {
      const years = this.dashboard.retrospect.years_ago
      return years === 1 ? 'Vor einem Jahr' : `Vor ${years} Jahren`
    },
  },
  mounted() {
    this.runAction(() => useDashboardStore().fetchDashboard())
  },
}
</script>
