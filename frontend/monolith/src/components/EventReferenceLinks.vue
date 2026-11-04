<template>
  <BaseCard>
    <div class="flex items-center justify-between gap-2 px-4 pt-4">
      <h3 class="text-xs font-bold uppercase tracking-wide text-wntrs-muted">
        Verknüpfte Referenzen
      </h3>
      <EditToggle v-model="editing" />
    </div>

    <div v-if="editing" class="px-4 py-3">
      <p v-if="!siblings.length" class="text-sm text-wntrs-muted">
        Das Ereignis hat keine weiteren Referenzen.
      </p>
      <ul v-else class="flex flex-wrap gap-1.5">
        <li v-for="sibling in siblings" :key="sibling.uuid">
          <button
            type="button"
            class="badge badge-sm cursor-pointer"
            :class="
              reference.links.includes(sibling.uuid)
                ? 'badge-primary'
                : 'badge-ghost hover:badge-primary'
            "
            :aria-pressed="reference.links.includes(sibling.uuid)"
            :disabled="saving"
            @click="toggle(sibling)"
          >
            {{ sibling.title }}
          </button>
        </li>
      </ul>
    </div>

    <ul v-else-if="linked.length" class="flex flex-col py-2">
      <li v-for="sibling in linked" :key="sibling.uuid">
        <RouterLink
          :to="{ name: 'event-reference', params: { ...$route.params, reference: sibling.uuid } }"
          class="flex items-center gap-2 px-4 py-2 text-sm hover:bg-base-200"
        >
          <img class="size-5 shrink-0" :src="referenceIcon(sibling)" alt="" />
          <span class="truncate">{{ sibling.title }}</span>
        </RouterLink>
      </li>
    </ul>

    <p v-else class="px-4 py-3 text-sm text-wntrs-muted">Keine Verknüpfungen.</p>

    <p v-if="error" class="text-error text-sm px-4 pb-3">{{ error }}</p>
  </BaseCard>
</template>

<script>
import { RouterLink } from 'vue-router'
import BaseCard from '@core/components/common/BaseCard.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import EditToggle from '@/components/EditToggle.vue'
import { referenceIcon } from '@/data/eventReferences.js'
import chatMixin from '@/mixins/chatMixin.js'

export default {
  name: 'EventReferenceLinks',
  components: { RouterLink, BaseCard, EditToggle },
  mixins: [asyncActionMixin, chatMixin],
  props: {
    siblings: { type: Array, required: true },
  },
  data() {
    return {
      editing: false,
    }
  },
  computed: {
    linked() {
      return this.siblings.filter((sibling) => this.reference.links.includes(sibling.uuid))
    },
  },
  methods: {
    referenceIcon,
    toggle(sibling) {
      const links = new Set(this.reference.links)
      if (!links.delete(sibling.uuid)) links.add(sibling.uuid)
      return this.runAction(async () => {
        this.$emit(
          'update',
          await this.dossiersStore.updateEventReference(
            this.uuid,
            this.event,
            this.reference.uuid,
            { links: [...links] },
          ),
        )
      })
    },
  },
}
</script>
