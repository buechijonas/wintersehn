<template>
  <BaseCard class="p-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
    <p class="text-sm text-wntrs-muted min-w-0">
      Diese Suche ist kostenlos, werbefrei und speichert nichts über dich. Wenn sie dir nützt, hilft
      eine Spende, den Server und das Tor-Netzwerk dahinter am Laufen zu halten.
    </p>
    <BaseButton
      variant="primary"
      class="shrink-0"
      :href="donateUrl"
      target="_blank"
      rel="noopener noreferrer"
    >
      <AppIcon name="hands-heart" />
      Spenden
    </BaseButton>
  </BaseCard>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import { donateUrl } from '@/data/settings.js'

export default {
  name: 'DonateSettings',
  components: { AppIcon, BaseButton, BaseCard },
  data() {
    return {
      donateUrl,
    }
  },
}
</script>
