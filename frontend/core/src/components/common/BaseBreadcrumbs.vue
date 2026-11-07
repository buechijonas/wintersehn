<template>
  <div
    v-if="!app.hideBreadcrumbs"
    class="flex items-center justify-between gap-4"
    :class="
      app.layout === 'sidebar'
        ? 'min-h-12 px-6 pt-4'
        : 'app-header sticky top-0 z-10 border-b border-wntrs-border bg-base-200 py-2 px-6'
    "
  >
    <div class="breadcrumbs text-sm">
      <ul>
        <li class="text-wntrs-muted" v-for="(item, index) in items" :key="index">
          <component :is="item.to ? 'RouterLink' : 'span'" v-bind="item.to ? { to: item.to } : {}">
            <CipherText v-if="item.cipher" :length="10" />
            <template v-else>{{ item.label }}</template>
          </component>
        </li>
      </ul>
    </div>
    <div v-if="$slots.actions" class="-my-1.5">
      <slot name="actions" />
    </div>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'
import CipherText from '@core/components/common/CipherText.vue'

export default {
  name: 'BaseBreadcrumbs',
  components: { RouterLink, CipherText },
  inject: ['app'],
  props: {
    items: {
      type: Array,
      required: true,
    },
  },
}
</script>
