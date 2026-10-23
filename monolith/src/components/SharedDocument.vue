<template>
  <BaseCard role="tablist" class="tabs flex-nowrap overflow-x-auto px-2 [scrollbar-width:none]">
    <RouterLink
      v-for="(section, index) in document.sections"
      :key="index"
      role="tab"
      class="tab h-12 shrink-0 whitespace-nowrap border-y-2 border-t-transparent"
      :class="active === index ? 'tab-active border-b-primary' : 'border-b-transparent'"
      :aria-selected="active === index"
      :to="{ query: { tab: index } }"
      replace
    >
      <span v-if="section.key">{{ sectionLabels[section.key] }}</span>
      <CipherText v-else />
    </RouterLink>
  </BaseCard>

  <BaseCard class="border-t-0">
    <ul v-if="current.items.length" class="flex flex-col divide-y divide-wntrs-border">
      <li
        v-for="(item, index) in current.items"
        :key="index"
        class="flex flex-col gap-1 px-6 py-4 text-sm"
      >
        <span v-if="labelShown(item)" class="font-bold break-words">
          {{ formatLabel(current.key, item.label) }}
        </span>
        <CipherText v-else :length="14" class="font-bold" />
        <span v-if="valueShown(item)" class="break-words whitespace-pre-line">
          {{ formatValue(current.key, item.value, item.label) }}
        </span>
        <CipherText v-else :length="24" />
        <ul v-if="item.links.length" class="flex flex-wrap gap-1.5 mt-1">
          <li
            v-for="(link, linkIndex) in item.links"
            :key="linkIndex"
            class="badge badge-sm badge-soft"
          >
            <template v-if="link.section">{{ formatLabel(link.section, link.label) }}</template>
            <CipherText v-else :length="6" />
          </li>
        </ul>
      </li>
    </ul>
    <p v-else class="px-6 py-4 text-sm text-wntrs-muted">Keine Einträge.</p>
  </BaseCard>
</template>

<script>
import { RouterLink } from 'vue-router'
import BaseCard from '@core/components/common/BaseCard.vue'
import CipherText from '@core/components/common/CipherText.vue'
import { activeTab, formatLabel, formatValue, labelShown, valueShown } from '@/data/sharing.js'
import { sectionLabels } from '@/data/tabs.js'

export default {
  name: 'SharedDocument',
  components: { RouterLink, BaseCard, CipherText },
  props: {
    document: { type: Object, required: true },
  },
  data() {
    return { sectionLabels }
  },
  computed: {
    active() {
      return activeTab(this.$route)
    },
    current() {
      return this.document.sections[this.active] ?? this.document.sections[0]
    },
  },
  methods: {
    formatLabel,
    formatValue,
    labelShown,
    valueShown,
  },
}
</script>
