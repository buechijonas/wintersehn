<template>
  <BaseDialog ref="dialog" :title="participant ? 'Teilnehmer bearbeiten' : 'Teilnehmer hinzufügen'">
    <form :id="formId" class="fieldset" @submit.prevent="confirm">
      <div class="flex items-center gap-4">
        <ChatAvatar
          :participant="{ name: draft.name || '?' }"
          :src="imageUrl(draft.avatar)"
          class="size-16! text-xl"
        />
        <div class="flex flex-col gap-2 flex-1">
          <ImagePickButton label="Profilbild wählen" :disabled="saving" @pick="setAvatar" />
          <BaseButton
            v-if="draft.avatar"
            variant="ghost"
            size="sm"
            :disabled="saving"
            @click="draft.avatar = null"
          >
            Profilbild entfernen
          </BaseButton>
        </div>
      </div>

      <label class="label mt-4" :for="`${formId}-name`">Username</label>
      <input
        :id="`${formId}-name`"
        ref="input"
        v-model.trim="draft.name"
        type="text"
        maxlength="100"
        class="input w-full"
        required
      />

      <label class="label mt-2" :for="`${formId}-health`">Start-Health</label>
      <input
        :id="`${formId}-health`"
        v-model.number="draft.health"
        type="number"
        min="1"
        max="1000"
        class="input w-full"
        required
      />

      <label class="label mt-2" :for="`${formId}-dossier`">Personalakte</label>
      <select :id="`${formId}-dossier`" v-model="draft.dossier" class="select w-full">
        <option :value="null">Keine Akte</option>
        <option v-for="dossier in dossiers" :key="dossier.uuid" :value="dossier.uuid">
          {{ dossier.title }}
        </option>
      </select>

      <span class="label mt-2">Seite im Chat</span>
      <div class="join w-full">
        <BaseButton
          v-for="(label, side) in chatSides"
          :key="side"
          class="join-item flex-1"
          :variant="draft.side === side ? 'primary' : 'neutral'"
          @click="draft.side = side"
        >
          {{ label }}
        </BaseButton>
      </div>

      <p v-if="error" class="text-error text-sm mt-2">{{ error }}</p>
    </form>

    <template #actions>
      <DeleteButton v-if="participant" class="mr-auto" @click="remove" />
      <BaseButton variant="neutral" @click="$refs.dialog.close()">
        <AppIcon name="cross" />
        Abbrechen
      </BaseButton>
      <BaseButton type="submit" :form="formId" variant="primary" :disabled="saving">
        <AppIcon :name="participant ? 'disk' : 'plus'" />
        {{ participant ? 'Speichern' : 'Hinzufügen' }}
      </BaseButton>
    </template>
  </BaseDialog>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseDialog from '@core/components/common/BaseDialog.vue'
import DeleteButton from '@core/components/common/DeleteButton.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import ChatAvatar from '@/components/ChatAvatar.vue'
import ImagePickButton from '@/components/ImagePickButton.vue'
import { chatSides } from '@/data/eventReferences.js'
import chatMixin from '@/mixins/chatMixin.js'

function emptyDraft(side) {
  return { name: '', health: 100, dossier: null, avatar: null, side }
}

export default {
  name: 'ChatParticipantDialog',
  components: { AppIcon, BaseButton, BaseDialog, ChatAvatar, DeleteButton, ImagePickButton },
  mixins: [asyncActionMixin, chatMixin],
  emits: ['confirm', 'remove'],
  data() {
    return {
      chatSides,
      formId: 'chat-participant-dialog-form',
      participant: null,
      draft: emptyDraft('left'),
    }
  },
  computed: {
    dossiers() {
      return this.dossiersStore.items ?? []
    },
  },
  methods: {
    open(participant = null) {
      const hasRight = this.reference.participants.some((p) => p.side === 'right')
      this.participant = participant
      this.error = ''
      this.draft = participant
        ? {
            name: participant.name,
            health: participant.health,
            dossier: participant.dossier?.uuid ?? null,
            avatar: participant.avatar,
            side: participant.side,
          }
        : emptyDraft(hasRight ? 'left' : 'right')
      if (!this.dossiersStore.items) this.dossiersStore.fetchDossiers()
      this.$refs.dialog.open()
      this.$nextTick(() => this.$refs.input.focus())
    },
    setAvatar(file) {
      return this.runAction(async () => {
        this.draft.avatar = await this.upload(file)
      })
    },
    confirm() {
      this.$refs.dialog.close()
      this.$emit('confirm', { participant: this.participant, data: { ...this.draft } })
    },
    remove() {
      this.$refs.dialog.close()
      this.$emit('remove', this.participant)
    },
  },
}
</script>
