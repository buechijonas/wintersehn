<template>
  <BaseButton variant="error" outline @click="$refs.confirm.open()">
    <AppIcon name="trash" />
    Löschen
  </BaseButton>
  <ConfirmDialog ref="confirm" :message="message" @confirm="$emit('confirm')" />
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import ConfirmDialog from '@core/components/common/ConfirmDialog.vue'

export default {
  name: 'DeleteAction',
  components: { AppIcon, BaseButton, ConfirmDialog },
  props: {
    message: { type: String, required: true },
  },
  emits: ['confirm'],
}
</script>
