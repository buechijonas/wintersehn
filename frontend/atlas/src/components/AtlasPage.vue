<template>
  <div class="flex flex-1 flex-col gap-6 px-6 pt-4 pb-16">
    <div v-if="breadcrumbs.length" class="flex min-h-8 items-center justify-between gap-4">
      <nav class="breadcrumbs py-0 text-sm text-wntrs-muted">
        <ul>
          <li v-for="item in breadcrumbs" :key="item.label">
            <RouterLink v-if="item.to" :to="item.to">{{ item.label }}</RouterLink>
            <span v-else>{{ item.label }}</span>
          </li>
        </ul>
      </nav>
      <div v-if="$slots.actions" class="flex shrink-0 items-center gap-2">
        <slot name="actions" />
      </div>
    </div>
    <p v-if="error" class="text-sm text-error">{{ error }}</p>
    <div v-if="loading" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="n in 3" :key="n" class="skeleton h-24"></div>
    </div>
    <slot v-else />
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'

export default {
  name: 'AtlasPage',
  components: { RouterLink },
  props: {
    breadcrumbs: { type: Array, default: () => [] },
    loading: { type: Boolean, default: false },
    error: { type: String, default: '' },
  },
}
</script>
