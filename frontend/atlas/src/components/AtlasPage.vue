<template>
  <BaseBreadcrumbs v-if="breadcrumbs.length" :items="breadcrumbs">
    <template v-if="$slots.actions" #actions>
      <div class="flex items-center gap-2">
        <slot name="actions" />
      </div>
    </template>
  </BaseBreadcrumbs>
  <div class="flex flex-1 flex-col gap-6 px-6 pt-4 pb-16">
    <p v-if="error" class="text-sm text-error">{{ error }}</p>
    <div v-if="loading" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="n in 3" :key="n" class="skeleton h-24"></div>
    </div>
    <slot v-else />
  </div>
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'

export default {
  name: 'AtlasPage',
  components: { BaseBreadcrumbs },
  props: {
    breadcrumbs: { type: Array, default: () => [] },
    loading: { type: Boolean, default: false },
    error: { type: String, default: '' },
  },
}
</script>
