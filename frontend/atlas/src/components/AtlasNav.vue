<template>
  <nav
    class="flex shrink-0 gap-1 overflow-x-auto border-b border-wntrs-border px-6 py-4 [scrollbar-width:none] lg:w-64 lg:flex-col lg:border-r lg:border-b-0 lg:pr-4"
  >
    <RouterLink
      v-for="tab in tabs"
      :key="tab.section"
      :to="tab.to"
      class="flex h-10 shrink-0 items-center gap-3 rounded-box px-3 text-sm"
      :class="
        $route.meta.section === tab.section
          ? 'bg-base-200 text-base-content'
          : 'text-wntrs-muted hover:bg-base-200 hover:text-base-content'
      "
    >
      <AppIcon :name="tab.icon" />
      {{ tab.label }}
    </RouterLink>
  </nav>
</template>

<script>
import { RouterLink } from 'vue-router'
import AppIcon from '@core/components/common/AppIcon.vue'

export default {
  name: 'AtlasNav',
  components: { AppIcon, RouterLink },
  data() {
    return {
      tabs: [
        { section: 'institutions', label: 'Institutionen', to: '/', icon: 'building' },
        {
          section: 'documentations',
          label: 'Dokumentationen',
          to: '/documentations',
          icon: 'poll-h',
        },
        {
          section: 'learning-sets',
          label: 'Lernsets',
          to: '/learning-sets',
          icon: 'cards-blank',
        },
      ],
    }
  },
}
</script>
