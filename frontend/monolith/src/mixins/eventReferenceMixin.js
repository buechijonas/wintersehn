export default {
  data() {
    return {
      reference: null,
      siblings: [],
    }
  },
  computed: {
    eventUuid() {
      return this.$route.params.event
    },
    eventRoute() {
      return { name: 'event', params: { uuid: this.uuid, event: this.eventUuid } }
    },
    referenceRoute() {
      return { name: 'event-reference', params: this.$route.params }
    },
    referenceBreadcrumbs() {
      return [...this.baseBreadcrumbs, { label: this.event?.title ?? '…', to: this.eventRoute }]
    },
  },
  watch: {
    '$route.params.reference': {
      immediate: true,
      handler(reference) {
        this.reference = null
        return this.runAction(async () => {
          const [loaded, all] = await Promise.all([
            this.dossiersStore.fetchEventReference(this.uuid, this.eventUuid, reference),
            this.dossiersStore.fetchEventReferences(this.uuid, this.eventUuid),
          ])
          this.reference = loaded
          this.siblings = all.filter((other) => other.uuid !== reference)
        })
      },
    },
  },
}
