<template>
  <BaseCard class="border-t-0">
    <form
      v-if="data?.recipients.length"
      class="flex gap-2 px-6 pt-4 pb-4 border-b border-wntrs-border"
      @submit.prevent="create({ recipient })"
    >
      <select v-model="recipient" aria-label="Empfänger" class="select flex-1 min-w-0" required>
        <option value="" disabled>Freigeben für …</option>
        <option v-for="dossier in data.recipients" :key="dossier.uuid" :value="dossier.uuid">
          {{ dossier.title }}
        </option>
      </select>
      <BaseButton type="submit" shape="square" title="Freigeben" :disabled="saving">
        <AppIcon name="plus" alt="Freigeben" />
      </BaseButton>
    </form>
    <p
      v-else-if="data"
      class="px-6 pt-4 pb-4 text-sm text-wntrs-muted border-b border-wntrs-border"
    >
      Keine weitere Akte mit govex-Verknüpfung verfügbar.
    </p>

    <form
      v-if="data"
      class="flex flex-wrap gap-2 px-6 pt-4 pb-4 border-b border-wntrs-border"
      @submit.prevent="create(link)"
    >
      <input
        v-model="link.name"
        aria-label="Name des Links"
        placeholder="Öffentlicher Link, z. B. «Für Mutter»"
        class="input flex-1 min-w-48"
        required
      />
      <input
        v-model="link.password"
        type="password"
        autocomplete="new-password"
        aria-label="Passwort (optional)"
        placeholder="Passwort (optional)"
        class="input flex-1 min-w-36"
      />
      <BaseButton type="submit" shape="square" title="Link erstellen" :disabled="saving">
        <AppIcon name="plus" alt="Link erstellen" />
      </BaseButton>
    </form>

    <div v-if="!data && !error" class="flex items-center gap-3 px-6 py-4">
      <div class="skeleton h-4 w-40"></div>
    </div>

    <ul v-else-if="data?.shares.length" class="flex flex-col divide-y divide-wntrs-border">
      <li v-for="share in data.shares" :key="share.uuid">
        <RouterLink
          :to="{ name: 'share-edit', params: { uuid, share: share.uuid } }"
          class="flex items-center justify-between gap-4 px-6 py-4 text-sm hover:bg-base-200"
        >
          <span class="flex items-center gap-2 min-w-0">
            <span class="font-bold truncate">{{ share.recipient?.title ?? share.name }}</span>
            <span v-if="!share.recipient" class="badge badge-sm badge-soft shrink-0">Link</span>
            <AppIcon
              v-if="share.has_password"
              name="lock"
              alt="Passwortgeschützt"
              class="size-3.5! shrink-0"
            />
          </span>
          <span class="shrink-0 font-mono italic text-xs text-wntrs-muted">
            {{ formatDate(share.created_at) }}
          </span>
        </RouterLink>
      </li>
    </ul>

    <p v-else-if="data" class="px-6 py-4 text-sm text-wntrs-muted">Noch keine Freigaben.</p>

    <p v-if="error" class="text-error text-sm px-6 py-4">{{ error }}</p>
  </BaseCard>
</template>

<script>
import { RouterLink } from 'vue-router'
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import { formatDate } from '@/data/dossierFields.js'
import { useDossiersStore } from '@/stores/dossiers.js'

export default {
  name: 'DossierSharesTab',
  components: { RouterLink, AppIcon, BaseButton, BaseCard },
  mixins: [asyncActionMixin],
  props: {
    uuid: { type: String, required: true },
  },
  data() {
    return {
      data: null,
      recipient: '',
      link: { name: '', password: '' },
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
  },
  watch: {
    uuid: {
      immediate: true,
      handler() {
        this.data = null
        return this.runAction(async () => {
          this.data = await this.dossiersStore.fetchShares(this.uuid)
        })
      },
    },
  },
  methods: {
    formatDate,
    create(payload) {
      return this.runAction(async () => {
        const share = await this.dossiersStore.createShare(this.uuid, payload)
        this.$router.push({ name: 'share-edit', params: { uuid: this.uuid, share: share.uuid } })
      })
    },
  },
}
</script>
