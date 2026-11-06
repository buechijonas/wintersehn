<template>
  <AtlasPage :breadcrumbs="[{ label: 'Lernsets' }]" :loading="!groups" :error="error">
    <GroupedOverview
      :groups="groups"
      base="/learning-sets"
      icon="cards-blank"
      :meta="cardProgress"
      empty="Noch keine Lernsets. Lege sie in einem Fach unter Institutionen an."
    />
  </AtlasPage>
</template>

<script>
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import AtlasPage from '@/components/AtlasPage.vue'
import GroupedOverview from '@/components/GroupedOverview.vue'
import { cardProgress } from '@/lib/progress.js'
import { useAtlasStore } from '@/stores/atlas.js'

export default {
  name: 'LearningSetsView',
  components: { AtlasPage, GroupedOverview },
  mixins: [asyncActionMixin],
  data() {
    return {
      groups: null,
    }
  },
  mounted() {
    this.runAction(async () => {
      this.groups = await useAtlasStore().load(
        '/learning-sets/',
        'Lernsets konnten nicht geladen werden.',
      )
    })
  },
  methods: {
    cardProgress,
  },
}
</script>
