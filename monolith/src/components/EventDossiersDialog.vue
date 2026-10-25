<template>
  <BaseDialog ref="dialog" title="Beteiligte Akten">
    <div class="flex flex-col gap-3 min-h-0">
      <input
        ref="input"
        v-model.trim="query"
        type="search"
        placeholder="Akte suchen"
        aria-label="Akte suchen"
        class="input w-full"
      />
      <div v-if="!dossiers" class="skeleton h-40 w-full"></div>
      <ul v-else class="flex flex-col max-h-80 overflow-y-auto">
        <li v-for="dossier in visible" :key="dossier.uuid">
          <label
            class="flex items-center gap-3 rounded-box px-2 py-2 cursor-pointer hover:bg-base-200"
          >
            <input
              v-model="selected"
              type="checkbox"
              class="checkbox checkbox-sm"
              :value="dossier.uuid"
            />
            <span class="text-sm truncate">{{ dossier.title }}</span>
          </label>
        </li>
      </ul>
      <p v-if="!selected.length" class="text-error text-sm">
        Ein Ereignis braucht mindestens eine Akte.
      </p>
    </div>

    <template #actions>
      <BaseButton variant="neutral" @click="$refs.dialog.close()">
        <AppIcon name="cross" />
        Abbrechen
      </BaseButton>
      <BaseButton variant="primary" :disabled="!selected.length" @click="confirm">
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
import { useDossiersStore } from '@/stores/dossiers.js'

export default {
  name: 'EventDossiersDialog',
  components: { AppIcon, BaseButton, BaseDialog },
  emits: ['confirm'],
  data() {
    return {
      query: '',
      linked: [],
      selected: [],
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
    dossiers() {
      return this.dossiersStore.items
    },
    visible() {
      const query = this.query.toLowerCase()
      const matches = this.dossiers.filter((dossier) => dossier.title.toLowerCase().includes(query))
      const linked = matches.filter((dossier) => this.linked.includes(dossier.uuid))
      return [...linked, ...matches.filter((dossier) => !this.linked.includes(dossier.uuid))]
    },
  },
  methods: {
    open(dossiers) {
      this.query = ''
      this.linked = dossiers.map((dossier) => dossier.uuid)
      this.selected = [...this.linked]
      this.dossiersStore.fetchDossiers()
      this.$refs.dialog.open()
      this.$nextTick(() => this.$refs.input.focus())
    },
    confirm() {
      this.$refs.dialog.close()
      this.$emit('confirm', [...this.selected])
    },
  },
}
</script>
