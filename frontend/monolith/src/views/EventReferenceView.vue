<template>
  <BaseBreadcrumbs :items="breadcrumbs">
    <template v-if="reference" #actions>
      <EditButton :to="{ name: 'event-reference-edit', params: $route.params }" />
    </template>
  </BaseBreadcrumbs>
  <div
    class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1"
  >
    <div class="mx-auto w-full max-w-250 pt-4">
      <div v-if="!reference && !error" class="grid gap-4 lg:grid-cols-[minmax(0,1fr)_18rem]">
        <div class="skeleton h-96 w-full"></div>
        <div class="skeleton h-48 w-full"></div>
      </div>

      <div v-else-if="reference" class="grid items-start gap-4 lg:grid-cols-[minmax(0,1fr)_18rem]">
        <BaseCard class="overflow-hidden">
          <div class="flex items-center gap-3 px-6 py-4 border-b border-wntrs-border">
            <img class="size-8 shrink-0" :src="referenceIcon(reference)" alt="" />
            <div class="flex flex-col min-w-0">
              <h2 class="font-bold truncate">{{ reference.title }}</h2>
              <span class="text-xs text-wntrs-muted">{{ referenceSummary(reference) }}</span>
            </div>
          </div>

          <template v-if="reference.kind === 'chat'">
            <ChatMessages
              class="bg-base-200 px-4 py-4 max-h-[65vh] overflow-y-auto"
              v-bind="chatProps"
              @edit="$refs.messageDialog.open($event)"
            />
            <ChatComposer
              class="px-4 py-4 border-t border-wntrs-border"
              v-bind="chatProps"
              @update="reference = $event"
            />
          </template>

          <MarkdownContent v-else :text="reference.text" class="px-6 py-5" />
        </BaseCard>

        <aside class="flex flex-col gap-4">
          <ChatParticipants
            v-if="reference.kind === 'chat'"
            v-bind="chatProps"
            @add="$refs.participantDialog.open()"
            @edit="$refs.participantDialog.open($event)"
          />
          <EventReferenceLinks
            v-bind="chatProps"
            :siblings="siblings"
            @update="reference = $event"
          />
        </aside>
      </div>

      <p v-if="error" class="text-error text-sm mt-4 text-center">{{ error }}</p>
    </div>
  </div>

  <ChatParticipantDialog
    v-if="reference"
    ref="participantDialog"
    v-bind="chatProps"
    @confirm="saveParticipant"
    @remove="removeItem('participants', $event)"
  />
  <ChatMessageDialog
    v-if="reference"
    ref="messageDialog"
    v-bind="chatProps"
    @confirm="saveMessage"
    @remove="removeItem('messages', $event)"
  />
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import EditButton from '@core/components/common/EditButton.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import ChatComposer from '@/components/ChatComposer.vue'
import ChatMessageDialog from '@/components/ChatMessageDialog.vue'
import ChatMessages from '@/components/ChatMessages.vue'
import ChatParticipantDialog from '@/components/ChatParticipantDialog.vue'
import ChatParticipants from '@/components/ChatParticipants.vue'
import EventReferenceLinks from '@/components/EventReferenceLinks.vue'
import MarkdownContent from '@/components/MarkdownContent.vue'
import { referenceIcon, referenceSummary } from '@/data/eventReferences.js'
import eventMixin from '@/mixins/eventMixin.js'
import eventReferenceMixin from '@/mixins/eventReferenceMixin.js'

export default {
  name: 'EventReferenceView',
  components: {
    BaseBreadcrumbs,
    BaseCard,
    ChatComposer,
    ChatMessageDialog,
    ChatMessages,
    ChatParticipantDialog,
    ChatParticipants,
    EditButton,
    EventReferenceLinks,
    MarkdownContent,
  },
  mixins: [asyncActionMixin, eventMixin, eventReferenceMixin],
  computed: {
    chatProps() {
      return { uuid: this.uuid, event: this.eventUuid, reference: this.reference }
    },
    breadcrumbs() {
      return [...this.referenceBreadcrumbs, { label: this.reference?.title ?? '…' }]
    },
  },
  methods: {
    referenceIcon,
    referenceSummary,
    chatArgs(collection) {
      return [this.uuid, this.eventUuid, this.reference.uuid, collection]
    },
    saveParticipant({ participant, data }) {
      const args = this.chatArgs('participants')
      return this.runAction(async () => {
        this.reference = participant
          ? await this.dossiersStore.updateChatItem(...args, participant.uuid, data)
          : await this.dossiersStore.addChatItem(...args, data)
      })
    },
    saveMessage({ message, data }) {
      return this.runAction(async () => {
        this.reference = await this.dossiersStore.updateChatItem(
          ...this.chatArgs('messages'),
          message.uuid,
          data,
        )
      })
    },
    removeItem(collection, item) {
      return this.runAction(async () => {
        this.reference = await this.dossiersStore.removeChatItem(
          ...this.chatArgs(collection),
          item.uuid,
        )
      })
    },
  },
}
</script>
