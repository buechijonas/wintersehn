<template>
  <BaseBreadcrumbs :items="breadcrumbs">
    <template v-if="share" #actions>
      <div class="flex gap-2">
        <BaseButton variant="neutral" size="sm" :disabled="saving" @click="togglePreview">
          {{ preview ? 'Bearbeiten' : 'Vorschau' }}
        </BaseButton>
        <SaveButton :disabled="saving" @click="save" />
        <DeleteButton title="Freigabe widerrufen" @click="$refs.confirmDialog.open()" />
      </div>
    </template>
  </BaseBreadcrumbs>
  <div
    class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1"
  >
    <div class="mx-auto w-full max-w-150 pt-4 flex flex-col gap-4">
      <div v-if="!share && !error" class="flex flex-col gap-4">
        <div class="skeleton h-12 w-full"></div>
        <div class="skeleton h-64 w-full"></div>
      </div>

      <div v-else-if="preview">
        <SharedDocument :document="preview" />
      </div>

      <template v-else-if="share">
        <p class="text-sm text-wntrs-muted">
          Alles, was nicht auf «Sichtbar» steht, sieht {{ audience }} zensiert.
        </p>

        <BaseCard v-if="share.link" class="flex flex-col gap-3 px-6 py-4 text-sm">
          <form class="flex items-center gap-2" @submit.prevent="update({ token })">
            <label for="share-token" class="text-wntrs-muted truncate shrink">
              {{ share.link.base }}
            </label>
            <input
              id="share-token"
              v-model="token"
              aria-label="Pfad"
              class="input input-sm flex-1 min-w-24"
              pattern="[A-Za-z0-9_\-]{6,64}"
              required
            />
            <SaveButton type="submit" :disabled="saving || token === share.token" />
            <BaseButton variant="neutral" size="sm" @click="copyLink">
              {{ copied ? 'Kopiert' : 'Kopieren' }}
            </BaseButton>
          </form>
          <form class="flex items-center gap-2" @submit.prevent="update({ password })">
            <input
              v-model="password"
              type="password"
              autocomplete="new-password"
              :placeholder="share.has_password ? 'Neues Passwort' : 'Passwort setzen'"
              aria-label="Passwort"
              class="input flex-1 min-w-0"
              required
            />
            <SaveButton type="submit" :disabled="saving" />
            <BaseButton
              v-if="share.has_password"
              variant="neutral"
              size="sm"
              :disabled="saving"
              @click="update({ password: '' })"
            >
              Entfernen
            </BaseButton>
          </form>
          <span class="text-xs text-wntrs-muted">
            <template v-if="share.has_password">Passwortgeschützt.</template>
            <template v-else>
              Ohne Passwort: Wer den Link hat, sieht die Akte. Ein eigener Pfad ist leichter zu
              erraten.
            </template>
          </span>
        </BaseCard>

        <BaseCard>
          <span class="block px-6 pt-4 font-bold">Breadcrumbs</span>
          <ul class="flex flex-col divide-y divide-wntrs-border">
            <li
              v-for="crumb in crumbs"
              :key="crumb.target"
              class="flex items-center justify-between gap-4 px-6 py-3 text-sm"
            >
              <div class="flex flex-col min-w-0">
                <span class="font-bold">{{ crumb.label }}</span>
                <span class="text-wntrs-muted truncate">{{ crumb.value }}</span>
              </div>
              <VisibilityToggle
                v-model="rules[crumb.target]"
                :options="titleVisibilities"
                :label="crumb.label"
              />
            </li>
          </ul>
        </BaseCard>

        <BaseCard v-for="section in share.sections" :key="section.target">
          <div class="flex items-center justify-between gap-4 px-6 py-4">
            <span class="font-bold">{{ sectionLabels[section.key] }}</span>
            <VisibilityToggle v-model="rules[section.target]" label="Tab" />
          </div>
          <template v-if="section.items.length">
            <div
              class="flex items-center justify-between gap-4 px-6 pb-3 border-b border-wntrs-border"
            >
              <span class="text-xs text-wntrs-muted">Alle Einträge</span>
              <VisibilityToggle
                label="Alle Einträge"
                @update:model-value="setAll(section, $event)"
              />
            </div>
            <ul
              class="flex flex-col divide-y divide-wntrs-border"
              :class="{ 'opacity-50': rules[section.target] !== 'visible' }"
            >
              <li
                v-for="item in section.items"
                :key="item.target"
                class="flex items-center justify-between gap-4 px-6 py-3 text-sm"
              >
                <div class="flex flex-col min-w-0">
                  <span class="font-bold truncate">
                    {{ formatLabel(section.key, item.label) }}
                  </span>
                  <span class="text-wntrs-muted truncate">
                    {{ formatValue(section.key, item.value, item.label) }}
                  </span>
                </div>
                <VisibilityToggle v-model="rules[item.target]" />
              </li>
            </ul>
          </template>
        </BaseCard>
      </template>

      <p v-if="error" class="text-error text-sm text-center">{{ error }}</p>
    </div>
  </div>

  <ConfirmDialog
    ref="confirmDialog"
    title="Freigabe widerrufen"
    :message="`${audience} verliert den Zugriff auf diese Akte.`"
    confirm-label="Widerrufen"
    @confirm="remove"
  />
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import ConfirmDialog from '@core/components/common/ConfirmDialog.vue'
import DeleteButton from '@core/components/common/DeleteButton.vue'
import SaveButton from '@core/components/common/SaveButton.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import SharedDocument from '@/components/SharedDocument.vue'
import VisibilityToggle from '@/components/VisibilityToggle.vue'
import { formatLabel, formatValue, titleVisibilities } from '@/data/sharing.js'
import { sectionLabels } from '@/data/tabs.js'
import { useDossiersStore } from '@/stores/dossiers.js'

