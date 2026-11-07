<template>
  <BaseCard
    tag="RouterLink"
    :to="to"
    class="flex h-full items-start gap-4 rounded-box p-4 transition-colors hover:bg-base-200"
  >
    <AppIcon :name="icon" class="mt-0.5 size-6! shrink-0 text-primary" />
    <span class="flex min-w-0 flex-col gap-0.5">
      <span class="text-wntrs-title">{{ title }}</span>
      <span v-if="meta" class="text-sm text-wntrs-muted">{{ meta }}</span>
    </span>
    <span v-if="$slots.aside" class="ml-auto self-center">
      <slot name="aside" />
    </span>
  </BaseCard>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseCard from '@core/components/common/BaseCard.vue'

export default {
  name: 'ItemCard',
  components: { AppIcon, BaseCard },
  props: {
    title: { type: String, required: true },
    to: { type: [String, Object], required: true },
    icon: { type: String, default: 'folder' },
    meta: { type: String, default: '' },
  },
}
</script>
