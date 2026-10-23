<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div
    class="flex flex-col pb-8 sm:px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1"
  >
    <div class="mx-auto w-full max-w-150 sm:pt-4">
      <div v-if="!shares && !error" class="flex flex-col gap-3">
        <div v-for="n in 3" :key="n" class="flex items-center gap-3 p-4">
          <div class="skeleton size-6 lg:size-5 shrink-0"></div>
          <div class="skeleton h-4 w-40"></div>
        </div>
      </div>

      <BaseCard
        v-else-if="shares?.length"
        tag="ul"
        class="divide-y divide-wntrs-border max-sm:border-x-0 max-sm:border-t-0"
      >
        <li v-for="share in shares" :key="share.uuid">
          <RouterLink
            :to="{ name: 'shared-dossier', params: { share: share.uuid } }"
            class="flex items-center gap-3 p-4 text-sm hover:bg-base-200"
          >
            <AppIcon name="folder" class="size-6! lg:size-5!" />
            <span v-if="share.title" class="font-bold truncate">{{ share.title }}</span>
            <CipherText v-else :length="10" class="font-bold" />
          </RouterLink>
        </li>
      </BaseCard>

      <BaseCard v-else-if="shares" class="p-6 max-sm:border-x-0 max-sm:border-t-0">
        <p class="text-wntrs-muted">Noch nichts mit dir geteilt.</p>
      </BaseCard>

      <p v-if="error" class="text-error text-sm mt-4 text-center">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import CipherText from '@core/components/common/CipherText.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import { useDossiersStore } from '@/stores/dossiers.js'

export default {
  name: 'SharedListView',
  components: { RouterLink, AppIcon, BaseBreadcrumbs, BaseCard, CipherText },
  mixins: [asyncActionMixin],
  data() {
    return {
      breadcrumbs: [{ label: 'Mit mir geteilt', to: '/shared' }],
      shares: null,
    }
  },
  mounted() {
    return this.runAction(async () => {
      this.shares = await useDossiersStore().fetchSharedWithMe()
    })
  },
}
</script>
