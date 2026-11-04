<template>
  <BaseCard>
    <div class="flex items-center justify-between gap-2 px-4 pt-4">
      <h3 class="text-xs font-bold uppercase tracking-wide text-wntrs-muted">Teilnehmer</h3>
      <BaseButton
        variant="neutral"
        shape="square"
        size="sm"
        title="Teilnehmer hinzufügen"
        @click="$emit('add')"
      >
        <AppIcon name="plus" alt="Teilnehmer hinzufügen" />
      </BaseButton>
    </div>

    <ul v-if="reference.participants.length" class="flex flex-col py-2">
      <li
        v-for="participant in reference.participants"
        :key="participant.uuid"
        class="flex flex-col gap-1.5 px-4 py-2"
      >
        <div class="flex items-center gap-2 min-w-0">
          <component
            :is="participant.dossier ? 'RouterLink' : 'div'"
            :to="
              participant.dossier && { name: 'dossier', params: { uuid: participant.dossier.uuid } }
            "
            class="flex items-center gap-2 min-w-0 flex-1"
            :class="{ 'group hover:text-primary': participant.dossier }"
            :title="participant.dossier && `Akte ${participant.dossier.title} öffnen`"
          >
            <ChatAvatar :participant="participant" :src="imageUrl(participant.avatar)" />
            <span class="flex flex-col min-w-0 flex-1">
              <span class="text-sm font-bold truncate group-hover:underline">
                {{ participant.name }}
              </span>
              <span class="text-xs text-wntrs-muted truncate">{{ role(participant) }}</span>
            </span>
          </component>
          <BaseButton
            variant="ghost"
            shape="square"
            size="xs"
            :title="`${participant.name} bearbeiten`"
            @click="$emit('edit', participant)"
          >
            <AppIcon name="pencil" :alt="`${participant.name} bearbeiten`" />
          </BaseButton>
        </div>
        <HealthBar :remaining="participant.remaining" :health="participant.health" />
        <span v-if="participant.dealt" class="text-xs text-error">
          {{ participant.dealt }} Angriffspunkte ausgeteilt
        </span>
      </li>
    </ul>

    <p v-else class="px-4 py-4 text-sm text-wntrs-muted">Noch keine Teilnehmer.</p>
  </BaseCard>
</template>

<script>
import { RouterLink } from 'vue-router'
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import ChatAvatar from '@/components/ChatAvatar.vue'
import HealthBar from '@/components/HealthBar.vue'
import { chatSides } from '@/data/eventReferences.js'
import chatMixin from '@/mixins/chatMixin.js'

export default {
  name: 'ChatParticipants',
  components: { RouterLink, AppIcon, BaseButton, BaseCard, ChatAvatar, HealthBar },
  mixins: [chatMixin],
  emits: ['add', 'edit'],
  methods: {
    role(participant) {
      return participant.dossier?.title ?? chatSides[participant.side]
    },
  },
}
</script>
