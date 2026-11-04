<template>
  <div class="group dropdown" :class="alignClasses[align]" @keydown.esc="closeMenu">
    <div
      tabindex="0"
      role="button"
      class="flex cursor-pointer items-center gap-1.5 rounded-full bg-wntrs-secure/15 py-1 pr-3 pl-2 text-xs font-medium text-base-content"
    >
      <AppIcon name="shield-check" class="text-wntrs-secure" />
      Sichere Suche
    </div>
    <div
      tabindex="0"
      class="dropdown-content invisible group-focus-within:visible z-30 my-2 flex w-80 flex-col gap-3 rounded-box border border-wntrs-border bg-base-100 p-4 text-sm"
    >
      <ul class="flex flex-col gap-2">
        <li class="flex items-start gap-2">
          <AppIcon name="shield-check" class="mt-0.5 text-wntrs-secure" />
          <span>{{ networkLine }}</span>
        </li>
        <li v-for="protection in protections" :key="protection" class="flex items-start gap-2">
          <AppIcon name="shield-check" class="mt-0.5 text-wntrs-secure" />
          <span>{{ protection }}</span>
        </li>
      </ul>
      <RouterLink
        :to="{ name: 'settings', query: { tab: 'privacy' } }"
        class="link link-hover text-xs text-wntrs-muted"
      >
        Mehr unter Einstellungen → Datenschutz
      </RouterLink>
    </div>
  </div>
</template>

<script>
import { closeMenu } from '@/lib/menu.js'
import { RouterLink } from 'vue-router'
import AppIcon from '@core/components/common/AppIcon.vue'
import { networkLabels, protections } from '@/data/settings.js'
import { useSearchStore } from '@/stores/search.js'

export default {
  name: 'SecureBadge',
  components: { RouterLink, AppIcon },
  props: {
    align: { type: String, default: 'end' },
  },
  data() {
    return {
      protections,
      alignClasses: { end: 'dropdown-end', top: 'dropdown-top dropdown-center' },
    }
  },
  computed: {
    networkLine() {
      const network = useSearchStore().activeNetwork()
      if (network === 'direct') return 'Anfragen gehen direkt vom Server, nie von deinem Gerät.'
      if (network === 'tor' && !import.meta.env.PROD) {
        return 'Tor ist in dieser Entwicklungsumgebung nicht aktiv.'
      }
      return `Anfragen laufen über ${networkLabels[network]}.`
    },
  },
  methods: {
    closeMenu,
  },
}
</script>