function collectRules(share) {
  const entries = [
    ...share.breadcrumbs,
    share.title,
    ...share.sections,
    ...share.sections.flatMap((section) => section.items),
  ]
  return Object.fromEntries(entries.map(({ target, visibility }) => [target, visibility]))
}

export default {
  name: 'ShareEditView',
  components: {
    BaseBreadcrumbs,
    BaseButton,
    BaseCard,
    ConfirmDialog,
    DeleteButton,
    SaveButton,
    SharedDocument,
    VisibilityToggle,
  },
  mixins: [asyncActionMixin],
  data() {
    return {
      sectionLabels,
      titleVisibilities,
      share: null,
      rules: {},
      preview: null,
      password: '',
      token: '',
      copied: false,
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
    audience() {
      return this.share?.recipient?.title ?? `Wer den Link «${this.share?.name}» hat`
    },
    crumbs() {
      const [root, tab] = this.share.breadcrumbs
      const crumbs = [
        { ...root, label: 'Bereich', value: 'Mit mir geteilt' },
        { ...this.share.title, label: 'Titel' },
        { ...tab, label: 'Tab', value: 'Name des geöffneten Tabs' },
      ]
      return this.share.recipient ? crumbs : crumbs.slice(1)
    },
    breadcrumbs() {
      const { uuid } = this.$route.params
      return [
        { label: 'Personalakten', to: '/' },
        {
          label: this.share?.title.value ?? '…',
          to: { name: 'dossier', params: { uuid }, query: { tab: 'shares' } },
        },
        { label: this.share ? `Freigabe: ${this.share.recipient?.title ?? this.share.name}` : '…' },
      ]
    },
  },
  watch: {
    '$route.params.share': {
      immediate: true,
      handler() {
        this.share = null
        this.preview = null
        return this.runAction(async () => this.load(await this.request('fetchShare')))
      },
    },
  },
  methods: {
    formatLabel,
    formatValue,
    request(action, ...args) {
      const { uuid, share } = this.$route.params
      return this.dossiersStore[action](uuid, share, ...args)
    },
    load(share) {
      this.share = share
      this.token = share.token
      this.rules = collectRules(share)
    },
    setAll(section, visibility) {
      section.items.forEach((item) => (this.rules[item.target] = visibility))
    },
    save() {
      return this.runAction(async () => this.load(await this.request('saveShareRules', this.rules)))
    },
    update(data) {
      return this.runAction(async () => {
        const share = await this.request('updateShare', data)
        this.share = share
        this.token = share.token
        this.password = ''
        this.copied = false
      })
    },
    async copyLink() {
      await navigator.clipboard.writeText(this.share.link.url)
      this.copied = true
    },
    togglePreview() {
      if (this.preview) {
        this.preview = null
        return
      }
      return this.showPreview()
    },
    showPreview() {
      return this.runAction(async () => {
        this.load(await this.request('saveShareRules', this.rules))
        this.preview = await this.request('fetchSharePreview')
      })
    },
    remove() {
      return this.runAction(async () => {
        await this.request('deleteShare')
        this.$router.push({
          name: 'dossier',
          params: { uuid: this.$route.params.uuid },
          query: { tab: 'shares' },
        })
      })
    },
  },
}
</script>
