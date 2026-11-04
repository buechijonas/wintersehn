<template>
  <BaseDialog ref="dialog" title="Ereignis hinzufügen">
    <form id="event-dialog-form" class="flex flex-col gap-2" @submit.prevent="confirm">
      <input
        ref="input"
        v-model.trim="title"
        type="text"
        placeholder="Titel"
        aria-label="Titel"
        class="input w-full"
        required
      />
      <input v-model="date" type="date" aria-label="Datum" class="input w-full" required />
    </form>

    <template #actions>
      <BaseButton variant="neutral" @click="$refs.dialog.close()">
        <AppIcon name="cross" />
        Abbrechen
      </BaseButton>
      <BaseButton type="submit" form="event-dialog-form" variant="primary">
        <AppIcon name="plus" />
        Hinzufügen
      </BaseButton>
    </template>
  </BaseDialog>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseDialog from '@core/components/common/BaseDialog.vue'

function today() {
  return new Date().toLocaleDateString('sv-SE')
}

export default {
  name: 'EventDialog',
  components: { AppIcon, BaseButton, BaseDialog },
  emits: ['confirm'],
  data() {
    return { title: '', date: today() }
  },
  methods: {
    open() {
      this.title = ''
      this.date = today()
      this.$refs.dialog.open()
      this.$nextTick(() => this.$refs.input.focus())
    },
    confirm() {
      this.$refs.dialog.close()
      this.$emit('confirm', { title: this.title, date: this.date })
    },
  },
}
</script>
