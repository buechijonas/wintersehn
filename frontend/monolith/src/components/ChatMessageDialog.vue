<template>
  <BaseDialog ref="dialog" title="Nachricht bearbeiten">
    <form :id="formId" class="fieldset" @submit.prevent="confirm">
      <label class="label" :for="`${formId}-sender`">Absender</label>
      <select :id="`${formId}-sender`" v-model="draft.sender" class="select w-full" required>
        <option
          v-for="participant in reference.participants"
          :key="participant.uuid"
          :value="participant.uuid"
        >
          {{ participant.name }}
        </option>
      </select>

      <label class="label mt-2" :for="`${formId}-text`">Text</label>
      <textarea
        :id="`${formId}-text`"
        v-model="draft.text"
        class="textarea w-full min-h-24 [field-sizing:content]"
      ></textarea>

      <span class="label mt-2">Bild</span>
      <div class="flex items-center gap-3">
        <img v-if="draft.image" :src="imageUrl(draft.image)" alt="Bild" class="h-20 rounded-lg" />
        <div class="flex flex-col gap-2 flex-1">
          <ImagePickButton
            :label="draft.image ? 'Bild ersetzen' : 'Bild wählen'"
            :selected="draft.image"
            @pick="draft.image = $event"
          />
          <BaseButton v-if="draft.image" variant="ghost" size="sm" @click="draft.image = null">
            Bild entfernen
          </BaseButton>
        </div>
      </div>

      <span class="label mt-2">Angriff</span>
      <div class="flex gap-2">
        <input
          v-model.number="draft.attack"
          type="number"
          min="0"
          max="1000"
          aria-label="Angriffspunkte"
          class="input w-24"
        />
        <select
          v-model="draft.target"
          aria-label="Ziel"
          class="select flex-1"
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
    </form>

    <template #actions>
      <DeleteButton class="mr-auto" @click="remove" />
      <BaseButton variant="neutral" @click="$refs.dialog.close()">
        <AppIcon name="cross" />
        Abbrechen
      </BaseButton>
      <BaseButton
        type="submit"
        :form="formId"
        variant="primary"
        :disabled="!(draft.text.trim() || draft.image)"
      >
        <AppIcon name="disk" />
        Speichern
      </BaseButton>
    </template>
  </BaseDialog>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseDialog from '@core/components/common/BaseDialog.vue'
import DeleteButton from '@core/components/common/DeleteButton.vue'
import ImagePickButton from '@/components/ImagePickButton.vue'
import { messageData } from '@/data/eventReferences.js'
import chatMixin from '@/mixins/chatMixin.js'

export default {
  name: 'ChatMessageDialog',
  components: { AppIcon, BaseButton, BaseDialog, DeleteButton, ImagePickButton },
  mixins: [chatMixin],
  emits: ['confirm', 'remove'],
  data() {
    return {
      formId: 'chat-message-dialog-form',
      message: null,
      draft: { sender: null, text: '', image: null, attack: 0, target: null },
    }
  },
  methods: {
    open(message) {
      const { sender, text, image, attack, target } = message
      this.message = message
      this.draft = { sender, text, image, attack, target }
      this.$refs.dialog.open()
    },
    confirm() {
      this.$refs.dialog.close()
      this.$emit('confirm', { message: this.message, data: messageData(this.draft) })
    },
    remove() {
      this.$refs.dialog.close()
      this.$emit('remove', this.message)
    },
  },
}
</script>
