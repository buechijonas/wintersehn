import { useDossiersStore } from '@/stores/dossiers.js'

export default {
  props: {
    uuid: { type: String, required: true },
    event: { type: String, required: true },
    reference: { type: Object, required: true },
  },
  emits: ['update'],
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
    participantsByUuid() {
      return Object.fromEntries(this.reference.participants.map((p) => [p.uuid, p]))
    },
  },
  methods: {
    targetsOf(sender) {
      return this.reference.participants.filter((participant) => participant.uuid !== sender)
    },
    imageUrl(attachment) {
      return (
        attachment &&
        this.dossiersStore.attachmentUrl(this.uuid, this.event, this.reference.uuid, attachment)
      )
    },
    upload(file) {
      return this.dossiersStore.uploadAttachment(this.uuid, this.event, this.reference.uuid, file)
    },
    addItem(collection, data) {
      return this.runAction(async () => {
        this.$emit(
          'update',
          await this.dossiersStore.addChatItem(
            this.uuid,
            this.event,
            this.reference.uuid,
            collection,
            data,
          ),
        )
      })
    },
    updateItem(collection, item, data) {
      return this.runAction(async () => {
        this.$emit(
          'update',
          await this.dossiersStore.updateChatItem(
            this.uuid,
            this.event,
            this.reference.uuid,
            collection,
            item,
            data,
          ),
        )
      })
    },
    removeItem(collection, item) {
      return this.runAction(async () => {
        this.$emit(
          'update',
          await this.dossiersStore.removeChatItem(
            this.uuid,
            this.event,
            this.reference.uuid,
            collection,
            item,
          ),
        )
      })
    },
  },
}
