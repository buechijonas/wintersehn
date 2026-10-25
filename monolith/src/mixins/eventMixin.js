import { useDossiersStore } from '@/stores/dossiers.js'

export default {
  data() {
    return {
      event: null,
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
    uuid() {
      return this.$route.params.uuid
    },
    eventKey() {
      return `${this.uuid}/${this.$route.params.event}`
    },
    dossierRoute() {
      return { name: 'dossier', params: { uuid: this.uuid }, query: { tab: 'events' } }
    },
    baseBreadcrumbs() {
      return [
        { label: 'Personalakten', to: '/' },
        { label: this.dossiersStore.current?.title ?? '…', to: this.dossierRoute },
      ]
    },
  },
  watch: {
    eventKey: {
      immediate: true,
      handler() {
        const event = this.$route.params.event
        this.event = null
        return this.runAction(async () => {
          const [loaded] = await Promise.all([
            this.dossiersStore.fetchEvent(this.uuid, event),
            this.dossiersStore.current?.uuid === this.uuid ||
              this.dossiersStore.fetchDossier(this.uuid),
          ])
          this.event = loaded
        })
      },
    },
  },
}
