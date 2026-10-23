<template>
  <BaseButton variant="error" outline shape="square" size="sm" title="Löschen">
    <AppIcon name="trash" alt="Löschen" />
  </BaseButton>
</template>

<script>
import BaseButton from '@core/components/common/BaseButton.vue'
import AppIcon from '@core/components/common/AppIcon.vue'

export default {
  name: 'DeleteButton',
  components: { BaseButton, AppIcon },
}
</script>
