<template>
  <div
    ref="panel"
    class="flex flex-col"
    :class="{ 'fixed inset-0 z-50 bg-base-200 p-4': fullscreen }"
    @keydown.esc="closeFullscreen"
  >
    <BaseTabs :tabs="tabs" :active="active" />
    <BaseCard class="relative p-4 border-t-0" :class="{ 'flex-1 min-h-0': fullscreen }">
      <BaseButton
        variant="ghost"
        shape="square"
        size="sm"
        class="absolute top-2 right-2 z-10"
        :title="fullscreen ? 'Vollbild beenden' : 'Vollbild'"
        @click="fullscreen ? closeFullscreen() : openFullscreen()"
      >
        <AppIcon
          :name="fullscreen ? 'compress' : 'expand'"
          :alt="fullscreen ? 'Vollbild beenden' : 'Vollbild'"
        />
      </BaseButton>
      <CountryMap :countries="countries" :class="{ 'h-full': fullscreen }" />
    </BaseCard>
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import BaseTabs from '@core/components/common/BaseTabs.vue'
import CountryMap from '@/components/common/CountryMap.vue'

export default {
  name: 'CountryMapPanel',
  components: { AppIcon, BaseButton, BaseCard, BaseTabs, CountryMap },
  props: {
    tabs: { type: Array, required: true },
    active: { type: String, required: true },
    countries: { type: Array, required: true },
  },
  data() {
    return { fullscreen: false }
  },
  mounted() {
    document.addEventListener('fullscreenchange', this.syncFullscreen)
  },
  beforeUnmount() {
    document.removeEventListener('fullscreenchange', this.syncFullscreen)
  },
  methods: {
    async openFullscreen() {
      this.fullscreen = true
      await this.$refs.panel.requestFullscreen?.().catch(() => {})
    },
    closeFullscreen() {
      this.fullscreen = false
      if (document.fullscreenElement) document.exitFullscreen()
    },
    syncFullscreen() {
      this.fullscreen = document.fullscreenElement === this.$refs.panel
    },
  },
}
</script>
