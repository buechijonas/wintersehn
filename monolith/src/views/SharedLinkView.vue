<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div
    class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1"
  >
    <div class="mx-auto w-full max-w-150 pt-4">
      <SharedDocument v-if="document" :document="document" />

      <BaseCard v-else-if="passwordRequired" class="p-6">
        <form class="flex flex-col gap-3" @submit.prevent="open(password)">
          <label for="share-password" class="text-sm font-bold">
            Diese Akte ist passwortgeschützt.
          </label>
          <div class="flex gap-2">
            <input
              id="share-password"
              v-model="password"
              type="password"
              autocomplete="off"
              class="input flex-1 min-w-0"
              required
            />
            <BaseButton type="submit" variant="primary" :disabled="saving">Öffnen</BaseButton>
          </div>
          <p v-if="attempted" class="text-error text-sm">Falsches Passwort.</p>
        </form>
      </BaseCard>

      <div v-else-if="!error" class="flex flex-col gap-4">
        <div class="skeleton h-12 w-full"></div>
        <div class="skeleton h-64 w-full"></div>
      </div>

      <p v-if="error" class="text-error text-sm mt-4 text-center">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import SharedDocument from '@/components/SharedDocument.vue'
import { activeTab, sharedBreadcrumbs } from '@/data/sharing.js'
import { useDossiersStore } from '@/stores/dossiers.js'

export default {
  name: 'SharedLinkView',
  components: { BaseBreadcrumbs, BaseButton, BaseCard, SharedDocument },
  mixins: [asyncActionMixin],
  data() {
    return {
      document: null,
      passwordRequired: false,
      attempted: false,
      password: '',
    }
  },
  computed: {
    breadcrumbs() {
      if (!this.document) return [{ cipher: true }]
      return sharedBreadcrumbs(this.document, activeTab(this.$route))
    },
  },
  mounted() {
    return this.open()
  },
  methods: {
    open(password) {
      return this.runAction(async () => {
        const result = await useDossiersStore().openSharedLink(this.$route.params.token, password)
        this.attempted = password !== undefined && result.passwordRequired
        this.passwordRequired = Boolean(result.passwordRequired)
        this.document = result.document ?? null
      })
    },
  },
}
</script>
