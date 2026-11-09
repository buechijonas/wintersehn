<template>
  <div class="flex flex-1 flex-col gap-8 px-6 pt-6 pb-16">
    <FeaturedHero v-if="netflix && featured" :title="featured" />
    <p v-if="error" class="text-sm text-error">{{ error }}</p>
    <template v-if="!rows.length && saving">
      <PosterRow v-for="n in 3" :key="n" title="Laden" loading />
    </template>
    <PosterRow v-for="row in rows" :key="row.key" :title="row.title" :items="row.items" />
    <SourceNotice class="mt-auto" />
  </div>
</template>

<script>
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import FeaturedHero from '@/components/FeaturedHero.vue'
import PosterRow from '@/components/PosterRow.vue'
import SourceNotice from '@/components/SourceNotice.vue'
import { lumonStyle } from '@/lib/style.js'
import { useLumonStore } from '@/stores/lumon.js'

export default {
  name: 'BrowseView',
  components: { FeaturedHero, PosterRow, SourceNotice },
  mixins: [asyncActionMixin],
  data() {
    return { featured: null, rows: [] }
  },
  computed: {
    netflix() {
      return lumonStyle.value === 'netflix'
    },
  },
  created() {
    this.runAction(async () => {
      const overview = await useLumonStore().load(
        `/catalog/browse/${this.$route.meta.mediaType}/`,
        'Übersicht konnte nicht geladen werden.',
      )
      this.featured = overview.featured
      this.rows = overview.rows
    })
  },
}
</script>
