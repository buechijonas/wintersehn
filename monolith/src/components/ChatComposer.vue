<template>
  <form v-if="reference.participants.length" class="flex flex-col gap-2" @submit.prevent="send">
    <div class="flex flex-wrap items-center gap-2">
      <select
        v-model="draft.sender"
        aria-label="Absender"
        class="select select-sm flex-1 min-w-36"
        required
      >
        <option
          v-for="participant in reference.participants"
          :key="participant.uuid"
          :value="participant.uuid"
        >
          {{ participant.name }}
        </option>
      </select>
      <label class="input input-sm w-32 shrink-0" title="Angriffspunkte">
        <span class="text-xs text-wntrs-muted">Angriff</span>
        <input v-model.number="draft.attack" type="number" min="0" max="1000" />
      </label>
      <select
        v-model="draft.target"
        aria-label="Ziel"
        class="select select-sm flex-1 min-w-36"
        :disabled="!draft.attack"
      >
        <option :value="null">Kein Ziel</option>
        <option
          v-for="participant in targetsOf(draft.sender)"
          :key="participant.uuid"
          :value="participant.uuid"
        >
          auf {{ participant.name }}
        </option>
      </select>
    </div>

    <div v-if="draft.image" class="flex items-center gap-2">
      <img :src="imageUrl(draft.image)" alt="Bild" class="h-16 rounded-lg" />
      <BaseButton
        variant="ghost"
        shape="square"
        size="xs"
        title="Bild entfernen"
        @click="draft.image = null"
      >
        <AppIcon name="cross" alt="Bild entfernen" />
      </BaseButton>
    </div>

    <div class="flex items-end gap-2">
      <input ref="file" type="file" accept="image/*" class="hidden" @change="attach" />
      <BaseButton
        variant="neutral"
        shape="square"
        title="Bild anhängen"
        :disabled="saving"
        @click="$refs.file.click()"
      >
        <AppIcon name="picture" alt="Bild anhängen" />
      </BaseButton>
      <textarea
        v-model="draft.text"
        aria-label="Nachricht"
        placeholder="Nachricht"
        class="textarea flex-1 min-h-10 [field-sizing:content]"
        rows="1"
        @keydown.enter.exact.prevent="send"
      ></textarea>
      <BaseButton
        type="submit"
        variant="primary"
        shape="square"
        title="Senden"
        :disabled="saving || !(draft.text.trim() || draft.image)"
      >
        <AppIcon name="plane" alt="Senden" />
      </BaseButton>
    </div>

    <p v-if="error" class="text-error text-sm">{{ error }}</p>
  </form>

  <p v-else class="text-sm text-wntrs-muted">Füge zuerst Teilnehmer hinzu.</p>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import { messageData } from '@/data/eventReferences.js'
import chatMixin from '@/mixins/chatMixin.js'

export default {
  name: 'ChatComposer',
  components: { AppIcon, BaseButton },
  mixins: [asyncActionMixin, chatMixin],
  data() {
    return {
      draft: { sender: null, text: '', image: null, attack: 0, target: null },
    }
  },
  watch: {
    'reference.participants': {
      immediate: true,
      handler(participants) {
        if (this.participantsByUuid[this.draft.sender]) return
        this.draft.sender = participants[0]?.uuid ?? null
      },
    },
    'draft.sender'(sender) {
      const targets = this.targetsOf(sender)
      this.draft.target = targets.length === 1 ? targets[0].uuid : null
    },
  },
  methods: {
    attach(event) {
      const [file] = event.target.files
      event.target.value = ''
      if (!file) return
      return this.runAction(async () => {
        this.draft.image = await this.upload(file)
      })
    },
    async send() {
      if (this.saving || !(this.draft.text.trim() || this.draft.image)) return
      await this.addItem('messages', messageData(this.draft))
      if (this.error) return
      this.draft = { ...this.draft, text: '', image: null, attack: 0 }
    },
  },
}
</script>
