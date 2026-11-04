<template>
  <BaseCard class="px-6 border-t-0">
    <div v-if="!link && !error" class="flex flex-col gap-3 py-4">
      <div class="skeleton h-4 w-full"></div>
      <div class="skeleton h-4 w-2/3"></div>
    </div>

    <div v-if="link" class="flex items-center justify-between gap-4 pt-4">
      <h3 class="font-bold">govex</h3>
      <div class="flex items-center gap-2">
        <BaseButton
          v-if="editing && link.linked"
          variant="neutral"
          shape="square"
          size="sm"
          title="Verknüpfung lösen"
          :disabled="saving"
          @click="unlink"
        >
          <AppIcon name="link-slash-alt" alt="Verknüpfung lösen" />
        </BaseButton>
        <EditToggle v-model="editing" />
      </div>
    </div>

    <template v-if="link?.linked">
      <AccountRow
        v-if="link.account"
        :name="link.account.name"
        :username="link.account.username"
        :avatar="link.account.avatar"
      >
        <a
          v-if="link.account.email"
          :href="`mailto:${link.account.email}`"
          class="link link-hover text-primary truncate"
          >{{ link.account.email }}</a
        >
      </AccountRow>
      <p v-else class="py-3 text-sm text-wntrs-muted">
        Das verknüpfte govex-Konto existiert nicht mehr.
      </p>
    </template>

    <p v-else-if="link && !editing" class="py-4 text-sm text-wntrs-muted">
      Kein govex-Konto verknüpft.
    </p>

    <div v-else-if="link" class="py-4">
      <input
        v-model.trim="query"
        type="search"
        placeholder="govex-Konto suchen"
        aria-label="govex-Konto suchen"
        class="input w-full"
      />
      <ul v-if="results.length" class="flex flex-col divide-y divide-wntrs-border mt-2">
        <AccountRow
          v-for="account in results"
          :key="account.sub"
          tag="li"
          :name="account.name"
          :username="account.username"
          :avatar="account.avatar"
        >
          <span class="text-wntrs-muted truncate">{{ account.email }}</span>
          <template #actions>
            <BaseButton size="sm" :disabled="saving" @click="linkAccount(account)">
              <AppIcon name="link-alt" />
              Verknüpfen
            </BaseButton>
          </template>
        </AccountRow>
      </ul>
      <p v-else-if="query.length >= 2 && !searching" class="mt-3 text-sm text-wntrs-muted">
        Keine govex-Konten gefunden.
      </p>
    </div>

    <p v-if="error" class="text-error text-sm py-3">{{ error }}</p>
  </BaseCard>

  <template v-if="link?.linked">
    <h3 class="text-xl font-light my-4">swissfy</h3>
    <BaseCard class="px-6">
      <div v-if="swissfy === null && !swissfyError" class="flex items-center gap-4 py-4">
        <div class="skeleton size-12 shrink-0 rounded-full"></div>
        <div class="skeleton h-4 w-1/2"></div>
      </div>
      <AccountRow
        v-else-if="swissfy?.profile"
        tag="a"
        :href="swissfy.profile.url"
        target="_blank"
        rel="noopener"
        :name="swissfyName"
        :username="swissfy.profile.username"
        :avatar="swissfy.profile.avatar"
        :src="swissfyPicture"
        class="-mx-6 px-6 hover:bg-base-200"
      />
      <p v-else-if="swissfy" class="py-3 text-sm text-wntrs-muted">Kein swissfy-Konto.</p>
      <p v-if="swissfyError" class="text-error text-sm py-3">{{ swissfyError }}</p>
    </BaseCard>
  </template>
</template>

<script>
import AccountRow from '@/components/AccountRow.vue'
import EditToggle from '@/components/EditToggle.vue'
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import { useDossiersStore } from '@/stores/dossiers.js'

const SEARCH_DELAY = 300

export default {
  name: 'DossierLinkTab',
  components: { AccountRow, AppIcon, BaseButton, BaseCard, EditToggle },
  mixins: [asyncActionMixin],
  props: {
    uuid: { type: String, required: true },
  },
  data() {
    return {
      link: null,
      editing: false,
      query: '',
      results: [],
      searching: false,
      swissfy: null,
      swissfyError: '',
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
    swissfyName() {
      const { first_name, last_name } = this.swissfy.profile
      return [first_name, last_name].filter(Boolean).join(' ')
    },
    swissfyPicture() {
      return this.swissfy.profile.has_picture ? this.dossiersStore.swissfyPictureUrl(this.uuid) : ''
    },
  },
  watch: {
    query(query) {
      clearTimeout(this.searchTimer)
      this.results = []
      if (query.length < 2) return
      this.searching = true
      this.searchTimer = setTimeout(() => this.search(query), SEARCH_DELAY)
    },
    'link.linked'(linked) {
      this.swissfy = null
      this.swissfyError = ''
      if (linked) this.loadSwissfy()
    },
  },
  mounted() {
    return this.runAction(async () => {
      this.link = await this.dossiersStore.fetchGovex(this.uuid)
    })
  },
  beforeUnmount() {
    clearTimeout(this.searchTimer)
  },
  methods: {
    async search(query) {
      await this.runAction(async () => {
        const results = await this.dossiersStore.searchGovex(query)
        if (query === this.query) this.results = results
      })
      this.searching = false
    },
    linkAccount(account) {
      return this.runAction(async () => {
        this.link = await this.dossiersStore.linkGovex(this.uuid, account.sub)
        this.query = ''
      })
    },
    unlink() {
      return this.runAction(async () => {
        await this.dossiersStore.unlinkGovex(this.uuid)
        this.link = { linked: false, account: null }
      })
    },
    async loadSwissfy() {
      try {
        this.swissfy = await this.dossiersStore.fetchSwissfy(this.uuid)
      } catch (e) {
        this.swissfyError = e.message
      }
    },
  },
}
</script>
