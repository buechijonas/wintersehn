<template>
  <div class="flex flex-col gap-4">
    <p v-if="!reference.messages.length" class="py-8 text-center text-sm text-wntrs-muted">
      Noch keine Nachrichten.
    </p>

    <div
      v-for="message in reference.messages"
      :key="message.uuid"
      class="group flex items-start gap-2"
      :class="{ 'flex-row-reverse': isRight(message) }"
    >
      <ChatAvatar :participant="sender(message)" :src="imageUrl(sender(message).avatar)" />
      <div
        class="flex flex-col gap-1 max-w-[75%] min-w-0"
        :class="isRight(message) ? 'items-end' : 'items-start'"
      >
        <span class="text-xs font-bold px-1">{{ sender(message).name }}</span>
        <div
          class="rounded-2xl px-3 py-2 text-sm break-words whitespace-pre-wrap"
          :class="
            isRight(message)
              ? 'bg-primary text-primary-content rounded-tr-sm'
              : 'bg-base-100 rounded-tl-sm'
          "
        >
          <img
            v-if="message.image"
            :src="imageUrl(message.image)"
            alt="Bild"
            class="rounded-xl max-h-72 w-auto cursor-zoom-in"
            :class="{ 'mb-1.5': message.text }"
            @click="$refs.lightbox.open(imageMessages.indexOf(message))"
          />
          <template v-if="message.text">{{ message.text }}</template>
        </div>
        <span v-if="message.target" class="badge badge-sm badge-error badge-soft">
          −{{ message.attack }} auf {{ participantsByUuid[message.target]?.name }} ·
          {{ message.remaining }} Health
        </span>
      </div>
      <BaseButton
        variant="ghost"
        shape="square"
        size="xs"
        class="self-center opacity-0 group-hover:opacity-100 focus:opacity-100"
        title="Nachricht bearbeiten"
        @click="$emit('edit', message)"
      >
        <AppIcon name="pencil" alt="Nachricht bearbeiten" />
      </BaseButton>
    </div>

    <ImageLightbox ref="lightbox" :images="images" />
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import ImageLightbox from '@core/components/common/ImageLightbox.vue'
import ChatAvatar from '@/components/ChatAvatar.vue'
import chatMixin from '@/mixins/chatMixin.js'

export default {
  name: 'ChatMessages',
  components: { AppIcon, BaseButton, ChatAvatar, ImageLightbox },
  mixins: [chatMixin],
  emits: ['edit'],
  computed: {
    imageMessages() {
      return this.reference.messages.filter((message) => message.image)
    },
    images() {
      return this.imageMessages.map((message) => this.imageUrl(message.image))
    },
  },
  methods: {
    sender(message) {
      return this.participantsByUuid[message.sender]
    },
    isRight(message) {
      return this.sender(message).side === 'right'
    },
  },
}
</script>
