<template>
  <ul class="flex flex-col gap-2 max-sm:-mx-4 sm:gap-8">
    <li v-if="sponsor" :class="cardClass">
      <ResultItem :item="sponsor" rel="sponsored noopener noreferrer">
        <template #prefix>
          <span :class="sponsorLabelClass" class="hidden sm:inline">Gesponsert</span>
        </template>
        <template #badge>
          <span :class="sponsorLabelClass" class="sm:hidden">Gesponsert</span>
        </template>
      </ResultItem>
    </li>
    <li v-for="item in results" :key="item.key" :class="cardClass">
      <ResultItem
        :item="item"
        :with-image="withImages"
        :rating="ratingOf(item, hostRatings)"
        :report="hostRatings[item.host]?.grade ? hostRatings[item.host] : null"
        :pending="pendingHosts.includes(item.host)"
        :risky-links="riskyLinks"
        :confirm-links="confirmLinks"
        @warn="warn"
      />
    </li>
  </ul>
  <BaseDialog
    ref="warnDialog"
    :title="warnTitle"
    :description="warnMessage"
    :buttons="warnButtons"
    @action="onWarnAction"
  />
</template>

<script>
import BaseDialog from '@core/components/common/BaseDialog.vue'
import ResultItem from '@/components/ResultItem.vue'
import { ratingOf } from '@/data/ratings.js'

export default {
  name: 'ResultList',
  components: { BaseDialog, ResultItem },
  props: {
    results: { type: Array, required: true },
    withImages: { type: Boolean, default: false },
    sponsor: { type: Object, default: null },
    hostRatings: { type: Object, default: () => ({}) },
    pendingHosts: { type: Array, default: () => [] },
    riskyLinks: { type: String, default: 'warn' },
    confirmLinks: { type: Boolean, default: false },
  },
  data() {
    return {
      warnItem: null,
      sponsorLabelClass: 'shrink-0 text-xs font-medium text-wntrs-sponsor',
      cardClass:
        'max-sm:rounded-box max-sm:border max-sm:border-wntrs-border max-sm:px-3 max-sm:py-3',
    }
  },
  computed: {
    isConfirm() {
      return this.warnItem?.rating === 'confirm'
    },
    warnTitle() {
      return this.isConfirm ? 'Link öffnen' : 'Unsichere Seite'
    },
    warnButtons() {
      return [
        { value: 'cancel', label: 'Abbrechen', icon: 'cross' },
        this.isConfirm
          ? { value: 'open', label: 'Öffnen', variant: 'primary', icon: 'share-square' }
          : {
              value: 'open',
              label: 'Trotzdem öffnen',
              variant: 'error',
              outline: true,
              icon: 'share-square',
            },
      ]
    },
    warnMessage() {
      if (!this.warnItem) return ''
      const { host, rating, grade, unicode, url } = this.warnItem
      if (rating === 'confirm') return `Du verlässt die Suche und öffnest ${url}`
      const reasons = {
        http: 'verwendet keine Verschlüsselung (http)',
        lookalike: `wird als ${unicode} dargestellt und kann eine bekannte Seite nachahmen`,
        insecure: `ist laut Mozilla Observatory schlecht abgesichert (Note ${grade})`,
      }
      return `${host} ${reasons[rating]}. Möchtest du die Seite trotzdem öffnen?`
    },
  },
  methods: {
    ratingOf,
    warn(item) {
      this.warnItem = item
      this.$refs.warnDialog.open()
    },
    onWarnAction(value) {
      if (value === 'open') window.location.assign(this.warnItem.url)
    },
  },
}
</script>
