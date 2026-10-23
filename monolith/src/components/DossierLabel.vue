<template>
  <div class="flex items-center gap-3 min-w-0 flex-1 text-sm">
    <AppIcon name="folder" class="size-6! lg:size-5!" />
    <div class="flex flex-col min-w-0 flex-1">
      <span class="font-bold truncate">{{ dossier.title }}</span>
      <span class="text-xs text-primary truncate">{{ dossier.uuid }}</span>
    </div>
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'

export default {
  name: 'DossierLabel',
  components: { AppIcon },
  props: {
    dossier: { type: Object, required: true },
  },
}
</script>
