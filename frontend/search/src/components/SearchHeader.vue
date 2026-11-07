<template>
  <TitleHeader
    title="Suche"
    home-icon="search"
    hide-title
    :switches="appSwitches"
    :reverse="handedness === 'left'"
  />
</template>

<script>
import TitleHeader from '@core/components/layout/TitleHeader.vue'
import { appSwitchTargets } from '@core/lib/appSwitch.js'
import { useAuthStore } from '@core/stores/auth.js'
import { handedness } from '@/lib/handedness.js'

export default {
  name: 'SearchHeader',
  components: { TitleHeader },
  inject: ['app'],
  computed: {
    appSwitches() {
      return appSwitchTargets(this.app, useAuthStore().user)
    },
    handedness() {
      return handedness.value
    },
  },
}
</script>
