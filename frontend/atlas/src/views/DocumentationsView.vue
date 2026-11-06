<template>
  <AtlasPage :breadcrumbs="[{ label: 'Dokumentationen' }]" :loading="!groups" :error="error">
    <GroupedOverview
      :groups="groups"
      base="/documentations"
      icon="poll-h"
      empty="Noch keine Dokumentationen. Lege sie in einem Fach unter Institutionen an."
    />
  </AtlasPage>
</template>

<script>
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import AtlasPage from '@/components/AtlasPage.vue'
import GroupedOverview from '@/components/GroupedOverview.vue'
import { useAtlasStore } from '@/stores/atlas.js'

export default {
  name: 'DocumentationsView',
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
        '/documentations/',
        'Dokumentationen konnten nicht geladen werden.',
      )
    })
  },
}
</script>
