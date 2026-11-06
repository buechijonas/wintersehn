<template>
  <AtlasPage :breadcrumbs="breadcrumbs" :loading="!learningSet" :error="error">
    <template #actions>
      <LearningSetActions v-if="learningSet" :learning-set="learningSet" @error="error = $event" />
    </template>
    <div class="mx-auto flex w-full max-w-160 flex-col gap-6">
      <p v-if="!cards.length" class="text-center text-wntrs-muted">
        Dieses Lernset hat noch keine Karten.
      </p>
      <template v-else>
        <span class="text-center text-sm text-wntrs-muted"
          >{{ index + 1 }} / {{ cards.length }}</span
        >
        <BaseCard
          tag="button"
          type="button"
          class="flex min-h-72 cursor-pointer items-center justify-center rounded-box p-8"
          @click="flipped = !flipped"
        >
          <CardFace
            :label="flipped ? 'Rückseite' : 'Vorderseite'"
            :text="flipped ? card.back : card.front"
            :image="flipped ? card.back_image_url : card.front_image_url"
          />
        </BaseCard>
        <div class="grid grid-cols-2 gap-2">
          <BaseButton :disabled="index === 0" @click="move(-1)">
            <AppIcon name="angle-left" />
            Zurück
          </BaseButton>
          <BaseButton variant="primary" :disabled="index === cards.length - 1" @click="move(1)">
            Weiter
            <AppIcon name="angle-left" class="rotate-180" />
          </BaseButton>
        </div>
      </template>
    </div>
  </AtlasPage>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import AtlasPage from '@/components/AtlasPage.vue'
import CardFace from '@/components/CardFace.vue'
import LearningSetActions from '@/components/LearningSetActions.vue'
import { learningSetBreadcrumbs } from '@/lib/breadcrumbs.js'
import { useAtlasStore } from '@/stores/atlas.js'

export default {
  name: 'BrowseView',
  components: { AppIcon, AtlasPage, BaseButton, BaseCard, CardFace, LearningSetActions },
  mixins: [asyncActionMixin],
  data() {
    return {
      learningSet: null,
      index: 0,
      flipped: false,
    }
  },
  computed: {
    cards() {
      return this.learningSet?.cards ?? []
    },
    card() {
      return this.cards[this.index]
    },
    breadcrumbs() {
      return learningSetBreadcrumbs(this.learningSet, 'Karten blättern')
    },
  },
  mounted() {
    this.runAction(async () => {
      this.learningSet = await useAtlasStore().load(
        `/learning-sets/${this.$route.params.uuid}/`,
        'Lernset konnte nicht geladen werden.',
      )
    })
  },
  methods: {
    move(step) {
      this.index += step
      this.flipped = false
    },
  },
}
</script>
