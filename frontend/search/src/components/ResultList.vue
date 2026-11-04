<template>
  <ul class="flex flex-col gap-2 max-sm:-mx-4 sm:gap-8">
    <li v-if="sponsor" :class="cardClass">
      <ResultItem :item="sponsor" rel="sponsored noopener noreferrer">
        <template #badge>
          <span
            class="shrink-0 rounded-full bg-wntrs-sponsor-surface px-2 py-0.5 text-xs font-medium text-wntrs-sponsor"
          >
            Sponsored
          </span>
        </template>
      </ResultItem>
    </li>
    <li v-for="item in results" :key="item.key" :class="cardClass">
      <ResultItem :item="item" :with-image="withImages" />
    </li>
  </ul>
</template>

<script>
import ResultItem from '@/components/ResultItem.vue'

export default {
  name: 'ResultList',
  components: { ResultItem },
  props: {
    results: { type: Array, required: true },
    withImages: { type: Boolean, default: false },
    sponsor: { type: Object, default: null },
  },
  data() {
    return {
      cardClass:
        'max-sm:rounded-box max-sm:border max-sm:border-wntrs-border max-sm:px-3 max-sm:py-3',
    }
  },
}
</script>
