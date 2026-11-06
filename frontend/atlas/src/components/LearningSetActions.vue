<template>
  <ActionsMenu
    :links="links"
    :edit-to="`/learning-sets/${learningSet.uuid}/edit`"
    :delete-message="`${learningSet.title} mit allen Karten löschen?`"
    @delete="destroy"
  />
</template>

<script>
import ActionsMenu from '@/components/ActionsMenu.vue'
import { useAtlasStore } from '@/stores/atlas.js'

export default {
  name: 'LearningSetActions',
  components: { ActionsMenu },
  props: {
    learningSet: { type: Object, required: true },
  },
  emits: ['error'],
  computed: {
    links() {
      const base = `/learning-sets/${this.learningSet.uuid}`
      return [
        { label: 'Lernmodus wählen', icon: 'brain', to: base },
        { label: 'Karten', icon: 'cards-blank', to: `${base}/cards` },
      ].filter((link) => link.to !== this.$route.path)
    },
  },
  methods: {
    async destroy() {
      try {
        await useAtlasStore().remove(
          `/learning-sets/${this.learningSet.uuid}/`,
          'Löschen fehlgeschlagen.',
        )
        this.$router.push(`/subjects/${this.learningSet.subject.uuid}`)
      } catch (e) {
        this.$emit('error', e.message)
      }
    },
  },
}
</script>
